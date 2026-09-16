# AI SPEC — Bản tin cuối ngày cho TA · Nhóm WhiteMonster · Zone E403

Hướng: [ ] A — VLearn  [x] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [x] Tối ưu tính năng có sẵn  [ ] Tính năng mới

*(Draft từ Canvas CP1 — chưa đầy đủ, hoàn thiện dần đến hạn chốt spec 21:00 17/9 tại CP4. Phần còn thiếu đánh dấu `⟵`.)*

- **Đội trưởng:** ⟵ Họ tên — MSSV ⟵ ____ (mã học viên nộp cả 5 mốc phải là người này)
- **Phòng / cụm:** E403 / cụm ⟵ ____
- **Track/đề:** B2 — Trợ lý Discord, tính năng mới cho TA (cải tiến trên nền bản tin "Học viên đang hỏi gì" đang chạy thật)

## §1. User & Job

- **Job executor + workflow:** TA/Mod trực các kênh Discord public của khoá — người cuối mỗi ngày cần biết câu nào học viên hỏi mà **chưa ai trả lời**, để chủ động vào trả lời trước khi ảnh hưởng đến deadline/tiến độ của học viên. *(Không phải "học viên nói chung": job ở đây là của người trực, không phải của người hỏi.)*
- **Core JTBD:** Rà lại các kênh cuối ngày để tìm và trả lời những câu hỏi còn bị bỏ sót.
- **Problem statement (không chữ AI):** TA/Mod cuối ngày — đang rà lại hàng trăm tin rải trên nhiều kênh song song để tìm câu học viên hỏi mà chưa ai trả lời — không có cách lọc nhanh nên dễ bỏ sót — học viên phải tự hỏi lại hoặc chờ lâu, mất niềm tin vào kênh hỗ trợ ngay tuần onboarding.
- **Evidence (chuẩn B — mining; chuẩn A sẽ bổ sung bằng khảo sát trước hạn chốt spec):**
  - **Số liệu mining:** trên `k4_messages.csv` (779 tin của học viên, 12–14/9/2026, 2 server). Phương pháp: lọc `content` chứa dấu `"?"` → **107 câu hỏi** (n = 107); đối chiếu `msg_id` của từng câu hỏi với toàn bộ giá trị cột `reply_to` trong file → **23/107 (21,5%)** không có bất kỳ tin nào trong pack trỏ `reply_to` về nó trong suốt 3 ngày. Cách đếm lại: `eval/mining_unanswered_questions.py <path/to/k4_messages.csv>` (không commit data pack kèm repo theo đúng quy định bảo mật).
  - **≥5 quote/ví dụ nguyên văn** (đã ẩn danh theo pack, trích ≤2 câu/ví dụ, dẫn `msg_id` thay vì chép dài):
    1. `M88027` — *"cho em hỏi Lab2 có được extend thời gian submit thêm không v ạ? Em lỡ nộp muộn 1 phút không submit bài được ạ"* — không có phản hồi trong pack; liên quan trực tiếp deadline.
    2. `M99769` — *"cho mình hỏi một team mấy bạn?"* — không có phản hồi.
    3. `M27566` — *"cho em hỏi khóa mình có cấp giấy chứng nhận sinh viên cho học viên không ạ?"* — không có phản hồi.
    4. `M83398` — *"đủ chỗ ở đây hiểu như thế nào [HV] nhỉ?"* — không có phản hồi.
    5. **Câu hỏi lặp vì chưa được trả lời:** cùng một tác giả (`D1253`) hỏi lại **y nguyên nội dung** sau 3 giờ 24 phút vì không thấy ai trả lời — `M30246` (19:51) *"Tại e thấy trong sổ tay phải có xác nhận của giám đốc, nên là k biết e có phải chờ mail phản hồi k ạ???"* → `M48859` (23:15) lặp lại gần như nguyên văn.
  - **Baseline sản phẩm đang chạy** (`k4_daily_reports.md`, 4/4 bản tin mẫu): mục "Đã có phản hồi, chưa xác nhận đã xử lý" lặp lại nhưng **không kèm link tới tin gốc** để TA bấm vào theo dõi; cả 4/4 bản tin còn dính lỗi chèn chuỗi "nguồn tham chiếu" vào giữa từ (vd. "khi" → "nguồn tham chiếuhi").
  - ⟵ Khảo sát chuẩn A (≥20 người ngoài nhóm, ≥50% xác nhận, log đầy đủ câu hỏi + từng câu trả lời) — bổ sung trước CP4.

## §2. Impact & quyết định chọn

