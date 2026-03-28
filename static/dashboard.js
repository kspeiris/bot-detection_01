let dashboardState = null;

function scoreBadge(score) {
    if (score >= 0.85) {
        return "critical";
    }
    if (score >= 0.5) {
        return "warning";
    }
    return "safe";
}

function formatLabel(label) {
    return String(label || "n/a")
        .replaceAll("_", " ")
        .replace(/\b\w/g, function (match) { return match.toUpperCase(); });
}

function formatTimestamp(epochSeconds) {
    if (!epochSeconds) {
        return "Not available";
    }
    return new Date(epochSeconds * 1000).toLocaleString();
}

function renderSummary(summary) {
    const cards = [
        ["Total Sessions", summary.total_sessions],
        ["Human Sessions", summary.human_sessions],
        ["Bot Sessions", summary.bot_sessions],
        ["Coordinated Groups", summary.coordinated_groups],
        ["Window Rows", summary.window_rows]
    ];

    document.getElementById("summaryCards").innerHTML = cards.map(function ([label, value]) {
        return `<div class="stat-card"><span>${label}</span><strong>${value}</strong></div>`;
    }).join("");
}

function renderPosture(posture, summary) {
    const container = document.getElementById("postureCard");
    const tone = posture.level === "High Alert" ? "critical" : posture.level === "Elevated" ? "warning" : "safe";
    container.innerHTML = `
        <div class="posture-head">
            <div>
                <p class="eyebrow">Detection Posture</p>
                <h3>${posture.level}</h3>
                <p class="lead">${posture.detail}</p>
            </div>
            <span class="posture-pill ${tone}">${posture.level}</span>
        </div>
        <div class="posture-grid">
            <div class="mini-metric">
                <span>Critical Sessions</span>
                <strong>${posture.critical_sessions}</strong>
            </div>
            <div class="mini-metric">
                <span>Watch Sessions</span>
                <strong>${posture.watch_sessions}</strong>
            </div>
            <div class="mini-metric">
                <span>Coordinated Groups</span>
                <strong>${summary.coordinated_groups}</strong>
            </div>
        </div>
    `;
}

function renderFeatureSummary(featureSummary) {
    const container = document.getElementById("featureSummary");
    const entries = Object.entries(featureSummary || {});
    if (!entries.length) {
        container.innerHTML = "<p>No feature summary available yet.</p>";
        return;
    }
    container.innerHTML = entries.map(function ([label, value]) {
        return `<div class="metric-row"><span>${formatLabel(label)}</span><strong>${value}</strong></div>`;
    }).join("");
}

function renderModelHealth(modelMetrics) {
    const container = document.getElementById("modelHealth");
    const session = modelMetrics.session || {};
    const windowed = modelMetrics.window || {};

    container.innerHTML = `
        <div class="model-card">
            <div class="model-head">
                <strong>Session Classifier</strong>
                <span>${session.dataset_rows || 0} rows</span>
            </div>
            <div class="metric-row"><span>Status</span><strong>${formatLabel(session.status || "unavailable")}</strong></div>
            <div class="metric-row"><span>Logistic Accuracy</span><strong>${session.logistic_accuracy ?? "n/a"}</strong></div>
            <div class="metric-row"><span>Random Forest Accuracy</span><strong>${session.random_forest_accuracy ?? "n/a"}</strong></div>
            <div class="metric-row"><span>XGBoost Accuracy</span><strong>${session.xgboost_accuracy ?? "n/a"}</strong></div>
            <p class="muted">${session.message || "No session model metrics available."}</p>
        </div>
        <div class="model-card">
            <div class="model-head">
                <strong>Window Classifier</strong>
                <span>${windowed.dataset_rows || 0} rows</span>
            </div>
            <div class="metric-row"><span>Status</span><strong>${formatLabel(windowed.status || "unavailable")}</strong></div>
            <div class="metric-row"><span>Logistic Accuracy</span><strong>${windowed.logistic_accuracy ?? "n/a"}</strong></div>
            <div class="metric-row"><span>Random Forest Accuracy</span><strong>${windowed.random_forest_accuracy ?? "n/a"}</strong></div>
            <div class="metric-row"><span>Held-Out Sessions</span><strong>${(windowed.held_out_sessions || []).length}</strong></div>
            <p class="muted">${windowed.message || "No window model metrics available."}</p>
        </div>
    `;
}

function renderDataStatus(dataStatus) {
    const container = document.getElementById("dataStatus");
    const rows = [
        ["Raw Events", dataStatus.events_updated_at],
        ["Session Features", dataStatus.features_updated_at],
        ["Window Features", dataStatus.window_features_updated_at]
    ];

    container.innerHTML = rows.map(function ([label, value]) {
        return `<div class="metric-row"><span>${label}</span><strong>${formatTimestamp(value)}</strong></div>`;
    }).join("");
}

