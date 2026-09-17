"""Đo lại CHỈ no_flag_cases + case hành vi (bỏ qua FP/Recall đã có số ở lượt 8) —
tránh phải chạy lại 21 lời gọi flawed_cases/clean_script không cần thiết.
Ghi đè đúng 3 field liên quan trong eval/evaluation_report.json, giữ nguyên fp/recall/gate_drops.
Chạy: python -u eval/run_extras_only.py
"""
import json
import sys
from run_eval import call_ai, _valid_span, MODEL

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

import time

def _call(text):
    result = call_ai(text)
    time.sleep(1)
    return result

def main():
    with open("eval/golden_set.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"=== ĐO LẠI no_flag_cases + case hành vi (MODEL: {MODEL}) ===\n", flush=True)

    no_flag_cases = data.get("no_flag_cases", [])
    no_flag_table = "| ID | Nguồn | Finding hợp lệ | Trạng thái |\n|---|---|---|---|\n"
    no_flag_fp = 0
    print(f"1. no_flag_cases ({len(no_flag_cases)} case):", flush=True)
    for case in no_flag_cases:
        text = case["text"]
        if not text.strip():
            no_flag_table += f"| {case['id']} | {case.get('source','-')} | 0 (input rỗng, bỏ qua gọi AI) | ✅ PASS |\n"
            print(f"   - {case['id']}: ✅ PASS (rỗng)", flush=True)
            continue
        findings = _call(text)
        valid = [f for f in findings if _valid_span(f.get("exact_span", ""), text)]
        no_flag_fp += len(valid)
        status = "✅ PASS" if not valid else "❌ FAIL"
        no_flag_table += f"| {case['id']} | {case.get('source','-')} | {len(valid)} | {status} |\n"
        print(f"   - {case['id']}: {status} ({len(valid)} finding)", flush=True)

    def manual_table(cases, label, text_key="text", expect_key="expected_behavior"):
        rows = f"### {label}\n\n| ID | Kỳ vọng | Output AI thô |\n|---|---|---|\n"
        print(f"\n{label} ({len(cases)} case):", flush=True)
        for case in cases:
            text = case.get(text_key) or case.get("scenario", "")
            expected = case.get(expect_key, "-")
            if not text.strip():
                raw = "(input rỗng, không gọi AI)"
            else:
                raw = json.dumps(_call(text), ensure_ascii=False)
            print(f"   - {case['id']}: xong", flush=True)
            rows += f"| {case['id']} | {expected} | `{raw}` |\n"
        return rows

    manual_tables = "\n\n".join([
        manual_table(data.get("scope_refusal_cases", []), "scope_refusal_cases (lớp ③, đã có sẵn)"),
        manual_table(data.get("ambiguous_low_confidence_cases", []), "ambiguous_low_confidence_cases (lớp ②)"),
        manual_table(data.get("security_refusal_cases", []), "security_refusal_cases (lớp ③ + bảo mật)"),
        manual_table(data.get("edge_format_cases", []), "edge_format_cases"),
    ])

    print(f"\nno_flag_extra_fp: {no_flag_fp}/{len(no_flag_cases)}", flush=True)

    with open("eval/evaluation_report.json", "r", encoding="utf-8") as f:
        report = json.load(f)
    report["metrics"]["no_flag_extra_fp"] = f"{no_flag_fp}/{len(no_flag_cases)}"
    report["no_flag_table"] = no_flag_table
    report["manual_review_tables"] = manual_tables
    report.pop("note_lot8", None)
    report["note_lot9"] = "no_flag_cases + case hành vi đo lại lượt 9 với logic chấm đã sửa (_valid_span). fp/recall/gate_drops vẫn là số lượt 8 (đã đo, không đo lại)."
    with open("eval/evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("\nĐã ghi vào eval/evaluation_report.json", flush=True)

if __name__ == "__main__":
    main()
