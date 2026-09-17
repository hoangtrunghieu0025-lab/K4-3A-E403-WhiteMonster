# AI SPEC — Agent QA kịch bản video tiếng Việt · Nhóm WhiteMonster · Zone E403

Hướng: [ ] A — VLearn  [ ] B — Trợ lý Học viên  [x] C — Lesson Studio (đề C2)
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

*(Chốt tại CP4 — 21:00 17/9. Chỗ chưa xong: `_________` hoặc `TODO:`.)*

- **Đội trưởng:** Hoàng Trung Hiếu — MSSV 2A202602945 (mã học viên nộp cả 5 mốc phải là người này)
- **Phòng / cụm:** E403 / cụm C1
- **Thành viên:** Nguyễn Thọ Đạt (2A202602484) · Đinh Trường An (2A202602393) · Phan Đức Duy (2A202602397)
- **Track/đề:** C2 — Vietnamese Spoken-Script QA (agent review kịch bản video trước khi thu âm/dựng hình)

## §1. User & Job

- **Job executor + workflow:** Biên tập viên/người viết kịch bản của Studio team; giảng viên duyệt kịch bản trước khi kịch bản được chuyển sang thu âm. Worksheet JTBD (job map 8 bước · job story · alternatives): [`jtbd-worksheet.md`](jtbd-worksheet.md)
- **Core JTBD:** Đọc lại kịch bản trước khi duyệt để tìm câu nghe sượng/khó đọc thành lời trước khi đưa vào thu âm.
- **Job stories:**
  1. **JS1** — *When* tôi vừa viết xong kịch bản ~40 câu sắp gửi thu âm, *I want to* biết ngay câu nào sẽ vấp khi đọc thành lời mà không phải đọc to cả bài, *so I can* sửa trước khi giọng được thu và cảnh được dựng khớp theo.
  2. **JS2** — *When* một công cụ gắn cờ hàng loạt câu dài trong bài tôi viết, *I want to* hiểu vì sao từng câu bị gắn cờ chứ không chỉ thấy cảnh báo "câu quá dài", *so I can* bỏ qua những câu tuy dài nhưng đọc vẫn xuôi thay vì cắt vụn cả bài.
  3. **JS3** — *When* tôi nhận lại kịch bản người khác viết hoặc một đoạn dịch từ tài liệu tiếng Anh, *I want to* được chỉ đúng chỗ sượng kèm gợi ý sửa tối thiểu, *so I can* sửa mà không viết lại cả bài làm mất giọng tác giả.
- **Alternatives hôm nay + chỗ fail:**

  | Alternative | Fail ở đâu | Vì sao chưa bỏ |
  |---|---|---|
  | Tự đọc thành tiếng cả bài | Phải đọc hết mới biết; cuối bài mệt nên bỏ sót; không lưu vết vì sao bỏ qua một câu | Cách duy nhất hiện bắt được lỗi "nghe" |
  | Nhờ LLM viết lại cả bài | Mất giọng tác giả; không nói câu nào sai, sai loại gì | Khi gấp vẫn nhanh hơn sửa tay |
  | Soát chính tả/ngữ pháp (Word, LanguageTool) | Không bắt câu đúng ngữ pháp mà đọc lên vẫn sượng | Miễn phí, có sẵn |
  | Nghe thử bằng TTS | Phải render cả bài; TTS đọc trơn cả câu sượng | Gần khâu thu âm nhất |

  TODO: thay cột "Vì sao chưa bỏ" bằng câu trả lời Q6 của người thật — [`interview-log.md`](interview-log.md)
