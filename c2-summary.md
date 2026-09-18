# C2 — Tổng hợp nghiên cứu đề · Nhóm WhiteMonster

> **ĐÃ LỖI THỜI (viết 16-17/9, giai đoạn lên ý tưởng).** Kiến trúc mô tả trong file này (10 luật đếm được, cấy lỗi ngược) khác với kiến trúc thật đã xây — xem `spec.md` và `codebase/README.md` để biết bản cuối cùng.
>
> File nội bộ để cả nhóm cùng nắm đề. Không phải deliverable nộp bài — deliverable là `spec.md`.
> **Không copy nội dung `data/studio-pack/` vào file này hay vào repo** (quy định bảo mật: chỉ trích ≤2 câu/ví dụ, dẫn đường dẫn thay vì dán dài).

**Đề đã chốt:** C2 · Vietnamese Spoken-Script QA — agent review kịch bản video tiếng Việt.
Đề gốc: `tracks/track-c-lesson-studio.md` mục C2 (trong repo đề bài `K4-3A-Day05-06-AI-Product-Hackathon`).

---

## 1. Bài toán thật là gì

Kịch bản video bài giảng **đúng ngữ pháp nhưng đọc lên nghe sượng**. Agent phải chỉ đúng span có vấn đề, phân loại, giải thích vì sao, và gợi ý sửa tối thiểu — trước khi chuyển cho người duyệt.

**Đề cấm rõ: không được xây "máy đo xác suất văn AI".** Một từ hay một câu trơn tru không đủ để kết luận. Lỡ dùng nhãn kiểu "đoạn này nghe như AI viết" là vi phạm mục an toàn & đạo đức của đề.

**Việc khó nhất không phải tìm lỗi** — LLM tìm lỗi rất dễ. Việc khó là **không bịa lỗi** trên văn người viết sạch. Báo động giả làm biên tập viên mất niềm tin rồi bỏ công cụ. Nên thứ tự ưu tiên là **precision trước, recall sau** — ngược với trực giác thường thấy.

## 2. Taxonomy lỗi (8 loại, theo đề)

1. Sai nghĩa / sai sắc thái từ
2. Translationese — cú pháp sượng, cấu trúc dịch
3. Câu quá dài / breath-group overload
4. Lặp ý, filler, conclusion residue
5. Register / xưng hô không nhất quán
6. Claim thiếu căn cứ, hoặc chứa chi tiết cụ thể không có nguồn
7. Số, acronym, URL, tên riêng, code-switch khó đọc
8. **Pronunciation-only issue — phải tách khỏi semantic issue**

Mỗi finding cần: exact span · category · severity · giải thích gắn ngữ cảnh · confidence · gợi ý sửa tối thiểu (hoặc "cần người xác minh") · trạng thái accept/reject + audit trail.

## 3. Vốn có sẵn trong data — điểm mạnh nhất của đề này

### 3.1 Sổ luật viết kịch bản (đếm được bằng máy)

`data/studio-pack/c3-scriptscout/mau-kich-ban.md` — giống nhau ở cả ba thư mục c3/c4/c5. Đây **không phải mẫu định dạng, mà là sổ luật của Studio team**. Phần lớn luật kiểm được bằng code, không cần AI:

| # | Luật trong sổ | Kiểm bằng |
|---|---|---|
| 1 | Không có chữ số trong lời đọc — viết "một trăm hai mươi" | regex `\d` |
| 2 | Không viết tắt mà người đọc không đọc thành tiếng (CTA, JSON, v.v.) | regex chữ hoa liền + danh sách |
| 3 | Thuật ngữ tiếng Anh phải có nghĩa tiếng Việt **đặt TRƯỚC**, ở **lần nhắc đầu tiên** | theo dõi first-mention toàn văn |
| 4 | "Trên màn hình" tối đa 40 ký tự | `len()` |
| 5 | `kieu` chỉ có 5 giá trị: `ke` / `giang` / `nhe` / `hoi` / `nhan` | whitelist |
| 6 | Một mục `Lời` là **một câu** — chứa 3 câu là lỗi | tách câu, đếm |
| 7 | Đừng tách mẩu quá ngắn thành cảnh riêng ("Hết.", "Một.") | đếm âm tiết |
| 8 | Không bịa số liệu — màn hình chỉ hiện số/tên có trong kịch bản | so khớp chuỗi |
| 9 | Không viết mốc giờ trong kịch bản | regex timecode |
| 10 | **2,9 âm tiết/giây** — câu 20 tiếng ≈ 7 giây | đếm âm tiết → ra giây |

Luật 10 là chìa khoá: **"câu quá dài" — hạng mục khó nhất — trở thành một phép tính**, không phải cảm tính.

