# AI SPEC — Agent QA kịch bản video tiếng Việt · Nhóm WhiteMonster · Zone E403

Hướng: [ ] A — VLearn  [ ] B — Trợ lý Học viên  [x] C — Lesson Studio (đề C2)
Loại: [ ] Tối ưu tính năng có sẵn  [x] Tính năng mới

*(Chốt tại CP4 — 21:00 17/9. Chỗ chưa xong: `_________` hoặc `TODO:`.)*

- **Đội trưởng:** Hoàng Trung Hiếu — MSSV 2A202602945 (mã học viên nộp cả 5 mốc phải là người này)
- **Phòng / cụm:** E403 / cụm C1
- **Thành viên:** Nguyễn Thọ Đạt (2A202602484) · Đinh Trường An (2A202602393) · Phan Đức Duy (2A202602397)
- **Track/đề:** C2 — Vietnamese Spoken-Script QA (agent review kịch bản video trước khi dựng video)

## §1. User & Job

- **Job executor + workflow:** **Lab coach của khoá** — học viên khoá trước làm video bài giảng: tự viết hoặc để AI sinh kịch bản, rồi dựng video bằng AI **kể cả giọng đọc (TTS)**. Không có khâu thu mic, không có giảng viên ngồi duyệt kịch bản — mentor là chuyên gia đi làm, không tham gia khâu này. Người này vừa viết, vừa duyệt, vừa xuất bản. Worksheet JTBD (job map 8 bước · job story · alternatives): [`jtbd-worksheet.md`](jtbd-worksheet.md)
- **Core JTBD:** Đọc lại kịch bản để tìm câu nghe sượng/khó đọc thành lời, trước khi đưa nó thành giọng đọc — dù giọng đó là AI, là mình tự thu, hay là người đọc trực tiếp.
- **Job stories:**
  1. **JS1** — *When* tôi sắp cho AI dựng video từ kịch bản này, *I want to* biết câu nào nghe sẽ sượng **trước khi render** — vì nghe lại bản đã dựng không phát hiện được, giọng máy đọc trôi hết, *so I can* bài giảng đăng ra không nghe như máy đọc.
  2. **JS2** — *When* một công cụ gắn cờ hàng loạt câu dài trong bài tôi viết, *I want to* hiểu vì sao từng câu bị gắn cờ chứ không chỉ thấy cảnh báo "câu quá dài", *so I can* bỏ qua những câu tuy dài nhưng đọc vẫn xuôi thay vì cắt vụn cả bài.
  3. **JS3** — *When* tôi cân nhắc đưa bài cho một công cụ soát, *I want to* được chỉ đúng chỗ sượng kèm gợi ý sửa tối thiểu chứ không bị viết lại hộ, *so I can* giữ nguyên giọng văn của mình. *(P1 Q6 — chưa dùng tool AI nào vì "sợ dùng máy móc nó sửa mất cái 'chất' giọng của mình".)*
- **Alternatives hôm nay + chỗ fail:**

  | Alternative | Fail ở đâu | Vì sao chưa bỏ |
  |---|---|---|
  | Tự đọc thành tiếng / đọc dò tay | Phải đọc hết mới biết; vẫn lọt (3/3 từng lọt); không lưu vết vì sao bỏ qua một câu | *"tiếng Việt lắt léo, đọc không có ngữ điệu là không biết câu đó sượng"* (P2) |
  | Word check chính tả | Chỉ bắt lỗi chính tả, không bắt câu đúng ngữ pháp mà đọc lên vẫn sượng | *"quen đọc bằng mắt rồi"* — miễn phí, có sẵn (P1) |
  | Grammarly | Dùng được cho tiếng Anh, tiếng Việt thì "chịu" | Vẫn giữ cho phần tiếng Anh (P2) |
  | Cho AI soát | P3 đã dùng — nhưng soát **logic và nguồn**, không soát độ trôi khi đọc | Giải được phần factuality, không giải phần đọc (P3) |
  | Nhờ AI viết lại cả bài | Mất giọng tác giả | *"sợ dùng máy móc nó sửa mất cái 'chất' giọng của mình"* — P1 **không dùng** vì lý do này |
