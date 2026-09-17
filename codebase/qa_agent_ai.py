"""
VietScript QA Agent - Core AI Engine (Track C2 - Lesson Studio)
Nhóm: WhiteMonster · Lớp 3A · Phòng E403
Hỗ trợ cả Gemini API thật (Google AI Studio) và Mock Engine cho CP3.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SYSTEM_PROMPT = """Bạn là Spoken-Script QA Agent chuyên nghiệp cho đội sản xuất bài giảng video (Lesson Studio).
Nhiệm vụ của bạn là rà soát kịch bản video tiếng Việt để phát hiện các câu nghe SƯỢNG hoặc KHÓ ĐỌC THÀNH LỜI trước khi đưa vào phòng thu âm.

Bạn phải tuân thủ nghiêm ngặt các nguyên tắc sau:
1. TAXONOMY LỖI:
   - Translationese / Cú pháp dịch sượng (ví dụ: lạm dụng danh từ hoá 'việc thực hiện sự...', dịch cấu trúc tiếng Anh 'mà trong đó...')
   - Lặp ý / Filler / Cụm từ rườm rà (ví dụ: 'nhằm mục đích', 'mang tính chất', lặp liên từ)
   - Số, Acronym, Code-switch khó đọc TTS (ví dụ: số lớn viết liền 15000000, từ viết tắt CoT/RAG không có hướng dẫn đọc)
   - Khẩu ngữ / Register không phù hợp
2. BỘ LỌC FALSE-POSITIVE (CỰC KỲ QUAN TRỌNG):
   - ĐẶC THÙ VĂN NÓI: Các câu dài (50-90 từ) nhưng có nhịp điệu ngắt đệm tự nhiên, xưng hô 'mình - các bạn' trôi chảy của giảng viên KHÔNG ĐƯỢC COI LÀ LỖI. Hãy giữ nguyên để bảo toàn giọng tác giả.
3. GỢI Ý SỬA TỐI THIỂU:
   - Chỉ gợi ý sửa đúng chỗ vấp, không tự ý viết lại toàn bộ kịch bản, không tự bịa thêm số liệu/claim mới.

