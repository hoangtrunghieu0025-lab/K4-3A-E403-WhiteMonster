"""Đếm câu hỏi của học viên chưa có phản hồi trong `data/discord-pack/k4_messages.csv`.

Dùng để kiểm lại con số trong canvas.md / spec.md §1-§2 — không commit data pack
vào repo này (theo quy định bảo mật của khoá), nên script tự tìm file ở
đường dẫn tương đối tới repo đề bài trên máy người chạy.

Cách chạy:
    python evidence/mining_unanswered_questions.py <đường dẫn tới k4_messages.csv>

Phương pháp đếm (ghi lại để đối chiếu):
  1. Lấy các tin có is_bot == False  → "tin của học viên".
  2. Trong đó, tin có ký tự "?" trong content → coi là "câu hỏi".
  3. Gom toàn bộ giá trị cột reply_to (của mọi tin, kể cả tin bot) thành tập
     "đã được trả lời" (một tin có id nằm trong tập này nghĩa là có ít nhất
     một tin khác reply lại nó).
  4. Câu hỏi có msg_id KHÔNG nằm trong tập trên → "chưa có phản hồi trong pack".
"""

import csv
import sys


def main(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    human = [r for r in rows if r["is_bot"] == "False"]
    questions = [r for r in human if "?" in r["content"]]
    replied_to_ids = {r["reply_to"] for r in rows if r["reply_to"]}
    unanswered = [r for r in questions if r["msg_id"] not in replied_to_ids]

    print(f"Tổng số tin: {len(rows)}")
    print(f"Tin của học viên (is_bot=False): {len(human)}")
    print(f"Câu hỏi (chứa dấu '?'): {len(questions)}")
    print(
        f"Câu hỏi chưa có phản hồi trong pack: {len(unanswered)}"
        f" ({len(unanswered) / len(questions):.1%})"
    )
    print()
    print("msg_id, created_at_vn, channel -- ví dụ chưa có phản hồi:")
    for r in unanswered[:10]:
        snippet = r["content"].replace("\n", " ")[:120]
        print(f"  {r['msg_id']} {r['created_at_vn']} {r['channel']} :: {snippet}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Dùng: python mining_unanswered_questions.py <path/to/k4_messages.csv>")
    main(sys.argv[1])
