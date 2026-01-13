import { Suspense } from 'react';
import RiskDashboard from '../RiskDashboard';
import PaywallCard from '../PaywallCard';
import { Metadata } from 'next';

type Props = {
    params: Promise<{ brand: string; scenario: string[] }>;
    searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
};

// 动态生成 SEO Meta Tags (Matrix Version)
export async function generateMetadata({ params }: Props): Promise<Metadata> {
    const brand = (await params).brand;
    const scenario = (await params).scenario;

    const decodedBrand = decodeURIComponent(brand).toUpperCase();
    // Join scenario array into a readable string (e.g. "frozen funds")
    const keywords = scenario.map(s => decodeURIComponent(s)).join(' ');
    const titleKeywords = keywords.charAt(0).toUpperCase() + keywords.slice(1);

    return {
        title: `⚠️ ${decodedBrand} ${titleKeywords} Alert | 2026 Compliance Report`,
        description: `Urgent ${keywords} warning for ${decodedBrand}. Specific analysis regarding ${keywords}, trademark infringement, and funds release strategies.`,
        robots: 'index, follow',
    };
}

export default async function ScenarioPage({ params }: Props) {
    const brand = (await params).brand;
    const scenario = (await params).scenario;

    const decodedBrand = decodeURIComponent(brand).toUpperCase();
    const keywords = scenario.map(s => decodeURIComponent(s)).join(' ');
    const displayKeywords = keywords.toUpperCase();

    // 模拟从数据库/API获取数据
    const mockRiskScore = Math.floor(Math.random() * (99 - 80) + 80); // Higher risk for specific scenarios
    const lawsuitCount = Math.floor(Math.random() * 5) + 3;

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-red-500 selection:text-white">
            {/* Navbar */}
            <nav className="border-b border-slate-800 bg-slate-900/50 backdrop-blur fixed w-full z-50">
                <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
                    <div className="font-bold text-xl tracking-tighter text-white">
                        GRICH <span className="text-red-500">MATRIX</span>
                    </div>
                    <div className="text-xs text-slate-500 font-mono hidden md:block">
                        SYSTEM STATUS: ONLINE | TARGET: {displayKeywords}
                    </div>
                </div>
            </nav>

            <main className="pt-24 pb-20 max-w-5xl mx-auto px-4">
                {/* Header Section (Specific Scenario) */}
                <header className="mb-12 text-center md:text-left animate-in fade-in slide-in-from-bottom-4 duration-1000">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-500/10 text-red-500 text-xs font-bold mb-4 border border-red-500/20">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
                        </span>
                        SPECIFIC THREAT: {displayKeywords}
                    </div>
                    <h1 className="text-4xl md:text-6xl font-black text-white mb-4 tracking-tight">
                        <span className="text-slate-400">{decodedBrand}:</span> <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-orange-500">{displayKeywords}</span>
                    </h1>
                    <p className="text-lg text-slate-400 max-w-2xl">
                        A focused compliance report addressing <strong className="text-white">{displayKeywords}</strong> issues related to <strong>{decodedBrand}</strong>. Includes recovery protocols and legal precedents.
                    </p>
                </header>

                {/* Client Side Interactive Dashboard */}
                <section className="mb-16">
                    <Suspense fallback={<div className="h-96 w-full bg-slate-900 animate-pulse rounded-xl"></div>}>
                        {/* We reuse the dashboard, but potentially it should know the scenario context too. 
                            For now, passing brand is enough to trigger the specific AI report. */}
                        <RiskDashboard brand={`${decodedBrand} ${displayKeywords}`} initialScore={mockRiskScore} lawsuitCount={lawsuitCount} />
                    </Suspense>
                </section>

                {/* Evidence Preview */}
                <section className="grid md:grid-cols-2 gap-8 mb-16">
                    <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-xl">
                        <h3 className="text-slate-400 text-sm font-bold uppercase mb-4 tracking-wider">Docket Context</h3>
                        <div className="space-y-4 font-mono text-sm">
                            <div className="flex justify-between border-b border-slate-800 pb-2">
                                <span className="text-slate-500">Related Case:</span>
                                <span className="text-white">2:26-cv-00{Math.floor(Math.random() * 999)}</span>
                            </div>
                            <div className="flex justify-between border-b border-slate-800 pb-2">
                                <span className="text-slate-500">Impact Area:</span>
                                <span className="text-red-400">{displayKeywords}</span>
                            </div>

                            <div className="mt-4 p-3 bg-red-950/20 border border-red-900/30 rounded text-red-200 text-xs leading-relaxed">
                                ⚠️ SYSTEM FLAG: High correlation detected between {decodedBrand} enforcement actions and {displayKeywords}.
                            </div>
                        </div>
                    </div>

                    {/* Paywall Card */}
                    <PaywallCard brand={decodedBrand} />
                </section>

            </main>

            {/* Footer */}
            <footer className="border-t border-slate-900 bg-slate-950 py-12 text-center text-slate-600 text-sm">
                <p>© 2026 GRICH Global Regulatory Intelligence Hub. All rights reserved.</p>
                <p className="mt-2 text-xs opacity-50">
                    Targeted Intelligence Report: {decodedBrand} / {displayKeywords}
                </p>
            </footer>
        </div>
    );
}
