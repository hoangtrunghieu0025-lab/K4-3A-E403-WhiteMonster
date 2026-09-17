"""
Bộ chạy đánh giá tự động (Automated Evaluation Runner) - Track C2
Nhóm WhiteMonster · Lớp 3A · Phòng E403
Chạy trên bộ Golden Set 24 cases (lỗi điển hình, ranh giới, và văn bản sạch giảng viên).
"""

import os
import sys
import json
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Đường dẫn thư mục
current_dir = Path(__file__).resolve().parent
repo_dir = current_dir.parent
codebase_dir = repo_dir / "codebase"
sys.path.append(str(codebase_dir))

from qa_agent_ai import analyze_script

def run_evaluation(api_key: str = None):
    golden_file = current_dir / "golden_set.json"
    if not golden_file.exists():
        print(f"Lỗi: Không tìm thấy file {golden_file}")
        return

    with open(golden_file, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    mode_name = "Gemini API (AI thật)" if (api_key or os.environ.get("GEMINI_API_KEY")) else "Heuristic Engine (Mock Baseline)"
    print("=" * 70)
    print(f"  VIETSCRIPT QA — ĐÁNH GIÁ TRÊN BỘ GOLDEN SET ({len(dataset)} CASES)")
    print(f"  Chế độ: {mode_name}")
    print("=" * 70 + "\n")

    error_cases = [c for c in dataset if c["type"] in ["error", "boundary_or_rare"]]
    clean_cases = [c for c in dataset if c["type"] == "clean_transcript"]

    tp = 0 # True Positive: Lỗi thật được phát hiện
    fn = 0 # False Negative: Lỗi thật bị bỏ sót
    fp = 0 # False Positive: Văn bản sạch bị bắt oan (LỖI NẶNG TRONG ĐỀ C2)
    tn = 0 # True Negative: Văn bản sạch không bị bắt lỗi

    detailed_results = []

    print("[*] Đang đánh giá từng case...")
    for item in dataset:
        case_id = item["id"]
        text = item["text"]
        expected_action = item["expected_action"]

        findings = analyze_script(text, api_key=api_key)
        # Loại trừ các finding chỉ là 'giữ nguyên' hoặc 'keep_original'
        actionable_findings = [f for f in findings if f.get("action") not in ["keep_original", "none"]]
        is_flagged = len(actionable_findings) > 0

        passed = False
        if expected_action == "flag_error":
            if is_flagged:
                tp += 1
                passed = True
            else:
                fn += 1
        elif expected_action == "keep_clean":
            if not is_flagged:
                tn += 1
                passed = True
            else:
                fp += 1
                print(f"    [!] CẢNH BÁO FALSE-POSITIVE tại Case #{case_id}: Bắt nhầm câu sạch của giảng viên!")

        detailed_results.append({
            "id": case_id,
            "type": item["type"],
            "difficulty": item.get("difficulty_class", "-"),
            "expected": expected_action,
            "flagged": is_flagged,
            "passed": passed,
            "findings_count": len(actionable_findings)
        })

    total = len(dataset)
    precision = (tp / (tp + fp)) * 100 if (tp + fp) > 0 else 0
    recall = (tp / (tp + fn)) * 100 if (tp + fn) > 0 else 0
    fp_rate = (fp / len(clean_cases)) * 100 if len(clean_cases) > 0 else 0
    overall_acc = ((tp + tn) / total) * 100

    print("\n" + "-" * 70)
    print("KẾT QUẢ ĐO LƯỜNG:")
    print(f"  • Tổng số case thử nghiệm:       {total}")
    print(f"  • Case lỗi thật & ranh giới:     {len(error_cases)}")
    print(f"  • Case văn bản sạch giảng viên:  {len(clean_cases)}")
    print(f"  1. Precision (Độ chính xác):     {tp}/{tp + fp} ({precision:.1f}%)")
    print(f"  2. Recall (Độ bao phủ lỗi):      {tp}/{len(error_cases)} ({recall:.1f}%)")
    print(f"  3. False-Positive Rate:          {fp}/{len(clean_cases)} ({fp_rate:.1f}%)")
    print(f"  4. Tỷ lệ case xử lý chuẩn:       {tp + tn}/{total} ({overall_acc:.1f}%)")
    print("-" * 70)

    # Kiểm tra Quality Bar đã chốt trong spec.md
    passed_quality_bar = (precision >= 80.0) and (fp == 0)
    print("\nĐỐI CHIẾU QUALITY BAR:")
    print("  Tiêu chí: Precision >= 80% VÀ False-Positive Rate trên văn sạch == 0%")
    if passed_quality_bar:
        print("  >>> KẾT QUẢ: [ ĐẠT QUALITY BAR ] <<<")
    else:
        print("  >>> KẾT QUẢ: [ CHƯA ĐẠT QUALITY BAR - CẦN TINH CHỈNH THÊM ] <<<")
    print("=" * 70 + "\n")

    # Lưu kết quả chạy ra file JSON phục vụ bảng kết quả
    run_log = {
        "mode": mode_name,
        "total_cases": total,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "precision_pct": round(precision, 1),
        "recall_pct": round(recall, 1),
        "false_positive_rate_pct": round(fp_rate, 1),
        "overall_accuracy_pct": round(overall_acc, 1),
        "quality_bar_met": passed_quality_bar
    }
    
    log_path = current_dir / "eval_results_run1.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(run_log, f, ensure_ascii=False, indent=2)

    return run_log

if __name__ == "__main__":
    key = sys.argv[1] if len(sys.argv) > 1 else None
    run_evaluation(api_key=key)

