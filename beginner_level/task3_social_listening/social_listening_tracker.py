import csv
import os
from collections import Counter


def analyze_social_mentions(csv_path: str):
    counts = Counter()
    sentiment_counts = Counter()
    mentions_by_cat = {"Praise": [], "Complaints": [], "Questions": [], "Ideas": []}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cat = row["Category"]
            counts[cat] += 1
            sentiment_counts[row["Sentiment"]] += 1
            if cat in mentions_by_cat:
                mentions_by_cat[cat].append(row)

    total_mentions = sum(counts.values())

    print("=" * 65)
    print("      NEXLEVR BRAND SOCIAL LISTENING & MENTIONS TRIAGE")
    print("=" * 65)
    print(f"Monitoring Period: 1 Week (Nov 15 - Nov 21, 2026)")
    print(f"Total Mentions Analyzed: {total_mentions}\n")

    print(f"{'Category':<15} {'Total Mentions':<18} {'Percentage':<12}")
    print("-" * 45)
    for cat in ["Praise", "Complaints", "Questions", "Ideas"]:
        cnt = counts[cat]
        pct = (cnt / total_mentions) * 100 if total_mentions else 0
        print(f"{cat:<15} {cnt:<18} {pct:>6.1f}%")
    print("-" * 45)

    print("\nSentiment Distribution:")
    for sent, c in sentiment_counts.items():
        print(f" - {sent:<10}: {c} mentions ({(c/total_mentions)*100:.1f}%)")

    return counts, sentiment_counts


if __name__ == "__main__":
    csv_file = os.path.join(os.path.dirname(__file__), "social_mentions_dataset.csv")
    analyze_social_mentions(csv_file)