function renderGroups(groups) {
    const container = document.getElementById("groupAlerts");
    if (!groups.length) {
        container.innerHTML = "<p>No coordinated groups flagged in the current dataset.</p>";
        return;
    }
    container.innerHTML = groups.map(function (group) {
        const members = group.members.map(function (member) {
            return `<li>${member.session_id.slice(0, 8)}... <span>${member.bot_type}</span></li>`;
        }).join("");
        return `
            <div class="alert-card">
                <div class="alert-head">
                    <strong>Group ${group.group_id}</strong>
                    <span class="pill bot">sim ${group.similarity}</span>
                </div>
                <p>${group.pair_count} suspicious pair links in the same coordination cluster.</p>
                <ul class="clean-list">${members}</ul>
            </div>
        `;
    }).join("");
}

function distributionMarkup(entries) {
    if (!entries.length) {
        return "<p>No distribution data available.</p>";
    }

    const max = Math.max(...entries.map(function (entry) { return entry.value; }), 1);
    return entries.map(function (entry) {
        const width = (entry.value / max) * 100;
        return `
            <div class="chart-row">
                <div class="chart-label">
                    <span>${entry.label}</span>
                    <strong>${entry.value}</strong>
                </div>
                <div class="bar-track">
                    <div class="bar-fill ${entry.tone || ""}" style="width:${width}%"></div>
                </div>
            </div>
        `;
    }).join("");
}

function renderDistributions(sessions) {
    const byType = {};
    const riskBands = { Safe: 0, Watch: 0, Critical: 0 };

    sessions.forEach(function (session) {
        const key = session.bot_type || session.actor_type;
        byType[key] = (byType[key] || 0) + 1;
        if (session.final_risk >= 0.85) {
            riskBands.Critical += 1;
        } else if (session.final_risk >= 0.5) {
            riskBands.Watch += 1;
        } else {
            riskBands.Safe += 1;
        }
    });

    document.getElementById("distributionChart").innerHTML = distributionMarkup(
        Object.entries(byType).map(function ([label, value]) {
            return { label: formatLabel(label), value: value, tone: label === "none" ? "safe" : "critical" };
        })
    );

    document.getElementById("riskChart").innerHTML = distributionMarkup(
        [
            { label: "Safe", value: riskBands.Safe, tone: "safe" },
            { label: "Watch", value: riskBands.Watch, tone: "warning" },
            { label: "Critical", value: riskBands.Critical, tone: "critical" }
        ]
    );
}

function getFilteredSessions() {
    const sessions = dashboardState ? dashboardState.sessions.slice() : [];
    const filter = document.getElementById("sessionFilter");
    const search = document.getElementById("sessionSearch");
    const sort = document.getElementById("sessionSort");
    const selected = filter ? filter.value : "all";
    const term = search ? search.value.trim().toLowerCase() : "";
    const sortKey = sort ? sort.value : "risk_desc";

    const filtered = sessions.filter(function (session) {
        if (selected === "human" && session.actor_type !== "human") {
            return false;
        }
        if (selected === "bot" && session.actor_type !== "bot") {
            return false;
        }
        if (selected === "high-risk" && session.final_risk < 0.85) {
            return false;
        }
        if (!term) {
            return true;
        }
        const haystack = [
            session.session_id,
            session.actor_type,
            session.bot_type,
            session.reasons.join(" ")
        ].join(" ").toLowerCase();
        return haystack.includes(term);
    });

    filtered.sort(function (left, right) {
        if (sortKey === "start_desc") {
            return right.start_time - left.start_time;
        }
        if (sortKey === "start_asc") {
            return left.start_time - right.start_time;
        }
        if (sortKey === "rate_desc") {
            return right.event_rate - left.event_rate;
        }
        return right.final_risk - left.final_risk;
    });

    return filtered;
}

