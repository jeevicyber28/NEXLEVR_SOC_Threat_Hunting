/**
 * NEXLEVR Minimalist Privacy-Preserving Web Analytics Tracker
 * Zero dependencies, cookie-less telemetry capture.
 */

(function () {
    const sessionStart = Date.now();
    const sessionId = "sess_" + Math.random().toString(36).substring(2, 10);

    const telemetry = {
        sessionId: sessionId,
        pageUrl: window.location.href,
        referrer: document.referrer || "direct",
        userAgent: navigator.userAgent,
        screenWidth: window.screen.width,
        screenHeight: window.screen.height,
        language: navigator.language,
        timestamp: new Date().toISOString(),
        events: []
    };

    function logEvent(eventName, eventDetails = {}) {
        const evt = {
            name: eventName,
            timeElapsedSec: ((Date.now() - sessionStart) / 1000).toFixed(2),
            details: eventDetails
        };
        telemetry.events.push(evt);
        console.log(`[NEXLEVR Analytics Event] ${eventName}:`, evt);

        // Update UI logger if present
        const logBox = document.getElementById("analytics-events-log");
        if (logBox) {
            const entry = document.createElement("div");
            entry.className = "log-entry";
            entry.textContent = `[+${evt.timeElapsedSec}s] Event: ${eventName} - ${JSON.stringify(eventDetails)}`;
            logBox.prepend(entry);
        }
    }

    // Pageview on load
    window.addEventListener("DOMContentLoaded", () => {
        logEvent("pageview", { title: document.title });
    });

    // Track user clicks on buttons / links
    document.addEventListener("click", (e) => {
        const target = e.target.closest("button, a");
        if (target) {
            logEvent("click", {
                tag: target.tagName,
                text: target.innerText.trim(),
                href: target.getAttribute("href") || null
            });
        }
    });

    // Track scroll depth
    let maxScroll = 0;
    window.addEventListener("scroll", () => {
        const scrollPercent = Math.round(
            (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
        );
        if (scrollPercent > maxScroll && scrollPercent % 25 === 0) {
            maxScroll = scrollPercent;
            logEvent("scroll_depth", { depthPercent: maxScroll });
        }
    });

    // Track session unload
    window.addEventListener("beforeunload", () => {
        logEvent("session_end", {
            totalDurationSec: ((Date.now() - sessionStart) / 1000).toFixed(2)
        });
    });

    // Expose logger globally for manual telemetry testing
    window.NexlevrTracker = { logEvent, getTelemetry: () => telemetry };
})();