- **Problem statement (không chữ AI):** Biên tập viên — đang tự đọc thành tiếng từng kịch bản trước khi duyệt để bắt câu "sượng" (dịch cứng, sai sắc thái, quá dài để đọc một hơi, số/viết tắt chưa chuẩn hoá) — không có công cụ chỉ đúng câu và loại lỗi, phải đọc hết cả bài mới phát hiện — dễ bỏ sót, phát hiện muộn thì phải thu lại giọng và dựng lại cảnh, tốn thời gian và tiền hơn nhiều so với sửa ngay ở bước kịch bản.
- **Evidence — chuẩn B, mining `data/vlearn-pack/`:**

  Phân bố độ dài câu trên 6 transcript giảng viên, đối chiếu với văn viết cùng domain (tutor reply K4):

  | Nguồn | Số câu | Trung vị | p90 | p95 | Dài nhất |
  |---|---|---|---|---|---|
  | Văn nói — 6 transcript giảng viên | 3.665 | 24 từ | 50 | 59 | 137 |
  | Văn viết — tutor reply K4 (3.097 lượt) | 22.191 | 27 từ | 46 | — | — |

  - **699/3.665 = 19,1% câu của giảng viên dài hơn 40 từ** — mà đây là văn nói tự nhiên, người nghe hiểu được bình thường.
  - 167 câu dài 60–95 từ vẫn là lời giảng trôi chảy.
  - Văn viết của tutor chỉ có 2,3% câu vượt ngưỡng p95 (59 từ) của văn nói — tức **văn viết không hề dài hơn văn nói**.

  **Phương pháp đếm:** `eval/mine_sentence_length.py "<path>/data/vlearn-pack"` — lấy mọi đoạn mã `[Txx-NNN]` (bỏ `[Hoạt động lớp]`), gỡ markdown phía tutor, tách câu theo `. ! ? …`, bỏ mẩu dưới 3 từ, đếm từ theo khoảng trắng.

  **6 ví dụ nguyên văn** — câu rất dài nhưng vẫn nghe được:
  1. `[T01-001]` — 72 từ — *"Một trong những kỹ năng mình nghĩ quan trọng và đang cần nhất — đặc biệt ở các công ty muốn đưa AI vào ứng dụng…"*
  2. `[T01-005]` — 66 từ — *"Mình nghĩ một điểm có thể tạo ra sự khác biệt với tất cả các bạn ở đây…"*
  3. `[T01-012]` — 91 từ — *"Bản thân mình trong quá trình nói chuyện với nhiều bạn và làm ở nhiều môi trường…"*
  4. `[T01-016]` — 72 từ — *"Đấy là lý do mà muốn thay đổi về mặt tư duy thì các bạn phải xác nhận…"*
  5. `[T01-018]` — 74 từ — *"Trong quá trình làm sản phẩm AI, bạn phải vừa có năng lực xây dựng sản phẩm…"*
  6. `[T01-020]` — 72 từ — *"Và cuối cùng người ta cũng không đủ kiên nhẫn để thử sai với sản phẩm của bạn…"*

  **Kết luận — số liệu bác bỏ giả thuyết ban đầu của nhóm.** Nhóm vào với giả định "câu quá dài = câu sượng"; số liệu nói ngược: **độ dài câu một mình không phân biệt được "sượng" với "nói tự nhiên có nhịp"** — ngưỡng 40 từ gắn cờ oan 19,1% lời giảng thật. Hệ quả thiết kế: agent không dùng luật độ dài đơn thuần, phải phân loại lỗi + giải thích lý do gắn với ngữ cảnh (§4), và đo false positive trên chính transcript này (§7).

  TODO: phỏng vấn ≥3 người trước CP4, ≥1 người thuộc Studio team/lab coach — chép số liệu + quote từ [`interview-log.md`](interview-log.md) vào đây (P1, P2 đã nhận lời; P3 chờ đầu mối BTC)

## §2. Impact & quyết định chọn

| Ứng viên | Bao nhiêu người gặp | Tần suất | Mỗi lần tốn gì | Khả thi trong sự kiện? |
|---|---|---|---|---|
| **A. Agent QA kịch bản trước thu âm, chỉ đúng câu sượng + gợi ý sửa tối thiểu (C2 — đã chọn)** | `_________` (Q7) — ước tính: kịch bản video của khoá đều qua tay một nhóm biên tập nhỏ | `_________` lần/tuần (Q7) — mỗi kịch bản trước khi thu | Đọc thành tiếng lại cả kịch bản; phát hiện muộn thì tốn công thu lại giọng + dựng lại cảnh | Trung bình — cần tự viết + gắn nhãn tay ≥10 case kịch bản lỗi làm golden set (pack không có sẵn) |
| B. Sinh graph tri thức + quiz có trích nguồn từ transcript (C1) | Giảng viên soạn quiz + học viên toàn khoá | Mỗi bài giảng mới | Giảng viên tự soạn tay câu hỏi; học viên học theo lộ trình tuyến tính dù đã hiểu một phần | Khó hơn — cần xây graph tri thức từ đầu, phạm vi rộng hơn nhiều so với 3 buổi build |
| C. ScriptScout — agent tự tìm tài liệu viết kịch bản có dẫn nguồn (C3) | Người viết kịch bản Studio team | Mỗi video mới cần kịch bản từ đầu | Nhiều ngày tự đọc tài liệu + viết + không ai kiểm được câu nào lấy từ đâu | Khó hơn — agent phải tự tìm & thẩm định nguồn web, rủi ro cao hơn (prompt injection từ trang lạ, hai nguồn mâu thuẫn) |
| D. FeedbackRadar — gom góp ý người học thành kế hoạch sửa video (C5) | Đội sản xuất + giảng viên, gián tiếp là người học | Sau mỗi đợt học có video mới | Đọc tay từng góp ý rồi tự quyết định sửa gì, hay làm lại gần cả video dù chỉ vài câu có vấn đề | Trung bình — cần tự thu thập ~100 góp ý thật (khảo sát bạn cùng lớp) để làm golden set |