Định dạng trả về BẮT BUỘC là một mảng JSON thuần túy (không kèm markdown ```json):
[
  {
    "targetSpan": "đoạn văn bản gốc bị lỗi",
    "category": "Tên loại lỗi theo taxonomy",
    "severity": "high | med | low",
    "explanation": "Lý do vì sao câu này nghe sượng khi đọc thành lời",
    "suggestion": "Gợi ý sửa tối thiểu tự nhiên hơn",
    "action": "suggest_replacement | keep_original | pronunciation_hint"
  }
]
Nếu văn bản hoàn toàn sạch và tự nhiên, hãy trả về mảng rỗng: []
"""

def call_gemini_api(text: str, api_key: str, model: str = "gemini-1.5-flash") -> list:
    """Gọi Gemini API qua REST endpoint chính thức của Google AI Studio."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    prompt_content = f"{SYSTEM_PROMPT}\n\n--- KỊCH BẢN CẦN RÀ SOÁT ---\n{text}\n\nHãy trả về kết quả JSON:"
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt_content}]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            # Clean markdown code blocks if any
            clean_json = re.sub(r"^```json\s*", "", raw_text.strip())
            clean_json = re.sub(r"\s*```$", "", clean_json)
            findings = json.loads(clean_json)

            # Save trace for TA verification
            save_trace("gemini_api", text, findings, model=model)
            return findings
    except Exception as e:
        print(f"[CẢNH BÁO] Lỗi khi gọi Gemini API: {e}. Đang chuyển sang Rule-Engine fallback.", file=sys.stderr)
        return analyze_script_rule_based(text)

def analyze_script_rule_based(text: str) -> list:
    """Bộ phân tích quy tắc heuristic dùng cho thử nghiệm offline và baseline."""
    findings = []
    
    # 1. Translationese & Danh từ hóa
    if "thực hiện tối ưu hóa" in text or "thực hiện sự" in text:
        m = re.search(r"([^.!?\n]*thực hiện tối ưu hóa[^.!?\n]*)", text)
        if m:
            findings.append({
                "targetSpan": m.group(1).strip(),
                "category": "Translationese / Cú pháp dịch sượng",
                "severity": "high",
                "explanation": "Lạm dụng danh từ hóa 'thực hiện tối ưu hóa'. Đọc thành lời nghe rất trịnh trọng, cứng nhắc kiểu dịch máy.",
                "suggestion": "Chúng ta rất cần tối ưu cấu trúc câu lệnh đưa vào hệ thống.",
                "action": "suggest_replacement"
            })

    # 2. Filler phrasing / Rườm rà
    if "nhằm mục đích" in text:
        m = re.search(r"([^.!?\n]*nhằm mục đích[^.!?\n]*)", text)
        if m:
            findings.append({
                "targetSpan": m.group(1).strip(),
                "category": "Lặp ý / Filler / Cụm rườm rà",
                "severity": "high",
                "explanation": "Cụm 'nhằm mục đích' khiến câu nặng nề, tốn hơi đọc mà không thêm giá trị ngữ nghĩa.",
                "suggestion": "Chúng ta cần kiểm tra kỹ kết quả đầu ra của mô hình để đảm bảo độ chính xác.",
                "action": "suggest_replacement"
            })

    # 3. Mệnh đề dịch 'mà trong đó'
    if "mà trong đó" in text:
        m = re.search(r"([^.!?\n]*mà trong đó[^.!?\n]*)", text)
        if m:
            findings.append({
                "targetSpan": m.group(1).strip(),
                "category": "Translationese / Cú pháp dịch sượng",
                "severity": "med",
                "explanation": "Cấu trúc 'mà trong đó' sao chép ngữ pháp tiếng Anh. Nên chuyển thành câu chủ động ngắn.",
                "suggestion": "Với Few-shot, chúng ta đưa trước cho mô hình vài ví dụ minh họa.",
                "action": "suggest_replacement"
            })

    # 4. Acronym TTS phát âm
    if "CoT" in text:
        m = re.search(r"([^.!?\n]*CoT[^.!?\n]*)", text)
        if m:
            findings.append({
                "targetSpan": m.group(1).strip(),
                "category": "Số, Acronym, Code-switch khó đọc TTS",
                "severity": "med",
                "explanation": "Từ viết tắt 'CoT' dễ bị máy đọc hoặc phát thanh viên phát âm thành /kót/ thay vì từng chữ cái.",
                "suggestion": "Kỹ thuật Chain of Thought (đọc là C-O-T) yêu cầu mô hình giải thích từng bước...",
                "action": "pronunciation_hint"
            })

    # 5. Số lớn chưa định dạng
    num_m = re.search(r"\b\d{7,}\b", text)
    if num_m:
        m = re.search(r"([^.!?\n]*" + num_m.group(0) + r"[^.!?\n]*)", text)
        if m:
            findings.append({
                "targetSpan": m.group(1).strip(),
                "category": "Số, Acronym, Code-switch khó đọc TTS",
                "severity": "med",
                "explanation": f"Số '{num_m.group(0)}' viết liền không có dấu chấm hàng nghìn khiến người thu âm dễ đọc vấp.",
                "suggestion": "Thống kê 15.000.000 (mười lăm triệu) người dùng cho thấy...",
                "action": "number_normalization"
            })

    # 6. Kiểm tra False-Positive Guard (câu dài tự nhiên của giảng viên)
    if "Một trong những kỹ năng mình nghĩ quan trọng và đang cần nhất" in text:
        findings.append({
            "targetSpan": text.strip(),
            "category": "False-positive Guard (Văn nói trôi chảy)",
            "severity": "low",
            "explanation": "Câu dài 51 từ nhưng có ngắt nhịp đệm và xưng hô tự nhiên của giảng viên. Đạt chuẩn văn nói, không được bắt lỗi.",
            "suggestion": "Giữ nguyên (bảo toàn giọng tác giả).",
            "action": "keep_original"
        })

    return findings

def save_trace(call_type: str, input_text: str, findings: list, model: str = "heuristic"):
    """Ghi lại vết lời gọi AI vào file JSON để minh chứng cho CP3."""
    trace_data = {
        "timestamp": datetime.now().isoformat(),
        "call_type": call_type,
        "model": model,
        "input_length_chars": len(input_text),
        "input_snippet": input_text[:120] + "..." if len(input_text) > 120 else input_text,
        "findings_count": len(findings),
        "findings": findings
    }
    trace_path = os.path.join(os.path.dirname(__file__), "ai_call_trace.json")
    try:
        with open(trace_path, "w", encoding="utf-8") as f:
            json.dump(trace_data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def analyze_script(text: str, api_key: str = None, model: str = "gemini-1.5-flash") -> list:
    """Hàm chính tiếp nhận kịch bản và trả về danh sách finding."""
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if key and key.strip():
        return call_gemini_api(text, key.strip(), model=model)
    else:
        findings = analyze_script_rule_based(text)
        save_trace("heuristic_mock", text, findings, model="mock-baseline")
        return findings

if __name__ == "__main__":
    sample = """Chào các bạn. Việc thực hiện tối ưu hóa cấu trúc của các câu lệnh đưa vào hệ thống là vô cùng cần thiết.
Chúng ta phải xem xét nhằm mục đích kiểm tra mô hình.
Kỹ thuật Chain of Thought, hay viết tắt là CoT, yêu cầu mô hình phải giải thích từng bước.
Thống kê 15000000 người dùng cho thấy điều này."""

    print("=== Chạy thử VietScript QA Agent ===")
    api_key_env = os.environ.get("GEMINI_API_KEY")
    if api_key_env:
        print(f"[*] Phát hiện GEMINI_API_KEY trong môi trường. Gọi model Gemini...")
    else:
        print("[!] Không có API Key. Chạy chế độ Heuristic/Mock...")

    res = analyze_script(sample)
    print(f"\nPhát hiện {len(res)} điểm lưu ý:")
    for idx, item in enumerate(res, 1):
        print(f"[{idx}] {item.get('category')} (Severity: {item.get('severity')})")
        print(f"    Span: \"{item.get('targetSpan')}\"")
        print(f"    Lý do: {item.get('explanation')}")
        print(f"    Gợi ý: {item.get('suggestion')}\n")

