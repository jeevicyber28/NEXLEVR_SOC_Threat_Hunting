import json
import os
import re
from typing import Any, Dict, List


def evaluate_alert_rules(telemetry_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    metrics = telemetry_data.get("metrics", {})
    fired_alerts = []

    # Rule 1: Traffic Collapse >= 30%
    curr_traffic = metrics.get("traffic_sessions_current", 0)
    base_traffic = metrics.get("traffic_sessions_baseline", 1)
    traffic_drop_pct = ((base_traffic - curr_traffic) / base_traffic) * 100
    if traffic_drop_pct >= 30.0:
        fired_alerts.append({
            "rule_id": "ALERT-RULE-001",
            "name": "Traffic Volume Collapse",
            "severity": "P1 - Critical",
            "evidence": f"Traffic dropped by {traffic_drop_pct:.1f}% below baseline ({curr_traffic} vs {base_traffic} expected)",
            "false_alarm_risk": "12% (Check holidays, maintenance window)"
        })

    # Rule 2: Escalated Negative Sentiment
    rev = metrics.get("social_review", {})
    keywords = ["breach", "scam", "data leak", "down", "unauthorized"]
    has_keyword = any(re.search(rf"\b{k}\b", rev.get("text", ""), re.I) for k in keywords)
    if rev.get("rating", 5) <= 1 and rev.get("author_followers", 0) > 500 and has_keyword:
        fired_alerts.append({
            "rule_id": "ALERT-RULE-002",
            "name": "Negative Sentiment & Brand Crisis",
            "severity": "P2 - High",
            "evidence": f"1-star review by account with {rev.get('author_followers')} followers containing critical risk terms",
            "false_alarm_risk": "18% (Verify sarcasm, brand name collision)"
        })

    # Rule 3: Latency & Core Web Vitals Degradation
    p95 = metrics.get("p95_latency_ms", 0)
    consec = metrics.get("latency_consecutive_breaches", 0)
    if p95 > 2500 and consec >= 3:
        fired_alerts.append({
            "rule_id": "ALERT-RULE-003",
            "name": "Site Latency Degradation (p95)",
            "severity": "P2 - High",
            "evidence": f"p95 latency is {p95}ms exceeding 2500ms threshold for {consec} consecutive checks",
            "false_alarm_risk": "8% (Check single-probe network congestion)"
        })

    # Rule 4: HTTP 5xx Server Error Rate Spike
    total_req = metrics.get("total_requests_5min", 0)
    errors_5xx = metrics.get("http_5xx_count", 0)
    err_rate = (errors_5xx / total_req * 100) if total_req > 0 else 0
    if total_req >= 100 and err_rate >= 5.0:
        fired_alerts.append({
            "rule_id": "ALERT-RULE-004",
            "name": "HTTP 5xx Server Error Rate Spike",
            "severity": "P1 - Critical",
            "evidence": f"5xx error rate at {err_rate:.2f}% ({errors_5xx}/{total_req} requests)",
            "false_alarm_risk": "5% (Check rolling redeployments)"
        })

    # Rule 5: Threat Hunting Credential Stuffing
    failed_logins = metrics.get("failed_logins_per_min", 0)
    target_users = metrics.get("failed_login_target_usernames", 0)
    if failed_logins > 50 and target_users > 15:
        fired_alerts.append({
            "rule_id": "ALERT-RULE-005",
            "name": "Credential Stuffing & Brute Force",
            "severity": "P1 - Critical",
            "evidence": f"{failed_logins} failed auth/min targeting {target_users} unique accounts from IP {metrics.get('source_ip')}",
            "false_alarm_risk": "3% (Corporate proxy password sync issue)"
        })

    return fired_alerts


if __name__ == "__main__":
    sample_file = os.path.join(os.path.dirname(__file__), "sample_telemetry.json")
    with open(sample_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    alerts = evaluate_alert_rules(data)
    print("=" * 70)
    print("         NEXLEVR SOC ALERT ENGINE EVALUATION SUMMARY")
    print("=" * 70)
    print(f"Timestamp: {data.get('timestamp')}")
    print(f"Total Rules Triggered: {len(alerts)}\n")

    for a in alerts:
        print(f"[{a['severity']}] {a['rule_id']}: {a['name']}")
        print(f"  -> Evidence: {a['evidence']}")
        print(f"  -> False Alarm Risk: {a['false_alarm_risk']}\n")
