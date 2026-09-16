# Canvas 4 ô — Checkpoint 1

**NHÓM:** WhiteMonster · **Lớp:** 3A · **Phòng:** E403 · **Cụm:** C1
**TRACK:** C — Lesson Studio · **Đề:** C2 (Vietnamese Spoken-Script QA — agent review kịch bản tiếng Việt)
**ĐỘI TRƯỞNG:** Hoàng Trung Hiếu — 2A202602945
**REPO:** https://github.com/hoangtrunghieu0025-lab/K4-3A-E403-WhiteMonster

---

## Ô 1 · NGƯỜI DÙNG & NỖI ĐAU

**JOB:** Biên tập viên / người viết kịch bản của Studio team (và giảng viên duyệt) đang rà lại kịch bản video trước khi chuyển sang thu âm.

**PAIN:** Kịch bản đúng ngữ pháp nhưng đọc lên bị sượng — câu dịch cứng, sai sắc thái, đứt hơi giữa chừng, số và từ viết tắt chưa chuẩn hoá. Biên tập viên phải đọc thành tiếng cả bài mới phát hiện, và vẫn dễ bỏ sót. Vì quy trình là thu giọng trước rồi dựng hình khớp theo độ dài giọng, một câu lọt xuống khâu sau kéo theo phải thu lại giọng câu đó và dựng lại cảnh đó — đắt hơn nhiều so với sửa ngay ở bước kịch bản. Cách thay thế là nhờ công cụ viết lại cả bài, nhưng như vậy mất giọng văn gốc của tác giả.

## Ô 2 · BẰNG CHỨNG BAN ĐẦU

**MINING (chuẩn B, trên `data/vlearn-pack/` — track C cho phép thay cho khảo sát 20 người):**
Đo phân bố độ dài câu của **3.665 câu văn nói tự nhiên** trong 6 transcript giảng viên.

| Nguồn | Số câu | Trung vị | p90 | p95 | Dài nhất |
|---|---|---|---|---|---|
| Văn nói — 6 transcript giảng viên | 3.665 | 24 từ | 50 | 59 | 137 |
| Văn viết — tutor reply K4 (3.097 lượt) | 22.191 | 27 từ | 46 | — | — |

- **699/3.665 câu (19,1%) dài hơn 40 từ** mà vẫn là lời giảng nghe được bình thường.
- Văn viết của tutor chỉ **2,3%** vượt ngưỡng p95 (59 từ) của văn nói — tức văn viết **không hề dài hơn** văn nói.

**VÍ DỤ NGUYÊN VĂN** (dẫn mã đoạn, đều là câu rất dài nhưng nghe tự nhiên):
`[T01-001]` 72 từ · `[T01-005]` 66 từ · `[T01-012]` 91 từ · `[T01-016]` 72 từ · `[T01-018]` 74 từ · `[T01-020]` 72 từ.

**PHƯƠNG PHÁP ĐẾM (kiểm lại được):** `eval/mine_sentence_length.py` — lấy mọi đoạn mã `[Txx-NNN]`, bỏ đoạn `[Hoạt động lớp]`, gỡ markdown phía tutor, tách câu theo `. ! ? …`, bỏ mẩu dưới 3 từ, đếm từ theo khoảng trắng. Chạy lại ra đúng số trên. Data pack không commit vào repo theo quy định bảo mật.

**KẾT LUẬN:** số liệu **bác bỏ giả thuyết ban đầu** của nhóm ("câu dài = câu sượng"). Đặt ngưỡng 40 từ sẽ gắn cờ oan 19,1% lời giảng thật — đúng bài toán false positive mà đề C2 nhấn mạnh (*"một câu trơn tru không đủ để kết luận"*). Hệ quả thiết kế: agent **không được** dùng luật độ dài đơn thuần, phải phân loại lỗi và giải thích lý do gắn với ngữ cảnh, và phải đo false positive trên chính 6 câu trên.

**ĐANG LÀM:** phỏng vấn Mom Test ≥3 người, trong đó ≥1 người thuộc Studio team hoặc lab coach (người dùng cuối thật). Khung 7 câu hỏi và bảng log nguyên văn đã dựng sẵn trong [`interview-log.md`](interview-log.md). Mining ở trên chứng minh *lỗi khó phân loại có tồn tại*; phỏng vấn để xác nhận *biên tập viên có thật sự đau vì nó*. Hoàn thành trước CP4.

## Ô 3 · LÁT CẮT & AUTOMATION

**LÁT CẮT (một câu):**
> Một biên tập viên · duyệt một kịch bản ~40 câu trước khi thu âm · AI chỉ đúng câu/đoạn nghe sượng kèm loại lỗi + lý do + gợi ý sửa tối thiểu · biên tập có bản kịch bản đã sạch câu sượng trước khi chuyển thu âm, không phải đọc dò lại cả bài.

**AUTOMATION: Augment** — AI gắn cờ, phân loại, giải thích và gợi ý sửa tối thiểu; người quyết từng chỗ bằng Accept/Reject.
*Lý do theo cost-of-error:* bỏ sót lỗi hoặc để AI tự sửa làm mất giọng tác giả thì phải thu lại giọng và dựng lại cảnh (đắt); còn gợi ý sai thì rẻ vì biên tập bấm Reject là xong.

**NON-GOALS:**
1. Không tự viết lại hoặc xuất bản toàn bài.
2. Không dùng nhãn "AI-generated" để kết luận về tác giả.
3. Không thêm claim hay số liệu mới không có trong kịch bản gốc.
4. Không dùng luật độ dài câu đơn thuần để kết luận lỗi.

## Ô 4 · NGƯỜI THỬ & PHÂN CÔNG

**WILLING USERS:** Nguyễn Đức Thái (2A202602648) và Trần Hồng Sơn (2A20262475) — đã đồng ý cho phỏng vấn và thử prototype trước demo. Đang xin BTC đầu mối thêm ≥1 người thuộc Studio team hoặc lab coach (người dùng cuối thật của C2).

**PHÂN CÔNG:**

| Họ tên | MSSV | Vai trò | Phần việc |
|---|---|---|---|
| Hoàng Trung Hiếu | 2A202602945 | Đội trưởng · Product owner & chủ spec | `spec.md` §1/§2/§4, nộp form cả 5 mốc, dựng `demo-slides.pdf`, mở đầu thuyết trình CP6 |
| Nguyễn Thọ Đạt | 2A202602484 | Research & evidence | Phỏng vấn Mom Test + log nguyên văn trong `interview-log.md`, tổng hợp số liệu/quote vào §1, §3, validation CP5 |
| Đinh Trường An | 2A202602393 | Prompt & eval | Prompt cho agent QA, golden set trong `eval/` (≥10 case lỗi gắn nhãn + ≥1 đoạn sạch đo false positive), bảng kết quả §7, chốt quality bar trước CP4 |
| Phan Đức Duy | 2A202602397 | Prototype & demo | `codebase/` (flow duyệt, Accept/Reject từng finding), lời gọi AI thật + log/trace, video CP3 và video dự phòng CP5 |
