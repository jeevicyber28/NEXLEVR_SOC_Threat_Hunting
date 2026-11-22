# NEXLEVR SOC Alert Engineering: 5 Enterprise Alert Rules

## Alert Philosophy & Design Principles
Alert engineering in a modern SOC requires a balance between **rapid incident detection** and **alert fatigue reduction**. An alert that fires falsely too often desensitizes analysts, increasing Mean Time to Detect (MTTD). Every rule below includes defined trigger conditions, telemetry sources, false alarm analysis, and mitigation strategies.

---

## Alert Rule Specifications

### 1. Alert Rule 1: Sudden Traffic Volume Collapse
- **Rule ID:** `ALERT-RULE-001`
- **Severity Level:** **P1 - Critical**
- **Trigger Condition:** Total website traffic (sessions/minute) drops by $\ge 30\%$ compared to the 14-day rolling hourly baseline for two consecutive 15-minute evaluation windows.
- **Telemetry Source:** Edge CDN / Load Balancer access logs (Cloudflare / AWS CloudWatch).
- **False Alarm Frequency:** ~12% probability of false positive.
- **Common False Alarm Causes:**
  - Regional public holidays (e.g., Thanksgiving, Diwali) causing sharp drops in B2B traffic.
  - Large-scale upstream transit ISP fiber cuts unrelated to our infrastructure.
  - Scheduled maintenance or planned database failovers.
- **Tuning & Mitigation:**
  - Implement day-of-week seasonality weighting.
  - Suppress alerts when the change management flag indicates approved maintenance.

---

### 2. Alert Rule 2: Escalated Negative Sentiment & Brand Crisis
- **Rule ID:** `ALERT-RULE-002`
- **Severity Level:** **P2 - High**
- **Trigger Condition:** A 1-star review or social media post containing critical risk keywords (`breach`, `scam`, `data leak`, `down`, `unauthorized`) published by a user with $>500$ followers or high visibility.
- **Telemetry Source:** Social listening webhooks (X/Twitter streaming API, Reddit RSS, Trustpilot API).
- **False Alarm Frequency:** ~18% probability of false positive.
- **Common False Alarm Causes:**
  - Sarcastic humor, slang, or non-technical usage of words (e.g., "this discount was so good it felt like a scam!").
  - Unrelated brands sharing similar acronyms or domain names.
  - Crypto spam bots mentioning trending hashtags.
- **Tuning & Mitigation:**
  - Require a dual-check: keyword presence AND negative NLP sentiment polarity score ($< -0.6$).
  - Account age filter: ignore accounts created within the last 72 hours with zero followers.

---

### 3. Alert Rule 3: Site Latency & Core Web Vitals Degradation
- **Rule ID:** `ALERT-RULE-003`
- **Severity Level:** **P2 - High**
- **Trigger Condition:** 95th percentile response latency (p95 TTFB) exceeds $2,500\text{ ms}$ for 3 consecutive synthetic check intervals across at least 2 distinct geographical probing locations.
- **Telemetry Source:** Synthetic monitoring probes (UptimeRobot / PageSpeed Insights / Datadog Synthetics).
- **False Alarm Frequency:** ~8% probability of false positive.
- **Common False Alarm Causes:**
  - Localized network congestion at a single synthetic probe datacenter.
  - CDN edge cache cold-starts immediately following a cache purge.
- **Tuning & Mitigation:**
  - Multi-region consensus requirement: require $\ge 2$ independent probe regions to report latency spikes simultaneously before paging on-call engineers.

---

### 4. Alert Rule 4: HTTP 5xx Server Error Rate Spike
- **Rule ID:** `ALERT-RULE-004`
- **Severity Level:** **P1 - Critical**
- **Trigger Condition:** The proportion of HTTP 500, 502, 503, or 504 responses exceeds $5.0\%$ of total incoming HTTP requests over any rolling 5-minute window.
- **Telemetry Source:** Reverse proxy access logs (Nginx / Envoy / AWS ALB).
- **False Alarm Frequency:** ~5% probability of false positive.
- **Common False Alarm Causes:**
  - Low-traffic off-peak hours where a single user triggering 2 errors skews the ratio above 5%.
  - Zero-downtime rolling container redeployments lasting $< 20$ seconds.
- **Tuning & Mitigation:**
  - Minimum sample size guard: Rule only evaluates if total request volume is $\ge 100$ requests within the 5-minute window.

---

### 5. Alert Rule 5: Threat Hunting Credential Stuffing & Brute-Force
- **Rule ID:** `ALERT-RULE-005`
- **Severity Level:** **P1 - Critical**
- **Trigger Condition:** Failed authentication attempts (`HTTP 401/403` on `/api/v1/auth/login`) exceed $50\text{ req/minute}$ originating from a single IP, `/24` CIDR block, or single ASN.
- **Telemetry Source:** Identity Provider (IdP) & Web Application Firewall (WAF) audit stream.
- **False Alarm Frequency:** ~3% probability of false positive.
- **Common False Alarm Causes:**
  - Enterprise corporate office behind a single NAT IP where multiple employees experience password expiration simultaneously.
  - Misconfigured internal automated integration testing scripts running against production.
- **Tuning & Mitigation:**
  - Username entropy evaluation: If requests target $>15$ distinct usernames, flag as malicious bot attack; if all attempts target 1 username, flag as single-user lockout.
