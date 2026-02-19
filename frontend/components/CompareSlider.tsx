"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { ArrowLeftRight, Sparkles } from "lucide-react";

interface CompareSliderProps {
  original: string;
  colorized: string;
}

export default function CompareSlider({ original, colorized }: CompareSliderProps) {
  const [sliderPosition, setSliderPosition] = useState(50);
  const [isResizing, setIsResizing] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleMouseDown = () => setIsResizing(true);
  const handleMouseUp = () => setIsResizing(false);

  const handleMouseMove = useCallback(
    (e: MouseEvent) => {
      if (!isResizing || !containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
      const percentage = (x / rect.width) * 100;
      setSliderPosition(percentage);
    },
    [isResizing]
  );

  useEffect(() => {
    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
    return () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };
  }, [handleMouseMove]);

  return (
    <div
      ref={containerRef}
      className="relative w-full rounded-2xl overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.5)] select-none neon-border group"
    >
      {/* Background Image (Colorized) - Determines Height */}
      <img
        src={colorized}
        alt="Colorized"
        className="relative w-full h-auto block"
      />

      {/* Foreground Image (Original B&W) - Clipped Overlay */}
      <div
        className="absolute inset-0 w-full h-full overflow-hidden"
        style={{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }}
      >
        <img
          src={original}
          alt="Original"
          className="absolute inset-0 w-full h-full object-contain filter grayscale contrast-125 bg-[#0f1016]"
        />
        {/* Subtle noise overlay */}
        <div className="absolute inset-0 opacity-[0.08] mix-blend-overlay bg-repeat"
          style={{ backgroundImage: 'url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPgo8cmVjdCB3aWR0aD0iNCIgaGVpZ2h0PSI0IiBmaWxsPSIjZmZmIi8+CjxyZWN0IHdpZHRoPSIxIiBoZWlnaHQ9IjEiIGZpbGw9IiMwMDAiLz4KPC9zdmc+")' }}>
        </div>
      </div>

      {/* Slider Handle */}
      <div
        className="absolute top-0 bottom-0 w-1 bg-purple-500/50 cursor-ew-resize z-30 backdrop-blur-[2px]"
        style={{ left: `${sliderPosition}%` }}
        onMouseDown={handleMouseDown}
      >
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-10 h-10 bg-black/40 backdrop-blur-xl border border-purple-500/50 rounded-full flex items-center justify-center shadow-[0_0_20px_rgba(168,85,247,0.4)] transition-transform hover:scale-110 active:scale-95 group-hover:scale-100 scale-90">
          <ArrowLeftRight className="w-4 h-4 text-purple-200 group-hover:text-white" />
        </div>
      </div>

      {/* Labels */}
      <div className="absolute top-4 left-4 bg-black/60 backdrop-blur-md border border-white/10 text-white px-3 py-1.5 rounded-full text-xs font-semibold tracking-wider z-20 pointer-events-none flex items-center gap-2 shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        <Sparkles className="w-3 h-3 text-purple-400" />
        <span>RESTORATION</span>
      </div>
      <div
        className="absolute top-4 right-4 bg-black/60 backdrop-blur-md border border-white/10 text-slate-300 px-3 py-1.5 rounded-full text-xs font-semibold tracking-wider z-20 pointer-events-none transition-opacity duration-300 opacity-0 group-hover:opacity-100"
        style={{ opacity: sliderPosition > 95 ? 0 : undefined }}
      >
        ORIGINAL
      </div>
    </div>
  );
}
