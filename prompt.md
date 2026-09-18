# Brief: sửa phép đo recall trong `eval/` — 6 vấn đề đã xác định bằng bằng chứng

Tài liệu giao việc, tự chứa. Người/agent nhận việc không cần ngữ cảnh nào khác ngoài repo này.

---

## 0. Đọc trước: hai nhánh đang đo bằng hai cách khác nhau

| | `main` | `truongan` (nhánh chứa file này) |
|---|---|---|
| Tầng luật `rule_findings()` | không có | có |
| Model đã đo | `gpt-4o` | `openai/gpt-4o-mini` |
| Recall | 13/20 (65%) | 20/20 (100%) |
| No-flag (số finding oan trên 7 câu sạch) | 1 | 9 |
| `_is_hit()` + `MAX_SPAN_RATIO = 3` | **giống hệt nhau ở cả hai nhánh** | |

Phân tích dưới đây thực hiện trên `main`. Nhưng **lỗi phép đo nằm trong `_is_hit()` — đoạn code y hệt ở cả hai nhánh** — nên kết luận áp dụng cho cả hai.

**Hệ quả cần cân nhắc khi nhận việc:** nếu phép đo được sửa cho công bằng, recall của `main` (không có tầng luật) sẽ tăng từ 13/20 lên khoảng 16-17/20 — tức khoảng cách mà tầng luật ở nhánh `truongan` đang lấp **nhỏ hơn nhiều so với vẻ ngoài**, trong khi tầng luật đang trả giá bằng no-flag 9 finding oan so với 1. Nên sửa phép đo **trước**, rồi mới quyết định tầng luật có đáng giữ hay không.

---

## 1. Phát hiện chính

Trên `main`, 7 case FAIL ở bộ recall. Trong đó **chỉ 3 case là model sai thật**. 4 case còn lại: model trả span **nằm trọn trong vùng ground truth**, tức chỉ đúng vị trí nhưng hẹp hơn GT, rồi bị `MAX_SPAN_RATIO` loại.

| Case | GT (ký tự) | Span model trả | Nằm trong GT | Ratio | Ngưỡng |
|---|---|---|---|---|---|
| C15 | 78 | `**Day 1: LLM Foundation**` (25) | có | **3.12** | 3.00 |
| C17 | 32 | `[trang 12]` (10) | có | **3.20** | 3.00 |
| C11 | 78 | `[trang 7]` (9) | có | 8.67 | 3.00 |
| C14 | 191 | `Day 1: **LLM Foundation**` (25) | có | 7.64 | 3.00 |

C15 trượt vì **0.12**, C17 trượt vì **0.20**.

Tra cứu lại lý do `MAX_SPAN_RATIO` ra đời (`eval/test-log.md`, Lượt 8): nó được thêm để chặn kiểu ăn may **"AI trả nguyên cả câu nên ground truth nào cũng nằm trong đó"**. Tức mục đích gốc chỉ nhắm **span TO hơn GT**. Nhưng code hiện tại dùng `max/min` nên phạt **cả hai chiều** — kể cả khi model trả span **nhỏ hơn và chính xác hơn** GT, vốn là hành vi sản phẩm mong muốn ("chỉ đúng span + gợi ý sửa tối thiểu").

---

## 2. Sáu việc cần làm

### 2.1 `_is_hit()` — làm ratio guard bất đối xứng

**File:** `eval/run_eval.py`

Hiện tại:

```python
MAX_SPAN_RATIO = 3

def _is_hit(ai_span, gt_span):
    if not ai_span or not gt_span:
        return False
    overlap = gt_span in ai_span or ai_span in gt_span
    if not overlap:
        return False
    ratio = max(len(ai_span), len(gt_span)) / min(len(ai_span), len(gt_span))
    return ratio <= MAX_SPAN_RATIO
```

Cần đổi thành hai ngưỡng riêng:

- **Span AI TO hơn GT** (`ai_span` chứa `gt_span`): giữ ngưỡng chặt (3x). Đây là chiều ăn may, không được nới.
- **Span AI NHỎ hơn GT** (`ai_span` nằm trong `gt_span`): nới ngưỡng, và thêm sàn tối thiểu để tránh span vụn vô nghĩa. Đề xuất: chấp nhận nếu `len(ai_span) >= 8` ký tự **và** `len(ai_span) / len(gt_span) >= 0.15`.

