"""A/B nhiều model trên cùng golden set + cùng SYSTEM_PROMPT (lượt 6, sau few-shot #4).
Chạy: python -u eval/run_model_ab.py   (flag -u để thấy log ngay, tránh buffer khi chạy nền)
Cần OPENAI_API_KEY trong .env. Model nào tài khoản không truy cập được sẽ bị bỏ qua,
ghi rõ lỗi trong báo cáo thay vì làm hỏng cả lượt so sánh.

Chỉ đo FP (clean_script) + Recall (flawed_cases) + Gate Drops — bỏ no_flag_cases và
case hành vi (include_extra=False) để giảm ~19 lời gọi/model, tránh cháy TPM tier thấp
khi nhân với 4 model. Bộ no_flag/case hành vi đã có kết quả đầy đủ cho gpt-4o ở
eval/evaluation_report.json (lượt 6), không cần lặp lại cho từng model ở đây.
"""
import json
import sys
from run_eval import run_eval

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

# Từ rẻ nhất đến đắt nhất, trải 2 thế hệ model của OpenAI.
# LƯU Ý (lượt 7, xem eval/test-log.md): gpt-5-mini và gpt-5 treo tái lập được (3/3 lần)
# đúng ở bước FP trên clean_script (~40 câu) trong môi trường build lúc đó — không phải
# lỗi model (câu đơn vẫn phản hồi bình thường 15-33s), nghi do OpenAI gửi keep-alive
# trong lúc suy luận dài khiến timeout của `requests` không kích hoạt. Nếu môi trường
# mạng ổn định hơn thì chạy lại bình thường được — không cần sửa gì thêm ở đây trước.
MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-5-mini", "gpt-5"]

# Model nào đã có kết quả "ok" trong eval/model_ab_report.json từ lượt trước thì bỏ qua,
# không tốn lời gọi API lại — chỉ chạy lại các model bị lỗi mạng/rate-limit lượt trước.
def _load_previous_ok():
    try:
        with open("eval/model_ab_report.json", "r", encoding="utf-8") as f:
            prev = json.load(f)
        return {r["model"]: r for r in prev.get("results", []) if r.get("ok")}
    except FileNotFoundError:
        return {}


def run_ab():
    previous_ok = _load_previous_ok()
    results = []
    for model in MODELS:
        if model in previous_ok:
            print(f"\n########## MODEL: {model} — đã có kết quả lượt trước, bỏ qua ##########", flush=True)
            results.append(previous_ok[model])
            continue
        print(f"\n########## MODEL: {model} ##########", flush=True)
        try:
            report = run_eval(model=model, save_report=False, verbose=True, include_extra=False)
            results.append({"model": model, "ok": True, **report["metrics"]})
        except Exception as e:
            print(f"   !! Bỏ qua {model}: {e}", flush=True)
            results.append({"model": model, "ok": False, "error": str(e)})

        # Ghi tạm sau mỗi model — lỡ bị ngắt giữa chừng vẫn còn kết quả các model đã xong.
        with open("eval/model_ab_report.json", "w", encoding="utf-8") as f:
            json.dump({"models": MODELS, "results": results}, f, ensure_ascii=False, indent=2)

    print("\n\n=== BẢNG SO SÁNH A/B (FP + Recall + Gate Drops) ===", flush=True)
    header = "| Model | Recall | FP (clean) | Gate Drops |\n|---|---|---|---|\n"
    rows = ""
    for r in results:
        if not r["ok"]:
            rows += f"| {r['model']} | LỖI: {r.get('error','?')[:80]} | - | - |\n"
            continue
        rows += f"| {r['model']} | {r['recall']} ({r['recall_pct']}%) | {r['fp']}/1 | {r['gate_drops']} |\n"
    print(header + rows, flush=True)

    with open("eval/model_ab_report.json", "w", encoding="utf-8") as f:
        json.dump({"models": MODELS, "results": results, "table": header + rows}, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    run_ab()
