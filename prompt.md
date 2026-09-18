# Brief + Plan: dọn tầng luật và sửa phép đo trong `eval/`

Tài liệu giao việc, tự chứa. Người/agent nhận việc không cần ngữ cảnh nào ngoài repo này.
Mọi số trong tài liệu đều kèm cách tự kiểm chứng lại.

---

## 0. Tóm tắt

Nhánh này (`truongan`) đang báo **recall 20/20 (100%)**. Kiểm tra lại cho thấy:

| Nguồn của con số 100% | Đóng góp |
|---|---|
| Regex chép nguyên văn đáp án trong `golden_set.json` | **14/20** |
| Rule tổng quát thật (dùng được cho kịch bản mới) | 6/20 |
| LLM | **0** (đóng góp biên bằng 0 — rule đã phủ hết 20/20 trước khi LLM nói gì) |

Ba việc cần xử lý, theo thứ tự nghiêm trọng:

1. **Tầng luật đang chép đáp án** → con số 100% không đo năng lực, và làm lời gọi AI mất vai trò ở quyết định trung tâm (rủi ro R5).
2. **No-flag 9 finding oan là do model `gpt-4o-mini`, không phải do tầng luật** → đổi về `gpt-4o` là xong.
3. **Ratio guard trong `_is_hit()` phạt nhầm chiều** → đang tính FAIL oan cho những lần model chỉ đúng chỗ nhưng chỉ gọn hơn ground truth. Lỗi này có ở **cả hai nhánh** vì đoạn code giống hệt nhau.

---

## 1. Phát hiện 1 — tầng luật chép đáp án (nghiêm trọng nhất)

### Bằng chứng

Chạy `rule_findings()` **một mình, không gọi LLM**, trên 20 case cấy lỗi → **hit 20/20**.

Đối chiếu từng regex trong `rule_findings()` (`eval/run_eval.py`) với `ground_truth_span` trong `eval/golden_set.json`:

| Regex | Trùng với |
|---|---|
| `khoa học tên lửa\|sự thay đổi cuộc chơi lớn vào cuối ngày` | GT của C7 và C2, nguyên văn |
| `parse file JSON để extract data ra format chuẩn\|GPT-4o-mini-2024-07-18` | GT của C5 và C9, nguyên văn |
| `tăng doanh thu lên \d+[,.]?\d*% ở các doanh nghiệp vừa và nhỏ` | GT của C4 |
| `\d+ triệu sinh viên trên toàn thế giới vào năm tới` | GT của C10 |
| `\(Learning Management System - LMS\)` | GT của C13, nguyên văn |
| `Dữ liệu sạch rất quan trọng\. Nếu không làm sạch dữ liệu thì mô hình sẽ học sai\.` | GT của C3, nguyên văn |
| `Nên nhớ là phần này cực kỳ đơn giản để vượt qua\.` | GT của C8, nguyên văn |
| `chuyển đổi một hệ thống RAG từ trạng thái demo \(...\) lên mức production \(...\)` | GT của C18, nguyên văn |
| `MVE/MVP/PoC` | GT của C17 |

Các rule này bắt được **đúng** những câu đã dùng để viết ra chúng, và bắt được **0** trên bất kỳ câu nào khác. Đưa một kịch bản mới có thành ngữ dịch cứng khác (không phải đúng chữ "khoa học tên lửa") thì tầng luật không thấy gì.

### Rule nào thật sự tổng quát

Chỉ 3 rule dùng được cho dữ liệu chưa từng thấy:

- `(?i)tại\s+trang\s+\d+` — trích dẫn trang dạng văn xuôi
- `(?i)\b[a-z]+\d+(?:-[a-z]+){2,}\b` — slug mã bài (`day13-monitoring-logging-observability`)
- Vòng lặp gắn cờ câu chứa `**` hoặc `[trang N]`

