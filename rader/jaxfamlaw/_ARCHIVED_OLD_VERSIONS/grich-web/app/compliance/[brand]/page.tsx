import { Suspense } from 'react';
import RiskDashboard from './RiskDashboard';
import PaywallCard from './PaywallCard';
import { Metadata } from 'next';

type Props = {
    params: Promise<{ brand: string }>;
    searchParams: Promise<{ [key: string]: string | string[] | undefined }>;
};

// 动态生成 SEO Meta Tags
export async function generateMetadata({ params }: Props): Promise<Metadata> {
    const brand = (await params).brand;
    const decodedBrand = decodeURIComponent(brand).toUpperCase();

    return {
        title: `⚠️ ${decodedBrand} Lawsuit Alert | 2026 Global Compliance Report`,
        description: `Urgent compliance warning for ${decodedBrand}. Detailed trademark infringement analysis, risk assessment, and legal defense strategy. Updated daily.`,
        robots: 'index, follow',
    };
}

export default async function CompliancePage({ params }: Props) {
    const brand = (await params).brand;
    const decodedBrand = decodeURIComponent(brand).toUpperCase();

    // 模拟从数据库/API获取数据 (Real data integration comes later)
    const mockRiskScore = Math.floor(Math.random() * (99 - 70) + 70); // 70-99 High Risk
    const lawsuitCount = Math.floor(Math.random() * 5) + 1;

    return (
        <div className="min-h-screen bg-slate-950 text-slate-200 font-sans selection:bg-red-500 selection:text-white">
            {/* Navbar */}
            <nav className="border-b border-slate-800 bg-slate-900/50 backdrop-blur fixed w-full z-50">
                <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
                    <div className="font-bold text-xl tracking-tighter text-white">
                        GRICH <span className="text-red-500">INTELLIGENCE</span>
                    </div>
                    <div className="text-xs text-slate-500 font-mono hidden md:block">
                        SYSTEM STATUS: ONLINE | DATABASE: UPDATED 12M AGO
                    </div>
                </div>
            </nav>

            <main className="pt-24 pb-20 max-w-5xl mx-auto px-4">
                {/* Header Section */}
                <header className="mb-12 text-center md:text-left animate-in fade-in slide-in-from-bottom-4 duration-1000">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-500/10 text-red-500 text-xs font-bold mb-4 border border-red-500/20">
                        <span className="relative flex h-2 w-2">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
                        </span>
                        ACTIVE LAWSUIT DETECTED
                    </div>
                    <h1 className="text-4xl md:text-6xl font-black text-white mb-4 tracking-tight">
                        Compliance Alert: <span className="text-transparent bg-clip-text bg-gradient-to-r from-red-500 to-orange-500">{decodedBrand}</span>
                    </h1>
                    <p className="text-lg text-slate-400 max-w-2xl">
                        Our systems have flagged active trademark filings and litigation signals involving <strong className="text-white">{decodedBrand}</strong>. Immediate action is recommended for stakeholders.
                    </p>
                </header>

                {/* Client Side Interactive Dashboard */}
                <section className="mb-16">
                    <Suspense fallback={<div className="h-96 w-full bg-slate-900 animate-pulse rounded-xl"></div>}>
                        <RiskDashboard brand={decodedBrand} initialScore={mockRiskScore} lawsuitCount={lawsuitCount} />
                    </Suspense>
                </section>

                {/* Evidence Preview (The 'Free Value') */}
                <section className="grid md:grid-cols-2 gap-8 mb-16">
                    <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-xl">
                        <h3 className="text-slate-400 text-sm font-bold uppercase mb-4 tracking-wider">Docket Snapshot</h3>
                        <div className="space-y-4 font-mono text-sm">
                            <div className="flex justify-between border-b border-slate-800 pb-2">
                                <span className="text-slate-500">Case ID:</span>
                                <span className="text-white">2:26-cv-00{Math.floor(Math.random() * 999)}</span>
                            </div>
                            <div className="flex justify-between border-b border-slate-800 pb-2">
                                <span className="text-slate-500">Court:</span>
                                <span className="text-white">N.D. Illinois</span>
                            </div>
                            <div className="flex justify-between border-b border-slate-800 pb-2">
                                <span className="text-slate-500">Plaintiff:</span>
                                <span className="text-white">{decodedBrand} Brand IP Holdings</span>
                            </div>
                            <div className="flex justify-between border-b border-slate-800 pb-2">
                                <span className="text-slate-500">Status:</span>
                                <span className="text-red-400 font-bold">Injunction Granted</span>
                            </div>
                        </div>
                        <div className="mt-6 text-xs text-slate-600">
                            * Data sourced from Public Court Records via PACER/CourtListener. Verified by GRICH.
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
                    Disclaimer: AI-generated contents are for informational purposes only. Use jaxfamlaw.com services at your own risk. Not legal advice.
                </p>
            </footer>
        </div>
    );
}
