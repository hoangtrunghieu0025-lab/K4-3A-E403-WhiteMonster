# Reflection — Nguyễn Thọ Đạt (2A202602484)

## Vai trò & phân công

Phụ trách "Research · Evidence" theo `spec.md` §8:
- Phỏng vấn người dùng tiềm năng (Studio team, lab coach, người làm nội dung) theo phương pháp Mom Test, lưu trữ log nguyên văn trong `interview-log.md`.
- Tổng hợp số liệu định lượng và trích dẫn trực tiếp vào `spec.md` §1 (Problem Statement).
- Nghiên cứu và phân tích các giải pháp thay thế trên thị trường trong `spec.md` §3 (Grammarly, LanguageTool, Hemingway, Word).
- Chuẩn bị và theo dõi vòng validation người dùng ở CP5 (`validation/`).

---

## Việc mình thực sự đã làm

1. **Phỏng vấn sâu 3 đối tượng người dùng theo chuẩn Mom Test (`interview-log.md`):**
   - Đã trực tiếp phỏng vấn 3 người: **P1 Nguyễn Đức Thái** (học viên tự làm nội dung, tự thu voice-off), **P2 Trần Hồng Sơn** (editor/reviewer kịch bản MC), và **P3** (lab coach trực tiếp dựng bài giảng bằng công cụ AI).
   - Áp dụng triệt để nguyên tắc Mom Test: không hỏi "Bạn có thích ý tưởng X không?", mà xoáy sâu vào hành vi quá khứ (*"Lần gần nhất bạn duyệt kịch bản là khi nào?", "Mất bao lâu?", "Hậu quả khi sót lỗi là gì?"*).
   - Bóc băng nguyên văn từng câu trả lời, kể cả câu cụt và lỗi diễn đạt, trích xuất ra **4 câu quote đắt giá nhất** và **3 case lỗi thực tế** đưa thẳng vào Golden Set của nhóm.

2. **Cung cấp bằng chứng định lượng cho `spec.md` §1:**
   - 3/3 người xác nhận từng để lọt câu sượng xuống khâu thu âm hoặc sân khấu.
   - Đo lường được chi phí đọc dò: mất từ **45 đến 60 phút** cho mỗi 5–10 trang kịch bản; tần suất 2–5 lần/tuần.
   - Làm rõ được nỗi đau cốt lõi: Khi lọt lỗi, P1 mất thêm gần 1 tiếng thu âm và cắt dựng lại mic; P2 khiến MC líu lưỡi vấp ngay trên sân khấu.

3. **Đánh giá giải pháp tương tự (`spec.md` §3):**
   - Kiểm thử thực tế các công cụ hiện có trên thị trường: LanguageTool bắt đúng **0/10 case** mẫu vì chỉ tập trung vào ngữ pháp viết; Grammarly chỉ hỗ trợ tiếng Anh; còn Word chỉ check chính tả cơ bản. Không một công cụ nào nhận diện được nhịp ngắt và văn phong dịch nói của người Việt.

4. **Kết nối Willing User cho vòng Validation CP5:**
   - Duy trì liên lạc với 2 willing user đã đồng ý từ 16/9 (Nguyễn Đức Thái và Trần Hồng Sơn), dựng khung theo dõi quan sát hành vi thực tế (số finding Áp dụng / Sửa tay / Bỏ qua) tại thư mục `validation/`.

---

## AI hỗ trợ thế nào

- **Thiết kế bảng hỏi Mom Test:** Mình sử dụng AI để rà soát bộ câu hỏi phỏng vấn, loại bỏ các câu hỏi mang tính định hướng hoặc gợi ý câu trả lời ("leading questions"), đảm bảo bộ câu hỏi chỉ tập trung vào sự thật đã xảy ra trong quá khứ.
- **Tổng hợp và phân loại dữ liệu định tính:** Sau khi phỏng vấn, mình đưa nội dung thô cho AI hỗ trợ bóc tách các mốc thời gian, chi phí lãng phí, và nhóm các loại lỗi ngữ nghĩa mà người dùng gặp phải để đối chiếu với 6 category của nhóm.
- **Ranh giới:** AI chỉ đóng vai trò phân loại và định dạng; toàn bộ các câu trả lời phỏng vấn, các quote trích dẫn và quan sát hành vi đều là dữ liệu thực tế 100% do mình thu thập từ con người thật ngoài đời.

---

## Quyết định mình không hoàn toàn đồng tình nhưng vẫn theo

- **Về việc ưu tiên thời gian giữa Prompt Tuning và Thử nghiệm thực tế:**
  - Tối 17/9 và sáng 18/9, nhóm dành phần lớn thời gian để tinh chỉnh prompt và chạy lặp đi lặp lại 16 lượt eval kỹ thuật trên máy. Với góc nhìn của người làm evidence, mình muốn đem prototype (dù mới ở mức 60-70% recall) đi đưa cho 2 willing user (Thái và Sơn) dùng thử ngay từ chiều tối 17/9 để lấy phản hồi hành vi sớm, thay vì đợi đến tận sát hạn CP5.
  - **Lý do vẫn theo nhóm:** Hiếu và An giải thích rất rõ rằng nếu đưa một mô hình chưa vượt qua Quality Bar (lúc Lượt 8 bị tụt xuống 45% do sửa lỗi chấm điểm) cho người dùng thật, họ sẽ gặp rất nhiều kết quả ảo giác (False Positive) hoặc bỏ sót lỗi nặng, dẫn đến việc họ mất lòng tin và đánh giá sai tiềm năng của sản phẩm. Việc giữ vững kỷ luật kỹ thuật để đạt mốc 70% trước khi mở vòng validation là một quyết định thận trọng và đúng đắn về mặt sản phẩm.

---

## Bài học từ case fail của chính nhóm

- **Bài học phân biệt giữa "lời nói" và "ngữ cảnh thực tế":**
  - Khi phỏng vấn P3 (lab coach dựng video bằng AI), bạn ấy trả lời câu Q4 rằng: *"Nếu phát hiện câu sượng thì chỉ mất 5 phút là xong"*. Ban đầu, mình suýt kết luận rằng đối với quy trình AI dựng video, chi phí sửa lỗi gần như bằng 0 nên sản phẩm của nhóm không có thị trường (no pain).
  - Tuy nhiên, khi cùng nhóm phân tích sâu hơn, nhóm nhận ra rằng: P3 sửa mất 5 phút vì giọng AI đọc câu nào cũng trơn tru như nhau, nên **người nghe không thể phát hiện ra câu sượng khi nghe lại bản dựng**, buộc người làm bài giảng vẫn phải bỏ ra 45–60 phút đọc dò từng chữ trước khi bấm máy. Bài học lớn nhất là không được lấy một câu trả lời đơn lẻ để phủ nhận toàn bộ vấn đề, mà phải nhìn toàn bộ chuỗi mắt xích công việc của người dùng.

---

## Nếu làm lại từ đầu

- Sẽ chủ động hẹn trước lịch demo 1-1 với 2 willing user vào đúng 10h sáng ngày thứ hai (18/9), chuẩn bị sẵn một máy đã cài đặt môi trường hoàn chỉnh để cho họ bấm trực tiếp, tránh việc phải đợi bản build hoàn thiện sát nút 13:00 CP5.
- Sẽ mở rộng phỏng vấn thêm 1–2 lab coach chuyên nghiệp nữa trong ngày đầu tiên để dữ liệu phỏng vấn ở §1 đồng đều hơn giữa nhóm người dùng làm nội dung tự do và nhóm giảng viên tổ chức.

