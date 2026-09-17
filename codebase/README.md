# codebase/ — prototype

## Mức prototype: **Working**

| File | Là gì | Trạng thái |
|---|---|---|
| `server.py` + `web/index.html` | **Bản chính.** FastAPI + một trang HTML/JS thuần, không build | **Thật** — gọi LLM thật ở quyết định trung tâm |
| `test_server.py` | Kiểm tách câu, chia khối, Evidence Gate (LLM giả, không tốn API) | `python codebase/test_server.py` → `OK` |
| `app.py` | Bản Streamlit cũ (CP3) | Dự phòng, sẽ bỏ khi bản chính chạy ổn với key thật |
| `mockup.html` | Bản mock nộp CP2 | **Mock** — findings tĩnh viết tay |

## Chạy

```bash
pip install -r requirements.txt
cp .env.example .env        # OPENAI_API_KEY, OPENCODE_API_KEY hoặc GEMINI_API_KEY (xem chú thích trong file)
python codebase/server.py   # → http://localhost:8000
```

Giọng nghe thử mặc định là **Piper, chạy trên máy, không cần key**. Model không nằm trong repo (63 MB, `codebase/models/` bị `.gitignore`), mỗi máy tải một lần — lệnh chạy được cả Windows/macOS/Linux:

```bash
python -m piper.download_voices vi_VN-vais1000-medium --download-dir codebase/models
```

Nếu Piper báo không tìm thấy `phontab`: đường dẫn cài Python quá dài (>160 ký tự) nên espeak-ng không đọc được — đặt `PIPER_ESPEAK_DATA` trỏ tới bản sao/symlink thư mục `piper/espeak-ng-data` ở đường dẫn ngắn.

## Kiến trúc AI — workflow cố định, không phải agent tự chạy

```text
Kịch bản dán vào
  ① [Luật]  Tách câu, gom khối ≤40 câu theo ranh giới đoạn
  ② [LLM]   Mỗi khối 1 lời gọi gpt-4o (không có key OpenAI thì gemini-3.6-flash, chưa đo), song song → JSON findings
  ③ [Luật]  Evidence Gate: span phải khớp nguyên văn trong khối, không khớp thì loại
  ④ [Người] Nghe thử câu gốc / bản sửa (TTS) · So cách đọc (đo audio) · Xem chữ máy đọc (chép lại audio) → Áp dụng / Sửa tay / Bỏ qua / Hoàn tác → audit
```

| Chọn | Vì sao (bằng chứng trong repo) |
|---|---|
| **Không ReAct / tool-calling** | Bài chỉ có 1 quyết định AI, các bước cố định, không có công cụ để chọn. Mọi số đo ở `spec.md` §7 là của **1 lời gọi**, đổi sang vòng lặp là số đo mất giá trị. Không có tool thì prompt injection trong kịch bản không làm được gì (§7 SEC2: *"an toàn nhờ kiến trúc"*) |
| **Không thuần luật** | Mining §1: luật độ dài gắn cờ oan 19,1% câu thật. §3: LanguageTool bắt 0/10, Hemingway bỏ qua câu dịch cứng |
| **Luật ở hai đầu LLM** | Tách câu và kiểm span có đáp án chắc chắn, không cần LLM đoán |
| **Khối ≤40 câu** | Đúng cỡ đã đo (đoạn sạch 40 câu, 1 lời gọi). Cắt theo đoạn để câu có nguồn không bị gắn cờ UNGROUNDED_CLAIM oan |
| **Đọc bằng Piper, chép lại bằng Gemini — hai model riêng** | Đo 17/9 trên M1: Piper tạo 3–8 giây audio trong 0,1–0,35 giây (lần đầu ~1 giây do nạp model), không mạng, không 503; Gemini TTS ~8 giây và hay quá tải. Chép lại cần model nghe hiểu nên vẫn gọi Gemini (~6–12 giây), chỉ khi người duyệt bấm |
| **TTS ở bước người, không ở bước phát hiện** | Thử 17/9: Gemini TTS đọc trơn câu dịch cứng "được thực hiện bởi McKinsey…" (chép lại audio để kiểm). Nghe không phát hiện được lỗi nội dung, chỉ giúp so hai bản và bắt lỗi đọc số/viết tắt |
| **"So cách đọc" đo từ audio, không hỏi LLM** | `numpy` đo âm lượng + cao độ mỗi 10 ms → chỗ ngắt hơi (lặng ≥0,12 s), đoạn dài nhất không ngắt, tốc độ, độ lên xuống giọng; có test bằng tín hiệu giả trong `test_server.py`. Piper chạy **tắt nhiễu** để cùng một câu luôn ra cùng một audio (để mặc định thì quãng ngắt dao động 0,08–0,18 s giữa các lần) và **chèn 0,3 s lặng sau mỗi câu** như `piper --sentence_silence`, vì bản thân giọng này gần như đọc liền qua dấu chấm |
| **Tốc độ đọc Nhanh / Vừa / Chậm, không ghi "0,8×"** | `length_scale` của Piper không tỉ lệ thuận với tốc độ nghe (đặt 1,5 chỉ chậm thêm 18%), nên đặt 3 mức theo số đo: Nhanh 1,0 → ~5 tiếng/giây (giọng gốc) · Vừa 1,6 → ~4 (mặc định) · Chậm 2,0 → ~3,5. Mỗi lần nghe, server đo lại tốc độ thật trên audio và giao diện hiện "Vừa nghe: x tiếng/giây". Mức chọn nhớ trong `localStorage`. Giọng dự phòng của trình duyệt dùng `rate` tương ứng |
| **Từ tiếng Anh đọc theo phiên âm Anh, cùng giọng Việt** | Giọng Piper tiếng Việt đọc `cost-of-error` thành "cát xê", `McKinsey` thành "Mắc Kin Xi". Server nhận ra từ tiếng Anh (chữ Latin không dấu mà không phải âm tiết Việt hợp lệ, có f/j/w/z, hoặc viết tắt in hoa), lấy phiên âm `en-us` từ espeak có sẵn trong Piper và chèn dạng `[[ kˈɔst ʌv ˈɛɹɚ ]]` — không cần tải thêm giọng tiếng Anh, vẫn một giọng, một lần tạo. Test nhận diện trong `test_server.py`. Chưa đo được chất lượng nghe bằng chép lại (thiếu key Gemini) — cần người nghe xác nhận |
| **Chép lại bằng `gemini-3.6-flash`, không dùng `gemini-3.5-transcribe`** | Bản chuyên chép tự đổi "bảy mươi phần trăm" về "70%", nên không thấy được máy đọc số thành gì. So chữ bằng `difflib` (thư viện chuẩn), có test trong `test_server.py` |
| **Một nguồn prompt** | `server.py` import thẳng `call_ai`, `SYSTEM_PROMPT`, `MODEL` từ `eval/run_eval.py` — bản demo chạy đúng prompt + model đã đo |

