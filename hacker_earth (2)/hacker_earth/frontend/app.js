const API_BASE = "/api";

const els = {
  apiStatus: document.getElementById("apiStatus"),
  statusText: document.getElementById("statusText"),
  uploadForm: document.getElementById("uploadForm"),
  pdfInput: document.getElementById("pdfInput"),
  fileName: document.getElementById("fileName"),
  mockMode: document.getElementById("mockMode"),
  loadDemo: document.getElementById("loadDemo"),
  processingMode: document.getElementById("processingMode"),
  requestId: document.getElementById("requestId"),
  caseNumber: document.getElementById("caseNumber"),
  parties: document.getElementById("parties"),
  priorityBadge: document.getElementById("priorityBadge"),
  riskBadge: document.getElementById("riskBadge"),
  appealBadge: document.getElementById("appealBadge"),
  riskMeter: document.getElementById("riskMeter"),
  heatScore: document.getElementById("heatScore"),
  riskFill: document.getElementById("riskFill"),
  heatFill: document.getElementById("heatFill"),
  complianceState: document.getElementById("complianceState"),
  authorityState: document.getElementById("authorityState"),
  actionCount: document.getElementById("actionCount"),
  actionsList: document.getElementById("actionsList"),
  deadlineCount: document.getElementById("deadlineCount"),
  deadlineList: document.getElementById("deadlineList"),
  summaryList: document.getElementById("summaryList"),
  reasoningList: document.getElementById("reasoningList"),
  toast: document.getElementById("toast")
};

function text(value, fallback = "-") {
  if (value === undefined || value === null || value === "") return fallback;
  return String(value);
}

function asArray(value) {
  return Array.isArray(value) ? value : [];
}

function colorClass(value) {
  const normalized = text(value, "secondary").toLowerCase();
  if (["critical", "danger", "high"].includes(normalized)) return normalized === "high" ? "warning" : "danger";
  if (["medium", "warning"].includes(normalized)) return "warning";
  if (["low", "success"].includes(normalized)) return "success";
  if (["info"].includes(normalized)) return "info";
  return "neutral";
}

function setBadge(el, label, value) {
  el.className = `badge ${colorClass(value)}`;
  el.textContent = `${label}: ${text(value, "Unknown")}`;
}

