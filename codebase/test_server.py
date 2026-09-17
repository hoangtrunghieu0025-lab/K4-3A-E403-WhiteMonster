"""Chạy: python codebase/test_server.py — không gọi API thật, thay LLM bằng hàm giả."""
import io, wave
import numpy as np
from server import english_spans, pack_chunks, prosody, readback_changes, review, split_sentences

# Tách câu: không cắt "2.5", "45,7%", URL; cắt ở cuối dòng không có dấu câu
s = "Dùng gemini-2.5-flash nhé. Tăng 45,7% tại example.com/a! Dòng không dấu\nCâu cuối"
assert [s[a:b] for a, b in split_sentences(s)] == [
    "Dùng gemini-2.5-flash nhé.", "Tăng 45,7% tại example.com/a!", "Dòng không dấu", "Câu cuối"]

# Chia khối: không cắt ngang đoạn; đoạn dài hơn cỡ khối thì buộc cắt
doc = "A. B. C.\n\nD. E.\n\nF. G. H. I. J."
chunks = pack_chunks(doc, split_sentences(doc), size=4)
assert [doc[a:b] for a, b in chunks] == ["A. B. C.", "D. E.", "F. G. H. I.", "J."], chunks

# Evidence Gate + số câu + cụm lặp lại + trùng lặp
script = "Câu một ổn. Mình nói lại nhé, mình nói lại nhé.\n\nCâu ba có 70% lỗi."
fake = lambda text: [
    {"exact_span": "mình nói lại nhé", "confidence": "HIGH", "minimal_suggestion": "x"},
    {"exact_span": "mình nói lại nhé", "confidence": "HIGH"},   # trùng, không còn chỗ → duplicate
    {"exact_span": "câu bịa không có", "confidence": "HIGH"},   # bịa → Gate loại
    {"exact_span": "70%", "confidence": "LOW", "minimal_suggestion": "bảy mươi phần trăm"},
]
r = review(script, llm=fake)
assert [(script[f["start"]:f["end"]], f["sentence"]) for f in r["findings"]] == [
    ("mình nói lại nhé", 2), ("70%", 3)], r["findings"]
assert r["findings"][1]["suggestion"] == "", "LOW confidence không được có gợi ý tự áp dụng"
assert r["trace"]["dropped"] == 1 and r["trace"]["chunks"][0]["duplicates"] == 1, r["trace"]

# Input rỗng: không gọi LLM
def boom(_): raise AssertionError("không được gọi LLM")
assert review("   \n ", llm=boom)["findings"] == []

# Câu dài không bị gắn cờ được liệt kê là "đã xét" (G2, mining §1)
long = " ".join(["từ"] * 45) + "."
assert review(long, llm=lambda t: [])["long_unflagged"] == [{"sentence": 1, "words": 45}]

# Chữ máy đọc: số/ký hiệu đọc thành chữ, từ bị bỏ; câu đọc đúng từng chữ thì không có khác biệt
written = "Năm 2024, có tới 70% dự án AI thất bại."
spoken = "Năm hai nghìn hai mươi tư có tới bảy mươi phần trăm dự án AI thất bại."
assert [(c["written"], c["spoken"]) for c in readback_changes(written, spoken)] == [
    ("2024", "hai nghìn hai mươi tư"), ("70%", "bảy mươi phần trăm")]
assert all(spoken[c["start"]:c["end"]] == c["spoken"] for c in readback_changes(written, spoken))
assert readback_changes("Sự thay đổi cuộc chơi lớn vào cuối ngày.", "sự thay đổi cuộc chơi lớn vào cuối ngày") == []
assert readback_changes("Dùng GPT-4o nhé.", "Dùng nhé") == [{"written": "GPT-4o", "spoken": "", "start": None, "end": None}]

# Cách đọc: 0,2s lặng | 0,5s 150 Hz | 0,3s ngắt | 1,0s 200 Hz | 0,1s (quá ngắn, không tính) | 0,5s 200 Hz | 0,2s lặng
sr = 22050
tone = lambda hz, s: 0.5 * np.sin(2 * np.pi * hz * np.arange(int(sr * s)) / sr)
gap = lambda s: np.zeros(int(sr * s))
sig = np.concatenate([gap(.2), tone(150, .5), gap(.3), tone(200, 1.0), gap(.1), tone(200, .5), gap(.2)])
buf = io.BytesIO()
with wave.open(buf, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((sig * 32767).astype(np.int16).tobytes())
p = prosody(buf.getvalue(), "một hai ba bốn năm sáu bảy tám")
assert len(p["pauses"]) == 1 and abs((p["pauses"][0][1] - p["pauses"][0][0]) - 0.3) < 0.07, p["pauses"]
assert abs(p["longest_run_s"] - 1.6) < 0.1, p["longest_run_s"]
assert abs(p["pitch_range_st"] - 12 * np.log2(200 / 150)) < 1, p["pitch_range_st"]
assert abs(np.nanmedian([x for x in p["pitch"] if x]) - 200) < 10

# Nhận ra từ tiếng Anh để đọc theo phiên âm Anh; từ Việt không dấu và chữ lẫn số thì giữ giọng Việt
spans = lambda t: [t[a:b] for a, b in english_spans(t)]
assert spans("Bạn click vào nút Submit Form sau đó parse file JSON để extract data ra format chuẩn.") == [
    "click", "Submit Form", "parse file JSON", "extract data", "format"]
assert spans("Chọn mức theo cost-of-error, McKinsey nói 70% dự án AI thất bại.") == ["cost-of-error", "McKinsey", "AI"]
assert spans("Theo dõi kết quả sau khi chạy xong con bot, nhanh thôi, Thanh Nga.") == []
assert spans("Dùng GPT-4o-mini nhé.") == ["GPT", "mini"]

print("OK")
