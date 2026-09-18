"""Chạy 1 lượt eval độc lập bằng model=gpt-4o, KHÔNG ghi đè eval/evaluation_report.json
(số chính thức hiện tại của nhóm là Lượt 8/9). Kết quả lưu riêng ra file khác để đối chiếu."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.join(os.path.dirname(__file__), ".."))

import run_eval as re_mod

if not re_mod.API_KEY:
    print("KHONG CO API KEY — kiem tra .env (can OPENAI_API_KEY/OPENROUTER_API_KEY/OPENCODE_API_KEY/GEMINI_API_KEY)")
    sys.exit(1)

# Chi goi dung gpt-4o that. Neu key dang route qua OpenCode Go hoac Gemini thi
# khong co gpt-4o that de goi — dung lai thay vi am tham doi model khac.
if "opencode.ai" in re_mod.URL or "generativelanguage.googleapis.com" in re_mod.URL:
    print(f"KHONG THE chay gpt-4o that: key hien co chi route duoc toi {re_mod.URL} (khong phai OpenAI/OpenRouter).")
    print("Can OPENAI_API_KEY (goi thang api.openai.com) hoac OPENROUTER_API_KEY that (sk-or-...) trong .env.")
    sys.exit(1)

if "openrouter.ai" in re_mod.URL:
    model_to_use = "openai/gpt-4o"  # ban goc, khong phai -mini, di qua OpenRouter
else:
    model_to_use = "gpt-4o"  # goi thang api.openai.com

print(f"Dang dung endpoint: {re_mod.URL}")
print(f"Model se goi: {model_to_use}")

report = re_mod.run_eval(model=model_to_use, save_report=False, verbose=True, include_extra=True)

out_path = "eval/evaluation_report.gpt4o-check.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"\nDa luu ket qua rieng vao {out_path} (KHONG dong voi eval/evaluation_report.json chinh thuc)")
print(f"Tom tat: FP={report['metrics']['fp']}/1, Recall={report['metrics']['recall']} ({report['metrics']['recall_pct']}%), Gate drops={report['metrics']['gate_drops']}, No-flag FP={report['metrics']['no_flag_extra_fp']}")
