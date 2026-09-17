# Worksheet JTBD — Nhóm WhiteMonster

**Nhóm:** WhiteMonster · Lớp 3A · Phòng E403 · cụm C1 · **Hướng:** [x] C — Lesson Studio (đề C2)

## 1. Job executor

**Job executor:** **Lab coach của khoá** — học viên khoá trước điểm cao, làm video bài giảng: tự viết hoặc để AI sinh kịch bản, rồi dựng video bằng AI, **giọng đọc cũng là AI**.

**Vì sao là người này:** Họ là người duy nhất chạm vào kịch bản ở lúc còn sửa được. Trong quy trình này không có ai khác: không có biên tập viên riêng, không có khâu thu mic, và mentor là chuyên gia đi làm nên không tham gia. Một người vừa viết, vừa duyệt, vừa xuất bản — nên không có ai soát chéo hộ.

**Đã loại:**
- *"Biên tập viên Studio team"* — nhóm giả định có một đội biên tập chuyên trách; hỏi lại thì khoá không có đội đó.
- *"Giảng viên duyệt kịch bản"* — mentor không ngồi duyệt video.
- *"Học viên xem video"* — chịu hậu quả, không làm job.

## 2. Workflow thật — job map 8 bước

Job: *đọc lại kịch bản để tìm câu nghe sượng, trước khi đưa nó thành giọng đọc.*

| # | Bước | Họ đang cố làm gì | Hôm nay dùng gì | Kẹt ở đâu | Đau |
|---|---|---|---|---|---|
| 1 | Define | Xác định "nghe được" nghĩa là gì với kịch bản này | Cảm tính cá nhân, không có chuẩn viết ra | Mỗi người một ngưỡng; hai người duyệt có thể không đồng ý | M |
| 2 | Locate | Tìm bản kịch bản mới nhất + tài liệu gốc để đối chiếu | P3: coi slide → research nguồn trên mạng → so sánh nguồn nào chất lượng hơn | `_________` | `__` |
| 3 | Prepare | Thu xếp thời gian và chỗ đủ yên tĩnh để đọc thành tiếng | Tự sắp lịch | Đọc thành tiếng cả bài không làm được ở chỗ đông người | M |
| 4 | Confirm | Chắc chắn bản đang soát đúng là bản sẽ đem dựng video | `_________` (Q1) | `_________` | `__` |
| 5 | **Execute** | **Đọc thành tiếng từng câu, nghe chỗ nào vấp** | P1 in ra giấy, cầm bút đỏ gạch chân · P2 mở Google Docs màn hình to, lẩm bẩm đọc to "xem có lọt lỗ tai không" | **Phải đọc hết cả bài mới biết câu nào sượng; không có gì chỉ thẳng vào câu và nói nó sai loại gì.** 45' cho 5 trang (P1), 1 tiếng cho 10 trang (P2) | **H** |
| 6 | **Monitor** | Biết đã soát hết chưa, câu nào còn nghi ngờ | Trí nhớ / ghi chú tay | **Vẫn lọt — 3/3 người từng để sót;** không lưu vết vì sao một câu bị bỏ qua | **H** |
| 7 | Modify | Sửa câu vấp mà vẫn giữ giọng tác giả | Tự viết lại, hoặc nhờ công cụ viết lại cả bài | Công cụ viết lại cả bài thì mất giọng gốc; sửa tay thì tốn thời gian | M |
| 8 | Conclude | Chốt bản sạch rồi cho AI dựng video + đọc giọng | Công cụ sinh video / TTS | **Nghe lại bản dựng không cứu được** — giọng máy đọc trơn cả câu sượng. Lỗi lọt qua đây là lọt thẳng tới người học | **H** |

**Hai chỗ đau nhất:** #1 bước 5 Execute · #2 bước 6 Monitor.

