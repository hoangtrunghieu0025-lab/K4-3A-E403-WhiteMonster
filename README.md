# Mini Hackathon AI — Batch 04 · Lớp 3A

**SPEC → Prototype → Demo.** Đây không phải cuộc thi code — đây là cuộc thi **tư duy sản phẩm AI**.

## 👥 Thành viên nhóm & Phân công vai trò

**Lớp:** 3A · **Phòng:** E403 · **Cụm:** C1 · **Track:** C — Lesson Studio (đề C2)

| Họ và Tên | Mã Học Viên | Vai trò chính | Phần việc đảm nhiệm trong dự án |
|---|---|---|---|
| Hoàng Trung Hiếu (đội trưởng) | 2A202602945 | Product owner · chủ spec | Chủ `spec.md` (§1 problem statement, §2 bảng impact, §4 lát cắt & non-goals); nộp form cả 5 mốc; dựng `demo-slides.pdf`; mở đầu phần thuyết trình CP6 |
| Nguyễn Thọ Đạt | 2A202602484 | Research · evidence | Phỏng vấn Studio team/lab coach theo Mom Test, giữ log nguyên văn trong `interview-log.md`; tổng hợp số liệu + quote vào `spec.md` §1; §3 nghiên cứu giải pháp tương tự; chạy vòng validation `validation/` ở CP5 |
| Đinh Trường An | 2A202602393 | Prompt · eval | Thiết kế prompt cho agent QA kịch bản; xây golden set trong `eval/` (≥10 case kịch bản lỗi gắn nhãn tay + ≥1 đoạn sạch đo false positive); chạy eval, lập bảng kết quả `spec.md` §7; chốt quality bar trước CP4 |
| Phan Đức Duy | 2A202602397 | Prototype · demo | Dựng prototype trong `codebase/` (flow duyệt kịch bản, accept/reject từng finding); nối lời gọi AI thật + lưu log/trace; quay video thao tác CP3 và video demo dự phòng CP5 |

> **CP1 (Canvas):** [`canvas.md`](canvas.md) · [`canvas.png`](canvas.png) — đã nộp. Nội dung cũng nằm trong `spec.md` (đầu file + §1–§2, §4).
>
> **Cập nhật prototype 17/9 — cách chạy và việc cần làm:** [`TONG-KET-17-9.md`](TONG-KET-17-9.md)

- Thời lượng: **47,5 giờ** từ phát đề đến thuyết trình (ca 3A) — LAB 5 (phát đề + build) · LEC 6 (tiếp tục build theo ca) · LAB 6 (vòng thi)
- Nhóm: **3-4 người** · thi theo phòng (E403 / E402), chia cụm rồi chung kết phòng — xem *Thể thức thi*
- **Chia cụm theo bàn**, không cần chung đề tài. Chủ đề tự chọn trong khuôn khổ đề bài
- Nhóm nhỏ thì **chọn lát cắt nhỏ**, và phải có **khảo sát nỗi đau thật** — đây là chỗ ăn điểm nặng nhất

## Bắt đầu từ đâu?

1. Đọc **`01-challenge-brief.md`** để hiểu khung chung và 5 tiêu chí, rồi **`tracks/README.md`** để chọn track và đề.
2. Mở **`02-guide.md`** — hướng dẫn từng giai đoạn, đứng ở đâu đọc mục đó.
3. Viết spec theo **`03-ai-spec-template.md`** — deliverable trung tâm của cả sự kiện.
4. Đọc **`04-rubric.md`** ngay từ đầu — biết trước bài được chấm theo tiêu chí nào.

| File / thư mục | Nội dung |
|---|---|
| `01-challenge-brief.md` | Đề bài: bảng 5 track · lát cắt · ràng buộc chung · 5 tiêu chí nghiệm thu |
| `02-guide.md` | Hướng dẫn 5 giai đoạn: khám phá → spec → build → đo & validate → demo |
| `03-ai-spec-template.md` | Template AI Spec (nộp tại **hạn chốt spec** — xem Lịch) |
| `04-rubric.md` | Rubric 100 điểm (25 nộp checkpoint + 67 chấm bài + 8 điểm R6) + checklist xác minh 6 mốc |
| `tracks/` | **5 track**, mỗi đề cùng một khung mục: A VLearn Tutor · B Trợ lý Discord · C Lesson Studio · D Học tập thích ứng & tương tác · E Làn mở (trong phạm vi AI20k) — bắt đầu từ `tracks/README.md` |
| `data/` | Dữ liệu thật đã ẩn danh: `vlearn-pack/` (chatlog VLearn tutor + 6 transcript bài giảng + 2 bộ slide bản hackathon) và **`discord-pack/` (tin nhắn Discord khoá 4 + bản tin bot)** — dùng để tìm bằng chứng và xây golden set. **Đọc `data/README.md` trước** |
| `further-reading/` | Tài liệu tham khảo có tóm lược tiếng Việt: **Mom Test** (phỏng vấn), **PAIR Guidebook** (Google, 6 chương), **HAX Toolkit** (Microsoft, 18 nguyên tắc), **JTBD Playbook** + worksheet — bắt đầu từ `further-reading/README.md` |

## Lịch — 6 checkpoint (ca 3A · 47,5 giờ)

| Mốc | Cần hoàn thành | Hạn (ca 3A) |
|---|---|---|
| — | Khai mạc 17:30 · phát đề 18:00 | 16/9 |
| **CP1** | Canvas 4 ô + đội trưởng + **link repo GitHub công khai** | **19:30** · 16/9 |
| **CP2** | Cho thấy **luồng hoạt động** — bấm thử được, hoặc sơ đồ luồng | **21:00** · 16/9 |
| **CP3** | **Video thao tác** 30 giây + **số đo** (thử bao nhiêu, đúng bao nhiêu) | **16:00** · 17/9 |
| **CP4** | Chốt `spec.md` — **khoá chuẩn "đạt"** · tự khai phần chưa xong | **21:00** · 17/9 |
| **CP5** | Slide PDF + **video demo dự phòng cho buổi pitch** — nộp cuối | **13:00** · 18/9 |
| **CP6** | Thuyết trình · không nộp thêm | **17:30** · 18/9 |

**CP1 đến CP5 mỗi mốc 5 điểm.** Nộp đúng hạn được đủ, nộp muộn là **0 điểm mốc đó** — không bù được bằng mốc khác.

## Cấu trúc repo

```
repo/
├── README.md          ← copy file này, điền bảng thành viên ở đầu
├── spec.md            ← AI Spec theo 03-ai-spec-template.md (chốt tại CP4)
├── jtbd-worksheet.md  ← worksheet JTBD đính kèm §1 (job map 8 bước · job story · alternatives)
├── demo-slides.pdf    ← slide 6 trang theo 02-guide.md §5.1
├── codebase/          ← prototype (ghi rõ phần nào mock)
├── eval/              ← golden set + bảng kết quả các lượt chạy
├── validation/        ← nhật ký cho người ngoài dùng thử (R6 — không làm thì trần điểm 92)
└── reflection/        ← mỗi người 1 file
```

**Không commit data pack** (`data/discord-pack/`, `data/vlearn-pack/`) vào repo này — chỉ trích dẫn ngắn (≤2 câu/ví dụ, kèm `msg_id`) trong `spec.md` / `eval/`, theo đúng quy định bảo mật dữ liệu của khoá.
