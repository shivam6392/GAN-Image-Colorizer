"use client";

import { useState } from "react";
import ImageUploader from "@/components/ImageUploader";
import CompareSlider from "@/components/CompareSlider";
import { Loader2, Download, RefreshCw, Wand2, Sparkles, ArrowRight } from "lucide-react";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [colorizedImage, setColorizedImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileSelect = (file: File) => {
    setError(null);
    setSelectedFile(file);
    // Create preview for original image immediately
    const objectUrl = URL.createObjectURL(file);
    setOriginalImage(objectUrl);
    setColorizedImage(null); // Reset previous result
  };

  const handleProcess = async () => {
    if (!selectedFile) return;

    try {
      setIsLoading(true);
      setError(null);

      // Prepare form data
      const formData = new FormData();
      formData.append("file", selectedFile);

      // Send to backend
      const response = await fetch("http://localhost:8000/colorize", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process image");
      }

      // Get result as blob
      const blob = await response.blob();
      const resultUrl = URL.createObjectURL(blob);
      setColorizedImage(resultUrl);

    } catch (err) {
      console.error(err);
      setError("Something went wrong. Please check if backend is running.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setOriginalImage(null);
    setColorizedImage(null);
    setError(null);
  };

  const handleDownload = () => {
    if (colorizedImage) {
      const a = document.createElement("a");
      a.href = colorizedImage;
      a.download = "colorized_image.png";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  };

  return (
    <main className="min-h-screen bg-[#0f1016] text-white selection:bg-purple-500/30 overflow-hidden font-sans">

      {/* Dynamic Background */}
      <div className="fixed inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-950 via-slate-950 to-purple-950 animate-gradient-xy opacity-50"></div>
        {/* Floating Orbs */}
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-600/20 rounded-full blur-[120px] animate-pulse"></div>
        <div className="absolute bottom-0 right-1/4 w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[150px]"></div>
      </div>

      {/* Grid Overlay */}
      <div className="fixed inset-0 z-0 opacity-[0.02]"
        style={{
          backgroundImage: 'linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px)',
          backgroundSize: '40px 40px'
        }}>
      </div>

      <div className="relative z-10 container mx-auto px-4 py-12 flex flex-col items-center min-h-screen">

        {/* Navbar / Brand */}
        <div className="w-full flex justify-between items-center mb-16 opacity-80 backdrop-blur-sm p-4 rounded-full border border-white/5 bg-black/20 max-w-5xl">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center shadow-lg shadow-purple-500/20">
              <Wand2 className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-lg tracking-wide">Developed by <span className="text-purple-400">Us</span></span>
          </div>
          <div className="text-xs font-mono text-slate-400 bg-white/5 px-2 py-1 rounded">SIC • Group Project</div>
        </div>

        {/* Hero Section */}
        <div className="text-center mb-16 space-y-6 max-w-3xl">
          <div className="inline-block px-4 py-1.5 rounded-full border border-purple-500/30 bg-purple-500/10 text-purple-300 text-xs font-medium tracking-wider mb-4 neon-border">
            DEEP LEARNING RESTORATION (GAN)
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight leading-tight">
            Relive the <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 text-glow">Colors</span> of the Past
          </h1>
          <p className="text-lg text-slate-400 max-w-xl mx-auto leading-relaxed">
            Transform historical black & white photography into vibrant reality using state-of-the-art deep learning models.
          </p>
        </div>

        {/* Main Interface */}
        <div className="w-full max-w-4xl">

          {/* Default View: Upload */}
          {!originalImage && !isLoading && (
            <div className="w-full flex justify-center animate-in fade-in zoom-in duration-700">
              <ImageUploader onFileSelect={handleFileSelect} />
            </div>
          )}

          {/* Preview State (New) */}
          {originalImage && !colorizedImage && !isLoading && (
            <div className="flex flex-col items-center gap-8 animate-in fade-in zoom-in duration-500">
              <div className="relative glass-panel p-2 rounded-2xl max-w-md w-full aspect-[4/3] neon-border overflow-hidden group">
                <img src={originalImage} alt="Preview" className="w-full h-full object-cover rounded-xl filter grayscale contrast-125" />
                <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <p className="text-white font-mono text-sm">ORIGINAL PREVIEW</p>
                </div>
              </div>

              <div className="flex gap-4">
                <button
                  onClick={handleReset}
                  className="px-6 py-3 rounded-xl bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleProcess}
                  className="group relative flex items-center gap-3 px-8 py-3 rounded-xl bg-gradient-to-r from-purple-600 to-blue-600 hover:scale-105 transition-all shadow-[0_0_30px_rgba(168,85,247,0.4)]"
                >
                  <Sparkles className="w-5 h-5 animate-pulse" />
                  <span className="font-bold tracking-wide">IGNITE COLORIZATION</span>
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
            </div>
          )}

          {/* Loading View */}
          {isLoading && (
            <div className="glass-panel w-full max-w-xl mx-auto h-64 rounded-2xl flex flex-col items-center justify-center p-12 space-y-6 animate-pulse neon-border">
              <div className="relative">
                <div className="absolute inset-0 bg-purple-500 blur-xl opacity-20 animate-ping"></div>
                <Loader2 className="relative w-16 h-16 animate-spin text-purple-400" />
              </div>
              <div className="text-center space-y-2">
                <p className="text-white text-xl font-medium tracking-wide">Neural Network Processing</p>
                <p className="text-slate-400 text-sm font-mono">Analyzing semantic context...</p>
              </div>
            </div>
          )}

          {/* Result View */}
          {originalImage && colorizedImage && !isLoading && (
            <div className="flex flex-col items-center gap-8 animate-in fade-in slide-in-from-bottom-8 duration-1000">

              <div className="glass-panel p-2 rounded-3xl w-full">
                <CompareSlider original={originalImage} colorized={colorizedImage} />
              </div>

              <div className="flex flex-wrap justify-center gap-4">
                <button
                  onClick={handleReset}
                  className="group flex items-center gap-2 px-8 py-3.5 rounded-xl bg-slate-900/80 hover:bg-slate-800 text-slate-300 hover:text-white border border-slate-700 hover:border-slate-500 transition-all duration-300 backdrop-blur-md"
                >
                  <RefreshCw className="w-4 h-4 group-hover:-rotate-180 transition-transform duration-500" />
                  <span>Process New Image</span>
                </button>

                <button
                  onClick={handleDownload}
                  className="group relative flex items-center gap-2 px-8 py-3.5 rounded-xl bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white font-medium shadow-lg shadow-purple-500/25 hover:shadow-purple-500/40 transition-all duration-300 overflow-hidden"
                >
                  <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 blur-md"></div>
                  <Download className="w-4 h-4 relative z-10" />
                  <span className="relative z-10">Save Enhancement</span>
                </button>
              </div>
            </div>
          )}

          {/* Error View */}
          {error && (
            <div className="mt-8 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-center backdrop-blur-md max-w-md mx-auto">
              <p className="font-semibold">Processing Failed</p>
              <p className="text-sm opacity-80">{error}</p>
            </div>
          )}

        </div>

        {/* Footer */}
        <div className="mt-20 text-slate-600 text-sm font-mono">
          POWERED BY PYTORCH & NEXT.JS
        </div>

      </div>
    </main>
  );
}