- **Ứng viên ĐÃ LOẠI + vì sao:** B/C1 (phạm vi quá rộng — xây graph tri thức từ đầu không vừa 3 buổi) · C/C3 (rủi ro kỹ thuật cao hơn — agent tự tìm nguồn web, phạm vi an toàn phức tạp hơn) · D/C5 (cần tự thu thập ~100 góp ý thật mới đủ golden set, khối lượng evidence lớn hơn C2) — cả ba giữ lại nếu nhóm đổi hướng sau phỏng vấn Studio team.
- **Ứng viên CHỌN + vì sao:** C2 — phạm vi hẹp nhất trong 5 đề Track C (chỉ QA một kịch bản, không phải dựng graph/tự tìm nguồn/gom góp ý), và có sẵn dữ liệu tham chiếu thật (transcript bản sạch) để định nghĩa chuẩn "nghe được" ngay cả khi chưa phỏng vấn xong. **Tự khai:** quyết định chưa "bằng số" vì cột người-gặp và tần suất còn trống.

## §3. Giải pháp tương tự đã nghiên cứu

TODO: mỗi người thử 1 sản phẩm gần giống rồi điền 4 ô — gợi ý LanguageTool · Grammarly · TTS preview của CapCut/Canva · editor gợi ý văn phong

| Sản phẩm | Người thử | Flow của họ | Đáng học | Đáng né | Mình khác gì ở lát cắt này |
|---|---|---|---|---|---|
| `_________` | `_________` | `_________` | `_________` | `_________` | `_________` |
| `_________` | `_________` | `_________` | `_________` | `_________` | `_________` |
| `_________` | `_________` | `_________` | `_________` | `_________` | `_________` |
| `_________` | `_________` | `_________` | `_________` | `_________` | `_________` |

## §4. Thiết kế

- **Lát cắt MỘT CÂU:** Một biên tập viên · duyệt một kịch bản ~40 câu trước khi thu âm · AI chỉ đúng câu/đoạn nghe sượng kèm loại lỗi + lý do + gợi ý sửa tối thiểu · biên tập có bản kịch bản đã sạch câu sượng trước khi chuyển thu âm, không phải đọc dò lại cả bài.
- **Non-goals (≥3 thứ KHÔNG build):**
  1. Không tự động viết lại hoặc xuất bản toàn bộ kịch bản.
  2. Không dùng nhãn "AI-generated" để kết luận về tác giả (chỉ chỉ ra câu khó đọc, không phán đoán ai viết).
  3. Không lưu trữ hay dùng kịch bản ngoài phạm vi buổi duyệt hiện tại.
  4. Không tự thêm claim/số liệu mới không có trong kịch bản gốc.
