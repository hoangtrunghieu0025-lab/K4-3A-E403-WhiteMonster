import streamlit as st
import requests
import json
import datetime
import os

# Cấu hình giao diện Streamlit
st.set_page_config(page_title="Spoken-Script QA", layout="wide")

st.title("🎙️ Spoken-Script QA - Agent Review Kịch Bản")
st.markdown("Hệ thống tự động phát hiện văn phong dịch, câu quá dài, và gợi ý cách sửa tối thiểu.")

# Sidebar: Nhập API Key
with st.sidebar:
    st.header("Cấu hình API (OpenRouter)")
    api_key = st.text_input("Nhập OpenRouter API Key", value="", type="password")
    model_choice = st.selectbox("Chọn Model", ["openai/gpt-4o-mini", "google/gemini-2.5-flash", "anthropic/claude-3-haiku"])
    
    st.divider()
    st.header("Số đo Overlay (Dành cho CP3)")
    st.markdown("""
    **Nhớ chèn text này vào video:**
    - FP sạch: 0/40 câu
    - Recall baseline: 6/10 span
    - Evidence Gate drops: _(Xem cảnh báo màu vàng khi chạy)_
    """)

# Giao diện chính: Ô nhập kịch bản
default_script = """Hôm nay mình sẽ hướng dẫn các bạn về LLM. 
Các mô hình ngôn ngữ lớn là một sự đột phá rất lớn trong ngành công nghiệp máy tính hiện đại. Cấu trúc này đã được chứng minh là cực kỳ hiệu quả trong việc tạo ra văn bản mới. 
Chúng tôi tin rằng công nghệ này sẽ thay đổi mọi thứ."""

script_input = st.text_area("Nhập kịch bản (15-20 câu):", value=default_script, height=200)
if "reviewed_script" not in st.session_state:
    st.session_state.reviewed_script = script_input

SYSTEM_PROMPT = """You are an Expert Educational Script Editor and Voice/TTS QA Specialist.
Task: Review the Vietnamese script chunk. Extract EXACT spans that sound unnatural, exhibit "translationese", or have inconsistent pronouns.
Categories: TRANSLATIONESE, REPETITION, INCONSISTENT_REGISTER, UNGROUNDED_CLAIM.
Constraint: Only flag errors with undeniable evidence. Do not rewrite the whole text.
Return ONLY a JSON object with a single key 'findings' containing an array of error objects.
Format of array objects:
{
    "exact_span": "exact substring from text (must match completely, no omissions)",
    "category": "TRANSLATIONESE",
    "severity": "HIGH",
    "reason": "short reason in Vietnamese (max 15 words)",
    "minimal_suggestion": "short replacement"
}
"""

if st.button("🚀 Rà soát kịch bản", type="primary"):
    if not api_key:
        st.error("⚠️ Vui lòng nhập API Key!")
    else:
        with st.spinner(f"🤖 AI ({model_choice}) đang phân tích ngữ nghĩa..."):
            try:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model_choice,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": script_input}
                    ],
                    "response_format": {"type": "json_object"}
                }
                
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
                response.raise_for_status()
                
                result_text = response.json()['choices'][0]['message']['content']
                result_data = json.loads(result_text)
                findings = result_data.get('findings', [])
                
                st.subheader("📋 Báo cáo lỗi (AI Findings)")
                
                if not findings:
                    st.success("✨ Kịch bản mượt mà, không phát hiện lỗi lớn!")
                
                # Tầng lọc: Evidence Gate
                valid_findings = []
                drops = 0
                for f in findings:
                    if f.get("exact_span") in script_input:
                        valid_findings.append(f)
                    else:
                        drops += 1
                        
                if drops > 0:
                    st.warning(f"🛡️ **Evidence Gate đã tự động chặn {drops} lỗi** do AI trích xuất span không khớp gốc (Chống False Positive).")
                
                # Hiển thị lỗi hợp lệ
                for i, finding in enumerate(valid_findings):
                    with st.expander(f"⚠️ {finding['category']} - Mức độ: {finding['severity']}", expanded=True):
                        st.markdown(f"**Đoạn bị sượng:** `{finding['exact_span']}`")
                        st.markdown(f"**Lý do:** {finding['reason']}")
                        st.markdown(f"**Gợi ý sửa:** `{finding['minimal_suggestion']}`")
                        
                        col1, col2 = st.columns(2)
                        if col1.button("✅ Accept (Áp dụng)", key=f"acc_{i}"):
                            st.session_state.reviewed_script = st.session_state.reviewed_script.replace(
                                finding['exact_span'], finding['minimal_suggestion'], 1
                            )
                            # Đảm bảo thư mục eval tồn tại
                            os.makedirs("eval", exist_ok=True)
                            log_entry = f"[{datetime.datetime.now()}] ACCEPTED: {finding['exact_span']} -> {finding['minimal_suggestion']}\n"
                            with open("eval/audit_trail.log", "a", encoding="utf-8") as f:
                                f.write(log_entry)
                            st.success("Đã áp dụng. (Lưu vào eval/audit_trail.log)")
                            
                        if col2.button("❌ Reject (Bỏ qua)", key=f"rej_{i}"):
                            os.makedirs("eval", exist_ok=True)
                            log_entry = f"[{datetime.datetime.now()}] REJECTED: {finding['exact_span']}\n"
                            with open("eval/audit_trail.log", "a", encoding="utf-8") as f:
                                f.write(log_entry)
                            st.info("Đã bỏ qua. (Lưu vào eval/audit_trail.log)")

                st.subheader("Kịch bản sau duyệt")
                st.text_area("Bản xuất", st.session_state.reviewed_script, height=180, key="reviewed_output")
                            
            except Exception as e:
                st.error(f"Có lỗi xảy ra khi gọi API OpenRouter: {e}")
                if 'response' in locals():
                    st.json(response.text)
