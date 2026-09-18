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

Đã dựng sẵn mẫu cho 2 willing user đã đồng ý từ 16/9 (xem `interview-log.md`, `spec.md` §8):
[`session-nguyen-duc-thai.md`](session-nguyen-duc-thai.md) · [`session-tran-hong-son.md`](session-tran-hong-son.md).

TODO: chưa có lượt thử nào — 2 người thử tự điền trực tiếp vào file mẫu tương ứng sau khi thử, trước hạn CP5 (13:00 18/9).
