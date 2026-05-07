import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { Activity, AlertCircle, Calendar, Check, Edit3, Flame, ShieldAlert, XCircle } from "lucide-react";
import { Link } from "react-router-dom";
import { cn } from "../lib/utils";
import { fetchDemoAnalysis, getLatestAnalysis, saveLatestAnalysis } from "../services/api";
import { normalizeAnalysis } from "../lib/analysis";

export default function DashboardPage({ demoMode = false }: { demoMode?: boolean }) {
  const [data, setData] = useState<ReturnType<typeof normalizeAnalysis> | null>(null);
  const [loadError, setLoadError] = useState("");
  const [verificationStatus, setVerificationStatus] = useState<"pending" | "approved" | "editing" | "rejected">("pending");

  useEffect(() => {
    let mounted = true;

    const loadDashboard = async () => {
      try {
        if (demoMode) {
          const response = await fetchDemoAnalysis();
          saveLatestAnalysis(response.data);
          if (mounted) setData(normalizeAnalysis(response.data));
          return;
        }

        const stored = getLatestAnalysis();
        if (mounted) setData(normalizeAnalysis(stored));
        if (!stored) setLoadError("No uploaded analysis found yet. Showing demo intelligence until a PDF is processed.");
      } catch {
        if (mounted) {
          setData(normalizeAnalysis(getLatestAnalysis()));
          setLoadError("Live dashboard refresh failed. Showing the most recent available analysis.");
        }
      }
    };

    loadDashboard();
    return () => {
      mounted = false;
    };
  }, [demoMode]);

  if (!data) {
    return <div className="p-10 flex justify-center"><Activity className="animate-spin text-gold" /></div>;
  }

  const { caseOverview, decision_intelligence, ui_recommended_actions, ui_appeal_suggestion, deadlines, metrics, ui_cards, ui_tags } = data;
  const riskScore = metrics.ui_risk_meter?.value ?? 0;
  const heatScore = metrics.ui_heat_score?.value ?? 0;
  const showVerification = metrics.verification_required && verificationStatus !== "approved";

  return (
    <div className="flex-1 flex overflow-hidden">
      <aside className="hidden lg:flex w-72 border-r border-cream/10 p-6 flex-col gap-6 bg-navy/10 overflow-y-auto">
        <div className="space-y-1">
          <p className="text-[10px] text-soft uppercase tracking-tighter">Active Case Reference</p>
          <h2 className="text-xl font-playfair italic text-white">{caseOverview.caseNumber}</h2>
        </div>

        <div className="space-y-4">
          <div className="p-3 border border-cream/10 bg-white/5 rounded">
            <p className="text-[10px] text-soft mb-1 uppercase">Parties Involved</p>
            <p className="text-sm leading-snug">{caseOverview.parties}</p>
          </div>
          <div className="p-3 border border-cream/10 bg-white/5 rounded">
            <p className="text-[10px] text-soft mb-1 uppercase">Court Authority</p>
            <p className="text-sm">{caseOverview.court}</p>
          </div>
          <div className="p-3 border border-cream/10 bg-white/5 rounded">
            <p className="text-[10px] text-soft mb-1 uppercase">Next Action</p>
            <p className="text-sm text-gold">{deadlines[0]?.date || caseOverview.date}</p>
          </div>
        </div>

        <div className="mt-auto">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] uppercase text-soft">Document Quality</span>
            <span className="text-[10px] text-green-400">{metrics.confidence_score}%</span>
          </div>
          <div className="h-1 w-full bg-white/10 rounded-full overflow-hidden">
            <div className="h-full bg-gold" style={{ width: `${Math.min(metrics.confidence_score, 100)}%` }} />
          </div>
        </div>
      </aside>

      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        <section className="flex-1 p-8 overflow-y-auto flex flex-col gap-6">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-cream/10 pb-6">
            <div>
              <h1 className="text-4xl font-playfair text-white tracking-tight">Intelligence Synthesis</h1>
              <p className="text-soft text-sm mt-1">Explainable AI reasoning for Government Compliance</p>
              {demoMode && <span className="inline-block mt-2 px-2 py-0.5 bg-blue-500/20 text-blue-400 text-[10px] uppercase tracking-widest border border-blue-500/30 rounded">Demo Mode</span>}
              {loadError && <p className="mt-3 text-xs text-amber-200/80">{loadError}</p>}
            </div>

            <div className="flex gap-3">
              {showVerification && (
                <Link to="/verification" className="px-4 py-2 border border-amber-500/50 text-amber-500 text-[10px] uppercase tracking-widest hover:bg-amber-500 hover:text-black transition-all flex items-center gap-2">
                  <ShieldAlert className="w-3 h-3 animate-pulse" />
                  Verification Required
                </Link>
              )}
              <button className="px-4 py-2 bg-gold text-black text-[10px] uppercase tracking-widest font-bold">Approve Action</button>
            </div>
          </div>

          <div className="space-y-6">
            {showVerification && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="p-5 rounded-xl border border-amber-500/30 bg-amber-500/10 shadow-[0_0_35px_rgba(245,158,11,0.08)]"
              >
                <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                  <div>
                    <h3 className="font-semibold text-amber-200 flex items-center gap-2">
                      <ShieldAlert className="w-5 h-5" />
                      Manual Verification Required
                    </h3>
                    <p className="text-sm text-amber-100/70 mt-2">{metrics.warning}</p>
                    <div className="flex flex-wrap gap-3 mt-4 text-[10px] uppercase tracking-widest text-soft">
                      <span>Confidence: <b className="text-white">{metrics.confidence_score}%</b></span>
                      <span>Quality: <b className="text-white">{metrics.document_quality}</b></span>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => setVerificationStatus("approved")} className="px-4 py-2 bg-gold text-black text-xs font-bold rounded flex items-center gap-2">
                      <Check className="w-4 h-4" /> Approve
                    </button>
                    <button onClick={() => setVerificationStatus("editing")} className="px-4 py-2 bg-white/10 text-white text-xs rounded flex items-center gap-2 hover:bg-white/20">
                      <Edit3 className="w-4 h-4" /> Edit
                    </button>
                    <button onClick={() => setVerificationStatus("rejected")} className="px-4 py-2 bg-red-500/10 text-red-200 border border-red-500/30 text-xs rounded flex items-center gap-2 hover:bg-red-500/20">
                      <XCircle className="w-4 h-4" /> Reject
                    </button>
                  </div>
                </div>
              </motion.div>
            )}

            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="p-6 rounded-xl bg-gradient-to-br from-[#1A1C20] to-navy border border-cream/10 relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <Activity className="w-16 h-16" />
              </div>
              <h3 className="text-xs uppercase text-gold tracking-[0.3em] mb-4">Executive Summary</h3>
              <p className="text-lg leading-relaxed text-cream/90">{decision_intelligence.executiveSummary}</p>

              {!!ui_cards?.length && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mt-6">
                  {ui_cards.slice(0, 4).map((card, index) => (
                    <div key={`${card}-${index}`} className="p-3 rounded bg-white/5 border border-white/5 text-sm text-cream/80">
                      {card}
                    </div>
                  ))}
                </div>
              )}

              {!!ui_tags?.length && (
                <div className="flex flex-wrap gap-2 mt-5">
                  {ui_tags.map((tag) => (
                    <span key={tag} className="px-2 py-1 rounded bg-gold/10 text-gold text-[10px] uppercase tracking-widest border border-gold/20">
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="flex flex-col gap-4">
                <h4 className="text-[10px] uppercase tracking-widest text-soft">Recommended Administrative Actions</h4>
                <div className="space-y-2">
                  {ui_recommended_actions.map((action, index) => (
                    <div key={action.id ?? index} className={cn("p-4 bg-white/5 flex flex-col gap-1 border-l-2", ["High", "Critical"].includes(action.priority) ? "border-gold" : "border-white/20 opacity-80")}>
                      <div className="flex justify-between items-center gap-3">
                        <span className="text-xs font-bold text-cream">{action.action}</span>
                        <span className={cn("px-2 py-0.5 text-[9px] rounded uppercase", ["High", "Critical"].includes(action.priority) ? "bg-gold/20 text-gold" : "bg-blue-500/20 text-blue-400")}>{action.priority}</span>
                      </div>
                      <p className="text-xs text-soft">Deadline: {action.deadline} | Dept: {action.department}</p>
                    </div>
                  ))}
                </div>
              </motion.div>

              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="flex flex-col gap-4">
                <h4 className="text-[10px] uppercase tracking-widest text-soft">Explainable AI Reasoning</h4>
                <div className="p-4 bg-navy/40 rounded-lg border border-blue-500/20 h-full text-xs text-cream/80 space-y-3">
                  <div className="flex gap-3">
                    <div className="w-1 bg-gold h-auto shrink-0" />
                    <p>{decision_intelligence.ui_decision_reasoning}</p>
                  </div>
                  <div className="flex gap-3">
                    <div className="w-1 bg-soft h-auto shrink-0" />
                    <p className="italic text-soft">Source: "{decision_intelligence.extracted_text_snippet}"</p>
                  </div>
                  <div className="flex gap-3">
                    <div className="w-1 bg-green-500 h-auto shrink-0" />
                    <p>Appeal Recommendation: {ui_appeal_suggestion}</p>
                  </div>
                </div>
              </motion.div>
            </div>

            <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }} className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {deadlines.map((deadline, index) => (
                <div key={`${deadline.label}-${index}`} className="p-4 bg-white/5 border border-white/10 rounded-lg">
                  <div className="flex items-center gap-2 text-gold mb-3">
                    <Calendar className="w-4 h-4" />
                    <span className="text-[10px] uppercase tracking-widest">Deadline Timeline</span>
                  </div>
                  <p className="text-sm font-semibold text-white">{deadline.label}</p>
                  <p className="text-xs text-soft mt-1">{deadline.date}</p>
                </div>
              ))}
            </motion.div>
          </div>
        </section>

        <aside className="w-full lg:w-80 border-t lg:border-t-0 lg:border-l border-cream/10 p-6 flex flex-col gap-8 bg-navy/20 overflow-y-auto">
          <div>
            <p className="text-[10px] uppercase tracking-widest text-soft mb-4">Risk Meter</p>
            <div className="relative h-32 flex flex-col items-center justify-center">
              <div className="w-full h-2 bg-white/10 rounded-full relative">
                <div
                  className={cn("absolute h-6 w-1 -top-2 rounded-full shadow-[0_0_10px_currentColor]", riskScore >= 75 ? "bg-red-500 text-red-500" : riskScore >= 45 ? "bg-amber-500 text-amber-500" : "bg-green-500 text-green-500")}
                  style={{ left: `${Math.min(Math.max(riskScore, 5), 95)}%` }}
                />
              </div>
              <div className="mt-6 text-center">
                <p className="text-3xl font-light text-white">{metrics.risk_level}</p>
                <p className="text-[10px] text-soft mt-1">Legal Risk: {riskScore}/100</p>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <p className="text-[10px] uppercase tracking-widest text-soft">Intelligence Confidence</p>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-3 bg-white/5 rounded border border-white/5">
                <p className="text-2xl text-white">{metrics.confidence_score}%</p>
                <p className="text-[9px] text-soft uppercase">Legal Logic</p>
              </div>
              <div className="text-center p-3 bg-white/5 rounded border border-white/5">
                <p className="text-2xl text-gold flex items-center justify-center gap-1">
                  <Flame className="w-5 h-5" /> {heatScore}
                </p>
                <p className="text-[9px] uppercase text-soft">Heat Score</p>
              </div>
            </div>
            {metrics.warning && (
              <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded flex items-start gap-3">
                <div className="mt-1 text-amber-500">
                  <AlertCircle className="w-3.5 h-3.5" />
                </div>
                <p className="text-[10px] text-amber-200/70">{metrics.warning}</p>
              </div>
            )}
          </div>

          <div>
            <p className="text-[10px] uppercase tracking-widest text-soft mb-4">Human Verification Status</p>
            <div className={cn("p-4 rounded border text-sm", showVerification ? "bg-amber-500/10 border-amber-500/20 text-amber-100" : "bg-green-500/10 border-green-500/20 text-green-200")}>
              {showVerification ? "Manual review is required before this intelligence is published." : "Output verified for administrative action."}
            </div>
          </div>

          {caseOverview.translated_text_used && (
            <div>
              <p className="text-[10px] uppercase tracking-widest text-soft mb-4">Source Context</p>
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-3">
                  <span className="text-[10px] px-2 py-0.5 border border-white/20 uppercase">{caseOverview.original_language.substring(0, 3)}</span>
                  <div className="flex-1 h-px bg-white/20" />
                  <span className="text-[10px] text-soft">Original</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-[10px] px-2 py-0.5 bg-gold text-black font-bold uppercase">ENG</span>
                  <div className="flex-1 h-px bg-white/20" />
                  <span className="text-[10px] text-gold">Processing</span>
                </div>
              </div>
            </div>
          )}

          <Link to="/upload" className="mt-auto w-full py-4 border border-dashed border-cream/20 text-soft text-xs hover:border-gold hover:text-white transition-colors text-center">
            Upload Supporting Evidence
          </Link>
        </aside>
      </div>
    </div>
  );
}
