# Tổng kết cập nhật 17/9 — Phan Đức Duy

**Tóm tắt:** prototype chính giờ là `codebase/server.py` (FastAPI) + `codebase/web/index.html`. Bản Streamlit `app.py` chỉ còn để dự phòng. Pull về, làm theo mục 1 là chạy được.

---

## 1. Chạy dự án — làm theo thứ tự

```bash
git pull origin main
pip install -r requirements.txt
python -m piper.download_voices vi_VN-vais1000-medium --download-dir codebase/models
cp .env.example .env          # Windows: copy .env.example .env
```

Mở `.env`, điền key (ít nhất 1 key để soát kịch bản):

| Biến | Dùng cho | Ghi chú |
|---|---|---|
| `OPENAI_API_KEY` | Soát kịch bản bằng `gpt-4o` | **Model đã đo** ở spec §7 — nên dùng khi demo |
| `OPENCODE_API_KEY`, `OPENCODE_MODEL` | Soát bằng OpenCode Go (mặc định `deepseek-v4-flash`) | Gói Go dành cho coding agent, không nên làm backend chính lúc demo |
| `GEMINI_API_KEY` | Soát (khi không có 2 key trên) + nút **"Xem chữ máy đọc"** | Nút này chỉ chạy với key Gemini |

Có nhiều key thì bước soát dùng key đầu tiên theo thứ tự **OpenAI → OpenCode Go → Gemini**. Nghe thử **không cần key** (Piper chạy trên máy).

```bash
python codebase/test_server.py    # phải in OK
python codebase/server.py         # mở http://localhost:8000
```

> **Không commit `.env`, không dán key vào chat/Zalo.** Key lỡ lộ thì thu hồi ngay trên trang của nhà cung cấp.
> Sửa `.env` xong phải **tắt server (Ctrl+C) rồi chạy lại** — server chỉ đọc key lúc khởi động.

---

## 2. Đã thêm những gì

### 2.1 `spec.md`
- **§3 Giải pháp tương tự** — đã điền bằng thử thật trên case tự viết C1–C10: LanguageTool bắt **0/10** (không có tiếng Việt), Hemingway **gắn cờ oan câu dài xuôi** và bỏ qua câu dịch cứng, Grammarly **có tiếng Việt nhưng chỉ bắt chính tả/dấu câu**, SSML của Google TTS (tra tài liệu).
- Sửa câu "Grammarly không dùng được cho tiếng Việt" ở §1/§2 (sai với bản hiện tại).
- **§4:** mức prototype → **Working**; thêm mục **Kiến trúc AI**; §4b (nguyên tắc HAX) và §6 (các đường đi) trỏ sang giao diện mới. Mọi thay đổi có dòng trong changelog §9.

### 2.2 Prototype (`codebase/`)
**Luồng:** dán cả kịch bản → hệ thống tự tách câu và soát → kịch bản bôi màu từng chỗ + checklist bên phải (**Áp dụng / Sửa tay / Bỏ qua / Hoàn tác**) → xuất kịch bản đã duyệt + audit report.

**Kiến trúc AI — cần nắm khi bị hỏi ở CP6:** workflow cố định, **không phải ReAct agent**.

```text
① [Luật]  Tách câu, gom khối ≤40 câu theo đoạn
② [LLM]   Mỗi khối 1 lời gọi → JSON findings (dùng NGUYÊN prompt + hàm gọi của eval/run_eval.py)
③ [Luật]  Evidence Gate: span không khớp nguyên văn kịch bản thì loại
④ [Người] Nghe thử / So cách đọc / Xem chữ máy đọc → Áp dụng / Sửa tay / Bỏ qua → audit
```

Vì sao không ReAct: bài chỉ có 1 quyết định AI, các bước cố định; mọi số đo §7 là của 1 lời gọi; không có tool thì lệnh nhúng trong kịch bản không làm được gì (SEC1–SEC4). Vì sao không thuần luật: luật độ dài gắn cờ oan 19,1% câu thật (§1), công cụ luật bắt 0/10 (§3).

**Phần giọng đọc (đều ở bước ④, không dùng để phát hiện lỗi):**

| Tính năng | Làm gì | Cần key? |
|---|---|---|
| **Nghe câu gốc / bản sửa** | Giọng **Piper** `vi_VN-vais1000-medium` chạy trên máy, ~0,3 giây mỗi câu. Lỗi thì tự đọc bằng giọng trình duyệt | Không |
| **Tốc độ đọc Nhanh / Vừa / Chậm** | Mặc định Vừa (~4 tiếng/giây). Mỗi lần nghe hiện tốc độ đo thật | Không |
| **Từ tiếng Anh** | Nhận ra từ tiếng Anh (`cost-of-error`, `McKinsey`, `AI`…) và đọc theo phiên âm Anh thay vì luật tiếng Việt | Không |
| **So cách đọc** | Vẽ âm lượng, chỗ ngắt hơi, đường lên xuống giọng của bản gốc và bản sửa trên cùng trục thời gian + bảng số (đoạn dài nhất không ngắt, tốc độ…) | Không |
| **Xem chữ máy đọc** | Chép lại audio vừa nghe, tô chỗ máy đọc khác chữ viết (vd `GPT-4o-mini-2024-07-18` → "giê pi ti bốn ô mi ni…") | **Gemini** |