Sổ luật còn ghi thẳng một lỗi **đã xảy ra thật**: *"Đừng để một đoạn dài cùng một kiểu, giọng sẽ đều đều. Đây là lỗi đã gặp thật ở một bộ video trước."* → dùng làm evidence cho §1.

### 3.2 Kịch bản sạch có thẩm quyền

`data/studio-pack/c5-feedbackradar/video-mau/kich-ban-d1.md` — 40 câu, ghi rõ là *kịch bản của một video đã dựng và phát hành thật, dùng để biết một kịch bản đạt chuẩn trông thế nào*.

→ **Studio team tuyên bố nó đạt chuẩn, không phải nhóm tự phong.** Mọi finding hệ thống báo trên 40 câu này đều là **false positive có thẩm quyền**. Đây chính là thứ đề bắt buộc phải có ("≥1 đoạn văn người viết sạch để đo false positive") — và nó có sẵn.

### 3.3 Dữ liệu thời lượng thật để hiệu chỉnh

| File | Có gì |
|---|---|
| `c5-feedbackradar/video-mau/cau-timecode-d1.csv` | 40 câu kèm `batDau`, `ketThucTieng`, `ketThuc`, `soFrame` — thời lượng đọc **thật đo được** |
| `c5-feedbackradar/video-mau/transcript-d1.txt` | cùng lời đó nhưng cắt theo **nhịp lời đọc thật** (câu 1 và câu 3 đều bị cắt làm 2 nhịp) |
| `c4-storyboardai/vi-du/loi-doc-d1-2.json` | video thứ hai, 42 câu, **mốc thời gian từng từ** |

→ Ngưỡng "câu dài bao nhiêu thì sượng" **kiểm chứng được trên số liệu thật**, và có bộ thứ hai để cross-check. Không đề nào khác trong track C cho phép hiệu chỉnh một tiêu chí chất lượng bằng dữ liệu đo được như vậy.

### 3.4 Mô hình chi phí — dùng chung cả cuộc thi

`data/studio-pack/c5-feedbackradar/bang-chi-phi-lam-lai.md`, ghi rõ là mô hình chi phí dùng chung cho cả cuộc thi nên C2 dùng được:

- Quy trình: **kịch bản → thu giọng → dựng hình khớp từng frame theo giọng**.
- Đổi một chữ trong `loi` sau khi đã thu → phải **thu lại giọng + dựng lại cảnh**.
- Máy đọc lấy ngữ điệu từ câu trước và câu sau → **sửa câu 20 phải thu lại câu 19, 20, 21**.
- Trung bình **93 ký tự/câu** (39 câu có lời, tổng 3 637 ký tự).
- Đổi *ý đồ hình* hoặc *chữ trên màn hình* thì rẻ hơn nhiều: không phải thu lại giọng.

→ Một lần sửa lọt xuống sau khi thu ≈ **279 ký tự thu lại + 1 cảnh dựng lại**.

## 4. Problem statement (không chữ AI)

> Một lỗi sượng bắt được **trước khi thu giọng** tốn vài giây của biên tập viên. Đúng lỗi đó lọt xuống sau khi thu tốn khoảng 279 ký tự thu lại giọng và một cảnh dựng lại. C2 là cái chặn ở cửa rẻ; C5 là cái dọn ở cửa đắt.

## 5. Lát cắt MỘT CÂU

> *Một biên tập viên · duyệt một đoạn kịch bản 15–20 câu **trước khi đem đi thu giọng** · AI chỉ đúng span sượng, phân định lỗi nội dung hay lỗi cách đọc, kèm gợi ý sửa tối thiểu và chi phí nếu để lọt · biên tập viên accept/reject từng chỗ, và hệ thống **không báo lỗi nào trên 40 câu kịch bản d1 đã phát hành**.*

Vế cuối là quality bar tự nó, và là vế khiến bài khác hẳn "LLM đọc rồi chê".

## 6. Kiến trúc — bản lười nhất còn đúng

```
kịch bản (.md/.json theo mẫu chung)
  │
  ├─ tầng 1 · LUẬT ĐẾM ĐƯỢC (10 luật mục 3.1)
  │     → finding có số, precision ~100%, không cần AI
  │
  ├─ tầng 2 · MỘT LỜI GỌI LLM cho những gì luật không kiểm được:
  │     · sai sắc thái   · translationese   · lặp ý giữa các câu xa nhau
  │     · xưng hô/register lệch   · claim có chi tiết cụ thể không nguồn
  │     · PHÂN ĐỊNH "lỗi nội dung" vs "chỉ là lỗi cách đọc"   ← quyết định trung tâm
  │     · gợi ý sửa tối thiểu, giữ giọng tác giả               ← quyết định trung tâm
  │
  ├─ CỔNG BẰNG CHỨNG: finding nào không nêu được tên luật hoặc một con số → nuốt đi
  ├─ HẠN MỨC: tối đa ~5 finding / 20 câu, xếp theo chi phí nếu để lọt
  │
  └─ bảng duyệt accept/reject → append vào log (audit trail)
```