- **Mức prototype nhắm tới:** [ ] Sketch [x] Mock [ ] Working — **thật:** luồng duyệt end-to-end trong `codebase/mockup.html` (hiển thị span, Accept / Sửa tay / Bỏ qua, hoàn tác, lọc theo nhóm lỗi, audit trail) · **mock:** 7 finding là dữ liệu tĩnh, chưa gọi AI. TODO: đổi sang Working nếu CP3 nối được lời gọi AI thật.
- **Automation:** [x] augment [ ] conditional [ ] automate — **lý do theo cost-of-error:** AI chỉ gắn cờ + giải thích + gợi ý sửa tối thiểu, không tự viết lại/xuất bản. Quy trình Studio là thu giọng trước rồi dựng hình khớp độ dài giọng — bỏ sót lỗi hoặc AI tự sửa sai giọng tác giả thì phải thu lại + dựng lại cảnh, đắt hơn nhiều so với việc người duyệt tự quyết định ngay ở bước kịch bản.
- **§4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR):**

  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | **G1** — làm rõ hệ thống làm được gì | Banner đầu trang `mockup.html`: "MOCK · findings là dữ liệu tĩnh, chưa gọi AI thật" + dòng "AI đề xuất — bạn quyết từng chỗ" |
  | **G2** — làm rõ nó làm tốt đến đâu | Mỗi finding có dòng **Độ chắc** (cao / vừa / thấp); `F2` tách riêng "lỗi phát âm, không phải lỗi nội dung" |
  | **G8** — gạt bỏ dễ dàng | Nút **Bỏ qua** trên mọi finding; bỏ qua rồi thì highlight biến khỏi kịch bản |
  | **G9** — sửa dễ dàng | Nút **Sửa tay** (sửa ngay trên gợi ý) và **Hoàn tác** trên mọi finding đã xử lý |
  | **G10** — thu hẹp phạm vi khi nghi ngờ | `F4`, `F6`: không đề xuất sửa, hiện khối "Không đủ căn cứ để tự sửa" thay vì đoán |
  | **G11** — giải thích vì sao | Mỗi finding có lý do gắn với ngữ cảnh câu đó, không phải nhãn lỗi chung chung |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)

**Bốn lớp cho lát cắt này:** ① **Nguồn sự thật** — câu trơn tru không đủ để kết luận là lỗi · ② **Mơ hồ** — ranh giới lỗi nội dung vs lỗi chỉ liên quan cách đọc · ③ **Ngoài phạm vi** — bị đòi viết lại cả đoạn · ④ **Đặc thù domain** — giữ giọng tác giả, không gắn cờ oan văn người viết tốt.

| # | Tình huống cụ thể | Lớp | Hành vi mong muốn | Nguyên tắc |
|---|---|---|---|---|
| 1 | Kịch bản khẳng định "tăng gấp đôi hiệu suất trong một quý", không nguồn nào trong bài | ① | Gắn cờ claim thiếu căn cứ, **không tự sửa, không bịa nguồn**; đề nghị người bổ sung nguồn hoặc hạ thành phát biểu định tính | G10 · PAIR 6.2 |
| 2 | Câu dài 63 từ nhưng đọc vẫn xuôi | ④ | **Không gắn cờ**; hiện khối "Không gắn cờ — câu 5 dài 63 từ" để người duyệt biết agent đã xét rồi bỏ qua | G2 |
| 3 | Cụm tiếng Anh "cost-of-error" xen giữa câu tiếng Việt — có thể là thuật ngữ chuẩn của khoá | ② | Độ chắc **THẤP**, không hiện nút Áp dụng, nói rõ cần người xác minh | G10 · G2 |
| 4 | Ký hiệu `%` chưa chuẩn hoá cách đọc | ② | Gắn cờ nhưng ghi rõ "lỗi phát âm, không phải lỗi nội dung" — tách khỏi lỗi ngữ nghĩa | G1 · G2 |
| 5 | Câu lặp nguyên vế + chồng 3 mệnh đề danh từ hoá | ④ | Lý do phải nói rõ "không phải vì câu dài — vấn đề là lặp và chồng mệnh đề" | G11 |
| 6 | Câu 1 xưng "các bạn", câu sau đổi sang "bạn" + khẩu ngữ | ④ | Gắn cờ register lệch, độ chắc **vừa**, gợi ý sửa tối thiểu giữ nguyên phần còn lại | G2 · G9 |
| 7 | Ẩn dụ chê nặng ("tự đâm đầu vào tường") lệch giọng giảng trung tính | ④ | Gắn cờ sai sắc thái kèm lý do gắn với đối tượng người học, gợi ý bản trung tính hơn | G11 |
| 8 | Người duyệt yêu cầu agent viết lại cả kịch bản cho mượt | ③ | `_________` — TODO: hành vi từ chối + giải thích phạm vi, chưa dựng trong `mockup.html` |  `_________` |
| 9 | `_________` | `_________` | `_________` | `_________` |

TODO: mỗi lớp ①②③④ cần ≥2 case tương ứng trong golden set §7 — hiện ① và ③ mới có 1.

## §6. Bốn đường đi của trải nghiệm

