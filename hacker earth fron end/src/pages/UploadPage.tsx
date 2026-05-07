import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { UploadCloud, File, Globe, ArrowRight, CheckCircle2, Loader2, Sparkles, Camera, X, AlertCircle } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { cn } from "../lib/utils";
import { uploadJudgmentWithFallback } from "../services/api";

export default function UploadPage() {
  const [isHovering, setIsHovering] = useState(false);
  const [uploadState, setUploadState] = useState<"idle" | "uploading" | "analyzing" | "complete" | "error">("idle");
  const [progress, setProgress] = useState(0);
  const [isScanning, setIsScanning] = useState(false);
  const [selectedFileName, setSelectedFileName] = useState("");
  const [statusMessage, setStatusMessage] = useState("");
  const [usedFallback, setUsedFallback] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const startProgress = () => {
    setProgress(8);
    return window.setInterval(() => {
      setProgress((current) => {
        if (current >= 88) return current;
        return current + Math.max(2, Math.round((90 - current) / 8));
      });
    }, 220);
  };

  const createDemoPdf = () => new File(
    [new Blob(["%PDF-1.4\n% Nyaya Saarathi demo-safe upload\n"], { type: "application/pdf" })],
    "nyaya-saarathi-demo.pdf",
    { type: "application/pdf" }
  );

  const handleUpload = async (file: File, mockMode = false) => {
    stopCamera();
    setIsScanning(false);
    setUsedFallback(false);
    setSelectedFileName(file.name);
    setStatusMessage("");
    setUploadState("uploading");
    const interval = startProgress();

    try {
      window.setTimeout(() => setUploadState("analyzing"), 550);
      const result = await uploadJudgmentWithFallback(file, mockMode);
      window.clearInterval(interval);
      setUsedFallback(result.usedFallback);
      setStatusMessage(result.usedFallback ? "Backend upload failed, so the dashboard is using the polished demo analysis." : "");
      setProgress(100);
      setUploadState("complete");
      window.setTimeout(() => navigate('/dashboard'), 900);
    } catch (err) {
      window.clearInterval(interval);
      setProgress(100);
      setUploadState("error");
      setStatusMessage("Backend unavailable and demo fallback could not be loaded. Please start FastAPI and try again.");
    }
  };

  const handleFileSelected = (file?: File | null, mockMode = false) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith(".pdf")) {
      setUploadState("error");
      setStatusMessage("Please upload a PDF court judgment.");
      return;
    }

    handleUpload(file, mockMode);
  };

  const startCamera = async () => {
    try {
      setIsScanning(true);
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error("Error accessing camera:", err);
      // Fallback or alert in a real app
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
    }
    setIsScanning(false);
  };
  
  useEffect(() => {
    // Cleanup on unmount
    return () => {
      stopCamera();
    };
  }, []);

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 overflow-y-auto w-full bg-gradient-to-b from-navy/10 to-matte">
      <div className="w-full max-w-3xl">
        <div className="text-center mb-12">
          <h1 className="font-cinzel text-3xl font-bold mb-4">Ingest Legal Document</h1>
          <p className="text-soft">Upload the court judgment PDF or scan it directly for AI decision intelligence processing.</p>
        </div>

        {/* Upload Area */}
        <AnimatePresence mode="wait">
          {uploadState === "idle" && !isScanning && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className={cn(
                "glass-panel rounded-3xl p-12 text-center border-2 border-dashed transition-colors relative overflow-hidden",
                isHovering ? "border-gold bg-gold/5" : "border-white/20 hover:border-gold/50 cursor-pointer"
              )}
              onMouseEnter={() => setIsHovering(true)}
              onMouseLeave={() => setIsHovering(false)}
              onDragOver={(e) => { e.preventDefault(); setIsHovering(true); }}
              onDragLeave={() => setIsHovering(false)}
              onDrop={(e) => { e.preventDefault(); handleFileSelected(e.dataTransfer.files?.[0]); }}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept="application/pdf,.pdf"
                className="hidden"
                onChange={(event) => handleFileSelected(event.target.files?.[0])}
              />

              <div onClick={() => fileInputRef.current?.click()}>
                <UploadCloud className="w-16 h-16 text-gold mx-auto mb-6 opacity-80" />
                <h3 className="font-semibold text-xl mb-2">Drag & Drop Judgment</h3>
                <p className="text-soft mb-8">or click to browse local files (PDF only)</p>
              </div>
              
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <button 
                  onClick={() => fileInputRef.current?.click()}
                  className="px-6 py-3 bg-white/10 hover:bg-white/20 rounded-lg font-medium transition-colors w-full sm:w-auto"
                >
                  Select File
                </button>
                <span className="text-soft text-sm">or</span>
                <button 
                  onClick={(e) => { e.stopPropagation(); handleUpload(createDemoPdf(), true); }}
                  className="px-6 py-3 bg-white/10 hover:bg-white/20 rounded-lg font-medium transition-colors w-full sm:w-auto"
                >
                  Demo-Safe Upload
                </button>
                <span className="text-soft text-sm">or</span>
                <button 
                  onClick={(e) => { e.stopPropagation(); startCamera(); }}
                  className="px-6 py-3 bg-gold/20 hover:bg-gold/30 text-gold border border-gold/50 rounded-lg font-medium transition-colors w-full sm:w-auto flex items-center justify-center gap-2"
                >
                  <Camera className="w-4 h-4" />
                  Scan Document
                </button>
              </div>
              <div className="flex items-center justify-center gap-2 text-sm text-soft mt-8">
                <Globe className="w-4 h-4" />
                Supports Kannada, Telugu, Hindi, English
              </div>
            </motion.div>
          )}

          {isScanning && (
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass-panel rounded-3xl overflow-hidden border border-white/20 relative"
            >
              <div className="absolute top-4 right-4 z-20">
                <button 
                  onClick={stopCamera}
                  className="p-2 bg-black/50 hover:bg-black/80 rounded-full text-white backdrop-blur-sm transition-colors"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>
              
              <div className="relative aspect-video bg-black flex items-center justify-center">
                <video 
                  ref={videoRef} 
                  autoPlay 
                  playsInline 
                  className="max-h-full w-full object-cover"
                />
                {/* Scanner Overlay */}
                <div className="absolute inset-x-12 inset-y-12 border-2 border-gold/50 rounded-lg pointer-events-none">
                  <div className="absolute -top-2 -left-2 w-4 h-4 border-t-2 border-l-2 border-gold"></div>
                  <div className="absolute -top-2 -right-2 w-4 h-4 border-t-2 border-r-2 border-gold"></div>
                  <div className="absolute -bottom-2 -left-2 w-4 h-4 border-b-2 border-l-2 border-gold"></div>
                  <div className="absolute -bottom-2 -right-2 w-4 h-4 border-b-2 border-r-2 border-gold"></div>
                  
                  {/* Scanning line animation */}
                  <motion.div 
                    animate={{ y: ["0%", "100%", "0%"] }}
                    transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
                    className="w-full h-0.5 bg-gold/70 shadow-[0_0_15px_#C8A96B]"
                  />
                </div>
              </div>
              
              <div className="p-6 text-center bg-navy/50">
                <p className="text-sm text-soft mb-4">Position the document within the frame</p>
                <button 
                  onClick={() => handleUpload(createDemoPdf(), true)}
                  className="px-8 py-3 bg-gold text-black rounded-lg font-bold transition-colors shadow-[0_0_15px_rgba(200,169,107,0.3)] hover:shadow-[0_0_25px_rgba(200,169,107,0.5)] flex items-center justify-center gap-2 mx-auto"
                >
                  <Camera className="w-5 h-5 flex-shrink-0" />
                  Capture & Process
                </button>
              </div>
            </motion.div>
          )}

          {(uploadState === "uploading" || uploadState === "analyzing" || uploadState === "complete" || uploadState === "error") && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={cn("glass-panel rounded-3xl p-12 relative overflow-hidden", uploadState === "error" ? "border-red-500/40" : "border-gold/30")}
            >
              {/* Animated Progress Background */}
              <div 
                className="absolute inset-y-0 left-0 bg-gold/10 transition-all duration-300 ease-out"
                style={{ width: `${progress}%` }}
              />

              <div className="relative z-10 flex flex-col items-center">
                {uploadState === "error" ? (
                  <AlertCircle className="w-16 h-16 text-red-400 mb-6" />
                ) : uploadState === "complete" ? (
                  <CheckCircle2 className="w-16 h-16 text-green-400 mb-6" />
                ) : uploadState === "analyzing" ? (
                  <Sparkles className="w-16 h-16 text-gold mb-6 animate-pulse" />
                ) : (
                  <File className="w-16 h-16 text-gold mb-6 animate-bounce" />
                )}

                <h3 className="font-semibold text-xl mb-4">
                  {uploadState === "uploading" && "Uploading document..."}
                  {uploadState === "analyzing" && "Analyzing Court Judgment..."}
                  {uploadState === "complete" && "Analysis Complete."}
                  {uploadState === "error" && "Analysis could not be completed."}
                </h3>

                {selectedFileName && <p className="text-xs text-soft mb-4">{selectedFileName}</p>}

                <div className="w-full max-w-md h-2 bg-matte rounded-full overflow-hidden mb-4">
                  <div 
                    className="h-full bg-gold transition-all duration-300 ease-out"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                
                {uploadState !== "complete" && uploadState !== "error" && (
                  <p className="text-soft flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    {uploadState === "uploading" ? `${progress}% uploaded` : "Extracting directives & translating..."}
                  </p>
                )}

                {statusMessage && (
                  <p className={cn("mt-4 text-sm text-center max-w-lg", usedFallback ? "text-amber-200" : "text-red-200")}>
                    {statusMessage}
                  </p>
                )}

                {uploadState === "error" && (
                  <button
                    onClick={() => {
                      setUploadState("idle");
                      setProgress(0);
                      setStatusMessage("");
                    }}
                    className="mt-6 px-5 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-sm transition-colors"
                  >
                    Try Again
                  </button>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Multilingual Workflow UI */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-12 glass-panel rounded-2xl p-6"
        >
          <h4 className="text-sm font-semibold text-soft uppercase tracking-wider mb-6 text-center">Neural Multilingual Pipeline</h4>
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex-1 text-center p-4 bg-white/5 rounded-lg border border-white/5">
              <span className="block text-xl mb-2">🇮🇳</span>
              <span className="text-sm font-medium">Regional Language</span>
            </div>
            <ArrowRight className="w-5 h-5 text-gold/50 rotate-90 md:rotate-0" />
            <div className="flex-1 text-center p-4 bg-white/5 rounded-lg border border-gold/20 shadow-[0_0_15px_rgba(200,169,107,0.1)]">
              <Sparkles className="w-6 h-6 text-gold mx-auto mb-2" />
              <span className="text-sm font-medium">Translation Layer</span>
            </div>
            <ArrowRight className="w-5 h-5 text-gold/50 rotate-90 md:rotate-0" />
            <div className="flex-1 text-center p-4 bg-white/5 rounded-lg border border-white/5">
              <File className="w-6 h-6 text-blue-400 mx-auto mb-2" />
              <span className="text-sm font-medium">English Processing</span>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
