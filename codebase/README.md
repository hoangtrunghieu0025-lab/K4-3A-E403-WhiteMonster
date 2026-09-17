# codebase/ — prototype

## Mức prototype hiện tại: **Mock** (CP2)

| Phần | Trạng thái |
|---|---|
| Luồng duyệt kịch bản (hiển thị span, Accept / Sửa tay / Bỏ qua, hoàn tác, lọc theo nhóm lỗi, xuất bản + audit trail) | **Thật** — chạy được end-to-end trong `mockup.html` |
| Phát hiện span sượng · phân loại lỗi · sinh lý do · sinh gợi ý sửa | **Mock** — 7 findings là dữ liệu tĩnh viết tay trong `FINDINGS` |
| Kịch bản mẫu 14 câu | Nhóm tự viết, **không lấy từ data pack** |

TODO (CP3): nối lời gọi AI thật vào quyết định trung tâm — nhận kịch bản → trả danh sách finding (span, category, severity, lý do, confidence, gợi ý), giữ nguyên luồng Accept/Reject; lưu log/trace vào thư mục này.

## Chạy thử

Mở `mockup.html` bằng trình duyệt bất kỳ — không cần cài gì, không cần server.

## Bốn đường đi của trải nghiệm đã dựng sẵn (cho `spec.md` §6)

| Đường đi | Xem ở finding |
|---|---|
| **Happy path** | `F1` (cú pháp dịch) — lý do rõ, gợi ý sửa tối thiểu, bấm Áp dụng là xong |
| **Low-confidence** ② | `F4` (code-switch "cost-of-error") — độ chắc THẤP, **không có nút Áp dụng**, agent nói rõ cần người xác minh |
| **Failure / không căn cứ** ① | `F6` (claim "tăng gấp đôi hiệu suất") — không có nguồn trong kịch bản, agent từ chối tự sửa claim |
| **Correction** | Nút **Sửa tay** ở mọi finding — biên tập sửa lại gợi ý trước khi áp dụng; mọi finding đã xử lý đều **Hoàn tác** được |
| **Ngoài phạm vi** ③ | Nút **"Yêu cầu viết lại cả bài"** trên header — agent từ chối viết lại toàn văn, chỉ nói rõ phạm vi là từng finding |

## Chỗ neo nguyên tắc HAX/PAIR (cho `spec.md` §4b)

| Nguyên tắc | Vị trí trong `mockup.html` |
|---|---|
| **G1** — làm rõ hệ thống làm được gì | Banner đầu trang: "MOCK · findings là dữ liệu tĩnh, chưa gọi AI thật" + dòng "AI đề xuất — bạn quyết từng chỗ" |
| **G2** — làm rõ nó làm tốt đến đâu | Mỗi finding có dòng **Độ chắc** (cao / vừa / thấp), và tách riêng "lỗi phát âm, không phải lỗi nội dung" ở `F2` |
| **G10** — thu hẹp phạm vi khi nghi ngờ | `F4` và `F6`: không đề xuất sửa, hiện khối vàng "Không đủ căn cứ để tự sửa" thay vì đoán liều · nút "Yêu cầu viết lại cả bài": agent từ chối, chỉ nói rõ phạm vi là từng finding |
| **G11** — giải thích vì sao | Mỗi finding có mục lý do gắn với ngữ cảnh câu đó, không phải nhãn lỗi chung chung |
| **G8** — gạt bỏ dễ dàng | Nút **Bỏ qua** trên mọi finding; bỏ qua rồi thì highlight biến mất khỏi kịch bản |
| **G9** — sửa dễ dàng | Nút **Sửa tay** (sửa ngay trên gợi ý) và **Hoàn tác** trên mọi finding đã xử lý |

## Bằng chứng → thiết kế

Khối xanh dưới kịch bản ("Không gắn cờ — câu 5 dài 63 từ") là chỗ hiện thực hoá kết luận mining ở `spec.md` §1: **19,1% câu nói thật của giảng viên dài hơn 40 từ**, nên agent không dùng luật độ dài để kết luận lỗi. `F3` cũng nói rõ *"Không phải vì câu dài — vấn đề là lặp và chồng mệnh đề"*.