**Chưa làm (và vì sao):** fine-tune classifier riêng · TTS thật để nghe thử · style-profile theo từng giảng viên · active learning từ accept/reject. Cả bốn đều là **bonus** của đề — thêm khi bản lõi đã đạt quality bar.

### Cái bẫy R5 phải để ý

Nếu tầng luật làm gần hết việc thì **lời gọi AI không còn ở quyết định trung tâm**, R5 (3 điểm) lung lay và giám khảo sẽ hỏi "vậy AI làm gì?". Cách chống: khai lát cắt sao cho quyết định AI là **phân định nội dung vs cách đọc** và **gợi ý sửa tối thiểu** — hai việc rule không làm được. Tầng luật chỉ là tiền xử lý.

## 7. Ba rủi ro và cách xử lý

### 7.1 Nhãn không đáng tin → cấy lỗi ngược từ bản sạch

Vấn đề gốc: nhóm tự quyết định câu nào sượng rồi tự đo xem máy có tìm ra không → **vòng luẩn quẩn**, giám khảo thấy ngay.

Cách thoát: **đừng gán nhãn cho câu có sẵn — tự cấy lỗi vào câu sạch.** Khi mình là người cấy, mình biết chính xác span nào, loại gì, không phải phán xét gì. Thẩm quyền của nhãn đến từ hai nguồn ngoài nhóm: **kịch bản d1 Studio đã công nhận sạch** + **sổ luật Studio viết ra**.

| Loại lỗi | Cấy thế nào | Ground truth từ đâu |
|---|---|---|
| Số chưa chuẩn hoá | "một trăm hai mươi" → "120" | Luật 1 |
| Viết tắt khó đọc | "mô hình ngôn ngữ lớn" → "LLM" | Luật 2 |
| Thuật ngữ thiếu nghĩa | bỏ cụm nghĩa tiếng Việt ở lần nhắc đầu | Luật 3 |
| Câu quá dài | nối câu 12 + 13 thành một `Lời` | Luật 10 + nhịp cắt thật trong `transcript-d1.txt` |
| Mẩu quá ngắn | tách một câu chốt thành hai mẩu | Luật 7 |
| **Translationese** | **dịch vòng câu sạch: Việt → Anh → Việt bằng máy** | câu đó **là văn dịch máy theo đúng nghĩa đen** |
| Lặp ý | nhân bản ý câu 9 vào câu 15, diễn đạt khác | biết mình vừa nhân bản |
| Xưng hô lệch | "mình" → "chúng tôi" ở đúng một câu | cả kịch bản dùng "mình"/"bạn" nhất quán |
| Claim vô căn cứ | chèn "giảm bốn mươi phần trăm" vào câu vốn không có số | Luật 8 |
| Kiểu đọc sai | `kieu: "vui"` | Luật 5 |

**Lợi ích kép:** recall đo trên bản đã cấy (biết có đúng K lỗi) · false positive đo trên 40 câu nguyên bản (mọi finding ở đây đều là báo động giả, không cần ai phán xử).

**Giới hạn phải khai thẳng trong spec:** cấy lỗi đo được "máy có bắt được lỗi **đã biết**", **không** đo được "máy có bắt được lỗi nhóm chưa nghĩ ra". Recall thật ngoài đời sẽ thấp hơn số báo cáo.

### 7.2 Báo lỗi quá tay → chặn bằng cấu trúc, không bằng lời dặn

Bảo LLM "hãy dè dặt" không ổn định. Ba biện pháp cấu trúc:

- **Cổng bằng chứng** — finding chỉ hiện nếu nêu được tên luật bị vi phạm **hoặc** một con số đo được. "Nghe sượng" trống trơn → nuốt đi.
- **Hạn mức chú ý** — tối đa ~5 finding/20 câu, xếp theo chi phí. Kịch bản đến từ người viết chuyên nghiệp: báo 15 lỗi trên 20 câu thì gần như chắc là máy sai. Ép hạn mức là ép **xếp hạng**, và xếp hạng đúng mới là giá trị sản phẩm.
- **Quality bar bất đối xứng, chốt tại CP4** — ví dụ *"≤2 false positive trên 40 câu sạch"* **và** *"≥60% recall trên bộ đã cấy"*. Nói rõ vì sao bất đối xứng: báo động giả làm mất niềm tin rồi bỏ công cụ, còn sót lỗi thì vẫn còn vòng người duyệt phía sau.

### 7.3 Không có biên tập viên duyệt nhãn → ba cách chứng minh "thực sự giúp"

