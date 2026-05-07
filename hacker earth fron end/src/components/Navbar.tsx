import { Link, useLocation } from "react-router-dom";
import { Scale, Upload, Activity, ShieldAlert, Cpu } from "lucide-react";
import { cn } from "../lib/utils";

export default function Navbar() {
  const location = useLocation();

  const links = [
    { name: "Upload", path: "/upload", icon: Upload },
    { name: "Dashboard", path: "/dashboard", icon: Activity },
    { name: "Verification", path: "/verification", icon: ShieldAlert },
    { name: "Demo Mode", path: "/demo", icon: Cpu },
  ];

  return (
    <nav className="sticky top-0 z-50 flex items-center justify-between px-8 h-16 border-b border-cream/10 bg-navy/20 backdrop-blur-md">
      <Link to="/" className="flex items-center gap-4 group">
        <div className="relative w-10 h-10 flex items-center justify-center">
          {/* Circular emblem background resembling the gold wheel */}
          <div className="absolute inset-0 rounded-full border border-gold/30 bg-gradient-to-br from-navy to-transparent"></div>
          <div className="absolute inset-1 rounded-full border border-gold/50 border-dashed animate-[spin_60s_linear_infinite]"></div>
          {/* Core icon */}
          <Scale className="relative z-10 w-5 h-5 text-cream group-hover:text-white transition-colors" />
        </div>
        <div className="flex flex-col">
          <span className="text-2xl tracking-wide font-playfair text-cream transition-all group-hover:text-white leading-none">
            Nyaya <span className="text-gold">Saarathi</span>
          </span>
          <div className="flex items-center gap-1 mt-1 justify-center">
            <div className="h-[1px] flex-1 bg-gradient-to-r from-transparent to-soft/50"></div>
            <span className="text-[7px] tracking-[0.25em] uppercase text-soft whitespace-nowrap">
              Guiding Judgments Into Action
            </span>
            <div className="h-[1px] flex-1 bg-gradient-to-l from-transparent to-soft/50"></div>
          </div>
        </div>
      </Link>
      <div className="flex items-center gap-8 text-xs tracking-widest uppercase text-soft">
        {links.map((link) => (
          <Link
            key={link.path}
            to={link.path}
            className={cn(
              "flex items-center gap-2 transition-colors hover:text-white",
              location.pathname === link.path ? "text-gold" : "text-soft"
            )}
          >
            <link.icon className="w-3 h-3" />
            {link.name}
          </Link>
        ))}
        <div className="h-6 w-px bg-cream/20 ml-2 mr-2" />
        <div className="flex items-center gap-3">
          <div className="text-right">
            <p className="text-white normal-case text-xs">Gov-System</p>
            <p className="text-[10px] text-soft">Active Session</p>
          </div>
          <div className="w-8 h-8 rounded-full bg-gold/20 border border-gold flex items-center justify-center relative">
            <span className="text-gold text-[10px]">GS</span>
            <div className="absolute -bottom-1 -right-1 w-3 h-3 rounded-full bg-green-500 border-2 border-matte"></div>
          </div>
        </div>
      </div>
    </nav>
  );
}