## Lưu gì, không lưu gì (non-goal §4 #3)

| Dữ liệu | Ở đâu | Sống bao lâu |
|---|---|---|
| Kịch bản + trạng thái duyệt | `sessionStorage` của tab trình duyệt | Tải lại trang còn, đóng tab là hết. **Server không lưu** |
| Audio nghe thử | Bộ nhớ tab (nghe lại không tạo giọng lại) | Đóng tab hoặc bấm "Bài mới" là hết. Server không cache |
| `models/` giọng Piper | Máy chạy server, **không commit** | Tải một lần theo lệnh ở trên |
| `logs/trace.jsonl` | Server | Chỉ số đếm mỗi lượt soát: model, số câu, số khối, thời gian, giữ/loại. **Không có nội dung kịch bản** |
| `logs/audit.jsonl` | Server, **không commit** (`.gitignore`) | Mỗi quyết định: `session_id`, câu, category, confidence, span, bản thay. Dùng tính chỉ số validation CP5 (§8) |
| Kịch bản đã duyệt + audit report | Tải về máy người duyệt (nút "Xuất bản đã duyệt") | Do người duyệt giữ |

## Chỗ neo nguyên tắc HAX (cho `spec.md` §4b) — tất cả trong `web/index.html`

| Nguyên tắc | Vị trí |
|---|---|
| **G1** — làm rõ hệ thống làm được gì | Màn nhập: khối "Cách hệ thống làm việc" (4 bước, gắn nhãn LUẬT/LLM/NGƯỜI) + khối "Không làm" · Màn duyệt: thanh 4 bước kèm số thật của lượt soát |
| **G2** — làm rõ nó làm tốt đến đâu | Khối "Đã đo được gì" (80–95% · 0/40 · 2/7) · mỗi finding có **Độ chắc** 3 vạch · nhãn "Chỉ ảnh hưởng cách đọc, không phải lỗi nội dung" · khối "Đã xét, không gắn cờ: câu N (x từ)" · "Xem chữ máy đọc": tô chỗ giọng máy đọc khác chữ viết, ghi rõ bản chép cũng có thể nghe nhầm |
| **G8** — gạt bỏ dễ dàng | Nút **Bỏ qua** trên mọi finding, bỏ qua thì chỗ tô màu biến mất |
| **G9** — sửa dễ dàng | **Sửa tay** trên mọi finding · **Hoàn tác** trên mọi chỗ đã quyết · **Nghe bản sửa của bạn** ngay trong lúc sửa tay |
| **G10** — thu hẹp phạm vi khi nghi ngờ | Độ chắc thấp: **không có nút Áp dụng**, khối vàng "Chưa đủ căn cứ để tự sửa" · claim không gợi ý: "Không có gợi ý tự sửa" · nút "Viết lại cả bài" → hộp thoại từ chối |
| **G11** — giải thích vì sao | Lý do riêng trên từng finding |

## Bốn đường đi (cho `spec.md` §6)

| Đường đi | Trên giao diện |
|---|---|
| Happy path | Finding có gợi ý, độ chắc cao/vừa → bấm **Áp dụng**, đoạn thay hiện màu xanh, tự chuyển sang chỗ kế tiếp |
| Low-confidence ② | Độ chắc thấp → gạch chân nét đứt, không có nút Áp dụng, khối vàng |
| Failure ① | Claim không nguồn → không có gợi ý tự sửa · span AI bịa → Evidence Gate chặn, thanh bước ③ báo "loại N" |
| Correction | Sửa tay / Hoàn tác |
| Ngoài phạm vi ③ | Nút "Viết lại cả bài" → hộp thoại từ chối |
| Đặc thù domain ④ | Câu >40 từ không bị gắn cờ → khối "Đã xét, không gắn cờ" |