- **Problem statement (không chữ AI):** Người làm video bài giảng — đang đọc dò từng kịch bản để bắt câu "sượng" (dịch cứng, sai sắc thái, quá dài để đọc một hơi, số/viết tắt chưa chuẩn hoá), mất **45 phút đến 1 tiếng mỗi bài, 2–10 lần mỗi tuần** — không có công cụ nào chỉ đúng câu và nói nó sai loại gì, phải đọc hết cả bài mới phát hiện, nên vẫn lọt: 3/3 người được hỏi đều từng để sót. **Nghe lại bản đã dựng cũng không cứu được** — giọng máy đọc trơn tru cả câu sượng, không hụt hơi, không líu lưỡi, nên lỗi chỉ lộ ra khi người xem thấy bài giảng nghe như máy đọc.
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

- **Evidence bổ sung — 3 phỏng vấn Mom Test, log nguyên văn:** [`interview-log.md`](interview-log.md)

  | Người | Vai | Đọc soát mỗi lần | Khi lọt xuống khâu sau | Tần suất |
  |---|---|---|---|---|
  | P1 · Nguyễn Đức Thái | Làm nội dung, tự thu voice-off | 45' / 5 trang | **~1 tiếng** thu lại + cắt ghép audio | 2–3 lần/tuần |
  | P2 · Trần Hồng Sơn | Editor/reviewer kịch bản MC | 1 tiếng / 10 trang | MC vấp ngay trên sân khấu; sau đó bắt cả nhóm đọc nháp thành tiếng trước mặt | ~10 lần/tuần |
  | P3 · lab coach | Soạn kịch bản bài giảng | nửa buổi – 1 ngày (tính cả soạn) | 5 phút | 5 kịch bản/tuần |

  - **3/3 đang đọc dò bằng tay hoặc đọc thành tiếng** — in ra giấy gạch bút đỏ (P1) · lẩm bẩm đọc to trên Google Docs (P2).
  - **3/3 từng để lọt câu sượng xuống khâu sau.**
  - **0/3 có công cụ soát được câu sượng tiếng Việt** — P1 chỉ dùng Word check chính tả · P2 dùng Grammarly nhưng chỉ cho tiếng Anh · P3 dùng AI soát logic và nguồn, không soát độ trôi khi đọc.

  **Quote nguyên văn:**
  1. *"Lúc thu âm voice-off xong xuôi hết rồi, đến đoạn nghe lại file audio mới thấy có một đoạn viết quá dài, lúc đọc bị hụt hơi nghe rất giả trân."* — P1, Q3
  2. *"lúc MC lên sân khấu đọc mới thấy cái câu đó nó không hợp văn nói, MC bị líu lưỡi vấp ngay trên sân khấu."* — P2, Q3
  3. *"tiếng Việt lắt léo, đọc không có ngữ điệu là không biết câu đó sượng."* — P2, Q6
  4. *"sợ dùng máy móc nó sửa mất cái 'chất' giọng của mình."* — P1, Q6

  **Ba người, ba khâu sau khác nhau — và P3 mới là người dùng đại diện:**

  | | Khâu sau | Sửa muộn tốn gì |
  |---|---|---|
  | P3 · lab coach | **AI dựng video, AI đọc giọng** | 5 phút — render lại gần như miễn phí |
  | P1 | Tự thu mic voice-off | ~1 tiếng thu lại + cắt ghép |
  | P2 | MC đọc trực tiếp trên sân khấu | Sự cố trước khán giả, không sửa lại được |

  Video bài giảng của khoá do lab coach làm bằng AI, giọng là TTS — **nên chi phí thật không nằm ở việc làm lại, mà nằm ở 45'–1 tiếng đọc dò mỗi bài và ở chất lượng bài giảng đăng ra**. P1 và P2 giữ trong evidence để cho thấy job tồn tại ngoài phạm vi một quy trình, nhưng lập luận §4 **không dựa vào chi phí thu lại của họ**.

  **Chuẩn khai:** B (mining) + 3 phỏng vấn có log nguyên văn. **Không khai chuẩn A** — A cần ≥20 người.

## §2. Impact & quyết định chọn

