'use client';

export default function PaywallCard({ brand }: { brand: string }) {
    const handlePayment = () => {
        // Logic to redirect using the constructed PayPal link
        // Using a generic link for now, in production this would be dynamic
        window.open(`https://www.paypal.me/baifan7575/9.99`, '_blank');
    };

    const handleAdminUnlock = () => {
        alert(`[SIMULATION]\n\nPAYMENT VERIFIED.\nGENERATING SECURE PDF FOR ${brand}...\n\n(In production, this would instantly download the file.)`);
    };

    return (
        <div className="bg-gradient-to-br from-slate-900 to-slate-800 border border-slate-700 p-6 rounded-xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 font-black text-9xl leading-none select-none">?</div>
            <h3 className="text-white text-xl font-bold mb-2">Defense Strategy</h3>
            <p className="text-slate-400 mb-6">
                AI Analysis has generated a 2,500-word comprehensive defense strategy specifically for sellers affected by {brand} enforcement.
            </p>
            <ul className="space-y-2 mb-8 text-slate-300">
                <li className="flex items-center gap-2">
                    <span className="text-green-500">✓</span> How to unfreeze funds (PayPal/Stripe)
                </li>
                <li className="flex items-center gap-2">
                    <span className="text-green-500">✓</span> Letter templates to Plaintiff attorney
                </li>
                <li className="flex items-center gap-2">
                    <span className="text-green-500">✓</span> Product liquidation safety guide
                </li>
            </ul>

            {/* The Paywall Button */}
            <button
                onClick={handlePayment}
                className="w-full bg-white text-black font-bold py-3 rounded-lg hover:bg-slate-200 transition-colors shadow-[0_0_20px_rgba(255,255,255,0.3)] flex items-center justify-center gap-2 group-hover:scale-[1.02] duration-200"
            >
                <span>UNLOCK FULL REPORT</span>
                <span className="bg-black text-white text-xs px-2 py-0.5 rounded">$9.99</span>
            </button>
            <p className="text-center text-xs text-slate-500 mt-3">
                Instant PDF Download • Secure Checkout via PayPal
            </p>

            {/* DEMO ONLY: Secret Unlock for Admin */}
            <div className="mt-4 text-center opacity-0 group-hover:opacity-100 transition-opacity duration-1000">
                <button
                    onClick={handleAdminUnlock}
                    className="text-[10px] text-slate-700 hover:text-green-500 uppercase tracking-widest border border-slate-800 hover:border-green-800 px-2 py-1 rounded transition-colors"
                >
                    [Admin] Simulate Unlock
                </button>
            </div>
        </div>
    );
}
