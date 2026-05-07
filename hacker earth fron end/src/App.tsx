import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import LandingPage from "./pages/LandingPage";
import UploadPage from "./pages/UploadPage";
import DashboardPage from "./pages/DashboardPage";
import VerificationPage from "./pages/VerificationPage";

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex flex-col h-screen w-screen overflow-hidden text-cream bg-matte font-inter">
        <Navbar />
        <main className="flex-1 flex overflow-hidden">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/upload" element={<UploadPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/verification" element={<VerificationPage />} />
            <Route path="/demo" element={<DashboardPage demoMode />} />
          </Routes>
        </main>
        
        {/* Bottom Status Bar matching mockup */}
        <footer className="h-10 shrink-0 border-t border-cream/10 px-8 flex items-center justify-between bg-black/40 text-[10px] text-soft tracking-wider uppercase">
          <div className="flex gap-6">
            <span className="flex items-center gap-2"><div className="w-1.5 h-1.5 rounded-full bg-green-500 shadow-[0_0_5px_green]"></div> AI Engine Online</span>
            <span>Model: Legal-LLM-v4.2-E</span>
          </div>
          <div className="flex gap-6 hidden md:flex">
            <span>Gov-Intel Encryption Active</span>
            <span className="text-white">System Time: {new Date().toLocaleTimeString('en-US', {hour12: false, timeZone: 'Asia/Kolkata'})} IST</span>
          </div>
        </footer>
      </div>
    </BrowserRouter>
  );
}
