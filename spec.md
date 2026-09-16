# AI SPEC — Agent QA kịch bản video tiếng Việt · Nhóm WhiteMonster · Zone E403

Hướng: [ ] A — VLearn  [ ] B — Trợ lý Học viên  [x] C — Lesson Studio (đề C2)
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

*(Draft từ Canvas CP1 — chưa đầy đủ, hoàn thiện dần đến hạn chốt spec 21:00 17/9 tại CP4. Phần còn thiếu đánh dấu `⟵`.)*

- **Đội trưởng:** Hoàng Trung Hiếu — MSSV 2A202602945 (mã học viên nộp cả 5 mốc phải là người này)
- **Phòng / cụm:** E403 / cụm C1
- **Thành viên:** Nguyễn Thọ Đạt (2A202602484) · Đinh Trường An (2A202602393) · Phan Đức Duy (2A202602397)
- **Track/đề:** C2 — Vietnamese Spoken-Script QA (agent review kịch bản video trước khi thu âm/dựng hình)

## §1. User & Job

- **Job executor + workflow:** Biên tập viên/người viết kịch bản của Studio team; giảng viên duyệt kịch bản trước khi kịch bản được chuyển sang thu âm.
- **Core JTBD:** Đọc lại kịch bản trước khi duyệt để tìm câu nghe sượng/khó đọc thành lời trước khi đưa vào thu âm.
- **Problem statement (không chữ AI):** Biên tập viên — đang tự đọc thành tiếng từng kịch bản trước khi duyệt để bắt câu "sượng" (dịch cứng, sai sắc thái, quá dài để đọc một hơi, số/viết tắt chưa chuẩn hoá) — không có công cụ chỉ đúng câu và loại lỗi, phải đọc hết cả bài mới phát hiện — dễ bỏ sót, phát hiện muộn thì phải thu lại giọng và dựng lại cảnh, tốn thời gian và tiền hơn nhiều so với sửa ngay ở bước kịch bản.
- **Evidence — điểm yếu cần nhóm tự bổ sung, chưa đạt chuẩn A/B đầy đủ:**
  - **Không có** dữ liệu "kịch bản lỗi" thật trong pack để đếm số (khác các track khác) — `data/studio-pack/c2/` (nếu có) hoặc mẫu kịch bản chung chỉ để tham khảo định dạng, chưa có kịch bản gắn nhãn lỗi.
  - **Có thật, dùng làm mốc so sánh (không phải bằng chứng pain):** 6 transcript bản sạch (`data/vlearn-pack/transcript/`, ~700 đoạn mã `[Txx-NNN]`) là văn nói tự nhiên thật của giảng viên — dùng làm chuẩn "nghe được".
  - **Minh hoạ khác biệt phong cách** (không phải bằng chứng đếm được): câu trả lời viết của AI tutor (`data/vlearn-pack/chatlog/tutor_turns.csv`) thường liệt kê bullet, câu ghép nhiều mệnh đề — khác cách giảng viên nói tự nhiên trong transcript (câu ngắn, có từ đệm, lặp ý khi giải thích, vd. đoạn `[T01-016]` về "tư duy nhanh/chậm"). Chỉ gợi ý *loại* khác biệt văn viết/văn nói, chưa chứng minh pain của Studio team.
  - ⟵ **Bằng chứng thật đúng chuẩn track C2** phải đến từ **phỏng vấn ≥3 người** (Mom Test, `02-guide.md` §1.3), trong đó **≥1 người thuộc Studio team/lab coach** vì đó mới là người dùng cuối. Khung câu hỏi + bảng log nguyên văn đã dựng sẵn tại **[`interview-log.md`](interview-log.md)** (P1 Nguyễn Đức Thái, P2 Trần Hồng Sơn đã nhận lời; P3 chờ đầu mối BTC) — **chưa phỏng vấn**, phải hoàn thành và chép số liệu + quote về mục này trước hạn chốt spec CP4.

## §2. Impact & quyết định chọn