Đo riêng 3 rule này: **6/20 (30%) trên bộ cấy lỗi, 0 finding oan trên 7 câu sạch.** Hit: C11, C12, C15, C16, C19, C20 — đều là AI_VOICE (markdown/trích trang) và PRONUNCIATION (slug), tức đúng nhóm lỗi mà luật đếm được thật sự xử lý được.

Đây chính là kiến trúc `c2-summary.md` đã thiết kế từ đầu: *"tầng 1 · LUẬT ĐẾM ĐƯỢC → precision ~100%, không cần AI"* + *"tầng 2 · LLM cho những gì luật không kiểm được"*. Vấn đề không phải có tầng luật, mà là tầng luật đã bị nhồi thêm đáp án.

### Rủi ro R5

`c2-summary.md` mục 6 đã tự cảnh báo: *"Nếu tầng luật làm gần hết việc thì lời gọi AI không còn ở quyết định trung tâm, R5 (3 điểm) lung lay và giám khảo sẽ hỏi 'vậy AI làm gì?'"*. Hiện trạng đúng như vậy: rule phủ 20/20 nên LLM không đóng góp gì đo được vào recall.

### Tự kiểm chứng lại

```python
import re, json
src = open('eval/run_eval.py', encoding='utf-8').read()
ns = {'re': re}
exec(src[src.index('def _rule_finding'):src.index('def call_ai')], ns)
g = json.load(open('eval/golden_set.json', encoding='utf-8'))

def is_hit(a, b):
    return bool(a) and bool(b) and (b in a or a in b) and max(len(a), len(b)) / min(len(a), len(b)) <= 3

hit = sum(any(is_hit(f['exact_span'], c['ground_truth_span'])
              for f in ns['rule_findings'](c['text'])) for c in g['flawed_cases'])
print(f'rule layer khong co LLM: {hit}/20')
print('finding oan tren 7 cau sach:',
      sum(len(ns['rule_findings'](c['text'])) for c in g['no_flag_cases']))
```

---

## 2. Phát hiện 2 — no-flag 9/7 là lỗi model, không phải lỗi tầng luật

`rule_findings()` chạy trên cả 7 câu `no_flag_cases`: **0 finding**. Toàn bộ 9 finding oan đến từ LLM.

Khác biệt duy nhất so với `main` (chỉ 1 finding oan) là **model**: nhánh này chạy `openai/gpt-4o-mini`, `main` chạy `gpt-4o`. Đổi model là hết, không cần đụng vào rule.

---

## 3. Phát hiện 3 — ratio guard phạt nhầm chiều

`_is_hit()` (giống hệt nhau ở cả hai nhánh):

```python
ratio = max(len(ai_span), len(gt_span)) / min(len(ai_span), len(gt_span))
return ratio <= MAX_SPAN_RATIO   # = 3
```

`MAX_SPAN_RATIO` ra đời ở Lượt 8 (`eval/test-log.md`) để chặn kiểu ăn may **"AI trả nguyên cả câu nên ground truth nào cũng nằm trong đó"** — tức chỉ nhắm **span TO hơn GT**. Nhưng `max/min` phạt cả hai chiều, nên span **nhỏ hơn và chính xác hơn** GT cũng bị loại, dù đó mới là hành vi sản phẩm mong muốn ("chỉ đúng span + gợi ý sửa tối thiểu").

Đo trên `main` (Lượt 16, 7 case FAIL) — 4 case dưới đây model trả span **nằm trọn trong GT**, tức chỉ đúng vị trí:

| Case | GT (ký tự) | Span model | Ratio | Ngưỡng |
|---|---|---|---|---|
| C15 | 78 | `**Day 1: LLM Foundation**` (25) | **3.12** | 3.00 |
| C17 | 32 | `[trang 12]` (10) | **3.20** | 3.00 |
| C11 | 78 | `[trang 7]` (9) | 8.67 | 3.00 |
| C14 | 191 | `Day 1: **LLM Foundation**` (25) | 7.64 | 3.00 |

C15 trượt vì **0.12**, C17 trượt vì **0.20**.

---

## 4. Plan

