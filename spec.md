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
- **Evidence — chuẩn B (mining `data/vlearn-pack/`, được track C cho phép thay cho khảo sát 20 người):**

  **Số đếm được.** Đo phân bố độ dài câu trên 6 transcript bản sạch (văn nói thật của giảng viên, đã trình bày trơn tru trước lớp) và đối chiếu với văn viết cùng domain (câu trả lời AI tutor, khoá K4):

  | Nguồn | Số câu | Trung vị | p90 | p95 | Dài nhất |
  |---|---|---|---|---|---|
  | Văn nói — 6 transcript giảng viên | 3.665 | 24 từ | 50 | 59 | 137 |
  | Văn viết — tutor reply K4 (3.097 lượt) | 22.191 | 27 từ | 46 | — | — |

  - **699/3.665 = 19,1% câu của giảng viên dài hơn 40 từ** — mà đây là văn nói tự nhiên, người nghe hiểu được bình thường.
  - 167 câu dài 60–95 từ vẫn là lời giảng trôi chảy.
  - Văn viết của tutor chỉ có 2,3% câu vượt ngưỡng p95 (59 từ) của văn nói — tức **văn viết không hề dài hơn văn nói**.

  **Phương pháp đếm (kiểm lại được):** `eval/mine_sentence_length.py "<path>/data/vlearn-pack"` — lấy mọi đoạn mã `[Txx-NNN]` (bỏ đoạn `[Hoạt động lớp]`), gỡ markdown ở phía tutor, tách câu theo `. ! ? …`, bỏ mẩu dưới 3 từ, đếm từ theo khoảng trắng. Data pack không commit vào repo theo quy định bảo mật.

  **≥5 ví dụ nguyên văn** (trích ngắn, dẫn mã đoạn theo đúng luật dùng vlearn-pack) — câu rất dài nhưng **vẫn nghe được**, tức là luật độ dài sẽ gắn cờ oan:
  1. `[T01-001]` — 72 từ — *"Một trong những kỹ năng mình nghĩ quan trọng và đang cần nhất — đặc biệt ở các công ty muốn đưa AI vào ứng dụng…"*
  2. `[T01-005]` — 66 từ — *"Mình nghĩ một điểm có thể tạo ra sự khác biệt với tất cả các bạn ở đây…"*
  3. `[T01-012]` — 91 từ — *"Bản thân mình trong quá trình nói chuyện với nhiều bạn và làm ở nhiều môi trường…"*
  4. `[T01-016]` — 72 từ — *"Đấy là lý do mà muốn thay đổi về mặt tư duy thì các bạn phải xác nhận…"*
  5. `[T01-018]` — 74 từ — *"Trong quá trình làm sản phẩm AI, bạn phải vừa có năng lực xây dựng sản phẩm…"*
  6. `[T01-020]` — 72 từ — *"Và cuối cùng người ta cũng không đủ kiên nhẫn để thử sai với sản phẩm của bạn…"*

  **Kết luận rút ra — và nó bác bỏ giả thuyết ban đầu của nhóm.** Nhóm đi vào với giả định "câu quá dài = câu sượng". Số liệu nói ngược: **độ dài câu một mình không phân biệt được "sượng" với "nói tự nhiên có nhịp"** — đặt ngưỡng 40 từ sẽ gắn cờ oan 19,1% lời giảng thật. Đây đúng là bài toán false-positive mà đề C2 nhấn mạnh (*"một câu trơn tru không đủ để kết luận"*, *"kiểm soát tốt false positive trên văn bản do con người viết"*). Hệ quả thiết kế: agent **không được** dùng luật độ dài đơn thuần, phải phân loại lỗi + giải thích lý do gắn với ngữ cảnh (§4), và **phải đo false positive trên chính transcript này** (§7).

  ⟵ **Bổ sung trước CP4 — phỏng vấn ≥3 người** (Mom Test, `02-guide.md` §1.3), trong đó ≥1 người thuộc Studio team/lab coach vì đó mới là người dùng cuối. Khung câu hỏi + bảng log nguyên văn đã dựng sẵn tại **[`interview-log.md`](interview-log.md)** (P1 Nguyễn Đức Thái, P2 Trần Hồng Sơn đã nhận lời; P3 chờ đầu mối BTC). Mining ở trên chứng minh *lỗi khó phân loại tồn tại*; phỏng vấn để xác nhận *biên tập viên có thật sự đau vì nó*.

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
- **Case đo false positive lấy từ chính evidence §1:** 6 câu nói dài 60–95 từ nhưng tự nhiên (`[T01-001]`, `[T01-005]`, `[T01-012]`, `[T01-016]`, `[T01-018]`, `[T01-020]`) — agent gắn cờ bất kỳ câu nào trong nhóm này là false positive. Đây là bar cứng, vì mining cho thấy 19,1% lời giảng thật dài hơn 40 từ.
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