| Ứng viên | Bao nhiêu người gặp | Tần suất | Mỗi lần tốn gì | Khả thi trong sự kiện? |
|---|---|---|---|---|
| **A. Agent QA kịch bản trước thu âm, chỉ đúng câu sượng + gợi ý sửa tối thiểu (C2 — đã chọn)** | ⟵ cần phỏng vấn Studio team để có số — ước tính toàn bộ kịch bản video của khoá đều qua tay một nhóm biên tập nhỏ | Mỗi kịch bản trước khi thu (tần suất theo lịch sản xuất video của Studio team — ⟵ xác nhận) | Đọc thành tiếng lại cả kịch bản; phát hiện muộn thì tốn công thu lại giọng + dựng lại cảnh | Trung bình — cần tự viết + gắn nhãn tay ≥10 case kịch bản lỗi làm golden set (pack không có sẵn) |
| B. Sinh graph tri thức + quiz có trích nguồn từ transcript (C1) | Giảng viên soạn quiz + học viên toàn khoá | Mỗi bài giảng mới | Giảng viên tự soạn tay câu hỏi; học viên học theo lộ trình tuyến tính dù đã hiểu một phần | Khó hơn — cần xây graph tri thức từ đầu, phạm vi rộng hơn nhiều so với 3 buổi build |
| C. ScriptScout — agent tự tìm tài liệu viết kịch bản có dẫn nguồn (C3) | Người viết kịch bản Studio team | Mỗi video mới cần kịch bản từ đầu | Nhiều ngày tự đọc tài liệu + viết + không ai kiểm được câu nào lấy từ đâu | Khó hơn — agent phải tự tìm & thẩm định nguồn web, rủi ro cao hơn (prompt injection từ trang lạ, hai nguồn mâu thuẫn) |
| D. FeedbackRadar — gom góp ý người học thành kế hoạch sửa video (C5) | Đội sản xuất + giảng viên, gián tiếp là người học | Sau mỗi đợt học có video mới | Đọc tay từng góp ý rồi tự quyết định sửa gì, hay làm lại gần cả video dù chỉ vài câu có vấn đề | Trung bình — cần tự thu thập ~100 góp ý thật (khảo sát bạn cùng lớp) để làm golden set |

- **Ứng viên ĐÃ LOẠI + vì sao:** B/C1 (phạm vi quá rộng — xây graph tri thức từ đầu không vừa 3 buổi) · C/C3 (rủi ro kỹ thuật cao hơn — agent tự tìm nguồn web, phạm vi an toàn phức tạp hơn) · D/C5 (cần tự thu thập ~100 góp ý thật mới đủ golden set, khối lượng evidence lớn hơn C2) — cả ba giữ lại nếu nhóm đổi hướng sau phỏng vấn Studio team.
- **Ứng viên CHỌN + vì sao:** C2 — phạm vi hẹp nhất trong 5 đề Track C (chỉ QA một kịch bản, không phải dựng graph/tự tìm nguồn/gom góp ý), và có sẵn dữ liệu tham chiếu thật (transcript bản sạch) để định nghĩa chuẩn "nghe được" ngay cả khi chưa phỏng vấn xong. **Lưu ý:** quyết định này chưa "bằng số" đúng nghĩa vì thiếu evidence — phải phỏng vấn Studio team trước CP4 để xác nhận hoặc đổi hướng.

## §3. Giải pháp tương tự đã nghiên cứu

⟵ Mỗi thành viên dùng thử 1 sản phẩm gần giống (vd. Grammarly/Vietnamese proofreading tool, TTS preview trong CapCut/Canva, LanguageTool, editor gợi ý văn phong) và trả lời 4 câu theo `02-guide.md` §2.2 — bổ sung trước CP4.

## §4. Thiết kế

- **Lát cắt MỘT CÂU:** Một biên tập viên · duyệt một kịch bản ~40 câu trước khi thu âm · AI chỉ đúng câu/đoạn nghe sượng kèm loại lỗi + lý do + gợi ý sửa tối thiểu · biên tập accept/reject từng chỗ trước khi chuyển giảng viên duyệt.
- **Non-goals (≥3 thứ KHÔNG build):**
  1. Không tự động viết lại hoặc xuất bản toàn bộ kịch bản.
  2. Không dùng nhãn "AI-generated" để kết luận về tác giả (chỉ chỉ ra câu khó đọc, không phán đoán ai viết).
  3. Không lưu trữ hay dùng kịch bản ngoài phạm vi buổi duyệt hiện tại.
  4. Không tự thêm claim/số liệu mới không có trong kịch bản gốc.
- **Mức prototype nhắm tới:** ⟵ [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật (chốt khi build ở CP2/CP3).
- **Automation:** [x] augment [ ] conditional [ ] automate — **lý do theo cost-of-error:** AI chỉ gắn cờ + giải thích + gợi ý sửa tối thiểu, không tự viết lại/xuất bản. Quy trình Studio là thu giọng trước rồi dựng hình khớp độ dài giọng — bỏ sót lỗi hoặc AI tự sửa sai giọng tác giả thì phải thu lại + dựng lại cảnh, đắt hơn nhiều so với việc người duyệt tự quyết định ngay ở bước kịch bản.
- **§4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR):**

  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | ⟵ | ⟵ (điền khi có prototype để trỏ vị trí cụ thể — xem `02-guide.md` §2.4; gợi ý G10 thu hẹp phạm vi khi nghi ngờ, G11 giải thích vì sao, G9 sửa dễ dàng cho accept/reject) |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)

