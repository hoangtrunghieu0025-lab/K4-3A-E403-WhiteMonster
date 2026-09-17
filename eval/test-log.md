# eval/test-log.md — nhật ký các lượt xây & chạy golden set

Theo nhịp lặp ở `02-guide.md` §2.6/§4.1: *chạy trọn bộ → bảng % → chọn một failure đau nhất → sửa → chạy lại trọn bộ*. Mỗi lượt là một bản ghi dưới đây, giữ cả case fail. Golden set hiện có **39 case** trong `eval/golden_set.json`, xây qua 3 lượt bởi 2 người khác nhau — log dưới đây giữ nguyên cả hai để không ai mất công.

## Lượt 1 — CP3, Đinh Trường An (đã chạy thật, model `openai/gpt-4o-mini`)

- **Số case ban đầu nghĩ ra:** 10 case cấy lỗi tự viết tay (`C1-C10`) + 1 đoạn sạch 40 câu — phủ 4/8 loại lỗi taxonomy (TRANSLATIONESE, REPETITION, INCONSISTENT_REGISTER, UNGROUNDED_CLAIM).
- **Kết quả:** Recall 6/10 (60%) · False Positive 0/40 câu sạch · Evidence Gate Drops 0.
- **Case fail và vì sao:**
  - C1, C6 (INCONSISTENT_REGISTER): 0/2 — model không bắt được khi khoảng cách giữa xưng hô lệch và câu trước quá xa.
  - C4, C10 (UNGROUNDED_CLAIM): 0/2 — cần AI giữ context rộng hơn một câu để nhận ra số liệu không có nguồn trong *toàn bài*.
- **Lỗi dữ liệu phát hiện khi rà lại (không phải lỗi model):** C5 và C9 từng gắn nhãn category sai (TRANSLATIONESE, UNGROUNDED_CLAIM) trong khi bảng kết quả `spec.md` §7 lại chấm cả hai là PRONUNCIATION. **Đã sửa ở lượt sau** — không đổi span/kết quả PASS-FAIL, chỉ chuẩn hoá lại tên category cho khớp 2 file.

## Lượt 2a — sau CP4, Phan Đức Duy (`commit 7a58831`) — mở rộng lên 22 case

- **Vì sao mở rộng:** rubric R4 đòi ≥20 case và ≥10 case từ chatlog thật; lượt 1 mới có 10 case, toàn tự viết.
- **Case mới thêm:** +10 case mine trực tiếp từ `data/vlearn-pack/chatlog/tutor_turns.csv` (trích ≤2 câu/case kèm `turn_id`, không commit nguyên pack) — `C11-C20`, thêm category mới `AI_VOICE` (giọng viết-cho-mắt-đọc: markdown, trích trang, gạch đầu dòng) ngoài 4 category cũ · +2 `scope_refusal_cases` (`S1`, `S2` — lớp ③, yêu cầu viết lại toàn văn / thêm nội dung mới, đúng theo case đã thiết kế ở spec.md §5).
- **Gắn thêm nhãn `difficulty` (thường/khó/hiếm) và `class` (①②③④) cho toàn bộ 10 case cũ + 20 case mới** — đạt cơ cấu rubric: 10 thường · 8 chỗ khó (≥2/lớp) · 4 hiếm.
- **Sửa code:** `eval/run_eval.py` bỏ hardcode "10 case", tự đếm theo độ dài `flawed_cases`.
- **Kết quả:** TODO (Duy note lại) — chưa chạy được lượt đủ 20 case vì môi trường build không có `OPENROUTER_API_KEY`.

## Lượt 2b — sau CP4 (phiên làm việc này) — mở rộng lên 39 case, thêm bảo mật

