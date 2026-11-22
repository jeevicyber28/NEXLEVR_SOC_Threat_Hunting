# Brand Social Listening & Intelligence Report

## Brand Monitored: NEXLEVR Cloud Security
**Monitoring Window:** 7-Day Window (Nov 15 – Nov 21, 2026)  
**Platforms Monitored:** Twitter/X, Reddit, LinkedIn, Trustpilot, G2

---

## 1. Executive Summary & Category Totals

Over the 7-day observation period, **25 cross-platform mentions** were captured, categorized, and analyzed.

| Category | Total Mentions | Share (%) | Primary Focus / Themes |
|---|---|---|---|
| **Praise** | 9 | 36.0% | Fast incident response, reliable threat detection, responsive support, UI speed. |
| **Complaints** | 5 | 20.0% | EU cluster latency (504 errors), MFA lockouts, billing transparency, mobile UI lag. |
| **Questions** | 6 | 24.0% | Compliance exports (ISO 27001), PCAP log retention, GDPR IP anonymization. |
| **Ideas** | 5 | 20.0% | Slack webhook integrations, SIEM integrations (Splunk/Elastic), community Sigma rules. |
| **Total** | **25** | **100.0%** | Overall Brand Net Sentiment: **68% Positive**, 20% Neutral, 12% Negative |

---

## 2. Threat Hunting & Operational Early Warning Signals
Social listening serves as an external telemetry feed for SOC analysts:
- **Outage Detection Ahead of PagerDuty:** Mention `MNT-102` on Reddit reported EU-Central cluster gateway timeouts 12 minutes before internal synthetic monitoring triggered an alert.
- **Account Takeover / Support Risk:** Mention `MNT-113` identified an MFA lockout escalation on Trustpilot, highlighting a bottleneck in identity verification turnaround time.
- **Vulnerability/Bug Intelligence:** Mention `MNT-109` uncovered a report export bug on Firefox that was not caught during Chrome-only regression testing.
