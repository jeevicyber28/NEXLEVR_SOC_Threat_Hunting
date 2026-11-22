import csv
import math
import os


def analyze_traffic(dataset_path: str):
    rows = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "date": r["Date"],
                "sessions": int(r["Sessions"]),
                "users": int(r["Users"]),
                "pageviews": int(r["Pageviews"]),
                "bounce_rate": float(r["Bounce_Rate_Pct"]),
                "duration": float(r["Avg_Duration_Sec"]),
                "error_rate": float(r["Error_5xx_Pct"]),
                "bot_score": float(r["Bot_Probability_Score"])
            })

    session_counts = [r["sessions"] for r in rows]
    # Filter non-outlier baseline (excluding top/bottom 10%)
    sorted_sessions = sorted(session_counts)
    trimmed_baseline = sorted_sessions[3:-3]
    baseline_mean = sum(trimmed_baseline) / len(trimmed_baseline)

    mean_sessions = sum(session_counts) / len(session_counts)
    std_dev = math.sqrt(sum((x - mean_sessions) ** 2 for x in session_counts) / len(session_counts))

    print(f"Traffic Baseline (Standard Rolling Mean): {baseline_mean:.1f} sessions/day")
    print("-" * 75)

    anomalies = []
    for r in rows:
        diff_pct = ((r["sessions"] - baseline_mean) / baseline_mean) * 100
        z_score = (r["sessions"] - mean_sessions) / std_dev
        if abs(diff_pct) >= 70.0:
            anomalies.append((r, z_score, diff_pct))

    return anomalies, baseline_mean


if __name__ == "__main__":
    csv_file = os.path.join(os.path.dirname(__file__), "sample_traffic_dataset.csv")
    anomalies, baseline = analyze_traffic(csv_file)
    print(f"Identified {len(anomalies)} Critical Traffic Anomalies (|Variance| >= 70%):\n")
    for a, z, diff in anomalies:
        direction = "SPIKE" if diff > 0 else "DROP"
        print(f"[{a['date']}] {direction} ({diff:+.1f}% vs baseline | Z-Score: {z:+.2f})")
        print(f"   Sessions: {a['sessions']} | Bounce Rate: {a['bounce_rate']}% | Avg Duration: {a['duration']}s | Error: {a['error_rate']}%\n")