| Đường đi | Hành vi | Xem ở đâu trong `mockup.html` |
|---|---|---|
| **Happy path** | Chỉ đúng span, lý do rõ, gợi ý sửa tối thiểu — bấm Áp dụng là xong | `F1` cú pháp dịch |
| **Low-confidence ②** | Độ chắc THẤP, **không có nút Áp dụng**, agent nói rõ cần người xác minh | `F4` code-switch |
| **Failure / không căn cứ ①** | Agent từ chối tự sửa claim, nêu hai lựa chọn cho người duyệt | `F6` claim "tăng gấp đôi hiệu suất" |
| **Correction** | **Sửa tay** trên mọi finding; mọi finding đã xử lý đều **Hoàn tác** được | Nút trên từng finding |
| **Ngoài phạm vi ③** | `_________` — TODO: bị đòi viết lại cả bài thì agent trả lời thế nào | Chưa dựng |
| **Đặc thù domain ④** | Câu dài nhưng xuôi thì không gắn cờ, và nói rõ đã xét | Khối xanh "Không gắn cờ — câu 5 dài 63 từ" |

## §7. Kiểm thử

- **Chiều chất lượng + định nghĩa kiểm chứng được:** `_________`
  TODO: chọn 2–3 chiều, mỗi chiều một định nghĩa pass/fail — gợi ý: precision trên span, đúng category, false positive trên đoạn văn sạch
- **Golden set** (file trong `eval/`): `_________`/20 case — TODO: ≥10 case lỗi kịch bản tự viết + gắn nhãn tay · ≥1 đoạn văn sạch đo false positive · ≥2 case cho mỗi lớp §5
- **Case đo false positive lấy từ evidence §1:** 6 câu nói dài 60–95 từ nhưng tự nhiên (`[T01-001]`, `[T01-005]`, `[T01-012]`, `[T01-016]`, `[T01-018]`, `[T01-020]`) — agent gắn cờ bất kỳ câu nào trong nhóm này là false positive.
- **Quality bar:** "Đạt khi ≥ `____`% qua bộ, và `_________`"
  TODO: chốt trước 21:00 17/9, sau đó giữ nguyên
- **Kết quả các lượt chạy:**

  | Lượt | Ngày | % qua bộ | False positive | Ghi chú |
  |---|---|---|---|---|
  | `____` | `____` | `____` | `____` | `____` |

## §8. Phân công & kế hoạch

- **Phân công có tên** (spec / evidence / prompt / code / demo):
  | Họ tên | MSSV | Phần việc |
  |---|---|---|
  | Hoàng Trung Hiếu (đội trưởng) | 2A202602945 | **Spec + điều phối** — §1 problem statement, §2 bảng impact, §4 lát cắt & non-goals; nộp form cả 5 mốc; dựng slide; mở đầu thuyết trình CP6 |
  | Nguyễn Thọ Đạt | 2A202602484 | **Evidence** — phỏng vấn theo Mom Test, log nguyên văn trong `interview-log.md`; tổng hợp số liệu + quote vào §1; §3 nghiên cứu giải pháp tương tự; validation CP5 |
  | Đinh Trường An | 2A202602393 | **Prompt + eval** — prompt cho agent QA; golden set trong `eval/` (≥10 case lỗi gắn nhãn + ≥1 đoạn sạch); chạy eval, bảng kết quả §7; chốt quality bar trước CP4 |
  | Phan Đức Duy | 2A202602397 | **Prototype + demo** — `codebase/` (flow duyệt, accept/reject từng finding), lời gọi AI thật + log/trace; video CP3 và video dự phòng CP5 |
- **Willing users:** Nguyễn Đức Thái (2A202602648) · Trần Hồng Sơn (2A20262475) — đã đồng ý cho phỏng vấn và thử prototype · `_________`
  TODO: xin BTC ≥1 đầu mối Studio team/lab coach — người dùng cuối thật của C2
- Multi-prototype: không áp dụng.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| CP1 | Chốt hướng B2 (Trợ lý Discord) + lát cắt + evidence mining ban đầu | Canvas CP1 |
| CP1 (cập nhật) | Đổi sang hướng C2 (Vietnamese Spoken-Script QA) | Nhóm muốn thử hướng Lesson Studio; đánh đổi: mất evidence đếm-được sẵn có của B2, đổi lấy phạm vi kỹ thuật hẹp hơn trong Track C. Cần phỏng vấn Studio team trước CP4 để xác nhận hoặc quay lại B2 |
