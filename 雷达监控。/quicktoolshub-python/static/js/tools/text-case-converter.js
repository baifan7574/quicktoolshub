// Text Case Converter Tool - 纯前端实现
(function() {
    'use strict';
    
    function initTextCaseConverter() {
        const container = document.getElementById('text-case-converter-tool');
        if (!container) return;
        
        const inputTextarea = container.querySelector('#input-text');
        const outputTextarea = container.querySelector('#output-text');
        const caseSelect = container.querySelector('#case-type');
        
        if (!inputTextarea || !outputTextarea || !caseSelect) return;
        
        function convertText(input, type) {
            if (!input) return '';
            
            switch(type) {
                case 'lowercase':
                    return input.toLowerCase();
                case 'uppercase':
                    return input.toUpperCase();
                case 'title':
                    return input.toLowerCase().split(' ').map(word => 
                        word.charAt(0).toUpperCase() + word.slice(1)
                    ).join(' ');
                case 'sentence':
                    return input.toLowerCase().split(/[.!?]+\s*/).map(sentence => 
                        sentence.trim().charAt(0).toUpperCase() + sentence.trim().slice(1)
                    ).join('. ');
                case 'camel':
                    return input.toLowerCase().replace(/[^a-zA-Z0-9]+(.)/g, (_, chr) => chr.toUpperCase());
                case 'pascal':
                    const camel = convertText(input, 'camel');
                    return camel.charAt(0).toUpperCase() + camel.slice(1);
                case 'snake':
                    return input.toLowerCase().replace(/[^a-zA-Z0-9]+/g, '_').replace(/^_|_$/g, '');
                case 'kebab':
                    return input.toLowerCase().replace(/[^a-zA-Z0-9]+/g, '-').replace(/^-|-$/g, '');
                default:
                    return input;
            }
        }
        
        function updateOutput() {
            const converted = convertText(inputTextarea.value, caseSelect.value);
            outputTextarea.value = converted;
        }
        
        inputTextarea.addEventListener('input', updateOutput);
        caseSelect.addEventListener('change', updateOutput);
        
        // Copy button
        const copyBtn = container.querySelector('.copy-btn');
        if (copyBtn) {
            copyBtn.addEventListener('click', () => {
                outputTextarea.select();
                document.execCommand('copy');
                showNotification('Text copied to clipboard!', 'success');
            });
        }
        
        // Clear button
        const clearBtn = container.querySelector('.clear-btn');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                inputTextarea.value = '';
                outputTextarea.value = '';
            });
        }
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
        document.addEventListener('DOMContentLoaded', initTextCaseConverter);
    } else {
        initTextCaseConverter();
    }
})();

