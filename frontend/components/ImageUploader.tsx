"use client";

import { UploadCloud, FileUp } from "lucide-react";
import { useState, useCallback } from "react";

interface ImageUploaderProps {
    onFileSelect: (file: File) => void;
}

export default function ImageUploader({ onFileSelect }: ImageUploaderProps) {
    const [isDragging, setIsDragging] = useState(false);

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    }, []);

    const handleDrop = useCallback(
        (e: React.DragEvent) => {
            e.preventDefault();
            setIsDragging(false);
            if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                onFileSelect(e.dataTransfer.files[0]);
            }
        },
        [onFileSelect]
    );

    const handleChange = useCallback(
        (e: React.ChangeEvent<HTMLInputElement>) => {
            if (e.target.files && e.target.files[0]) {
                onFileSelect(e.target.files[0]);
            }
        },
        [onFileSelect]
    );

    return (
        <div
            className={`relative w-full max-w-xl h-64 rounded-2xl flex flex-col items-center justify-center transition-all duration-300 cursor-pointer overflow-hidden group ${isDragging
                    ? "neon-border bg-purple-500/10 scale-[1.02]"
                    : "border-2 border-dashed border-slate-700 bg-slate-900/40 hover:border-purple-500/50 hover:bg-slate-800/60 backdrop-blur-sm"
                }`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
        >
            <input
                type="file"
                accept="image/*"
                onChange={handleChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-50"
            />

            {/* Animated Background Grid */}
            <div className={`absolute inset-0 opacity-[0.03] pointer-events-none transition-opacity duration-500 ${isDragging ? "opacity-10" : "group-hover:opacity-10"}`}
                style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)', backgroundSize: '24px 24px' }}>
            </div>

            <div className="flex flex-col items-center gap-6 text-slate-400 z-10 transition-transform duration-300 group-hover:scale-105">
                <div className={`p-5 rounded-full transition-all duration-300 ${isDragging ? "bg-purple-500/20 shadow-[0_0_30px_rgba(168,85,247,0.3)]" : "bg-slate-800/80 group-hover:bg-purple-900/20"}`}>
                    {isDragging ? (
                        <FileUp className="w-10 h-10 text-purple-400 animate-bounce" />
                    ) : (
                        <UploadCloud className="w-10 h-10 text-slate-300 group-hover:text-purple-300 transition-colors" />
                    )}
                </div>
                <div className="text-center space-y-2">
                    <p className="font-semibold text-xl text-slate-200 group-hover:text-white transition-colors">
                        {isDragging ? "Drop to Scan" : "Click to Upload"}
                    </p>
                    <p className="text-sm text-slate-500 group-hover:text-slate-400">
                        or drag and drop your B&W photo
                    </p>
                </div>
            </div>
        </div>
    );
}
