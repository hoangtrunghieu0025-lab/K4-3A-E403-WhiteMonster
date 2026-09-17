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
| 2 | Locate | Tìm bản kịch bản mới nhất + tài liệu gốc để đối chiếu | `_________` (Q1) | `_________` | `__` |
| 3 | Prepare | Thu xếp thời gian và chỗ đủ yên tĩnh để đọc thành tiếng | Tự sắp lịch | Đọc thành tiếng cả bài không làm được ở chỗ đông người | M |
| 4 | Confirm | Chắc chắn bản đang soát đúng là bản sẽ đem thu | `_________` (Q1) | `_________` | `__` |
| 5 | **Execute** | **Đọc thành tiếng từng câu, nghe chỗ nào vấp** | Miệng + mắt, không công cụ | **Phải đọc hết cả bài mới biết câu nào sượng; không có gì chỉ thẳng vào câu và nói nó sai loại gì** | **H** |
| 6 | **Monitor** | Biết đã soát hết chưa, câu nào còn nghi ngờ | Trí nhớ / ghi chú tay | **Cuối bài mệt nên bỏ sót; không lưu vết vì sao một câu bị bỏ qua** | **H** |
| 7 | Modify | Sửa câu vấp mà vẫn giữ giọng tác giả | Tự viết lại, hoặc nhờ công cụ viết lại cả bài | Công cụ viết lại cả bài thì mất giọng gốc; sửa tay thì tốn thời gian | M |
| 8 | Conclude | Chốt bản sạch, bàn giao sang thu âm | Gửi file | Lỗi lọt xuống đây mới lộ thì phải thu lại giọng + dựng lại cảnh | **H** |

**Hai chỗ đau nhất:** #1 bước 5 Execute · #2 bước 6 Monitor.

**Bằng chứng cho 2 chỗ này:** mining 3.665 câu văn nói trong `data/vlearn-pack/` ([`spec.md`](spec.md) §1) — 19,1% câu giảng viên dài hơn 40 từ mà vẫn nghe bình thường, nên bước 5 không rút gọn được bằng một luật đếm từ.

TODO (Q3/Q4): xác nhận quy trình "thu giọng trước → dựng hình khớp độ dài giọng". Đây đang là giả định của nhóm, chưa ai trong Studio team xác nhận — nếu sai thì cột "Đau" của bước 8 sụp, và cả lý do chọn augment ở [`spec.md`](spec.md) §4 phải viết lại.

## 3. Core JTBD

- **Bản nháp:** "Dùng AI kiểm tra kịch bản trước khi thu âm"
- **Từ solution lỡ nhét vào (gạch bỏ):** ~~dùng AI~~ · ~~kiểm tra tự động~~ · ~~agent QA~~
- **Bản chốt:**

> **Đọc lại kịch bản trước khi duyệt để tìm câu nghe sượng / khó đọc thành lời, trước khi đưa vào thu âm.**

## 4. Ba job stories

| # | When | I want to | So I can | Nguồn |
|---|---|---|---|---|
| **JS1** | Tôi vừa viết xong một kịch bản ~40 câu và sắp gửi sang thu âm | Biết ngay câu nào sẽ vấp khi đọc thành lời, không phải đọc to cả bài | Sửa xong trước khi giọng được thu và cảnh được dựng khớp theo | Suy từ lát cắt C2 |
| **JS2** | Một công cụ gắn cờ hàng loạt câu dài trong bài tôi viết | Hiểu vì sao từng câu bị gắn cờ, không chỉ thấy cảnh báo "câu quá dài" | Bỏ qua những câu tuy dài nhưng đọc vẫn xuôi, thay vì cắt vụn cả bài | Mining: 699/3.665 câu (19,1%) dài hơn 40 từ vẫn nghe được |
| **JS3** | Tôi nhận lại kịch bản người khác viết, hoặc một đoạn dịch từ tiếng Anh | Được chỉ đúng chỗ sượng kèm gợi ý sửa tối thiểu | Sửa mà không viết lại cả bài, giữ nguyên giọng văn tác giả | Đề C2 + [`canvas.md`](canvas.md) ô 1 |

TODO (Q3/Q5): thay JS1 và JS3 bằng tình huống nguyên văn của người thật — hai story này hiện suy từ đề bài, chỉ JS2 đứng trên số đo.

