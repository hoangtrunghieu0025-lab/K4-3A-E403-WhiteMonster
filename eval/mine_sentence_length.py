"""Đo phân bố độ dài câu trong văn nói tự nhiên của giảng viên (transcript bản sạch)
và đối chiếu với văn viết cùng domain (câu trả lời của AI tutor trên VLearn).

Mục đích: lấy số cho `spec.md` §1 — chứng minh rằng luật "câu quá dài = lỗi
breath-group" (một trong 8 nhóm lỗi taxonomy của đề C2) KHÔNG dùng một mình được,
vì văn nói tự nhiên của giảng viên cũng có tỉ lệ lớn câu rất dài.

Không commit data pack vào repo (quy định bảo mật) — script nhận đường dẫn tới
thư mục `data/vlearn-pack/` trên máy người chạy.

Cách chạy:
    python eval/mine_sentence_length.py "<path>/data/vlearn-pack"

Phương pháp đếm (ghi lại để người khác kiểm lại):
  1. Transcript: lấy mọi đoạn có mã [Txx-NNN] trong 6 file transcript-*-clean.md,
     bỏ các đoạn [Hoạt động lớp: ...] vì đó là ghi chú rút gọn, không phải lời giảng.
  2. Tutor: lấy cột tutor_reply của các lượt cohort_hint == "K4", gỡ markdown
     (bullet, bảng, **đậm**, [trang N]) để chỉ còn phần chữ.
  3. Tách câu bằng dấu . ! ? … theo sau là khoảng trắng; bỏ mẩu dưới 3 từ
     (đầu mục, số trang lẻ).
  4. Độ dài câu = số từ tách theo khoảng trắng (tiếng Việt: từ = âm tiết).
"""

import csv
import glob
import re
import sys


def sentences(text):
    text = re.sub(r"\[không nghe rõ\]", " ", text)
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?…])\s+", text)
    return [p.strip() for p in parts if len(p.strip().split()) >= 3]


def strip_markdown(t):
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"[*_`#>|]+", " ", t)
    t = re.sub(r"\[trang \d+\]", " ", t)
    t = re.sub(r"^\s*[-*+]\s+", "", t, flags=re.M)
    return t


def load_transcript(base):
    out = []
    for path in sorted(glob.glob(base + "/transcript/transcript-*-clean.md")):
        raw = open(path, encoding="utf-8").read()
        for code, para in re.findall(r"\*\*\[(T\d+-\d+)\]\*\*(.+?)(?=\n\n|\Z)", raw, flags=re.S):
            if "[Hoạt động lớp" in para:
                continue
            out += [(code, s) for s in sentences(para)]
    return out


def load_tutor(base):
    out = []
    with open(base + "/chatlog/tutor_turns.csv", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["cohort_hint"] != "K4":
                continue
            out += [(row["turn_id"], s) for s in sentences(strip_markdown(row["tutor_reply"]))]
    return out


def pct(values, q):
    return sorted(values)[int(len(values) * q)]


def main(base):
    tr = load_transcript(base)
    tu = load_tutor(base)
    tr_len = [len(s.split()) for _, s in tr]
    tu_len = [len(s.split()) for _, s in tu]

    p95 = pct(tr_len, 0.95)
    over40 = sum(1 for n in tr_len if n > 40)

    print(f"VĂN NÓI (6 transcript giảng viên): {len(tr)} câu")
    print(f"  trung vị {pct(tr_len, 0.5)} từ | p90 {pct(tr_len, 0.90)} | p95 {p95} | dài nhất {max(tr_len)}")
    print(f"  câu > 40 từ: {over40} ({over40 / len(tr_len):.1%})  <-- sẽ bị gắn cờ oan nếu dùng luật độ dài")

    over95 = sum(1 for n in tu_len if n > p95)
    print(f"\nVĂN VIẾT (tutor reply K4): {len(tu)} câu")
    print(f"  trung vị {pct(tu_len, 0.5)} từ | p90 {pct(tu_len, 0.90)}")
    print(f"  câu vượt p95 của văn nói ({p95} từ): {over95} ({over95 / len(tu_len):.1%})")

    print(f"\nVí dụ câu nói dài 60-95 từ nhưng vẫn tự nhiên (dẫn mã đoạn):")
    shown = 0
    for code, s in tr:
        n = len(s.split())
        if 60 <= n <= 95 and shown < 8:
            print(f"  [{code}] {n} từ :: {' '.join(s.split()[:18])} …")
            shown += 1


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit('Dùng: python eval/mine_sentence_length.py "<path>/data/vlearn-pack"')
    main(sys.argv[1].rstrip("/\\"))