| Ứng viên | Bao nhiêu người gặp | Tần suất | Mỗi lần tốn gì | Khả thi trong sự kiện? |
|---|---|---|---|---|
| **A. Bản tin cuối ngày liệt kê câu hỏi chưa trả lời sau 4h kèm link** *(đã chọn)* | 23/107 câu hỏi trong pack 3 ngày không có phản hồi; nhân rộng ra cả khoá ~1.000 học viên × nhiều kênh mỗi ngày | Lặp lại mỗi ngày trong suốt build phase | Học viên chờ/hỏi lại (vd. `D1253` phải hỏi lại sau 3h24'); TA tốn thời gian dò lại lịch sử kênh cuối ca | Có — đã có bản tin baseline chạy thật để cải tiến, chỉ cần thêm bước lọc "chưa trả lời sau N giờ" + link |
| B. Bot trả lời logistics chỉ từ nguồn thông báo chính thức (B1) | Chỉ 4/107 câu hỏi trong pack liên quan trực tiếp deadline, nhưng mỗi thông báo sai ảnh hưởng nhiều người cùng lúc | Thấp hơn về tần suất câu hỏi nhưng hậu quả nặng khi sai | Học viên nộp trễ mất điểm; TA phải xử lý khiếu nại | Khó hơn — cần nguồn "thông báo chính thức" làm căn cứ, không có sẵn trong data pack |
| C. Sửa lỗi hiển thị của bản tin hiện tại (chuỗi "nguồn tham chiếu" chèn giữa từ, tóm tắt cắt cụt) | Toàn bộ người đọc 4 bản tin mẫu (TA/Mod, xuất hiện ở 4/4 bản tin) | Xảy ra ở mọi bản tin đã đăng | TA mất thời gian đoán nghĩa, giảm độ tin cậy, có thể bỏ qua không dùng bản tin nữa | Có, nhưng đây là bug hiển thị (không cần quyết định AI) — không đủ để làm lát cắt riêng |
| D. Chủ động phát hiện học viên "stuck" (nhắn lặp lại nhiều lần chưa được trả lời) để TA hỗ trợ sớm | Bằng chứng hiện có: 1 case rõ (`D1253`) trong 3 ngày — mẫu còn nhỏ để khẳng định quy mô | Không đủ dữ liệu ước lượng tần suất đáng tin | Học viên mất kiên nhẫn, cảm giác bị bỏ rơi | Rủi ro cao: ranh giới "chủ động" và "phiền" (an toàn track B2) chưa rõ, dễ làm quá phạm vi |

- **Ứng viên ĐÃ LOẠI + vì sao:** B (thiếu nguồn thông báo chính thức để build kịp trong sự kiện) · C (chỉ là bug hiển thị, không đủ chiều sâu cho một quyết định AI) · D (bằng chứng còn mỏng — 1 case, rủi ro "chủ động thành phiền" chưa kiểm soát được) — cả ba giữ lại làm việc mở rộng sau nếu có thêm evidence.
- **Ứng viên CHỌN + vì sao (bằng số):** A — có 23/107 (21,5%) case đếm được trong 3 ngày (nhiều hơn hẳn B với 4/107), và build nổi trong sự kiện vì đã có sản phẩm baseline (`k4_daily_reports.md`) để cải tiến trực tiếp thay vì làm từ đầu.

## §3. Giải pháp tương tự đã nghiên cứu

⟵ Mỗi thành viên dùng thử 1 sản phẩm gần giống (vd. Discord "forum post" chưa resolve, GitHub issue triage bot, Intercom "unanswered" filter...) và trả lời 4 câu theo `02-guide.md` §2.2 — bổ sung trước CP4.

## §4. Thiết kế

- **Lát cắt MỘT CÂU:** Một TA trực kênh · cuối ngày · AI liệt kê các câu hỏi của học viên chưa có phản hồi sau 4 giờ kèm link tin gốc · TA không bỏ sót câu nào và trả lời đúng người trước khi qua ngày mới.
- **Non-goals (≥3 thứ KHÔNG build):**
  1. Không tự động soạn hoặc gửi câu trả lời thay TA.
  2. Không xử lý tin nhắn riêng (DM) hay kênh private — chỉ kênh public như data pack.
  3. Không suy đoán danh tính/định danh học viên ngoài mã ẩn danh có sẵn.
  4. ⟵ (bổ sung nếu cần)
- **Mức prototype nhắm tới:** ⟵ [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật (chốt khi build ở CP2/CP3).
- **Automation:** [x] augment [ ] conditional [ ] automate — **lý do theo cost-of-error:** AI chỉ lọc & xếp danh sách câu hỏi chưa có phản hồi kèm link nguồn; TA đọc lại và tự quyết định trả lời, AI không tự soạn/gửi câu trả lời thay. Bỏ sót hoặc gắn nhầm một câu liên quan deadline/điểm số (như `M88027`) thì hậu quả đến thẳng học viên và đắt (trễ hạn, mất điểm, khiếu nại) — nên bước quyết định cuối phải là người.
- **§4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR):**

  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | ⟵ | ⟵ (điền khi có prototype để trỏ vị trí cụ thể — xem `02-guide.md` §2.4) |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)

⟵ Cụ thể hoá ①②③④ theo taxonomy trong `01-challenge-brief.md` + ≥8 kịch bản (guide §2.5) — hoàn thiện trước CP4.

## §6. Bốn đường đi của trải nghiệm

⟵ Happy path · Low-confidence (②) · Failure/không căn cứ (①) · Correction (user sửa) · Ngoài phạm vi (③) · Case đặc thù domain (④) — hoàn thiện trước CP4.

## §7. Kiểm thử

- ⟵ Chiều chất lượng + định nghĩa kiểm chứng được.
- ⟵ Golden set (≥20 case theo cơ cấu guide §2.6, file trong `eval/`) — bao gồm mở rộng từ các case thật đã tìm ở §1 (`M88027`, `M99769`, `M30246`/`M48859`, ...).
- ⟵ Quality bar: "Đạt khi ≥ ___% qua bộ, và ___" (chốt tại hạn chốt spec 21:00 17/9, giữ nguyên sau đó).
- ⟵ Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6).

## §8. Phân công & kế hoạch

- ⟵ Phân công có tên: spec / evidence / prompt / code / demo — theo bảng thành viên ở đầu `README.md`.
- **Willing users dự kiến (≥2-3 tên, khai chính thức trước CP5):** ⟵ điền tên thật khi khảo sát TA/Mod trong giờ nghỉ (hỏi về lần gần nhất họ bị bỏ sót câu hỏi, không hỏi "bạn có muốn tính năng X không" — theo `02-guide.md` §1.3).
- Multi-prototype: không áp dụng.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| CP1 | Chốt hướng B2 + lát cắt + evidence mining ban đầu | Canvas CP1 |