## 5. Current alternatives

| Alternative | Làm tốt gì | Fail ở đâu | Vì sao chưa bỏ nó |
|---|---|---|---|
| **Tự đọc thành tiếng cả bài** | Bắt đúng thứ tai nghe thấy | Phải đọc hết mới biết; cuối bài mệt nên bỏ sót; không để lại vết vì sao bỏ qua một câu | Cách duy nhất hiện bắt được lỗi "nghe" |
| **Nhờ LLM viết lại cả bài** | Nhanh, câu ra mượt | Mất giọng tác giả; không nói câu nào sai và sai loại gì; có thể thêm claim không có trong bản gốc | Khi gấp vẫn nhanh hơn sửa tay |
| **Soát chính tả / ngữ pháp** (Word, LanguageTool) | Bắt lỗi chính tả, lỗi ngữ pháp rõ ràng | Không bắt được câu đúng ngữ pháp mà đọc lên vẫn sượng | Miễn phí, có sẵn trong trình soạn thảo |
| **Nghe thử bằng TTS** | Nghe đúng thứ máy sẽ đọc; bắt tốt lỗi số / viết tắt | Phải render cả bài mới nghe được; TTS đọc trơn cả câu sượng nên lỗi ngữ nghĩa vẫn lọt | Gần khâu thu âm nhất |
| **Bỏ qua, để lộ ở khâu thu** | Tốn 0 công ở bước kịch bản | Đẩy chi phí sang thu lại giọng + dựng lại cảnh | Lịch sản xuất gấp |

**Nếu sản phẩm nhóm không ra đời, user sẽ tiếp tục:** đọc thành tiếng cả bài bằng tay và chấp nhận tỉ lệ bỏ sót; thỉnh thoảng nhờ LLM viết lại khi quá gấp, đổi lại mất giọng tác giả.

TODO (Q6): cột "Vì sao chưa bỏ nó" hiện là suy đoán — thay bằng câu trả lời thật, [`interview-log.md`](interview-log.md).

## 6. AI leverage point

**AI vào bước nào, vai trò gì:** bước **5–6 (Execute + Monitor)** — chỉ đúng span sượng, phân loại lỗi, giải thích lý do gắn với ngữ cảnh, gợi ý sửa tối thiểu. Người duyệt accept/reject từng chỗ, mỗi quyết định để lại audit trail. Mức: **augment**.

**Vì sao không phải bước khác:**
- **Không vào bước 7 (Modify)** — để AI tự sửa là mất giọng tác giả, đúng chỗ alternative "LLM viết lại cả bài" đang fail.
- **Không vào bước 8 (Conclude)** — tự động duyệt/xuất bản thì cost-of-error rơi hết xuống khâu thu lại + dựng lại.
- **Không vào bước 1–4** — việc điều phối file và lịch, không phải chỗ đau.

**Product hypothesis:**

> Nếu giúp **biên tập viên Studio team** làm việc **"tìm câu nghe sượng trong kịch bản trước khi thu âm"** tốt hơn ở **bước đọc soát**, bằng cách **chỉ đúng span + loại lỗi + lý do + gợi ý sửa tối thiểu**, họ sẽ chuyển từ **đọc thành tiếng dò cả bài** sang **đọc soát có chỉ dẫn**, vì **chỉ phải tập trung vào số câu được gắn cờ thay vì cả 40 câu, mà vẫn tự giữ quyền quyết định từng chỗ sửa.**

**Assumption nguy hiểm nhất nếu nhóm đang sai:**

1. **Chưa ai trong Studio team xác nhận job này đủ đau.** Evidence hiện có chứng minh *lỗi khó phân loại tồn tại*, chưa chứng minh *biên tập viên đau vì nó*. Kiểm bằng phỏng vấn P3 trước CP4.
2. **Precision phải đủ cao thì người ta mới tin.** Mining đã bác bỏ giả thuyết ban đầu ("câu dài = câu sượng"): ngưỡng 40 từ gắn cờ oan 19,1% lời giảng thật. Nếu agent báo oan ở mức đó, biên tập viên quay lại tự đọc. Kiểm bằng golden set + đo false positive ([`spec.md`](spec.md) §7).
