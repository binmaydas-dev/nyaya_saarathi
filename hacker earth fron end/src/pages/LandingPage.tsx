import { motion } from "motion/react";
import { Link } from "react-router-dom";
import { FileText, Clock, AlertTriangle, EyeOff, Globe2, ShieldCheck, ArrowRight, ChevronDown, Gavel } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex-1 overflow-y-auto w-full">
      {/* Hero Section */}
      <section className="relative min-h-[90vh] flex items-center justify-center overflow-hidden">
        {/* Abstract Cinematic Background */}
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-gradient-to-b from-navy/20 via-matte to-matte z-10" />
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.3 }}
            transition={{ duration: 2 }}
            className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gold/10 rounded-full blur-[120px]"
          />
        </div>

        <div className="relative z-10 max-w-5xl mx-auto px-6 text-center">
          
          {/* Emblem Assembly */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="flex justify-center mb-10"
          >
            <div className="relative w-48 h-48 flex items-center justify-center">
              {/* Outer Split Ring (Navy left, Gold right) */}
              <div className="absolute inset-0 rounded-full border-[12px] border-transparent" style={{ background: 'linear-gradient(to right, #0B1F3A 50%, #C8A96B 50%)', WebkitMask: 'radial-gradient(transparent 60%, black 61%)' }}></div>
              <div className="absolute inset-0 rounded-full border-[12px] border-gold/10 drop-shadow-2xl"></div>

              {/* Gold Inner Elements */}
              <div className="absolute inset-4 rounded-full border-4 border-gold shadow-[inset_0_0_20px_rgba(200,169,107,0.3)]"></div>
              
              {/* Radiant Spokes */}
              <div className="absolute inset-[15%] flex items-center justify-center pointer-events-none bg-white rounded-full">
                {[...Array(24)].map((_, i) => (
                  <div 
                    key={i} 
                    className="absolute w-[2px] h-[75%] bg-gradient-to-t from-gold/50 to-transparent"
                    style={{ transform: `rotate(${i * 15}deg)` }}
                  />
                ))}
              </div>

              {/* Core Emblem Stand-in */}
              <div className="relative z-10 flex flex-col items-center">
                <div className="flex gap-1 mb-1">
                  {/* We use cream colors for the inner piece to contrast on dark */}
                  <ShieldCheck className="w-16 h-16 text-navy drop-shadow-md" fill="#F5F2EA" />
                </div>
                {/* Base / Chakra */}
                <div className="w-8 h-8 rounded-full border-4 border-navy flex items-center justify-center bg-cream shadow-sm -mt-2">
                  <Globe2 className="w-4 h-4 text-navy drop-shadow-sm" strokeWidth={3} />
                </div>
                {/* Pedestal */}
                <div className="w-20 h-2 bg-navy rounded-sm mt-1 z-10"></div>
                <div className="w-24 h-1.5 bg-navy rounded-sm mt-0.5 z-10"></div>
              </div>

              {/* Open Book Flourish (Double lines overlapping) */}
              <div className="absolute -bottom-8 w-64 flex flex-col items-center justify-center text-gold z-20">
                <svg viewBox="0 0 200 40" className="w-full fill-navy stroke-gold stroke-[3px]">
                   <path d="M 100 20 Q 50 0 0 20 Q 50 40 100 20 Q 150 0 200 20 Q 150 40 100 20 Z" />
                   <path d="M 100 30 Q 50 10 0 30 Q 50 50 100 30 Q 150 10 200 30 Q 150 50 100 30 Z" className="stroke-navy fill-gold" />
                </svg>
              </div>
            </div>
          </motion.div>

          <motion.h1 
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="font-playfair text-5xl md:text-7xl tracking-wide text-cream flex items-center justify-center gap-4 flex-wrap"
          >
            <span>Nyaya</span>
            <span className="text-gold font-bold">Saarathi</span>
          </motion.h1>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.1 }}
            className="flex items-center justify-center gap-4 my-6"
          >
            <div className="h-[2px] w-32 bg-gradient-to-r from-transparent to-navy rounded-full"></div>
            <div className="w-1.5 h-1.5 rounded-full bg-gold"></div>
            <Gavel className="w-6 h-6 text-gold -rotate-12" />
            <div className="w-1.5 h-1.5 rounded-full bg-gold"></div>
            <div className="h-[2px] w-32 bg-gradient-to-l from-transparent to-navy rounded-full"></div>
          </motion.div>
          
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
            className="text-[10px] md:text-xs tracking-[0.3em] uppercase text-soft mb-12 inline-block px-12"
          >
            Guiding Judgments Into Action
          </motion.h2>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="text-lg md:text-xl text-soft max-w-2xl mx-auto mb-16 font-inter"
          >
            AI-Assisted Legal Intelligence for Smarter Governance. Transform lengthy court orders into actionable directives instantly.
          </motion.p>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto mb-16 text-center"
          >
            {[
              { icon: FileText, title: "Judgment Analysis" },
              { icon: ShieldCheck, title: "Action Recommendation" },
              { icon: AlertTriangle, title: "Department Alerts" },
              { icon: Clock, title: "Tracking & Monitoring" }
            ].map((feature, i) => (
              <div key={i} className="flex flex-col items-center gap-3 p-4">
                <div className="w-12 h-12 rounded-full bg-navy/50 border border-gold/30 flex items-center justify-center text-gold">
                  <feature.icon className="w-5 h-5" />
                </div>
                <span className="text-xs font-semibold uppercase tracking-wider text-cream/90">{feature.title}</span>
              </div>
            ))}
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.8 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-6"
          >
            <Link 
              to="/upload" 
              className="px-8 py-4 bg-cream text-matte font-semibold rounded-lg hover:bg-gold transition-colors flex items-center gap-2 group w-full sm:w-auto justify-center"
            >
              Upload Judgment
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link 
              to="/demo" 
              className="px-8 py-4 glass-panel text-cream font-semibold rounded-lg hover:bg-white/10 transition-colors flex items-center gap-2 w-full sm:w-auto justify-center"
            >
              Load Demo Case
            </Link>
          </motion.div>
        </div>

        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5, duration: 1 }}
          className="absolute bottom-10 left-1/2 -translate-x-1/2"
        >
          <ChevronDown className="w-8 h-8 text-soft animate-bounce" />
        </motion.div>
      </section>

      {/* Existing Challenges Section */}
      <section className="py-24 bg-matte relative">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h3 className="font-cinzel text-3xl font-bold mb-4">Existing Challenges</h3>
            <p className="text-soft">The bottlenecks in modern administrative legal response</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { icon: FileText, title: "Lengthy Legal PDFs", desc: "Complex 50+ page documents obscure immediate action items." },
              { icon: Clock, title: "Manual Review Delays", desc: "Hours spent summarizing rulings delay active compliance." },
              { icon: AlertTriangle, title: "Hidden Deadlines", desc: "Buried dates lead to contempt of court risks." },
              { icon: EyeOff, title: "No Explainable AI", desc: "Black-box models fail to provide reasoning for government use." },
              { icon: Globe2, title: "Multilingual Challenges", desc: "Regional language judgments require slow human translation." },
              { icon: ShieldCheck, title: "Lack of Human Verification", desc: "Current solutions remove the human-in-the-loop necessity." }
            ].map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
                className="glass-panel p-8 rounded-2xl hover:border-gold/30 transition-colors group"
              >
                <div className="w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center mb-6 group-hover:bg-gold/10 transition-colors">
                  <feature.icon className="w-6 h-6 text-gold" />
                </div>
                <h4 className="font-semibold text-lg mb-3">{feature.title}</h4>
                <p className="text-soft leading-relaxed">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
