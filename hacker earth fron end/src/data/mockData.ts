export const mockCaseData = {
  caseOverview: {
    caseNumber: "WP/1203/2026",
    court: "High Court of Karnataka",
    date: "2026-05-04",
    parties: "State of Karnataka vs. XYZ Builders",
    status: "Judgment Passed",
    original_language: "Kannada",
    translated_text_used: true,
    translation_confidence: 96.4,
    translation_notice: "Translated using Neural Legal Translation V4"
  },
  decision_intelligence: {
    executiveSummary: "The court has explicitly directed the Urban Development Department to reassess the zoning approval of XYZ Builders within 30 days due to preliminary environmental survey discrepancies.",
    ui_decision_reasoning: "The order highlights violation of Environmental Protection Act section 3(A). Key directives pinpoint immediate halt to construction pending reassessment.",
    extracted_text_snippet: "...it is hereby ordered that all ongoing construction activities at the specified site be suspended immediately. The competent authority must conclude the reassessment and file a report by June 4, 2026."
  },
  ui_recommended_actions: [
    { id: 1, action: "Issue Halt Order", department: "Urban Development", priority: "High", deadline: "2026-05-08" },
    { id: 2, action: "Convene Environmental Board", department: "Environmental Protection", priority: "Medium", deadline: "2026-05-15" },
    { id: 3, action: "File Compliance Affidavit", department: "Legal Cell", priority: "High", deadline: "2026-06-03" }
  ],
  ui_appeal_suggestion: "Compliance Preferred. Overturn probability is low due to explicit environmental statute violations.",
  deadlines: [
    { label: "Construction Halt Implemented", date: "2026-05-08", status: "pending", type: "warning" },
    { label: "Appeal Window Closes", date: "2026-06-03", status: "upcoming", type: "neutral" },
    { label: "Final Compliance Report", date: "2026-06-04", status: "upcoming", type: "critical" }
  ],
  metrics: {
    risk_level: "High",
    confidence_score: 92.5,
    document_quality: "Scanned PDF (OCR Applied, 94% Legibility)",
    verification_required: true,
    warning: "Automated extraction detected ambiguous deadline constraint on page 14."
  }
};
