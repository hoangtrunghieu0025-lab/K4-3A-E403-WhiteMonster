import json
import requests
import time
import os
import sys
from dotenv import load_dotenv

load_dotenv()
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Chạy thẳng OpenAI API (không qua OpenRouter) — key OpenAI (sk-proj-...) không xác thực
# được với openrouter.ai. Chấp nhận cả 2 tên biến để không phải sửa lại .env đã điền.
API_KEY = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "gpt-4o"
URL = "https://api.openai.com/v1/chat/completions"

SYSTEM_PROMPT = """You are an Expert Educational Script Editor and Voice/TTS QA Specialist.
Task: Review the Vietnamese script chunk. Extract EXACT spans that sound unnatural, exhibit "translationese", or have inconsistent pronouns.
Categories: TRANSLATIONESE, REPETITION, INCONSISTENT_REGISTER, UNGROUNDED_CLAIM.
Constraint: Only flag errors with undeniable evidence. Return ONLY a JSON object with a single key 'findings' containing an array of error objects.
Format of array objects:
{
    "exact_span": "exact substring from text (must match completely)",
    "category": "TRANSLATIONESE",
    "severity": "HIGH",
    "reason": "short reason in Vietnamese",
    "minimal_suggestion": "short replacement"
}
"""

def call_ai(text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text}
        ],
        "response_format": {"type": "json_object"}
    }
    if not API_KEY:
        raise RuntimeError("Thiếu OPENAI_API_KEY (hoặc OPENROUTER_API_KEY) trong .env")
    resp = requests.post(URL, headers=headers, json=payload, timeout=45)
    if resp.status_code != 200:
        print(f"   !! Lỗi API {resp.status_code}: {resp.text[:300]}")
        return []
    result = json.loads(resp.json()['choices'][0]['message']['content'])
    return result.get('findings', [])

def run_eval():
    with open("eval/golden_set.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"=== ĐÁNH GIÁ (MODEL: {MODEL}) ===\n")
    
    # 1. Đo False Positive trên Clean Script
    print("1. Kiểm tra False Positive (Tập kịch bản sạch 40 câu):")
    clean_findings = call_ai(data["clean_script"])
    
    # Evidence Gate cho tập sạch
    valid_clean = [f for f in clean_findings if f.get("exact_span", "") in data["clean_script"]]
    fp_count = len(valid_clean)
    print(f"   -> Kết quả: Bắt sai {fp_count} lỗi. (Kỳ vọng: 0)")
    
    # 2. Đo Recall trên Flawed Cases
    total_cases = len(data["flawed_cases"])
    print(f"\n2. Kiểm tra Recall (Tập cấy lỗi - {total_cases} cases):")
    correct_hits = 0
    gate_drops = 0
    
    markdown_table = "| ID | Câu test | Lỗi cần bắt (Ground Truth) | Loại lỗi | Kết quả AI | Trạng thái |\n"
    markdown_table += "|---|---|---|---|---|---|\n"
    
    for case in data["flawed_cases"]:
        text = case["text"]
        gt_span = case["ground_truth_span"]
        
        findings = call_ai(text)
        
        # Evidence Gate
        valid_findings = []
        for f in findings:
            if f.get("exact_span", "") in text:
                valid_findings.append(f)
            else:
                gate_drops += 1
                
        # Kiểm tra hit
        hit = False
        ai_span = "-"
        for vf in valid_findings:
            # So sánh xem span AI tìm được có overlap với ground truth không
            if gt_span in vf["exact_span"] or vf["exact_span"] in gt_span:
                hit = True
                ai_span = vf["exact_span"]
                break
                
        status = "✅ PASS" if hit else "❌ FAIL"
        if hit: correct_hits += 1
        
        markdown_table += f"| {case['id']} | {text} | `{gt_span}` | {case['category']} | `{ai_span}` | {status} |\n"
        print(f"   - {case['id']}: {status}")
        
    recall_pct = round(correct_hits / total_cases * 100) if total_cases else 0
    print("\n=== TỔNG KẾT BÁO CÁO ===")
    print(f"False Positive (Sạch): {fp_count}/1")
    print(f"Recall (Lỗi): {correct_hits}/{total_cases} ({recall_pct}%)")
    print(f"Evidence Gate Drops (Chặn ảo giác): {gate_drops}")

    # 3. No-flag cases bổ sung (lớp ④ mined + input rỗng) — kỳ vọng 0 finding hợp lệ mỗi case
    no_flag_cases = data.get("no_flag_cases", [])
    no_flag_table = "| ID | Nguồn | Finding hợp lệ | Trạng thái |\n|---|---|---|---|\n"
    no_flag_fp = 0
    for case in no_flag_cases:
        text = case["text"]
        if not text.strip():
            no_flag_table += f"| {case['id']} | {case.get('source','-')} | 0 (input rỗng, bỏ qua gọi AI) | ✅ PASS |\n"
            continue
        findings = call_ai(text)
        valid = [f for f in findings if f.get("exact_span", "") in text]
        no_flag_fp += len(valid)
        no_flag_table += f"| {case['id']} | {case.get('source','-')} | {len(valid)} | {'✅ PASS' if not valid else '❌ FAIL'} |\n"

    # 4. Case hành vi (ambiguous / scope_refusal / security_refusal / edge) — chấm tay theo expected_behavior,
    #    không so khớp span tự động vì đây là test hành vi (từ chối / confidence thấp), không phải test trích span.
    def manual_table(cases, label, text_key="text", expect_key="expected_behavior"):
        rows = f"### {label}\n\n| ID | Kỳ vọng | Output AI thô |\n|---|---|---|\n"
        for case in cases:
            text = case.get(text_key) or case.get("scenario", "")
            expected = case.get(expect_key, "-")
            if not text.strip():
                raw = "(input rỗng, không gọi AI)"
            else:
                raw = json.dumps(call_ai(text), ensure_ascii=False)
            rows += f"| {case['id']} | {expected} | `{raw}` |\n"
        return rows

    manual_tables = "\n\n".join([
        manual_table(data.get("scope_refusal_cases", []), "scope_refusal_cases (lớp ③, đã có sẵn)"),
        manual_table(data.get("ambiguous_low_confidence_cases", []), "ambiguous_low_confidence_cases (lớp ②)"),
        manual_table(data.get("security_refusal_cases", []), "security_refusal_cases (lớp ③ + bảo mật)"),
        manual_table(data.get("edge_format_cases", []), "edge_format_cases"),
    ])

    print(f"\nNo-flag set bổ sung: {no_flag_fp} finding lọt trên {len(no_flag_cases)} case (kỳ vọng 0).")
    print("Case hành vi (ambiguous/scope/security/edge): xem eval/evaluation_report.json, cần người chấm tay.")

    # Lưu report
    report = {
        "metrics": {
            "fp": fp_count,
            "recall": f"{correct_hits}/{total_cases}",
            "gate_drops": gate_drops,
            "no_flag_extra_fp": f"{no_flag_fp}/{len(no_flag_cases)}"
        },
        "markdown_table": markdown_table,
        "no_flag_table": no_flag_table,
        "manual_review_tables": manual_tables
    }
    with open("eval/evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_eval()