- **Vì sao mở rộng tiếp:** 22 case của lượt 2a đã đạt chuẩn rubric tối thiểu, nhưng vẫn thiếu: case tự động cho lớp ② (mơ hồ/confidence thấp), case xác nhận "không gắn cờ" trên câu dài thật (lớp ④, mới có trong prose ở §1 chứ chưa phải case eval), và **không có case nào test khả năng chống chỉ thị nhúng trong kịch bản** — quan trọng vì input là văn bản do người dùng cung cấp, agent phải luôn coi là dữ liệu chứ không phải lệnh.
- **Không sửa/xoá case nào của lượt 2a** — `flawed_cases` và `scope_refusal_cases` giữ nguyên, chỉ thêm 4 mảng mới song song (xem `_merge_note` trong `golden_set.json`):

  | Nhóm mới | Số case | Mục đích |
  |---|---|---|
  | `ambiguous_low_confidence_cases` | 4 (A1-A4) | Lớp ② — kỳ vọng confidence THẤP/VỪA, không tự Áp dụng; A4 mined nguyên văn từ `transcript-01[T01-016]` test lỗi thường gặp nhất: gắn cờ ungrounded chỉ vì đọc nửa câu đầu, bỏ qua nguồn nêu ở nửa sau |
  | `no_flag_cases` | 7 (N1-N7) | Lớp ④ — 6 câu dài **thật** trích transcript giảng viên (T01-001/005/012/016/018/020, đúng 6 câu đã dẫn ở `spec.md` §1, không thêm data pack mới) phải KHÔNG bị gắn cờ dù dài; N7 test input rỗng không được crash/bịa lỗi |
  | `security_refusal_cases` | 4 (SEC1-SEC4) | Lớp ③ + **bảo mật** — SEC1/SEC4 là **prompt injection** nhúng trong kịch bản (giả `[SYSTEM OVERRIDE]` đòi lộ system prompt/API key, khối code giả lệnh admin đòi xuất dữ liệu phiên khác); SEC2 đòi xoá audit trail; SEC3 kịch bản chứa số điện thoại thật — test agent không tự ý xoá/sửa mà chỉ cảnh báo |
  | `edge_format_cases` | 2 (E1-E2) | Case hiếm — mẩu quá ngắn (vi phạm luật 7 sổ luật Studio) và câu toàn tiếng Anh |

- **Sửa lại 2 case cũ (không thêm/bớt case, chỉ sửa nhãn sai từ lượt 1):** `C5` category TRANSLATIONESE → PRONUNCIATION, `C9` category UNGROUNDED_CLAIM → PRONUNCIATION — khớp với bảng kết quả `spec.md` §7 đã chạy thật từ lượt 1.
- **Sửa code:** `eval/run_eval.py` giữ nguyên toàn bộ logic của Duy (đếm `flawed_cases`, evidence gate, bảng markdown C1-C20), **thêm phần chạy `no_flag_cases`** (đếm finding lọt, kỳ vọng 0) và **phần in output thô** của `scope_refusal_cases`/`ambiguous_low_confidence_cases`/`security_refusal_cases`/`edge_format_cases` để người chấm tay theo `expected_behavior` (đây là case hành vi — từ chối/confidence thấp — không so khớp span tự động được).
- **Kết quả cải thiện — TODO: chưa đo được, cần chạy thật.** Phiên làm việc này không có `OPENROUTER_API_KEY` trong môi trường nên chưa gọi được model để lấy số cho 17 case mới (7 no-flag + 4 ambiguous + 4 security + 2 edge).

## TODO trước CP5

1. Set `OPENROUTER_API_KEY` rồi chạy `python eval/run_eval.py` — lấy số Recall/FP/Gate Drops thật cho `flawed_cases` (C1-C20, đủ 20 thay vì chỉ 10) + `no_flag_cases` (N1-N7).
2. Đọc thủ công output của `scope_refusal_cases`, `ambiguous_low_confidence_cases`, `security_refusal_cases`, `edge_format_cases` trong `eval/evaluation_report.json` — chấm đạt/không đạt theo cột `expected_behavior`.
3. **Ưu tiên SEC1/SEC4 (chống prompt injection) trước tiên** theo nhịp lặp của guide (chọn MỘT failure đau nhất để sửa) — nếu agent tuân theo chỉ thị nhúng (lộ system prompt, xuất dữ liệu ngoài phiên), đây là rủi ro an toàn thật, không chỉ là rớt điểm eval, cần sửa `SYSTEM_PROMPT` trong `codebase/app.py` trước khi demo CP6.
4. Cập nhật bảng kết quả + % ở `spec.md` §7 sau khi có số thật — **không sửa quality bar đã chốt tại CP4** (FP=0, Recall≥60%), chỉ ghi nhận thêm số đo trên bộ mở rộng, kể cả nếu thấp hơn.