| Ứng viên | Bao nhiêu người gặp | Tần suất | Mỗi lần tốn gì | Khả thi trong sự kiện? |
|---|---|---|---|---|
| **A. Agent QA kịch bản trước khi dựng video, chỉ đúng câu sượng + gợi ý sửa tối thiểu (C2 — đã chọn)** | **3/3 người được hỏi đều gặp**; đều không có công cụ nào soát được | **2–10 lần/tuần** mỗi người (P1 2–3 · P3 5 · P2 ~10) | **45'–1 tiếng đọc dò mỗi kịch bản**, mà vẫn lọt; lọt rồi thì bài giảng đăng ra nghe như máy đọc — giọng TTS không để lộ câu sượng | Trung bình — cần tự viết + gắn nhãn tay ≥10 case kịch bản lỗi làm golden set (pack không có sẵn) |
| B. Sinh graph tri thức + quiz có trích nguồn từ transcript (C1) | Giảng viên soạn quiz + học viên toàn khoá | Mỗi bài giảng mới | Giảng viên tự soạn tay câu hỏi; học viên học theo lộ trình tuyến tính dù đã hiểu một phần | Khó hơn — cần xây graph tri thức từ đầu, phạm vi rộng hơn nhiều so với 3 buổi build |
| C. ScriptScout — agent tự tìm tài liệu viết kịch bản có dẫn nguồn (C3) | Người viết kịch bản Studio team | Mỗi video mới cần kịch bản từ đầu | Nhiều ngày tự đọc tài liệu + viết + không ai kiểm được câu nào lấy từ đâu | Khó hơn — agent phải tự tìm & thẩm định nguồn web, rủi ro cao hơn (prompt injection từ trang lạ, hai nguồn mâu thuẫn) |
| D. FeedbackRadar — gom góp ý người học thành kế hoạch sửa video (C5) | Đội sản xuất + giảng viên, gián tiếp là người học | Sau mỗi đợt học có video mới | Đọc tay từng góp ý rồi tự quyết định sửa gì, hay làm lại gần cả video dù chỉ vài câu có vấn đề | Trung bình — cần tự thu thập ~100 góp ý thật (khảo sát bạn cùng lớp) để làm golden set |

- **Ứng viên ĐÃ LOẠI + vì sao:** B/C1 (phạm vi quá rộng — xây graph tri thức từ đầu không vừa 3 buổi) · C/C3 (rủi ro kỹ thuật cao hơn — agent tự tìm nguồn web, phạm vi an toàn phức tạp hơn) · D/C5 (cần tự thu thập ~100 góp ý thật mới đủ golden set, khối lượng evidence lớn hơn C2) — cả ba giữ lại nếu nhóm đổi hướng sau phỏng vấn Studio team.
- **Ứng viên CHỌN + vì sao (bằng số):** C2 — **3/3 người được hỏi đang làm việc này 2–10 lần/tuần, mất 45'–1 tiếng mỗi lần, và 3/3 từng để lọt câu sượng xuống khâu sau** (P1 mất thêm ~1 tiếng thu lại, P2 để MC vấp trên sân khấu). **0/3 có công cụ soát được** — Word chỉ bắt chính tả, Grammarly không dùng được cho tiếng Việt, AI thì soát logic chứ không soát độ trôi. Ba ứng viên còn lại không có con số nào tương đương vì nhóm chưa phỏng vấn người dùng của chúng. C2 cũng là đề hẹp nhất Track C và có sẵn transcript bản sạch làm chuẩn "nghe được".

## §3. Giải pháp tương tự đã nghiên cứu

TODO: mỗi người thử 1 sản phẩm gần giống rồi điền 4 ô — gợi ý LanguageTool · Grammarly · TTS preview của CapCut/Canva · editor gợi ý văn phong

| Sản phẩm | Người thử | Flow của họ | Đáng học | Đáng né | Mình khác gì ở lát cắt này |
|---|---|---|---|---|---|
| `_________` | `_________` | `_________` | `_________` | `_________` | `_________` |
| `_________` | `_________` | `_________` | `_________` | `_________` | `_________` |
| `_________` | `_________` | `_________` | `_________` | `_________` | `_________` |
| `_________` | `_________` | `_________` | `_________` | `_________` | `_________` |