**Lưu gì:** kịch bản chỉ nằm trong tab trình duyệt (đóng tab là hết — non-goal §4). Server ghi `codebase/logs/trace.jsonl` (chỉ số đếm, **được commit** làm bằng chứng lời gọi AI thật) và `codebase/logs/audit.jsonl` (quyết định duyệt, **không commit**).

Chi tiết kỹ thuật + chỗ neo từng nguyên tắc HAX: [`codebase/README.md`](codebase/README.md).

### 2.3 Eval (`eval/run_eval.py`)
- Thêm nhà cung cấp **OpenCode Go** (kèm header `x-opencode-session` bắt buộc) và **Gemini**; tự retry khi 503; bóc JSON nếu model bọc trong ```` ``` ````.
- Mini-eval OpenCode Go trên 10 case tự viết + đoạn sạch 40 câu (1 lượt, **chưa phải số chính thức**):

| Model | Bắt đúng | Không tính span cả câu | Gắn cờ oan đoạn sạch |
|---|---|---|---|
| `deepseek-v4-flash` | 10/10 | 8/10 | 0 |
| `gpt-5.6-luna` | 9/10 | 6/10 | 0 |
| `glm-5.3` | 9/10 | 8/10 | 3 |
| `kimi-k3` | 7/10 | 6/10 | 2 |

---

## 3. Việc cần làm tiếp

| Việc | Đề xuất người làm | Hạn |
|---|---|---|
| **Chốt model dùng khi demo.** Khối "Đã đo được gì" trên giao diện là số của `gpt-4o`. Demo bằng model khác thì phải chạy lại golden set và sửa khối đó | Hiếu + An | Trước CP5 |
| **Sửa 2 lỗi chấm trong `run_eval.py`:** span rỗng `""` được tính PASS; span rộng cả câu cũng tính PASS → recall trong spec có thể cao hơn thực tế | An | Trước CP5 |
| **Nhánh `feat/cp3-ai-eval`** sửa trùng `eval/run_eval.py`, `eval/golden_set.json`, `spec.md`, `codebase/README.md` → **đừng merge thẳng**, so với `main` rồi gộp phần cần giữ | Tác giả nhánh | Trước khi merge |
| **Nghe thử phần đọc tiếng Anh** trên app — nếu nghe tệ hơn cách đọc cũ thì báo Duy gỡ | Ai cũng được | Sớm |
| **Chuẩn bị máy demo:** cài đủ, tải giọng Piper, điền `.env`, `test_server.py` in OK, soát thử 1 kịch bản | Người demo | Trước dry run CP5 |
| **Quay video demo dự phòng CP5** trên giao diện mới (1 case chuẩn + 1 case chỗ khó) | Duy | 13:00 18/9 |
| Xoá `codebase/app.py` và `streamlit` khỏi `requirements.txt` sau khi demo ổn | Duy | Sau CP5 |

> **Luật vibe-coding CP6:** ai đứng tên phần nào phải tự giải thích được phần đó. Người phụ trách `codebase/` nên đọc qua `server.py` (khoảng 450 dòng, có chú thích tiếng Việt).

---

## 4. Lỗi hay gặp

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| Bấm "Soát kịch bản" báo lỗi *"Thiếu OPENAI_API_KEY, OPENCODE_API_KEY hoặc GEMINI_API_KEY"* | `.env` chưa có key soát | Điền key, tắt rồi chạy lại server |
| Nút **"Xem chữ máy đọc · cần key Gemini"** bị mờ | Không có `GEMINI_API_KEY` | Điền key Gemini, chạy lại server |
| Bấm nghe báo *"Chưa có giọng vi_VN-vais1000-medium"* | Chưa tải giọng Piper | Chạy lệnh `python -m piper.download_voices …` ở mục 1 |
| Piper báo không tìm thấy `phontab` | Đường dẫn cài Python dài hơn ~160 ký tự | Đặt `PIPER_ESPEAK_DATA` trỏ tới thư mục `piper/espeak-ng-data` ở đường dẫn ngắn |
| OpenCode Go trả 400 `MissingSessionID` | Code cũ chưa gửi header phiên | Đã sửa trong `run_eval.py`, pull bản mới |
| VS Code hiện *"Enable python.terminal.useEnvFile"* | Chỉ là gợi ý của extension | Bỏ qua — app tự đọc `.env` |
