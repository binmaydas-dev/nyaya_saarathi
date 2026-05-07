import { mockCaseData } from "../data/mockData";
import type { BackendResponse } from "../services/api";

type FieldValue = {
  value?: unknown;
  confidence?: number;
};

const asRecord = (value: unknown): Record<string, any> =>
  value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, any> : {};

const readField = (value: unknown, fallback = "Unavailable") => {
  if (value && typeof value === "object" && "value" in value) {
    return String((value as FieldValue).value || fallback);
  }

  if (value === undefined || value === null || value === "") return fallback;
  return String(value);
};

const asList = (value: unknown): any[] => Array.isArray(value) ? value : [];

const asPercent = (value: unknown, fallback = 0) => {
  if (typeof value === "number" && Number.isFinite(value)) {
    return value <= 1 ? Math.round(value * 100) : Math.round(value);
  }

  const parsed = Number(value);
  if (Number.isFinite(parsed)) return parsed <= 1 ? Math.round(parsed * 100) : Math.round(parsed);
  return fallback;
};

const riskLabel = (value: number | string | undefined) => {
  if (typeof value === "string" && value) return value;
  const score = typeof value === "number" ? value : 0;
  if (score >= 75) return "High";
  if (score >= 45) return "Medium";
  return "Low";
};

const normalizeAction = (action: any, index: number) => ({
  id: action?.id ?? index + 1,
  action: readField(action?.action || action?.title || action?.content, "Review court directive"),
  department: readField(action?.department || action?.authority || action?.owner, "Legal Department"),
  priority: readField(action?.priority || action?.risk_level, "Medium"),
  deadline: readField(action?.deadline || action?.raw_text || action?.raw, "To be verified"),
});

export const normalizeAnalysis = (response?: BackendResponse | null) => {
  response = response || {};

  const dashboard = asRecord(response.dashboard);
  const adapted = asRecord(response.frontend_adapted);
  const rawData = asRecord(response.data);
  const decision = asRecord(response.decision_intelligence || dashboard.decision_intelligence);
  const executiveReport = asRecord(dashboard.executive_report);
  const riskMeter = asRecord(response.ui_risk_meter || adapted.ui_risk_meter);
  const heatScore = asRecord(response.ui_heat_score || adapted.ui_heat_score);
  const riskValue = asPercent(riskMeter.value ?? dashboard.risk_meter ?? response.ui_risk_meter, 60);
  const confidence = asPercent(
    response.confidence_score ?? dashboard.ai_confidence_score ?? rawData.case_number?.confidence,
    dashboard.extraction_quality === "High" ? 96 : 82
  );

  const petitioner = readField(rawData.petitioner, "");
  const respondent = readField(rawData.respondent, "");
  const parties = petitioner || respondent
    ? [petitioner, respondent].filter(Boolean).join(" vs. ")
    : readField(decision.parties || rawData.parties, mockCaseData.caseOverview.parties);

  const cards = asList(response.ui_cards || adapted.ui_cards || dashboard.summary_cards)
    .map((card) => typeof card === "string" ? card : readField(card?.content || card?.title, "Summary unavailable"));

  const actions = asList(response.ui_recommended_actions || dashboard.recommended_actions || decision.recommended_actions)
    .map(normalizeAction);

  const deadlines = asList(response.ui_deadlines || adapted.ui_deadlines || dashboard.deadline_alerts || dashboard.timeline)
    .map((deadline, index) => ({
      label: readField(deadline?.event || deadline?.label || deadline?.context || deadline?.raw_text || deadline?.raw, `Deadline ${index + 1}`),
      date: readField(deadline?.date || deadline?.raw_text || deadline?.raw, "To be verified"),
      status: deadline?.is_critical ? "critical" : index === 0 ? "pending" : "upcoming",
      type: deadline?.is_critical ? "critical" : "neutral",
      days: deadline?.days ?? deadline?.normalized_days,
    }));

  const reasoningItems = asList(response.ui_decision_reasoning || dashboard.decision_reasoning || decision.reasoning);
  const reasoning = reasoningItems.length
    ? reasoningItems.join(" ")
    : readField(response.ui_decision_reasoning || adapted.ui_ai_reasoning || dashboard.ai_reasoning || decision.reasoning, mockCaseData.decision_intelligence.ui_decision_reasoning);

  const appealSuggestion = readField(
    response.ui_appeal_suggestion || dashboard.appeal_suggestion || decision.appeal_suggestion,
    dashboard.appeal_recommended || adapted.ui_appeal_recommended ? "Appeal Recommended" : "Compliance Preferred"
  );

  const verificationRequired = Boolean(
    response.verification_required ||
    confidence < 90 ||
    dashboard.extraction_quality === "Low" ||
    response.warning ||
    response.errors?.length
  );

  return {
    ...mockCaseData,
    sourceResponse: response,
    caseOverview: {
      ...mockCaseData.caseOverview,
      caseNumber: readField(decision.case_number || rawData.case_number, mockCaseData.caseOverview.caseNumber),
      court: readField(rawData.court_name || rawData.court || decision.court, mockCaseData.caseOverview.court),
      date: readField(rawData.date || decision.date, mockCaseData.caseOverview.date),
      parties,
      original_language: readField(response.original_language || rawData.original_language, "English"),
      translated_text_used: Boolean(response.translated_text_used || rawData.translated_text_used || false),
    },
    decision_intelligence: {
      executiveSummary: readField(
        executiveReport.case_overview || dashboard.voice_narration || adapted.ui_voice || cards[0],
        mockCaseData.decision_intelligence.executiveSummary
      ),
      ui_decision_reasoning: reasoning,
      extracted_text_snippet: readField(cards[0] || dashboard.model_decision_basis, "Evidence snippet unavailable."),
    },
    ui_recommended_actions: actions.length ? actions : mockCaseData.ui_recommended_actions,
    ui_appeal_suggestion: appealSuggestion,
    deadlines: deadlines.length ? deadlines : mockCaseData.deadlines,
    ui_cards: cards,
    ui_tags: asList(response.ui_tags || adapted.ui_tags || dashboard.tags).map((tag) => typeof tag === "string" ? tag : tag?.label).filter(Boolean),
    metrics: {
      risk_level: riskLabel(decision.risk_level || dashboard.escalation_risk || riskValue),
      confidence_score: confidence,
      document_quality: readField(response.document_quality || dashboard.extraction_quality, "Backend extraction completed"),
      verification_required: verificationRequired,
      warning: readField(response.warning || dashboard.alerts?.[0]?.message || response.errors?.[0], verificationRequired ? "Review recommended before publishing." : ""),
      ui_risk_meter: { value: riskValue, label: readField(riskMeter.label, "Legal Risk") },
      ui_heat_score: { value: asPercent(heatScore.value ?? dashboard.heat_score, riskValue), label: readField(heatScore.label, "Action Heat") },
    },
  };
};