**a. A/B trên bạn cùng lớp — đo người, không đo máy.** 20 câu có cấy sẵn K lỗi đã biết. 3 bạn làm không có công cụ, 2 bạn có. Đo: tìm ra mấy/K lỗi, mất bao lâu. Không cần ai là chuyên gia vì đáp án khách quan. **Ăn hai khối điểm bằng một hoạt động**: vừa là R6 (≥5 người ngoài nhóm), vừa là bằng chứng "có giúp". Kết quả ngược (nhóm có công cụ chậm hơn vì mải đọc finding) vẫn đủ điểm R6 và còn hay hơn để kể.

**b. Đọc to.** Tiền đề cả đề là "đúng ngữ pháp nhưng khó nghe" → phép thử cuối cùng là đọc lên thành tiếng. Ghi lại câu nào vấp, câu nào phải lấy hơi giữa chừng. Đối chiếu với finding loại "câu quá dài". Không cần chuyên môn, chỉ cần một cái miệng và một cái tai. Mốc tham chiếu: `transcript-d1.txt`.

**c. Đồng thuận hai người ngoài nhóm.** Rubric R4 ghi thẳng *"người ngoài nhóm chấm ra cùng kết quả"* (4 điểm). 20 finding, 2 bạn chấm độc lập đồng ý/không, báo % đồng thuận. Đồng thuận thấp cũng **đủ điểm nếu báo số thật** + phân tích loại nào hay lệch.

**Nếu gặp được biên tập viên/lab coach:** đừng xin chấm 100 case (không kịp, họ sẽ từ chối). Xin đúng hai thứ trong 15 phút: (1) **10 finding, accept/reject** → bộ hiệu chỉnh + quote cho R1; (2) *"lỗi nào để lọt thì tốn nhất?"* → xác nhận thang severity. Track C ghi rõ user gồm cả **lab coach/giảng viên** — họ có mặt ngay tại lớp.

## 8. Chuẩn evidence riêng của track C

Nhẹ hơn các track khác: **phỏng vấn ≥3 người Studio team và/hoặc lab coach** theo Mom Test, có log nguyên văn; **và/hoặc** mining tài liệu thật với số đếm + ví dụ. **Không cần khảo sát 20 người.** BTC bố trí đầu mối — hỏi ở kênh chung.

## 9. Ánh xạ rubric

| Khối | Điểm | Ăn bằng gì |
|---|---|---|
| R1 · Bằng chứng & impact | 15 | Quote phỏng vấn + lỗi đã ghi trong sổ luật + bảng impact quy ra chi phí thu lại (mục 3.4) |
| R2 · Lát cắt & thiết kế | 15 | Lát cắt mục 5 · non-goals (không rewrite toàn văn, không gắn nhãn "văn AI", không thêm claim mới) · automation = accept/reject vì cost-of-error cao · ≥4 nguyên tắc HAX/PAIR trỏ vào vị trí cụ thể |
| R3 · Chỗ khó & kịch bản | 11 | ① false positive trên câu sạch · ② hai người chấm khác nhau → cần confidence · ③ không được tự sửa hộ · ④ lỗi đọc số/acronym sai → sai kiến thức trên video giáo dục |
| R4 · Kiểm thử | 15 | Golden set từ bộ cấy lỗi + 40 câu sạch làm case "không lỗi" (≥10 case từ nguồn thật) · quality bar bất đối xứng · bảng kết quả 2 chiều recall/FP |
| R5 · Prototype | 8 | 1 lời gọi LLM ở phân định nội dung-vs-cách đọc; phần regex khai rõ là rule |
| R6 · Validation | +8 | A/B mục 7.3a |
| R7 · Repo | 3 | cấu trúc chuẩn + README có phân công tên người |

## 10. Ranh giới — để không nói quá

Bộ cách trên chứng minh được: hệ thống bắt được lỗi vi phạm luật đã công bố · không báo bừa trên văn bản chuyên nghiệp · giúp người không chuyên tìm lỗi nhanh hơn.

**Không** chứng minh được: bắt được những lỗi tinh tế mà chỉ biên tập viên lâu năm nhận ra. Khai thẳng trong `spec.md` §8 — giám khảo sẽ hỏi, và nhóm nào trả lời được ranh giới của chính mình thì thắng phần Q&A.

## 11. Việc còn treo

- [ ] Sửa `README.md` + `spec.md` từ B2 sang C2 (§1, §2, §4 phải viết lại — evidence B2 không chuyển sang được)
- [ ] Hẹn phỏng vấn Studio team / lab coach — **làm sớm**, đừng để tới CP4
- [ ] Viết script cấy lỗi + bộ 10 luật đếm được
- [ ] Chốt quality bar bằng số trước 21:00 17/9 (CP4)
- [ ] Tạo `codebase/`, `validation/`, `reflection/`
