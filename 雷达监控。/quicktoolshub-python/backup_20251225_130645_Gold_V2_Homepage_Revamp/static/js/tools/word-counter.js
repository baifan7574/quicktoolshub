// Word Counter Tool - 纯前端实现
(function() {
    'use strict';
    
    function initWordCounter() {
        const container = document.getElementById('word-counter-tool');
        if (!container) return;
        
        const textarea = container.querySelector('textarea');
        const statsContainer = container.querySelector('.word-stats');
        
        if (!textarea || !statsContainer) return;
        
        function calculateStats(text) {
            const trimmedText = text.trim();
            
            // Word count
            const words = trimmedText ? trimmedText.split(/\s+/).filter(word => word.length > 0) : [];
            
            // Character counts
            const characters = text.length;
            const charactersNoSpaces = text.replace(/\s/g, '').length;
            
            // Paragraph count
            const paragraphs = trimmedText ? trimmedText.split(/\n\s*\n/).filter(p => p.trim().length > 0).length || 1 : 0;
            
            // Sentence count
            const sentences = trimmedText ? trimmedText.split(/[.!?]+(\s|$)/).filter(s => s.trim().length > 0).length : 0;
            
            // Line count
            const lines = text ? text.split('\n').length : 0;
            
            return {
                words: words.length,
                characters,
                charactersNoSpaces,
                paragraphs,
                sentences: sentences || 1,
                lines
            };
        }
        
        function updateStats() {
            const stats = calculateStats(textarea.value);
            statsContainer.innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${stats.words.toLocaleString()}</div>
                    <div class="stat-label">Words</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.characters.toLocaleString()}</div>
                    <div class="stat-label">Characters</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.charactersNoSpaces.toLocaleString()}</div>
                    <div class="stat-label">Characters (no spaces)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.paragraphs.toLocaleString()}</div>
                    <div class="stat-label">Paragraphs</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.sentences.toLocaleString()}</div>
                    <div class="stat-label">Sentences</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.lines.toLocaleString()}</div>
                    <div class="stat-label">Lines</div>
                </div>
            `;
        }
        
        textarea.addEventListener('input', updateStats);
        updateStats();
        
        // Clear button
        const clearBtn = container.querySelector('.clear-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                textarea.value = '';
                updateStats();
            });
        }
    }
    
    // 初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWordCounter);
    } else {
        initWordCounter();
    }
})();