## §4. Thiết kế

- **Lát cắt MỘT CÂU:** Một lab coach · duyệt một kịch bản ~40 câu trước khi cho AI dựng video · AI chỉ đúng câu/đoạn nghe sượng kèm loại lỗi + lý do + gợi ý sửa tối thiểu · biên tập có bản kịch bản đã sạch câu sượng trước khi chuyển thu âm, không phải đọc dò lại cả bài.
- **Non-goals (≥3 thứ KHÔNG build):**
  1. Không tự động viết lại hoặc xuất bản toàn bộ kịch bản.
  2. Không dùng nhãn "AI-generated" để kết luận về tác giả (chỉ chỉ ra câu khó đọc, không phán đoán ai viết).
  3. Không lưu trữ hay dùng kịch bản ngoài phạm vi buổi duyệt hiện tại.
  4. Không tự thêm claim/số liệu mới không có trong kịch bản gốc.
- **Mức prototype nhắm tới:** [ ] Sketch [x] Mock [ ] Working — **thật:** luồng duyệt end-to-end trong `codebase/mockup.html` (hiển thị span, Accept / Sửa tay / Bỏ qua, hoàn tác, lọc theo nhóm lỗi, audit trail) · **mock:** 7 finding là dữ liệu tĩnh, chưa gọi AI. TODO: đổi sang Working nếu CP3 nối được lời gọi AI thật.
- **Automation:** [x] augment [ ] conditional [ ] automate — **lý do theo cost-of-error:**
  - **Lỗi không lộ ra ở khâu nghe, nên phải bắt ở khâu văn bản.** Giọng TTS đọc trơn tru cả câu sượng — không hụt hơi, không líu lưỡi, không vấp. Người làm video nghe lại bản đã dựng vẫn thấy "ổn", lỗi chỉ lộ khi người học xem và thấy bài giảng nghe như máy đọc. Đây là lý do khâu duyệt văn bản là chỗ duy nhất chặn được, và cũng là ranh giới đề C2 yêu cầu: tách lỗi nội dung khỏi lỗi chỉ liên quan cách đọc.
  - **Bỏ sót thì mất chất lượng bài giảng, không chỉ mất thời gian.** Render lại video rẻ, nhưng không ai render lại thứ mình tưởng là đúng. Cái đắt là bài đã đăng cho cả khoá xem.
  - **AI tự sửa thì user không dùng.** P1: *"sợ dùng máy móc nó sửa mất cái 'chất' giọng của mình"* — đó là lý do P1 chưa đụng tool AI nào. Agent tự viết lại sẽ phá đúng thứ người dùng sợ mất, và họ bỏ công cụ.
  - **Gợi ý sai thì rẻ** — bấm Bỏ qua là xong, highlight biến mất, hoàn tác được.

  Nên AI gắn cờ + phân loại + giải thích + gợi ý sửa tối thiểu; người quyết từng chỗ bằng Accept / Sửa tay / Bỏ qua.
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
| 9 | Đoạn dài liên tục không có chỗ ngắt hơi (case thật của P1 khi tự thu mic) | ④ | Gắn cờ breath-group overload ở **khâu văn bản** — giọng TTS đọc trôi nên nghe lại bản dựng sẽ không phát hiện được; chỉ chỗ tách câu, **không rút gọn ý** | G11 · G9 |

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
- **Golden set** (file trong `eval/`): `_________`/20 case — TODO: gom vào `eval/`, cần thêm ~4 case nữa. Đã có sẵn 16:
  - **7 case lỗi** — 7 finding trong `codebase/mockup.html`, đã gắn nhãn tay span + category + lý do
  - **6 case sạch** — 6 câu transcript dài 60–95 từ ở §1, dùng đo false positive
  - **3 case từ phỏng vấn** — cặp câu trước/sau do P1 và P2 tự đưa, và pattern văn AI của P3 ([`interview-log.md`](interview-log.md))
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
- **Willing users:** Nguyễn Đức Thái (2A202602648) · Trần Hồng Sơn (2A20262475) — đã phỏng vấn 16/9, đồng ý thử prototype · lab coach (P3) — đã phỏng vấn, tên ở [`interview-log.md`](interview-log.md)
  TODO: xin thêm 1–2 lab coach khác — hiện chỉ P3 ở đúng quy trình AI dựng video của khoá