Làm theo thứ tự. Mỗi bước đo lại trước khi sang bước sau — không gộp, nếu gộp thì không biết bước nào có tác dụng.

### Bước 1 — Đổi model về `gpt-4o`

Sửa định tuyến model trong `eval/run_eval.py` để nhánh này dùng cùng model với `main`.

**Kỳ vọng:** no-flag từ 9 finding oan xuống ~1. Recall gần như không đổi (rule đang phủ hết).
**Chi phí:** 1 lượt chạy.

### Bước 2 — Xoá rule chép đáp án, giữ rule tổng quát

Trong `rule_findings()`:

- **Giữ:** `tại\s+trang\s+\d+` · `[a-z]+\d+(?:-[a-z]+){2,}` · vòng lặp câu chứa `**` hoặc `[trang N]`.
- **Xoá:** mọi regex chứa nguyên văn thành ngữ/câu/số liệu của case cụ thể (9 mục ở bảng mục 1).
- **Viết lại hoặc xoá** 3 rule nửa-tổng-quát vì đang bám sát từng case: `^hello!\s*(?:welcome|i'm)` (nên thay bằng phát hiện câu toàn tiếng Anh thật sự, hoặc bỏ hẳn vì `SYSTEM_PROMPT` đã có luật này), và 2 regex xưng hô `hôm qua mình...chúng ta` / `các bạn...chúng tôi...tôi` (đang dùng `re.S` nên quét cả kịch bản dài, rủi ro oan cao trên văn nói thật).

**Kỳ vọng:** recall tụt từ 20/20 xuống khoảng **15/20 (75%)** — đây là con số thật. Phân rã: LLM `gpt-4o` đậu 13/20, rule tổng quát bổ sung C11 và C15 mà LLM trượt.
**Nếu kết quả lệch nhiều so với 15/20:** dừng, kiểm tra xem còn sót rule chép đáp án không.

### Bước 3 — Ratio guard bất đối xứng

Trong `_is_hit()`, tách hai chiều:

- **Span AI to hơn GT** (`gt_span in ai_span`): giữ ngưỡng chặt 3x. Đây là chiều ăn may, **không được nới**.
- **Span AI nhỏ hơn GT** (`ai_span in gt_span`): nới, kèm sàn chống span vụn. Đề xuất: chấp nhận nếu `len(ai_span) >= 8` **và** `len(ai_span)/len(gt_span) >= 0.15`. Sàn 8 ký tự vì `[trang 7]` (9 ký tự) là span đúng và hữu ích nhất có thể cho lỗi trích dẫn trang.

**Tuyệt đối không** chỉ nâng `MAX_SPAN_RATIO` từ 3 lên 4 — làm vậy nới luôn chiều ăn may, đúng lỗi Lượt 8 đã mất công vá.

**Kỳ vọng:** thêm C11, C14, C15, C17 được tính đúng.

### Bước 4 — Dọn `golden_set.json`

4 việc, độc lập nhau:

1. **Ground truth nhiều span.** Nhiều câu có nhiều lỗi khác loại chồng nhau nhưng GT chỉ có một span. Ví dụ C11 gom 3 lỗi (liệt kê hai chấm + mệnh đề bị động cụt + `[trang 7]`) vào một span 78 ký tự; C17 gom acronym (PRONUNCIATION) và trích trang (AI_VOICE) rồi dán một nhãn. Đổi sang danh sách `ground_truths: [{span, category}, ...]`, chấm PASS nếu khớp bất kỳ mục nào, giữ tương thích ngược với `ground_truth_span`.
2. **Thống nhất nhãn category.** C14 (câu tiếng Anh nguyên khối) đang gắn `TRANSLATIONESE`, trong khi `SYSTEM_PROMPT` và case E2 đều quy định toàn-câu-tiếng-Anh là `PRONUNCIATION`. C18 gắn `TRANSLATIONESE` cho câu thực chất chỉ chèn thuật ngữ tiếng Anh (`PRONUNCIATION`). Không đổi điểm (chấm chỉ so span) nhưng nhãn mâu thuẫn làm golden set mất giá trị làm chuẩn.
3. **Chuyển C18 sang `ambiguous_low_confidence_cases`.** Case mang `class: "②"` và note tự ghi *"agent không đủ căn cứ để tự quyết, cần người xác minh"* — đó là mô tả hành vi confidence thấp, không phải lỗi phải bắt dứt khoát, nhưng đang nằm trong bộ chấm recall nhị phân.
4. **Bổ sung ranh giới cho REPETITION.** Định nghĩa hiện tại *"nói lại nguyên ý vừa nói"* khiến case N5 (transcript thật, *"...quy trình bên trong nó cũng đang thay đổi — quy trình làm sản phẩm đang thay đổi..."*) bị gắn cờ đúng theo chữ nghĩa, trong khi `expected_behavior` là KHÔNG gắn cờ vì nhắc lại để nhấn mạnh là thủ pháp tự nhiên của văn nói. Cần bổ sung ranh giới này vào định nghĩa trong `SYSTEM_PROMPT`.