⟵ Cụ thể hoá ①②③④ theo taxonomy trong `01-challenge-brief.md` + ≥8 kịch bản (guide §2.5) — hoàn thiện trước CP4. Gợi ý riêng cho C2 (từ `tracks/track-c-lesson-studio.md`):
- ① Nguồn sự thật: câu trơn tru không đủ để kết luận là lỗi — cần tránh "máy đo xác suất văn AI" đoán bừa.
- ② Mơ hồ: ranh giới lỗi nội dung vs lỗi chỉ liên quan cách đọc TTS.
- ③ Ngoài phạm vi: người dùng yêu cầu AI viết lại cả đoạn thay vì chỉ gợi ý.
- ④ Đặc thù domain: giữ đúng giọng tác giả, không tạo false positive trên văn bản người viết tốt.

## §6. Bốn đường đi của trải nghiệm

⟵ Happy path (chỉ đúng câu sượng, gợi ý hợp lý) · Low-confidence (② — câu mơ hồ giữa "phong cách riêng" và "lỗi") · Failure/không căn cứ (① — không đủ căn cứ kết luận là lỗi) · Correction (biên tập reject gợi ý, agent không lặp lại) · Ngoài phạm vi (③) · Case đặc thù domain (④) — hoàn thiện trước CP4.

## §7. Kiểm thử

- ⟵ Chiều chất lượng + định nghĩa kiểm chứng được (vd. precision trên span/category, false-positive trên đoạn văn sạch).
- ⟵ Golden set (≥20 case theo cơ cấu guide §2.6, file trong `eval/`) — track C2 yêu cầu riêng: **≥10 case tự viết/gắn nhãn tay lỗi kịch bản** + **≥1 đoạn văn sạch để đo false positive** (theo `tracks/track-c-lesson-studio.md`).
- ⟵ Quality bar: "Đạt khi ≥ ___% qua bộ, và ___" (chốt tại hạn chốt spec 21:00 17/9, giữ nguyên sau đó).
- ⟵ Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6).

## §8. Phân công & kế hoạch

- **Phân công có tên** (spec / evidence / prompt / code / demo):
  | Họ tên | MSSV | Phần việc |
  |---|---|---|
  | Hoàng Trung Hiếu (đội trưởng) | 2A202602945 | **Spec + điều phối** — §1 problem statement, §2 bảng impact, §4 lát cắt & non-goals; nộp form cả 5 mốc; dựng slide; mở đầu thuyết trình CP6 |
  | Nguyễn Thọ Đạt | 2A202602484 | **Evidence** — phỏng vấn theo Mom Test, log nguyên văn trong `interview-log.md`; tổng hợp số liệu + quote vào §1; §3 nghiên cứu giải pháp tương tự; validation CP5 |
  | Đinh Trường An | 2A202602393 | **Prompt + eval** — prompt cho agent QA; golden set trong `eval/` (≥10 case lỗi gắn nhãn + ≥1 đoạn sạch); chạy eval, bảng kết quả §7; chốt quality bar trước CP4 |
  | Phan Đức Duy | 2A202602397 | **Prototype + demo** — `codebase/` (flow duyệt, accept/reject từng finding), lời gọi AI thật + log/trace; video CP3 và video dự phòng CP5 |
- **Willing users dự kiến (≥2-3 tên, khai chính thức trước CP5):** Nguyễn Đức Thái (2A202602648) · Trần Hồng Sơn (2A20262475) — hai người đã đồng ý cho phỏng vấn và thử prototype; ⟵ cần thêm ≥1 đầu mối Studio team/lab coach do BTC giới thiệu (người dùng cuối thật của C2).
- Multi-prototype: không áp dụng.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| CP1 | Chốt hướng B2 (Trợ lý Discord) + lát cắt + evidence mining ban đầu | Canvas CP1 |
| CP1 (cập nhật) | Đổi sang hướng C2 (Vietnamese Spoken-Script QA) | Nhóm muốn thử hướng Lesson Studio; đánh đổi: mất evidence đếm-được sẵn có của B2, đổi lấy phạm vi kỹ thuật hẹp hơn trong Track C. Cần phỏng vấn Studio team trước CP4 để xác nhận hoặc quay lại B2 |
