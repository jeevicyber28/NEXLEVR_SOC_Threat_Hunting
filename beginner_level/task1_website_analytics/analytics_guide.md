# Website Analytics Setup & Key Metrics Telemetry Guide

## Overview
This document provides a comprehensive guide to setting up web analytics, understanding essential web performance metrics, and applying web analytics telemetry within a **Security Operations Center (SOC) & Threat Hunting** context.

---

## 1. Analytics Setup Walkthrough

### Free Implementation Methods
1. **Google Analytics 4 (GA4):**
   - Create a Google Analytics account and configure a new Data Stream for Web.
   - Obtain the Measurement ID (format: `G-XXXXXXXXXX`).
   - Insert the global tracking tag (`gtag.js`) into the `<head>` section of the web application.

2. **Free & Privacy-Preserving Open Source Alternative (Self-Hosted Umami / Minimal Tracker):**
   - Implemented using our lightweight client-side script [`tracker.js`](tracker.js) attached to [`mock_analytics_site.html`](mock_analytics_site.html).
   - Collects session metadata, event timestamps, referrers, and viewport analytics without tracking invasive user cookies.

```html
<!-- Client-Side Analytics Tracker Integration -->
<script src="tracker.js" defer></script>
```

---

## 2. Key Metrics & Definitions

| Metric | Definition | Industry Benchmark | SOC & Threat Hunting Significance |
|---|---|---|---|
| **Total Users** | Total count of unique visitors during the selected date range. | Varies by domain | Sudden 10x surge from single ASN suggests bot crawling or scraping. |
| **New Users** | First-time visitors who have not previously visited the site. | 60% – 80% of total users | Unusually high % of new users with identical User-Agents indicates headless browser automation. |
| **Sessions** | Groups of user interactions within a given time frame (30 min inactivity window). | 1.2 – 1.8 sessions/user | Disproportionate sessions per user indicates scripted session cycling. |
| **Engagement Rate** | Percentage of sessions lasting >10s, with 2+ pageviews or a conversion event. | 55% – 70% | Extremely low engagement (<5%) during high traffic = automated volumetric attack / bot spam. |
| **Bounce Rate** | Inverse of engagement rate; sessions without meaningful interaction. | 30% – 50% | High bounce rates on sensitive endpoints (`/login`, `/checkout`) indicate credential stuffing probes. |
| **Event Count** | Total number of trigger events logged (clicks, scrolls, form submissions). | Varies | Sudden surge in form submission events without matching session time points to spam/injection bots. |
| **Conversions** | Completed actions deemed valuable (signup, checkout, contact). | 2% – 5% | 0% conversion despite massive traffic spike indicates DDoS or brute-force scanning. |
| **Avg. Engagement Time** | Median time the application was in the foreground active state. | 50s – 120s | Sessions of exactly 0.0s – 0.5s are synthetic crawler signatures. |
| **Device Breakdown** | Proportion of traffic across Desktop, Mobile, and Tablet. | ~60% Mobile / 40% Desktop | 100% desktop Linux traffic from non-tech markets points to automated server farms. |
| **Geographic Distribution**| Country and regional origin of visitors. | Depends on target audience | Traffic spikes from countries where the business does not operate signal proxy/VPN attack vectors. |

---

## 3. Threat Hunting & SOC Correlation
In modern enterprise defensive operations, web analytics acts as an early warning sensor:
- **Credential Stuffing Probes:** Elevated bounce rate (>95%) specifically hitting `/api/auth/login` or `/wp-login.php`.
- **DDoS Telemetry:** Traffic volume surges accompanied by near-zero page dwell time and identical HTTP headers.
- **Referrer Spoofing:** Suspicious referrers pointing to malicious domains attempting SEO poisoning or phishing verification.