function showToast(message) {
  els.toast.textContent = message;
  els.toast.hidden = false;
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => {
    els.toast.hidden = true;
  }, 4200);
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Request failed with ${response.status}`);
  }
  return response.json();
}

async function checkHealth() {
  try {
    await requestJson(`${API_BASE}/health`);
    els.apiStatus.className = "status-dot ok";
    els.statusText.textContent = "API online";
  } catch (error) {
    els.apiStatus.className = "status-dot error";
    els.statusText.textContent = "API unavailable";
  }
}

async function loadDemoCase(reason) {
  if (reason) showToast(reason);
  try {
    const payload = await requestJson(`${API_BASE}/demo-test`);
    renderDashboard(payload);
  } catch (err) {
    console.error("Failed to load demo case:", err);
  }
}

async function uploadPdf(event) {
  event.preventDefault();

  const file = els.pdfInput.files[0];
  if (!file) {
    await loadDemoCase("No PDF selected. Loaded the verified demo case.");
    return;
  }

  const data = new FormData();
  data.append("file", file);
  const mockQuery = els.mockMode.checked ? "?mock_mode=true" : "";

  try {
    showToast("Analyzing document...");
    const payload = await requestJson(`${API_BASE}/upload${mockQuery}`, {
      method: "POST",
      body: data
    });
    renderDashboard(payload);
  } catch (error) {
    await loadDemoCase("Upload failed. Switched to demo-safe response.");
  }
}

function getCaseValue(data, key) {
  const item = data && data[key];
  if (item && typeof item === "object") return text(item.value, "");
  return text(item, "");
}

function makeEmpty(container, message) {
  container.innerHTML = `<div class="summary-item">${message}</div>`;
}

function renderActions(actions) {
  els.actionCount.textContent = `${actions.length} action${actions.length === 1 ? "" : "s"}`;
  if (!actions.length) {
    makeEmpty(els.actionsList, "No administrative recommendations found.");
    return;
  }

  els.actionsList.innerHTML = actions.map((action) => `
    <div class="action-item">
      <div class="action-header">
        <strong>${text(action.action, "Review order")}</strong>
        <span class="badge ${colorClass(action.priority)}">${text(action.priority, "Low")}</span>
      </div>
      <div class="meta-row">
        <span>Department: <strong>${text(action.department, "Legal Department")}</strong></span>
        <span>Risk: <strong>${text(action.risk_level, "Low")}</strong></span>
        <span>Deadline: <strong>${text(action.deadline, "Not specified")}</strong></span>
      </div>
    </div>
  `).join("");
}

function renderDeadlines(deadlines) {
  els.deadlineCount.textContent = `${deadlines.length} deadline${deadlines.length === 1 ? "" : "s"}`;
  if (!deadlines.length) {
    makeEmpty(els.deadlineList, "No mandatory deadline detected.");
    return;
  }

  els.deadlineList.innerHTML = deadlines.map((deadline) => `
    <div class="timeline-item">
      <strong>${text(deadline.raw_text || deadline.raw, "Deadline")}</strong>
      <div class="meta-row">
        <span>Days: <strong>${text(deadline.days ?? deadline.normalized_days, "N/A")}</strong></span>
        <span>${deadline.is_critical ? "Critical timeline" : "Standard timeline"}</span>
      </div>
    </div>
  `).join("");
}

function renderSummary(cards, report) {
  const reportItems = [];
  if (report && typeof report === "object") {
    ["case_overview", "primary_issue", "court_direction", "risk_assessment", "recommended_next_step"].forEach((key) => {
      if (report[key]) reportItems.push(report[key]);
    });
  }

  const summary = cards.length ? cards.map((card) => card.content || card) : reportItems;
  if (!summary.length) {
    makeEmpty(els.summaryList, "Summary unavailable for this response.");
    return;
  }

  els.summaryList.innerHTML = summary.map((item) => `
    <div class="summary-item">${text(item)}</div>
  `).join("");
}

function renderReasoning(reasoning) {
  if (!reasoning.length) {
    makeEmpty(els.reasoningList, "No reasoning trace available.");
    return;
  }

  els.reasoningList.innerHTML = reasoning.map((item, index) => `
    <div class="reasoning-item"><strong>${index + 1}.</strong> ${text(item)}</div>
  `).join("");
}

function renderDashboard(payload) {
  const data = payload.data || {};
  const dashboard = payload.dashboard || {};
  const ui = payload.frontend_adapted || {};
  const decision = ui.decision_intelligence || dashboard.decision_intelligence || {};

  const caseNumber = decision.case_number || getCaseValue(data, "case_number") || "Demo case";
  const petitioner = getCaseValue(data, "petitioner") || "Petitioner unavailable";
  const respondent = getCaseValue(data, "respondent") || "Respondent unavailable";

  const actions = asArray(ui.ui_recommended_actions).length
    ? asArray(ui.ui_recommended_actions)
    : asArray(decision.recommended_actions || dashboard.recommended_actions);
  const deadlines = asArray(ui.ui_deadlines).length
    ? asArray(ui.ui_deadlines)
    : asArray(dashboard.deadline_alerts);
  const summaryCards = asArray(ui.ui_cards).length ? asArray(ui.ui_cards) : asArray(dashboard.summary_cards);
  const reasoning = asArray(ui.ui_decision_reasoning).length
    ? asArray(ui.ui_decision_reasoning)
    : asArray(decision.reasoning || dashboard.decision_reasoning || dashboard.reasoning_trace);

  els.processingMode.textContent = text(payload.processing_mode, "unknown");
  els.requestId.textContent = text(payload.request_id || payload.id, "-");
  els.caseNumber.textContent = caseNumber;
  els.parties.textContent = `${petitioner} vs ${respondent}`;

  setBadge(els.priorityBadge, "Priority", decision.priority_level || ui.ui_urgency?.badge_text || dashboard.urgency_badge);
  setBadge(els.riskBadge, "Risk", decision.risk_level || ui.ui_severity || dashboard.severity);
  setBadge(els.appealBadge, "Appeal", decision.appeal_suggestion || ui.ui_appeal_suggestion || dashboard.appeal_suggestion);

  const riskValue = Number(ui.ui_risk_meter?.value ?? dashboard.risk_meter ?? 0);
  const heatValue = Number(ui.ui_heat_score?.value ?? dashboard.heat_score ?? 0);
  const safeRisk = Number.isFinite(riskValue) ? riskValue : 0;
  const safeHeat = Number.isFinite(heatValue) ? heatValue : 0;
  
  els.riskMeter.textContent = safeRisk;
  els.heatScore.textContent = safeHeat;
  els.riskFill.style.width = `${Math.max(0, Math.min(100, safeRisk))}%`;
  els.heatFill.style.width = `${Math.max(0, Math.min(100, safeHeat))}%`;

  els.complianceState.textContent = text(ui.ui_compliance_probability || dashboard.compliance_probability, "Unknown");
  els.authorityState.textContent = text(ui.ui_authority_involved || dashboard.authority_involved, "Authority pending");

  renderActions(actions);
  renderDeadlines(deadlines);
  renderSummary(summaryCards, ui.ui_executive_report || dashboard.executive_report);
  renderReasoning(reasoning);
}

els.pdfInput.addEventListener("change", () => {
  const file = els.pdfInput.files[0];
  els.fileName.textContent = file ? file.name : "Choose a court PDF";
});

els.uploadForm.addEventListener("submit", uploadPdf);
els.loadDemo.addEventListener("click", () => loadDemoCase("Loaded verified demo case."));

checkHealth();
loadDemoCase();
