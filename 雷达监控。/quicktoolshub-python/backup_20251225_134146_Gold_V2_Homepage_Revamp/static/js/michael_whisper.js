console.log("🚀 MICHAEL WHISPER ENGINE STARTING...");

document.addEventListener('DOMContentLoaded', () => {
    console.log("✅ DOM Loaded. Searching for triggers...");

    // 1. Create Tooltip
    const tooltip = document.createElement('div');
    tooltip.className = 'michael-tooltip';
    tooltip.style.display = 'none'; // Default hidden
    tooltip.innerHTML = `
        <div class="michael-avatar"></div>
        <div class="michael-content">
            <span class="michael-name">Michael</span>
            <span class="michael-text">Start text...</span>
        </div>
    `;
    document.body.appendChild(tooltip);
    console.log("✅ Tooltip element injected into body.");

    // 2. Select Triggers
    const triggers = document.querySelectorAll('[data-michael-tip]');
    console.log(`Found ${triggers.length} triggers.`);

    triggers.forEach(el => {
        // Red border to confirm they are found
        el.style.border = "2px dashed red";

        el.addEventListener('mouseenter', (e) => {
            console.log("🖱️ Mouse Enter detected!");
            const text = el.getAttribute('data-michael-tip');
            const persona = el.getAttribute('data-michael-persona');

            showTooltip(el, text, persona);
        });

        el.addEventListener('mouseleave', () => {
            console.log("👋 Mouse Leave detected!");
            tooltip.style.display = 'none';
        });
    });

    function showTooltip(targetEl, text, persona) {
        console.log(`Showing tooltip: ${text}`);

        // Update Content
        const textEl = tooltip.querySelector('.michael-text');
        textEl.textContent = text;

        // Force Styles
        tooltip.style.display = 'block';
        tooltip.style.background = 'yellow'; // DEBUG COLOR
        tooltip.style.border = '2px solid black';
        tooltip.style.zIndex = '999999';

        // Position
        const rect = targetEl.getBoundingClientRect();
        const scrollTop = window.scrollY || document.documentElement.scrollTop;

        tooltip.style.top = (rect.top + scrollTop - 100) + 'px';
        tooltip.style.left = rect.left + 'px';
    }
});
