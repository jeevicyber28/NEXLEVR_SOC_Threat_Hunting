import csv
import os
from collections import Counter


def evaluate_triage_accuracy(csv_path: str):
    total = 0
    matches = 0
    mismatches = []
    error_types = Counter()

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            total += 1
            if r["Agreement_Status"] == "Match":
                matches += 1
            else:
                mismatches.append(r)
                err_category = r["AI_Error_Analysis"].split(":")[0]
                error_types[err_category] += 1

    accuracy_pct = (matches / total) * 100

    print("=" * 70)
    print("      AI-ASSISTED CUSTOMER REVIEW TRIAGE ACCURACY BENCHMARK")
    print("=" * 70)
    print(f"Total Customer Messages Evaluated: {total}")
    print(f"Correct Classifications:           {matches}")
    print(f"Misclassifications / Errors:       {len(mismatches)}")
    print(f"Overall AI Classification Accuracy: {accuracy_pct:.1f}%\n")

    print("Breakdown of AI Misclassification Patterns:")
    print("-" * 55)
    for err, count in error_types.items():
        print(f" - {err:<32}: {count} occurrences")
    print("-" * 55)

    print("\nDetailed Review of AI Mistakes:")
    for m in mismatches:
        print(f"\n[{m['Message_ID']}] Text: \"{m['Customer_Message'][:60]}...\"")
        print(f"   Human Ground Truth : Urgency: {m['Human_Urgency']} | Topic: {m['Human_Topic']}")
        print(f"   AI Model Prediction: Urgency: {m['AI_Urgency']} | Topic: {m['AI_Topic']}")
        print(f"   Analysis: {m['AI_Error_Analysis']}")


if __name__ == "__main__":
    csv_file = os.path.join(os.path.dirname(__file__), "reviews_triage_comparison.csv")
    evaluate_triage_accuracy(csv_file)
