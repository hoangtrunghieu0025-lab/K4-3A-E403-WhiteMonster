# Worksheet JTBD — Nhóm WhiteMonster

**Nhóm:** WhiteMonster · Lớp 3A · Phòng E403 · cụm C1 · **Hướng:** [x] C — Lesson Studio (đề C2)

## 1. Job executor

**Job executor:** Biên tập viên / người viết kịch bản video của Studio team — người trực tiếp đọc soát kịch bản trước khi nó được chuyển sang thu âm.

**Vì sao là người này:** Họ cầm bản kịch bản ở đúng thời điểm còn sửa được mà chưa tốn gì. Giảng viên duyệt cũng chạm vào job này nhưng ở vai phê duyệt, không phải người ngồi dò từng câu. Học viên xem video không tham gia job — chỉ chịu hậu quả khi câu sượng lọt xuống video.

**Đã loại:** "giảng viên nói chung", "đội sản xuất video" — không trỏ được vào một người đang ngồi trước một bản kịch bản.

## 2. Workflow thật — job map 8 bước

Job: *đọc lại kịch bản trước khi duyệt để tìm câu nghe sượng.*

| # | Bước | Họ đang cố làm gì | Hôm nay dùng gì | Kẹt ở đâu | Đau |
|---|---|---|---|---|---|
| 1 | Define | Xác định "nghe được" nghĩa là gì với kịch bản này | Cảm tính cá nhân, không có chuẩn viết ra | Mỗi người một ngưỡng; hai người duyệt có thể không đồng ý | M |
| 2 | Locate | Tìm bản kịch bản mới nhất + tài liệu gốc để đối chiếu | P3: coi slide → research nguồn trên mạng → so sánh nguồn nào chất lượng hơn | `_________` | `__` |
| 3 | Prepare | Thu xếp thời gian và chỗ đủ yên tĩnh để đọc thành tiếng | Tự sắp lịch | Đọc thành tiếng cả bài không làm được ở chỗ đông người | M |
| 4 | Confirm | Chắc chắn bản đang soát đúng là bản sẽ đem thu | `_________` (Q1) | `_________` | `__` |
| 5 | **Execute** | **Đọc thành tiếng từng câu, nghe chỗ nào vấp** | P1 in ra giấy, cầm bút đỏ gạch chân · P2 mở Google Docs màn hình to, lẩm bẩm đọc to "xem có lọt lỗ tai không" | **Phải đọc hết cả bài mới biết câu nào sượng; không có gì chỉ thẳng vào câu và nói nó sai loại gì.** 45' cho 5 trang (P1), 1 tiếng cho 10 trang (P2) | **H** |
| 6 | **Monitor** | Biết đã soát hết chưa, câu nào còn nghi ngờ | Trí nhớ / ghi chú tay | **Vẫn lọt — 3/3 người từng để sót;** không lưu vết vì sao một câu bị bỏ qua | **H** |
| 7 | Modify | Sửa câu vấp mà vẫn giữ giọng tác giả | Tự viết lại, hoặc nhờ công cụ viết lại cả bài | Công cụ viết lại cả bài thì mất giọng gốc; sửa tay thì tốn thời gian | M |
| 8 | Conclude | Chốt bản sạch, bàn giao sang thu âm / lên sân khấu | Gửi file | **Lọt xuống đây thì đắt:** P1 thu lại + cắt ghép audio mất ~1 tiếng · P2 để MC vấp ngay trên sân khấu | **H** |

**Hai chỗ đau nhất:** #1 bước 5 Execute · #2 bước 6 Monitor.

**Bằng chứng cho 2 chỗ này:**
- Mining 3.665 câu văn nói trong `data/vlearn-pack/` — 19,1% câu giảng viên dài hơn 40 từ mà vẫn nghe bình thường, nên bước 5 không rút gọn được bằng một luật đếm từ.
- 3/3 người phỏng vấn đang làm bước 5 bằng tay, mất 45'–1 tiếng mỗi kịch bản, và 3/3 vẫn để lọt ([`interview-log.md`](interview-log.md)).

**Giả định đã được xác nhận một phần:** P1 xác nhận chi phí thu lại giọng là thật (*"set up lại mic thu lại nguyên đoạn đó, mất toi thêm gần tiếng đồng hồ tính cả lúc cắt ghép lại audio"*). Riêng vế **"dựng hình khớp theo độ dài giọng"** thì chưa ai nhắc tới — bỏ vế đó ra khỏi lập luận, chi phí thu lại audio một mình đã đủ.

## 3. Core JTBD

- **Bản nháp:** "Dùng AI kiểm tra kịch bản trước khi thu âm"
- **Từ solution lỡ nhét vào (gạch bỏ):** ~~dùng AI~~ · ~~kiểm tra tự động~~ · ~~agent QA~~
- **Bản chốt:**

> **Đọc lại kịch bản trước khi duyệt để tìm câu nghe sượng / khó đọc thành lời, trước khi đưa vào thu âm hoặc đọc trước khán giả.**

*Đổi sau phỏng vấn:* bản cũ dừng ở "trước khi đưa vào thu âm". P2 duyệt kịch bản MC cho sự kiện — không qua thu âm, nhưng chịu đúng hậu quả đó ở dạng khác (MC vấp trên sân khấu). Job giống nhau, chỉ khác khâu sau.

## 4. Ba job stories

| # | When | I want to | So I can | Nguồn |
|---|---|---|---|---|
| **JS1** | Tôi sắp gửi kịch bản sang thu âm / sắp đưa MC lên đọc | Biết ngay câu nào sẽ vấp khi đọc thành lời, không phải đọc dò cả bài | Sửa trước khi lọt xuống khâu thu hoặc lên sân khấu | **P1 Q3** — lọt xuống khâu thu, hụt hơi, thu lại mất ~1 tiếng · **P2 Q3** — MC vấp trên sân khấu |
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
- **Không vào bước 8 (Conclude)** — tự động duyệt/xuất bản thì cost-of-error rơi hết xuống khâu thu lại + dựng lại.
- **Không vào bước 1–4** — việc điều phối file và lịch, không phải chỗ đau.

**Product hypothesis:**

> Nếu giúp **biên tập viên Studio team** làm việc **"tìm câu nghe sượng trong kịch bản trước khi thu âm"** tốt hơn ở **bước đọc soát**, bằng cách **chỉ đúng span + loại lỗi + lý do + gợi ý sửa tối thiểu**, họ sẽ chuyển từ **đọc thành tiếng dò cả bài** sang **đọc soát có chỉ dẫn**, vì **chỉ phải tập trung vào số câu được gắn cờ thay vì cả 40 câu, mà vẫn tự giữ quyền quyết định từng chỗ sửa.**

**Assumption nguy hiểm nhất nếu nhóm đang sai:**

1. **Đã hỏi 3 người, cả 3 xác nhận — nhưng chưa ai thuộc đúng Studio team sản xuất video của khoá.** P1 là học viên tự thu voice-off, P2 làm kịch bản MC sự kiện, P3 là lab coach soạn bài giảng. Job và hậu quả giống nhau, nhưng nếu quy trình của Studio team khác hẳn thì lát cắt phải chỉnh. Hỏi thêm khi BTC cho đầu mối.
2. **Precision phải đủ cao thì người ta mới tin.** Mining đã bác bỏ giả thuyết ban đầu ("câu dài = câu sượng"): ngưỡng 40 từ gắn cờ oan 19,1% lời giảng thật. Nếu agent báo oan ở mức đó, biên tập viên quay lại tự đọc. Kiểm bằng golden set + đo false positive ([`spec.md`](spec.md) §7).