### Bước 5 — Báo cáo tách bạch

Sau khi xong, `eval/evaluation_report.json` và `eval/test-log.md` phải ghi **ba con số riêng**, không gộp:

- recall của **rule layer** chạy một mình
- recall của **LLM** chạy một mình
- recall của **hệ thống hợp nhất**

Không tách được ba số này thì không chứng minh được lời gọi AI nằm ở quyết định trung tâm (R5).

### Ngoài phạm vi plan này

Case **A3** (`workflow` — ranh giới thuật ngữ chuẩn của khoá vs chèn tiếng Anh tuỳ tiện) đã thử sửa bằng prompt hai lần, cả hai đều thất bại có kiểm chứng (`eval/test-log.md`, Lượt 10 và Lượt 14). Gốc rễ là hệ thống không có cách nào biết từ nào là thuật ngữ chuẩn của khoá. Việc thật cần làm là cho nạp **glossary**, tức thay đổi kiến trúc — tách thành task riêng, đừng thử hướng prompt thứ ba.

---

## 5. Cách xác minh

1. `temperature=0` phải đang được set trong payload của `call_ai()`.
2. Mỗi thay đổi chạy **tối thiểu 2 lượt độc lập**; chỉ coi là thật khi tái lập được. Lịch sử dự án: từng có lượt báo case A3 "PASS lần đầu tiên", đo lại với `temperature=0` thì sai — chỉ là may mắn ngẫu nhiên (`eval/test-log.md`, Lượt 12 → 13).
3. Sau mỗi bước chạy lại **đủ 39 case**, không chỉ 20 case recall, để phát hiện hồi quy ở no-flag và case hành vi.
4. Dùng đoạn script ở mục 1 để kiểm tra lại rule layer sau mỗi lần sửa — nó không tốn API.

---

## 6. Ràng buộc bắt buộc về tính trung thực

Con số recall sẽ **giảm** từ 20/20 xuống khoảng 15/20 sau khi dọn. Đó là kết quả đúng, không phải hồi quy: 20/20 trước đó được tạo ra bởi regex chứa sẵn đáp án nên không đo năng lực gì.

Khi cập nhật `spec.md` §7 và `eval/test-log.md`:

- Ghi rõ **vì sao** con số giảm, kèm bằng chứng rule layer chép đáp án.
- Ghi rõ thay đổi ratio guard là **sửa phép đo sau CP4**, kèm cả số trước và sau.
- Không trình bày con số sau khi nới ratio guard như thể hệ thống đã tốt lên — năng lực model không đổi, chỉ là thôi phạt oan.

Dự án đã mất gần một ngày để phát hiện và đính chính chuỗi số 85-95% bị thổi phồng do lỗi chấm điểm (`eval/test-log.md`, Lượt 8). Lần đó là bug vô tình. Giữ lại regex chép đáp án sau khi đã biết, hoặc báo số cao mà không khai cách đo đã đổi, sẽ là cố ý.