Lý do chọn ngưỡng: `[trang 7]` = 9 ký tự là span đúng và hữu ích nhất có thể cho lỗi trích dẫn trang, nên sàn phải ≤ 9. Tỉ lệ 0.15 giữ cho span không nhỏ đến mức vô nghĩa so với GT.

**Không được** chỉ nâng `MAX_SPAN_RATIO` từ 3 lên 4 — làm thế sẽ nới luôn chiều ăn may, đúng cái lỗi Lượt 8 đã mất công vá.

### 2.2 Ground truth phải cho phép nhiều span hợp lệ

**File:** `eval/golden_set.json`

Hiện mỗi case trong `flawed_cases` chỉ có **một** `ground_truth_span` + **một** `category`. Nhưng nhiều câu chứa **nhiều lỗi khác loại chồng nhau**, và GT hiện gom chúng vào một span duy nhất:

- **C11** — GT là `Được xác định là "engine" cốt lõi cho cả Generative AI và Agentic AI [trang 7]` (78 ký tự), thực chất gom 3 lỗi: cấu trúc liệt kê hai chấm, mệnh đề bị động cụt chủ ngữ, và trích dẫn `[trang 7]`.
- **C17** — GT là `phân biệt MVE/MVP/PoC [trang 12]`, gom 2 lỗi khác loại: cụm acronym (PRONUNCIATION) và trích dẫn trang (AI_VOICE), rồi dán một nhãn PRONUNCIATION lên cả cụm.

Cần đổi schema sang danh sách, ví dụ:

```json
"ground_truths": [
  {"span": "[trang 7]", "category": "AI_VOICE"},
  {"span": "Vai trò của LLM:", "category": "AI_VOICE"}
]
```

Chấm PASS nếu khớp **bất kỳ** mục nào. Giữ tương thích ngược với `ground_truth_span` cũ nếu chưa chuyển hết.

### 2.3 Thống nhất nhãn category — đang mâu thuẫn nội bộ

Hai mâu thuẫn đã xác định:

1. **Toàn câu tiếng Anh.** `SYSTEM_PROMPT` có luật: *"Nếu TOÀN BỘ câu là tiếng Anh thì gắn cờ PRONUNCIATION severity HIGH"*, và case `E2` trong `edge_format_cases` cũng expect PRONUNCIATION (đang PASS ổn định). Nhưng **C14** — cũng là câu tiếng Anh nguyên khối — lại gắn nhãn `TRANSLATIONESE`. Cùng hiện tượng, hai nhãn.
2. **Code-switch thuật ngữ.** **C18** gắn `TRANSLATIONESE` cho `chuyển đổi một hệ thống RAG từ trạng thái demo... lên mức production...`. Câu này không có cấu trúc nào dịch sát từ tiếng Anh — chỉ là chèn thuật ngữ tiếng Anh vào câu tiếng Việt, tức `PRONUNCIATION` theo đúng taxonomy đang dùng.

Chốt một quy ước rồi sửa nhãn cho nhất quán. Hiện phép chấm chỉ so span, không so category, nên việc này **không đổi điểm** — nhưng nhãn mâu thuẫn làm golden set mất giá trị làm chuẩn.

### 2.4 Chuyển C18 sang đúng bucket

**C18** mang `"class": "②"` (lớp mơ hồ) và note của chính nó ghi: *"agent không đủ căn cứ để tự quyết đổi sang tiếng Việt, cần người xác minh"*. Đây là mô tả hành vi **confidence thấp**, không phải lỗi phải bắt dứt khoát. Nhưng case đang nằm trong `flawed_cases` — bộ chấm recall nhị phân pass/fail.

Chuyển sang `ambiguous_low_confidence_cases` với `expected_behavior` mô tả rõ: gắn cờ với `confidence: LOW`, không tự quyết.

### 2.5 Bổ sung ranh giới cho category REPETITION

Định nghĩa hiện tại trong `SYSTEM_PROMPT`: *"REPETITION: lặp ý, filler, conclusion residue (nói lại nguyên ý vừa nói)"*.

