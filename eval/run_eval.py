import json
import requests
import time
import os

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
MODEL = "openai/gpt-4o-mini"
URL = "https://openrouter.ai/api/v1/chat/completions"

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
        raise RuntimeError("Thiếu OPENROUTER_API_KEY")
    resp = requests.post(URL, headers=headers, json=payload, timeout=45)
    if resp.status_code != 200:
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
    print("\n2. Kiểm tra Recall (Tập cấy lỗi - 10 cases):")
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
        
    print("\n=== TỔNG KẾT BÁO CÁO ===")
    print(f"False Positive (Sạch): {fp_count}/1")
    print(f"Recall (Lỗi): {correct_hits}/10 ({correct_hits*10}%)")
    print(f"Evidence Gate Drops (Chặn ảo giác): {gate_drops}")
    
    # Lưu report
    report = {
        "metrics": {
            "fp": fp_count,
            "recall": f"{correct_hits}/10",
            "gate_drops": gate_drops
        },
        "markdown_table": markdown_table
    }
    with open("eval/evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    run_eval()
