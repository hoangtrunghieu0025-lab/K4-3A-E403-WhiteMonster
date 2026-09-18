# validation/ — vòng validation CP5 (R6)

Nhật ký cho người ngoài nhóm dùng thử prototype (`codebase/server.py` + `codebase/web/index.html` —
chạy `python codebase/server.py` rồi mở `http://localhost:8000`), theo kế hoạch ở `spec.md` §8.

**Assumption đang kiểm:** kịch bản do AI viết và AI đọc, nên chủ nhân bài giảng có thể chấp nhận luôn
giọng văn đó thay vì bỏ công sửa.

## Cách ghi log (mỗi lượt thử 1 file `session-<tên>.md`)

- Người thử: tên + vai trò (không cùng nhóm)
- Thời gian, kịch bản dùng để thử
- Quan sát: họ Accept / Sửa tay / Bỏ qua bao nhiêu finding, có đọc hết `why` trước khi quyết không
- Trích nguyên văn phản hồi (không diễn giải hộ)
- Kết luận: assumption có đứng vững không, vì sao

Đã có 2 lượt thử từ 2 willing user đã đồng ý từ 16/9 (xem `interview-log.md`, `spec.md` §8), sáng 18/9:
[`session-nguyen-duc-thai.md`](session-nguyen-duc-thai.md) (kịch bản giảng dạy — Áp dụng 4/7) ·
[`session-tran-hong-son.md`](session-tran-hong-son.md) (kịch bản MC sự kiện — Sửa tay 5/8, ngược tỉ lệ với Thái).

**Kết luận chung sau 2 lượt:** assumption đứng vững ở mức độ khác nhau tuỳ thể loại kịch bản — kịch bản giảng dạy (Thái) chấp nhận nhiều hơn vì sửa tay vẫn nhanh hơn thu âm lại; kịch bản MC sự kiện (Sơn) cần gọt giũa lại phần lớn vì thiếu "nhấn nhá, cảm xúc". Chưa có thay đổi nào áp dụng vào prototype dựa trên 2 lượt này — để TODO sau CP5.
