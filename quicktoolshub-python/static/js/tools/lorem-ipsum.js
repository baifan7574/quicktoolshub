// Lorem Ipsum Generator Tool - 纯前端实现
(function() {
    'use strict';
    
    const loremWords = [
        'lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit',
        'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
        'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis', 'nostrud',
        'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip', 'ex', 'ea', 'commodo',
        'consequat', 'duis', 'aute', 'irure', 'in', 'reprehenderit', 'voluptate', 'velit',
        'esse', 'cillum', 'fugiat', 'nulla', 'pariatur', 'excepteur', 'sint', 'occaecat',
        'cupidatat', 'non', 'proident', 'sunt', 'culpa', 'qui', 'officia', 'deserunt',
        'mollit', 'anim', 'id', 'est', 'laborum'
    ];
    
    function initLoremIpsum() {
        const container = document.getElementById('lorem-ipsum-tool');
        if (!container) return;
        
        const typeSelect = container.querySelector('#type');
        const countInput = container.querySelector('#count');
        const outputTextarea = container.querySelector('#lorem-output');
        const generateBtn = container.querySelector('.generate-btn');
        const copyBtn = container.querySelector('.copy-btn');
        const clearBtn = container.querySelector('.clear-btn');
        
        if (!typeSelect || !countInput || !outputTextarea) return;
        
        function generateWords(num) {
            const words = [];
            for (let i = 0; i < num; i++) {
                words.push(loremWords[i % loremWords.length]);
            }
            return words.join(' ');
        }
        
        function generateSentence() {
            const wordCount = Math.floor(Math.random() * 10) + 5; // 5-15 words
            const words = generateWords(wordCount);
            return words.charAt(0).toUpperCase() + words.slice(1) + '.';
        }
        
        function generateParagraph() {
            const sentenceCount = Math.floor(Math.random() * 3) + 3; // 3-5 sentences
            const sentences = [];
            for (let i = 0; i < sentenceCount; i++) {
                sentences.push(generateSentence());
            }
            return sentences.join(' ');
        }
        
        function generate() {
            const type = typeSelect.value;
            const count = parseInt(countInput.value) || 5;
            let result = '';
            
            if (type === 'words') {
                result = generateWords(count);
            } else if (type === 'sentences') {
                const sentences = [];
                for (let i = 0; i < count; i++) {
                    sentences.push(generateSentence());
                }
                result = sentences.join(' ');
            } else if (type === 'paragraphs') {
                const paragraphs = [];
                for (let i = 0; i < count; i++) {
                    paragraphs.push(generateParagraph());
                }
                result = paragraphs.join('\n\n');
            }
            
            outputTextarea.value = result;
        }
        
        function copyOutput() {
            if (outputTextarea.value) {
                outputTextarea.select();
                document.execCommand('copy');
                showNotification('Text copied to clipboard!', 'success');
            }
        }
        
        function clearAll() {
            outputTextarea.value = '';
        }
        
        if (generateBtn) generateBtn.addEventListener('click', generate);
        if (copyBtn) copyBtn.addEventListener('click', copyOutput);
        if (clearBtn) clearBtn.addEventListener('click', clearAll);
    }
    
    function showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#10b981' : '#2563eb'};
            color: white;
            border-radius: 8px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            z-index: 1000;
            animation: fadeIn 0.3s ease-out;
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'fadeOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initLoremIpsum);
    } else {
        initLoremIpsum();
    }
})();

