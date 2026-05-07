import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { mockCaseData } from "../data/mockData";
import { ShieldAlert, FileText, Check, AlertTriangle, X, ChevronRight, Save, ChevronDown, ChevronUp, Clock, CheckCircle } from "lucide-react";
import { cn } from "../lib/utils";
import { useNavigate } from "react-router-dom";

export default function VerificationPage() {
  const [data, setData] = useState<typeof mockCaseData | null>(null);
  const [status, setStatus] = useState<"pending" | "approved" | "editing" | "low_confidence">("low_confidence");
  const [showEvidence, setShowEvidence] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    setData(mockCaseData);
  }, []);

  if (!data) return null;

  const handleApprove = () => {
    setStatus("approved");
    setTimeout(() => {
      navigate('/dashboard');
    }, 1500);
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden">
      {/* Top Warning Banner */}
      {(status === "pending" || status === "low_confidence" || status === "editing") && (
        <motion.div 
          initial={{ y: -50 }}
          animate={{ y: 0 }}
          className={cn(
            "p-3 flex items-center justify-center gap-3 border-b",
            status === "low_confidence" ? "bg-amber-500/10 border-amber-500/20 text-amber-500" : "bg-blue-500/10 border-blue-500/20 text-blue-400"
          )}
        >
          {status === "low_confidence" ? <ShieldAlert className="w-5 h-5 animate-pulse" /> : <FileText className="w-5 h-5" />}
          <span className="font-medium">
            {status === "low_confidence" ? "⚠ Manual Verification Required: Automated extraction detected ambiguous deadline constraint." : "Pending Review: Please verify the extracted legal directives."}
          </span>
        </motion.div>
      )}

      {status === "approved" && (
        <motion.div 
          initial={{ y: -50 }}
          animate={{ y: 0 }}
          className="bg-green-500/10 border-b border-green-500/20 p-3 flex items-center justify-center gap-3"
        >
          <Check className="w-5 h-5 text-green-400" />
          <span className="text-green-400 font-medium">Verification Complete. Generating Dashboard...</span>
        </motion.div>
      )}

      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        {/* Left Pane - Original Document */}
        <div className="w-full lg:w-1/2 flex flex-col border-r border-white/10 bg-[#1A1D24]">
          <div className="p-4 border-b border-white/10 flex items-center justify-between bg-matte">
            <h3 className="font-semibold flex items-center gap-2 text-soft">
              <FileText className="w-4 h-4" /> Source Document (PDF)
            </h3>
            <span className="text-xs font-mono bg-white/10 px-2 py-1 rounded">Page 14</span>
          </div>
          <div className="flex-1 p-8 overflow-y-auto relative">
            {/* Simulated PDF Viewer */}
            <div className="bg-[#EFEGDF] w-full max-w-2xl mx-auto min-h-[800px] shadow-2xl p-12 text-black font-serif leading-relaxed text-sm">
              <p className="opacity-50 text-center mb-10 text-xs">HIGH COURT OF KARNATAKA - WP/1203/2026</p>
              <div className="space-y-6 text-justify">
                <p>...upon reviewing the submissions and the preliminary environmental survey, it is evident that XYZ Builders bypassed mandatory ecological clearances stipulated under the Environmental Protection Act, section 3(A).</p>
                
                {/* Highlighted portion matching the extraction */}
                <div className="relative group">
                  <div className="absolute -inset-2 bg-gold/30 rounded-lg -z-10 animate-pulse" />
                  <p className="font-bold relative z-10">
                    Consequently, it is hereby ordered that all ongoing construction activities at the specified site be suspended immediately. The competent authority must conclude the reassessment and file a report by June 4, 2026.
                  </p>
                </div>
                
                <p>Failure to comply will result in further contempt proceedings. The registry is directed to communicate this order to the Secretary of Urban Development forthwith.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Pane - Extracted Intelligence Workflow */}
        <div className="w-full lg:w-1/2 flex flex-col bg-matte overflow-y-auto">
          <div className="p-6 space-y-8 max-w-2xl mx-auto w-full">
            
            <div className="flex items-start justify-between">
              <div>
                <h2 className="font-cinzel text-2xl font-bold mb-2">Review Intelligence</h2>
                <p className="text-soft text-sm">Verify the AI-extracted directives before adding them to the governance dashboard.</p>
              </div>
              {/* Status Display Badge */}
              <div className="flex gap-2">
                {status === "pending" || status === "editing" ? (
                  <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-500/10 border border-blue-500/30 text-blue-400 text-sm font-medium shadow-[0_0_10px_rgba(59,130,246,0.1)]">
                    <Clock className="w-4 h-4" />
                    Needs Review
                  </div>
                ) : status === "low_confidence" ? (
                  <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-500 text-sm font-medium shadow-[0_0_10px_rgba(245,158,11,0.1)]">
                    <AlertTriangle className="w-4 h-4" />
                    Caution: Low Confidence
                  </div>
                ) : status === "approved" ? (
                   <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-500/10 border border-green-500/30 text-green-400 text-sm font-medium shadow-[0_0_10px_rgba(34,197,94,0.1)]">
                    <CheckCircle className="w-4 h-4" />
                    Verified Output
                  </div>
                ) : null}
              </div>
            </div>

            {/* AI Decision Card */}
            <div className="glass-panel p-6 rounded-2xl border-l-4 border-l-gold">
              <div className="flex items-center justify-between mb-4">
                <h4 className="text-gold font-semibold text-sm uppercase tracking-wider">Extracted Directive</h4>
                <div className="flex items-center gap-2 bg-white/5 px-2 py-1 rounded text-xs">
                  <span className="text-soft">Confidence:</span>
                  <span className="text-green-400 font-mono">92.5%</span>
                </div>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="text-xs text-soft mb-1 block">Executive Summary</label>
                  <textarea 
                    className="w-full bg-black/20 border border-white/10 rounded-lg p-3 text-sm focus:border-gold outline-none transition-colors min-h-[100px]"
                    defaultValue={data.decision_intelligence.executiveSummary}
                    readOnly={status !== "editing"}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-xs text-soft mb-1 block">Target Department</label>
                    <input 
                      type="text"
                      className="w-full bg-black/20 border border-white/10 rounded-lg p-2 text-sm focus:border-gold outline-none"
                      defaultValue="Urban Development"
                      readOnly={status !== "editing"}
                    />
                  </div>
                  <div>
                    <label className="text-xs text-soft mb-1 block">Critical Deadline</label>
                    <div className="relative">
                      <input 
                        type="date"
                        className="w-full bg-amber-500/10 border border-amber-500/30 text-amber-500 rounded-lg p-2 text-sm focus:border-amber-500 outline-none"
                        defaultValue="2026-06-04"
                        readOnly={status !== "editing"}
                      />
                      <AlertTriangle className="w-4 h-4 text-amber-500 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* AI Reasoning */}
            <div className="bg-navy/20 border border-navy p-5 rounded-xl flex flex-col gap-4">
              <div>
                <h4 className="text-sm font-semibold mb-2">Explainable AI Trace</h4>
                <p className="text-sm text-soft leading-relaxed">{data.decision_intelligence.ui_decision_reasoning}</p>
              </div>

              <div className="border-t border-navy/50 pt-4">
                <button 
                  onClick={() => setShowEvidence(!showEvidence)}
                  className="flex items-center justify-between w-full text-sm text-gold hover:text-gold/80 transition-colors"
                >
                  <span className="font-medium flex items-center gap-2">
                    <FileText className="w-4 h-4"/> 
                    {showEvidence ? 'Hide Evidence' : 'Show Evidence'}
                  </span>
                  {showEvidence ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </button>
                
                <AnimatePresence>
                  {showEvidence && (
                    <motion.div 
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="overflow-hidden"
                    >
                      <div className="mt-4 p-4 bg-black/40 border border-white/5 rounded-lg">
                        <p className="font-mono text-xs text-cream/80 italic pl-3 border-l-2 border-gold/50">
                          "{data.decision_intelligence.extracted_text_snippet}"
                        </p>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>

            {/* Action Bar */}
            <div className="flex items-center gap-4 pt-6 border-t border-white/10">
              <button 
                onClick={handleApprove}
                disabled={status === "approved"}
                className={cn(
                  "flex-1 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition-all",
                  status === "approved" 
                    ? "bg-green-500/20 text-green-400 border border-green-500/30 cursor-not-allowed"
                    : "bg-gold hover:bg-gold/90 text-matte"
                )}
              >
                {status === "approved" ? "Verified" : "Approve & Publish"}
                {!status && <Check className="w-5 h-5" />}
              </button>
              
              {status === "pending" && (
                <button 
                  onClick={() => setStatus("editing")}
                  className="px-6 py-3 glass-panel hover:bg-white/10 rounded-lg font-semibold transition-colors"
                >
                  Edit Output
                </button>
              )}

              {status === "editing" && (
                <button 
                  onClick={() => setStatus("pending")}
                  className="px-6 py-3 bg-white/10 hover:bg-white/20 rounded-lg font-semibold transition-colors flex items-center gap-2"
                >
                  <Save className="w-4 h-4" /> Save Edits
                </button>
              )}
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}
