# Reflection — Phan Đức Duy (2A202602397)

## Vai trò & phân công

Theo `spec.md` §8: **Prototype + demo** — `codebase/` (flow duyệt, accept/reject từng finding), lời gọi AI thật + log/trace; video CP3 và video dự phòng CP5.

## Việc mình thực sự đã làm

- Xây lại prototype thật thay cho bản Streamlit cũ: `codebase/server.py` (FastAPI, ~450 dòng) + `codebase/web/index.html` (~876 dòng, thuần HTML/JS). Luồng: dán cả kịch bản → tách câu, gom khối ≤40 câu → gọi thẳng `call_ai` + `SYSTEM_PROMPT` + `MODEL` import nguyên từ `eval/run_eval.py` (không viết prompt riêng cho demo, để bản demo chạy đúng số đã đo ở §7) → Evidence Gate loại span không khớp nguyên văn → bôi màu + checklist Áp dụng/Sửa tay/Bỏ qua/Hoàn tác → xuất kịch bản đã duyệt + audit report. Viết `codebase/test_server.py` để tự kiểm server khởi động đúng.
- Thêm cụm tính năng nghe thử ở bước ④ (chỉ hỗ trợ người quyết, không dùng để phát hiện lỗi): giọng Piper `vi_VN-vais1000-medium` chạy offline không cần key, đo thật trên máy (~0,1–0,35s/audio); thử `gemini-3.1-flash-tts-preview` trước rồi bỏ vì chậm (~8s) và hay lỗi 503. Thêm tốc độ đọc Nhanh/Vừa/Chậm, đọc từ tiếng Anh theo phiên âm riêng, "So cách đọc" (vẽ âm lượng/chỗ ngắt hơi/cao độ 2 bản trên cùng trục), và "Xem chữ máy đọc" (chép lại audio bằng Gemini, tô chỗ khác chữ viết).
- Tách 2 tầng log theo ranh giới riêng tư đã chốt ở §4: `trace.jsonl` (chỉ số đếm lời gọi, commit làm bằng chứng gọi AI thật) và `audit.jsonl` (span + quyết định duyệt, không commit vì chứa nội dung kịch bản thật của người dùng).
- Phát hiện 2 lỗi chấm điểm nghiêm trọng trong `eval/run_eval.py` (tối 17/9): `exact_span=""` luôn được Python coi là substring nên tự PASS giả, và AI trả nguyên cả câu làm span vẫn được tính khớp ground truth. Hai lỗi này làm recall báo cáo suốt Lượt 3–7 bị thổi phồng thành 85–95% trong khi số thật chỉ 45% (xem `spec.md` dòng 350).
- Đóng góp vào "Đợt 1" mở rộng golden set (`eval/golden_set.json`): viết case trong 20 flawed case (exact_span + category) + 2 scope-refusal case (lớp ③) + 1 đoạn sạch 40 câu — nguồn gồm case tự viết (C1–C10, đã eval tay) và case trích từ chatlog thật (`tutor_turns.csv`, ≤2 câu/case kèm `turn_id`, không commit data pack).
- Bổ sung đủ ≥2 case cho lớp ③ ở §5 (từ chối ngoài phạm vi): case 8 — từ chối viết lại toàn văn khi người duyệt yêu cầu; case 11 — từ chối tự bịa thêm ví dụ/số liệu mới ngoài kịch bản gốc.
- Tự thử tay 3 công cụ cạnh tranh để viết §3, trên đúng bộ case C1–C10: LanguageTool (API công khai, bắt đúng 0/10, không có tiếng Việt), Hemingway Editor (gắn cờ oan câu dài-nhưng-xuôi, bỏ qua cả 2 câu dịch cứng), Grammarly (chỉ bắt 2/nhiều lỗi, toàn chính tả/dấu câu). Sửa lại 1 câu sai fact ở §1/§2 ("Grammarly không dùng được tiếng Việt" — thử lại thì nay đã hỗ trợ).
- Viết phần kiến trúc AI trong `spec.md` §4: sơ đồ 4 bước Luật/LLM/Luật/Người, lý do không dùng ReAct agent, lý do không thuần luật, và bảng §4b neo ≥4 nguyên tắc HAX vào đúng chỗ trong giao diện.
- Dựng khung `validation/README.md` + `reflection/README.md` và 2 file mẫu ghi log thử prototype cho vòng validation CP5.
- Viết `c2-summary.md` — tổng hợp đề C2 (taxonomy 8 loại lỗi, luận điểm "precision trước recall vì báo động giả làm mất niềm tin", ranh giới không được xây "máy đo văn AI").
- Thêm 2 provider vào `eval/run_eval.py` (OpenCode Go kèm header session bắt buộc, Gemini kèm tự retry 503) và chạy một lượt mini-eval so 4 model trên 10 case tự viết.
- Giải merge conflict giữa các nhánh song song trên `eval/run_eval.py`, `eval/golden_set.json`, `spec.md`, `codebase/README.md`.

**Còn nợ tính đến lúc viết reflection này (18/9):** file mẫu ghi log validation vẫn còn trống, chưa có số thật (cần Thái/Sơn tự thử và điền); phần đọc tiếng Anh theo phiên âm riêng chưa xác nhận lại bằng chép audio vì key Gemini dùng để test đã bị thu hồi giữa chừng. Đã gỡ `codebase/app.py` (Streamlit) + `streamlit` khỏi `requirements.txt` (18/9) đúng kế hoạch "làm sau CP5" ghi trong `TONG-KET-17-9.md`.

## Quyết định của nhóm mình không hoàn toàn đồng tình nhưng vẫn theo

Phân công ở §8 khoanh phần của mình chỉ ở `codebase/` (prototype + demo), còn `eval/run_eval.py` (prompt + eval) là phần của người khác — mình không đồng ý với việc tự giới hạn đúng ranh giới đó, vì lúc tự chạy prototype để demo, số liệu recall báo cáo (85–95%) không khớp với cảm giác thực tế khi tự tay duyệt kịch bản. Thay vì chỉ báo lại rồi chờ, mình chủ động đọc thẳng logic chấm điểm trong `run_eval.py` dù không phải phần được giao, và phát hiện ra `exact_span=""` luôn được tính là substring nên tự PASS giả, cùng lỗi AI trả nguyên câu vẫn tính khớp ground truth. Việc "làm khác" so với ranh giới phân công này là chủ động, không xin phép trước, vì nếu đợi đúng quy trình phân công thì lỗi có thể còn kéo dài thêm nhiều lượt đo nữa trước khi ai đó tình cờ phát hiện ra.

## Nếu làm lại từ đầu

Đọc kỹ `_valid_span()`/`_is_hit()` trong `run_eval.py` ngay từ Lượt 3 — trước khi tin bất kỳ con số recall nào — thay vì đợi đến tối 17/9 mới phát hiện. Đây là việc không tốn thêm công nếu làm sớm (chỉ là đọc ~15 dòng logic chấm), nhưng để chậm đã khiến số liệu sai được dùng suốt từ CP3 đến gần CP5.