Case no-flag **N5** (câu 74 từ mined từ transcript thật) chứa: *"...quy trình bên trong nó cũng đang thay đổi — quy trình làm sản phẩm đang thay đổi..."* — **đúng là "nói lại nguyên ý vừa nói" theo nguyên văn định nghĩa**, nên model gắn cờ là hợp lệ theo luật. Nhưng `expected_behavior` của case là **KHÔNG gắn cờ**, vì trong văn nói, nhắc lại để nhấn mạnh là thủ pháp tự nhiên.

Định nghĩa đang thiếu ranh giới này. Cần bổ sung, đại ý: *nhắc lại để nhấn mạnh trong văn nói không phải lỗi; chỉ gắn cờ khi lặp không thêm thông tin và không có chức năng nhấn mạnh.*

Đây là mục có khả năng thành công cao nhất trong 6 mục, vì nó vá đúng một mơ hồ đã xác định được bằng bằng chứng, chứ không phải đoán.

### 2.6 A3 — không sửa bằng prompt được, cần glossary

Case **A3** (`Hôm nay chúng ta sẽ dùng workflow này để tự động hoá việc chấm bài.`) yêu cầu model gắn cờ `workflow` với `confidence: LOW` và nói rõ đang đoán. Model im lặng vì `workflow` là loanword quá phổ biến.

Gốc rễ: **hệ thống không có cách nào biết từ nào là thuật ngữ chuẩn của khoá.** Đã thử hai hướng prompt, cả hai đều thất bại có kiểm chứng (xem `eval/test-log.md`, Lượt 10 và Lượt 14). Không nên thử hướng prompt thứ ba.

Việc thật cần làm: cho phép nạp **glossary thuật ngữ của khoá** vào pipeline, để tra thay vì đoán. Đây là thay đổi kiến trúc, tách thành task riêng.

---

## 3. Cách xác minh

Bắt buộc, vì dự án đã một lần báo cáo sai do bỏ qua bước này:

1. `temperature=0` phải đang được set trong payload của `call_ai()` (`eval/run_eval.py`).
2. Chạy **tối thiểu 2 lượt độc lập** cho mỗi thay đổi. Kết quả chỉ được coi là thật khi **tái lập được**. Lịch sử dự án: một lượt từng báo case A3 "PASS lần đầu tiên", đo lại với `temperature=0` thì sai — đó chỉ là may mắn ngẫu nhiên (xem `eval/test-log.md`, Lượt 12 → 13).
3. Sau khi sửa `_is_hit()`, **chạy lại toàn bộ 39 case**, không chỉ 20 case recall. Cần kiểm tra no-flag và case hành vi không bị ảnh hưởng.
4. Ghi số trước/sau vào `eval/test-log.md` cho từng thay đổi riêng lẻ, không gộp nhiều thay đổi vào một lượt đo — nếu gộp thì không biết cái nào có tác dụng.

**Kỳ vọng sau mục 2.1 + 2.2:** recall trên `main` từ 13/20 lên khoảng 16-17/20. Nếu kết quả lệch nhiều so với con số này, dừng lại và kiểm tra xem có nới nhầm chiều ăn may không.

---

## 4. Ràng buộc bắt buộc về tính trung thực

Mọi thay đổi ở đây là **sửa phép đo**, không phải cải thiện năng lực hệ thống. Năng lực model không đổi; chỉ là thôi phạt oan những lần model chỉ đúng chỗ nhưng chỉ gọn hơn ground truth.

Khi cập nhật số vào `spec.md` §7:

- Ghi **cả số cũ lẫn số mới**, kèm lý do đổi cách chấm.
- Ghi rõ đây là thay đổi **sau CP4**, tức sau thời điểm chốt quality bar.
- Không được trình bày con số mới như thể hệ thống đã tốt lên.

Dự án đã mất gần một ngày để phát hiện và đính chính chuỗi số 85-95% bị thổi phồng do lỗi chấm điểm (`eval/test-log.md`, Lượt 8). Báo số cao hơn mà không khai đã nới cách đo sẽ lặp lại đúng sai lầm đó, ở mức nghiêm trọng hơn vì lần này là cố ý.
