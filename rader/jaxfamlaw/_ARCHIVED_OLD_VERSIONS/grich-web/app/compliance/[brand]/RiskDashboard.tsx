'use client';

import { useEffect, useState } from 'react';

export default function RiskDashboard({ brand, initialScore, lawsuitCount }: { brand: string, initialScore: number, lawsuitCount: number }) {
    const [score, setScore] = useState(0);
    const [typedText, setTypedText] = useState('');
    const fullText = `Analyzing global litigation databases... Found ${lawsuitCount} active cases against ${brand}... Cross-referencing 32 state court records... DETECTED PRELIMINARY INJUNCTION REQUEST... CALCULATING FINANCIAL RISK EXPOSURE...`;

    // Score Animation
    useEffect(() => {
        const timer = setTimeout(() => {
            let current = 0;
            const interval = setInterval(() => {
                current += 1;
                if (current >= initialScore) {
                    current = initialScore;
                    clearInterval(interval);
                }
                setScore(current);
            }, 20);
            return () => clearInterval(interval);
        }, 500); // Delay start
        return () => clearTimeout(timer);
    }, [initialScore]);

    // Fetch Real AI Data (Streaming)
    useEffect(() => {
        let isMounted = true;

        const fetchAIAnalysis = async () => {
            // Initial hacker-style loading text
            setTypedText("INITIALIZING SECURE CONNECTION TO DEEPSEEK NEURAL NET...\n");

            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ brand }),
                });

                if (!response.body) return;

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let firstChunk = true;

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    if (!isMounted) break;

                    const chunk = decoder.decode(value);

                    // Clear loading text on first real byte
                    if (firstChunk) {
                        setTypedText("");
                        firstChunk = false;
                    }

                    // Simulate typing effect for the chunk (smoother UX)
                    for (let i = 0; i < chunk.length; i++) {
                        if (!isMounted) break;
                        setTypedText(prev => prev + chunk[i]);
                        // Tiny random delay for realism
                        await new Promise(r => setTimeout(r, Math.random() * 15 + 5));
                    }
                }
            } catch (error) {
                setTypedText("\n[ERROR] CONNECTION TERMINATED. RETRYING...");
            }
        };

        fetchAIAnalysis();

        return () => { isMounted = false; };
    }, [brand]);

    // Color logic
    const getColor = (s: number) => {
        if (s < 30) return 'text-green-500 stroke-green-500';
        if (s < 70) return 'text-yellow-500 stroke-yellow-500';
        return 'text-red-500 stroke-red-500';
    }

    const colorClass = getColor(score);

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 md:p-8 relative overflow-hidden">
            {/* Background Grid */}
            <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20"></div>

            <div className="flex flex-col md:flex-row items-center gap-8 relative z-10">
                {/* Gauge Chart */}
                <div className="relative w-48 h-48 flex-shrink-0">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="#1e293b" strokeWidth="8" />
                        <circle
                            cx="50" cy="50" r="45" fill="none"
                            stroke="currentColor"
                            strokeWidth="8"
                            strokeDasharray="283"
                            strokeDashoffset={283 - (283 * score) / 100}
                            className={`transition-all duration-1000 ease-out ${colorClass.split(' ')[1]}`}
                            strokeLinecap="round"
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className={`text-4xl font-black ${colorClass.split(' ')[0]}`}>{score}</span>
                        <span className="text-slate-500 text-xs font-bold uppercase mt-1">Risk Index</span>
                    </div>
                </div>

                {/* AI Console */}
                <div className="flex-1 w-full">
                    <div className="flex items-center gap-2 mb-2">
                        <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
                        <h2 className="text-sm font-bold text-slate-300 uppercase tracking-widest">AI Live Analysis Protocol</h2>
                    </div>
                    <div className="h-32 bg-black/50 rounded-lg p-4 border border-slate-800 font-mono text-sm text-green-400 overflow-y-auto w-full">
                        {typedText}
                        <span className="animate-pulse">_</span>
                    </div>
                </div>
            </div>
        </div>
    );
}