**Bằng chứng cho 2 chỗ này:**
- Mining 3.665 câu văn nói trong `data/vlearn-pack/` — 19,1% câu giảng viên dài hơn 40 từ mà vẫn nghe bình thường, nên bước 5 không rút gọn được bằng một luật đếm từ.
- 3/3 người phỏng vấn đang làm bước 5 bằng tay, mất 45'–1 tiếng mỗi kịch bản, và 3/3 vẫn để lọt ([`interview-log.md`](interview-log.md)).

**Giả định đã bị bác bỏ:** nhóm từng cho rằng khâu sau là thu giọng người + dựng hình, nên sửa muộn rất đắt. Quy trình thật của khoá là **AI dựng video và AI đọc giọng** — render lại gần như miễn phí. Chi phí thu lại mic của P1 không áp dụng cho người dùng thật.

**Cái thay thế nó:** chi phí nằm ở **bước 5–6** (45'–1 tiếng đọc dò mỗi bài, 2–10 lần/tuần, mà vẫn lọt) và ở **bước 8** (giọng máy không để lộ câu sượng, nên bài đăng ra mới là chỗ lỗi hiện hình — lúc đó người học đã xem rồi).

## 3. Core JTBD

- **Bản nháp:** "Dùng AI kiểm tra kịch bản trước khi dựng video"
- **Từ solution lỡ nhét vào (gạch bỏ):** ~~dùng AI~~ · ~~kiểm tra tự động~~ · ~~agent QA~~
- **Bản chốt:**

> **Đọc lại kịch bản để tìm câu nghe sượng / khó đọc thành lời, trước khi đưa nó thành giọng đọc.**

*Đổi sau phỏng vấn:* bản cũ dừng ở "trước khi đưa vào thu âm". Ba người được hỏi có ba khâu sau khác nhau — AI đọc (P3), tự thu mic (P1), MC đọc trực tiếp (P2) — nhưng cùng một job. Câu chốt bỏ tên khâu sau đi, giữ đúng phần chung: kịch bản sắp thành giọng đọc.

## 4. Ba job stories

| # | When | I want to | So I can | Nguồn |
|---|---|---|---|---|
| **JS1** | Tôi sắp cho AI dựng video từ kịch bản này | Biết câu nào nghe sẽ sượng **trước khi render**, vì nghe lại bản đã dựng không phát hiện được — giọng máy đọc trôi hết | Bài giảng đăng ra không nghe như máy đọc | **P3** — quy trình AI dựng + AI giọng · **P1/P2 Q3** cho thấy cùng lỗi đó ở khâu người đọc thì lộ ngay, còn ở TTS thì không |
| **JS2** | Một công cụ gắn cờ hàng loạt câu dài trong bài tôi viết | Hiểu vì sao từng câu bị gắn cờ, không chỉ thấy cảnh báo "câu quá dài" | Bỏ qua những câu tuy dài nhưng đọc vẫn xuôi, thay vì cắt vụn cả bài | Mining: 699/3.665 câu (19,1%) dài hơn 40 từ vẫn nghe được |
| **JS3** | Tôi cân nhắc đưa bài cho công cụ soát | Được chỉ đúng chỗ sượng kèm gợi ý sửa tối thiểu, không bị viết lại hộ | Giữ nguyên giọng văn của mình | **P1 Q6** — *"sợ dùng máy móc nó sửa mất cái 'chất' giọng của mình"*, nên chưa dùng tool AI nào |

## 5. Current alternatives

| Alternative | Làm tốt gì | Fail ở đâu | Vì sao chưa bỏ nó |
|---|---|---|---|
| **Tự đọc thành tiếng / đọc dò tay** (3/3 đang dùng) | Bắt đúng thứ tai nghe thấy | Phải đọc hết mới biết; **vẫn lọt — 3/3 từng để sót**; không để lại vết vì sao bỏ qua một câu | *"tiếng Việt lắt léo, đọc không có ngữ điệu là không biết câu đó sượng"* (P2 Q6) |
| **Word check chính tả** (P1) | Bắt lỗi chính tả | Không bắt được câu đúng ngữ pháp mà đọc lên vẫn sượng | *"quen đọc bằng mắt rồi"*; miễn phí, có sẵn |
| **Grammarly** (P2) | Dùng tốt cho tiếng Anh | *"tiếng Việt thì chịu"* | Vẫn giữ cho phần tiếng Anh |
| **Cho AI soát** (P3) | Kiểm được logic, nguồn, kiến thức có chuẩn không | Không soát độ trôi khi đọc — đúng phần C2 nhắm | Giải được phần factuality |
| **Nhờ AI viết lại cả bài** | Nhanh, câu ra mượt | Mất giọng tác giả | **P1 không dùng** — *"sợ dùng máy móc nó sửa mất cái 'chất' giọng của mình"* |
| **Bắt cả nhóm đọc nháp thành tiếng trước mặt mình** (P2, sau sự cố) | Chắc chắn bắt được lỗi nghe | *"Tốn thêm cả đống thời gian prep"* — mỗi kịch bản mất thêm người và thêm buổi | Đắt nhưng an toàn hơn để MC vấp trên sân khấu |

**Nếu sản phẩm nhóm không ra đời, user sẽ tiếp tục:** đọc dò bằng tay và chấp nhận tỉ lệ lọt — hoặc trả giá bằng cách của P2: bắt cả nhóm đọc nháp thành tiếng, tốn thời gian prep cho mọi kịch bản.

## 6. AI leverage point

**AI vào bước nào, vai trò gì:** bước **5–6 (Execute + Monitor)** — chỉ đúng span sượng, phân loại lỗi, giải thích lý do gắn với ngữ cảnh, gợi ý sửa tối thiểu. Người duyệt accept/reject từng chỗ, mỗi quyết định để lại audit trail. Mức: **augment**.

**Vì sao không phải bước khác:**
- **Không vào bước 7 (Modify)** — để AI tự sửa là mất giọng tác giả, đúng chỗ alternative "LLM viết lại cả bài" đang fail.
- **Không vào bước 8 (Conclude)** — tự động duyệt/xuất bản thì không còn ai chặn, mà bước 8 chính là chỗ lỗi tàng hình: giọng máy đọc trôi nên không ai nghe ra.
- **Không vào bước 1–4** — việc điều phối file và tìm nguồn, không phải chỗ đau.

**Product hypothesis:**

> Nếu giúp **lab coach làm video bài giảng** làm việc **"tìm câu nghe sượng trong kịch bản trước khi cho AI dựng video"** tốt hơn ở **bước đọc soát**, bằng cách **chỉ đúng span + loại lỗi + lý do + gợi ý sửa tối thiểu**, họ sẽ chuyển từ **đọc dò cả bài 45'–1 tiếng** sang **đọc soát có chỉ dẫn**, vì **chỉ phải tập trung vào số câu được gắn cờ, mà vẫn tự giữ quyền quyết định từng chỗ sửa.**

**Assumption nguy hiểm nhất nếu nhóm đang sai:**

1. **Người dùng có thể không thấy đây là vấn đề đáng sửa.** Nếu kịch bản do AI viết và AI đọc, chủ nhân bài giảng có thể chấp nhận luôn giọng văn đó thay vì bỏ công sửa — 3/3 người được hỏi đều đang bỏ 45'–1 tiếng đọc dò, nhưng đó là lời họ nói, chưa quan sát được họ có thật sự sửa hay không. Kiểm ở vòng validation CP5: đưa prototype cho họ, xem tỉ lệ Accept thật.
2. **Precision phải đủ cao thì người ta mới tin.** Mining đã bác bỏ giả thuyết ban đầu ("câu dài = câu sượng"): ngưỡng 40 từ gắn cờ oan 19,1% lời giảng thật. Agent báo oan ở mức đó thì họ quay lại tự đọc. Kiểm bằng golden set + đo false positive ([`spec.md`](spec.md) §7).
3. **Chưa hỏi ai ngoài 3 người.** Cả ba làm job này ở ba khâu sau khác nhau (TTS, mic, sân khấu), nhưng chỉ P3 ở đúng quy trình của khoá. n=1 cho quy trình thật.