- **Kế hoạch vòng validation (CP5) — để kiểm assumption nguy hiểm nhất:**

  **Assumption:** kịch bản do AI viết và AI đọc, nên chủ nhân bài giảng có thể **chấp nhận luôn** giọng văn đó thay vì bỏ công sửa. Cả 3 người nói họ đang bỏ 45'–1 tiếng đọc dò, nhưng đó là lời nói — chưa quan sát được họ có thật sự sửa hay không.

  **Cách kiểm (không hỏi ý kiến, chỉ đo hành vi):** đưa prototype + một kịch bản thật của chính họ, để họ tự duyệt, không hướng dẫn. Đo:

  | Chỉ số | Ý nghĩa nếu thấp |
  |---|---|
  | **Tỉ lệ Accept / tổng finding** | Họ không thấy đáng sửa → assumption đúng, lát cắt sai |
  | **Tỉ lệ Bỏ qua kèm lý do "không phải lỗi"** | False positive quá cao → sửa agent, không sửa lát cắt |
  | **Có dùng Sửa tay không** | Có → họ quan tâm giọng văn, đúng như P1 Q6 |
  | **Sau buổi thử có hỏi xin dùng tiếp không** | Tín hiệu thật, mạnh hơn mọi câu khen |

  Ghi vào `validation/` kèm changelog: đổi gì sau mỗi người thử. Kết quả âm vẫn ghi đúng như thế.
- Multi-prototype: không áp dụng.

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| CP1 | Chốt hướng B2 (Trợ lý Discord) + lát cắt + evidence mining ban đầu | Canvas CP1 |
| CP1 (cập nhật) | Đổi sang hướng C2 (Vietnamese Spoken-Script QA) | Nhóm muốn thử hướng Lesson Studio; đánh đổi: mất evidence đếm-được sẵn có của B2, đổi lấy phạm vi kỹ thuật hẹp hơn trong Track C. Cần phỏng vấn Studio team trước CP4 để xác nhận hoặc quay lại B2 |
| 17/9 | Thêm 3 phỏng vấn vào §1, điền số cho bảng impact §2, viết lại lý do augment §4 | Phỏng vấn P1/P2/P3 (`interview-log.md`) — 3/3 xác nhận pain, cho con số tần suất và chi phí mà mining không đo được |
| 17/9 | Core JTBD bỏ tên khâu sau, chỉ giữ "trước khi đưa nó thành giọng đọc" | Ba người được hỏi có ba khâu sau khác nhau (AI đọc · tự thu mic · MC đọc trực tiếp) nhưng cùng một job |
| 17/9 | Bỏ vế "dựng hình khớp độ dài giọng" khỏi lập luận cost-of-error §4 | Không ai trong 3 người nhắc tới việc dựng hình |
| 17/9 (sau) | **Đổi job executor: không phải "biên tập viên Studio team" mà là lab coach của khoá** — học viên khoá trước làm video bằng AI, giọng TTS. Bỏ luôn vai "giảng viên duyệt kịch bản" | Hỏi lại về quy trình thật của khoá: không có Studio team, mentor là chuyên gia đi làm nên không tham gia khâu video |
| 17/9 (sau) | **Đổi trục cost-of-error §4**: bỏ "sửa muộn thì đắt", thay bằng "giọng TTS đọc trơn cả câu sượng nên lỗi chỉ bắt được ở khâu văn bản" | Giọng là AI nên render lại gần như miễn phí — chi phí thu lại của P1 không áp dụng cho người dùng thật. P3 trả lời "5 phút là xong" hoá ra không phải ngoại lệ mà là đúng quy trình |
| 17/9 (sau) | Đồng bộ `canvas.md` / `canvas.html` / `canvas.png` theo bản đã sửa, giữ ghi chú bản CP1 gốc ghi gì | Canvas là bản nộp CP1 nhưng để lệch với spec thì người chấm đối chiếu sẽ thấy mâu thuẫn |