function renderSessions() {
    const tbody = document.getElementById("sessionRows");
    const explanationPanel = document.getElementById("explanationPanel");
    const filteredSessions = getFilteredSessions();

    if (!filteredSessions.length) {
        tbody.innerHTML = "<tr><td colspan='8'>No session rows match the current filters.</td></tr>";
        explanationPanel.innerHTML = "<p>Select a session row to view its strongest explanation details.</p>";
        return;
    }

    tbody.innerHTML = filteredSessions.map(function (session) {
        const reasons = session.reasons.join(", ") || "none";
        return `
            <tr data-session="${encodeURIComponent(JSON.stringify(session))}">
                <td>${session.session_id.slice(0, 8)}...</td>
                <td><span class="pill ${session.actor_type}">${session.actor_type}</span></td>
                <td>${formatLabel(session.bot_type)}</td>
                <td><span class="risk ${scoreBadge(session.rule_score)}">${session.rule_score}</span></td>
                <td><span class="risk ${scoreBadge(session.individual_bot_score)}">${session.individual_bot_score}</span></td>
                <td><span class="risk ${scoreBadge(session.coordination_score)}">${session.coordination_score}</span></td>
                <td><span class="risk ${scoreBadge(session.final_risk)}">${session.final_risk}</span></td>
                <td>${reasons}</td>
            </tr>
        `;
    }).join("");

    tbody.querySelectorAll("tr[data-session]").forEach(function (row, index) {
        row.addEventListener("click", function () {
            tbody.querySelectorAll("tr").forEach(function (candidate) {
                candidate.classList.remove("selected");
            });
            row.classList.add("selected");

            const payload = JSON.parse(decodeURIComponent(row.dataset.session));
            explanationPanel.innerHTML = `
                <div class="detail-header">
                    <div>
                        <h4>${payload.session_id}</h4>
                        <p class="muted">${formatLabel(payload.actor_type)} session${payload.bot_type !== "none" ? ` · ${formatLabel(payload.bot_type)}` : ""}</p>
                    </div>
                    <span class="posture-pill ${scoreBadge(payload.final_risk)}">Risk ${payload.final_risk}</span>
                </div>
                <div class="detail-grid">
                    <div class="metric-row"><span>Start Time</span><strong>${formatTimestamp(payload.start_time)}</strong></div>
                    <div class="metric-row"><span>Total Events</span><strong>${payload.total_events}</strong></div>
                    <div class="metric-row"><span>Duration</span><strong>${payload.session_duration}s</strong></div>
                    <div class="metric-row"><span>Event Rate</span><strong>${payload.event_rate}</strong></div>
                    <div class="metric-row"><span>Sequence Entropy</span><strong>${payload.entropy}</strong></div>
                    <div class="metric-row"><span>Repetition Score</span><strong>${payload.repetition_score}</strong></div>
                </div>
                <div class="reason-block">
                    <strong>Alert Reasons</strong>
                    <ul class="clean-list compact-list">${payload.reasons.map(function (reason) { return `<li>${reason}</li>`; }).join("") || "<li>No explicit rule reasons.</li>"}</ul>
                </div>
            `;
        });

        if (index === 0) {
            row.click();
        }
    });
}

function renderTimeline(timeline) {
    const container = document.getElementById("timeline");
    if (!timeline.length) {
        container.innerHTML = "<p>No timeline data available.</p>";
        return;
    }

    container.innerHTML = timeline.map(function (point) {
        return `
            <div class="timeline-item ${point.label}">
                <span>${point.session_id.slice(0, 8)}...</span>
                <strong>${formatLabel(point.bot_type)}</strong>
                <small>${point.event_rate} events/s</small>
            </div>
        `;
    }).join("");
}

function renderDemoStatus(status) {
    const container = document.getElementById("demoStatus");
    if (!status) {
        container.innerHTML = "<p>No demo status available.</p>";
        return;
    }

    const preview = status.output_preview ? `<pre class="status-log">${status.output_preview}</pre>` : "";
    container.innerHTML = `
        <p><strong>Action:</strong> ${formatLabel(status.action)}</p>
        <p><strong>Status:</strong> <span class="pill ${status.status === "failed" ? "bot" : status.status === "running" ? "warning-pill" : "human"}">${status.status}</span></p>
        <p><strong>Message:</strong> ${status.message}</p>
        <p><strong>Updated:</strong> ${status.updated_at ? formatTimestamp(status.updated_at) : "n/a"}</p>
        ${preview}
    `;
}

function renderAll(data) {
    dashboardState = data;
    renderSummary(data.summary);
    renderPosture(data.posture, data.summary);
    renderFeatureSummary(data.feature_summary);
    renderModelHealth(data.model_metrics || {});
    renderDataStatus(data.data_status || {});
    renderGroups(data.groups);
    renderTimeline(data.timeline);
    renderDistributions(data.sessions);
    renderDemoStatus(data.demo_status);
    renderSessions();
}

function refreshDashboard() {
    return fetch("/api/dashboard")
        .then(function (response) { return response.json(); })
        .then(function (data) {
            renderAll(data);
        });
}

function bindDemoControls() {
    document.querySelectorAll(".demo-action").forEach(function (button) {
        button.addEventListener("click", function () {
            const action = button.dataset.action;
            button.disabled = true;
            const originalText = button.textContent;
            button.textContent = "Running...";

            fetch("/api/demo-action", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ action: action })
            })
                .then(function (response) { return response.json(); })
                .then(function (payload) {
                    if (payload.status !== "ok") {
                        alert(payload.output || payload.message || "Action failed.");
                    }
                    return refreshDashboard();
                })
                .finally(function () {
                    button.disabled = false;
                    button.textContent = originalText;
                });
        });
    });
}

function bindTableControls() {
    ["sessionFilter", "sessionSearch", "sessionSort"].forEach(function (id) {
        const element = document.getElementById(id);
        if (!element) {
            return;
        }
        element.addEventListener("input", renderSessions);
        element.addEventListener("change", renderSessions);
    });
}

refreshDashboard().then(function () {
    bindDemoControls();
    bindTableControls();
});
