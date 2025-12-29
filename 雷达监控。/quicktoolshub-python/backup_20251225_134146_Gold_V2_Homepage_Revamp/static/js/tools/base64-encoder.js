// Base64 Encoder/Decoder Tool - 纯前端实现
(function() {
    'use strict';
    
    function initBase64Encoder() {
        const container = document.getElementById('base64-encoder-tool');
        if (!container) return;
        
        const inputTextarea = container.querySelector('#base64-input');
        const outputTextarea = container.querySelector('#base64-output');
        const encodeRadio = container.querySelector('#mode-encode');
        const decodeRadio = container.querySelector('#mode-decode');
        const convertBtn = container.querySelector('.convert-btn');
        const copyBtn = container.querySelector('.copy-btn');
        const clearBtn = container.querySelector('.clear-btn');
        
        if (!inputTextarea || !outputTextarea) return;
        
        function encode() {
            try {
                const encoded = btoa(unescape(encodeURIComponent(inputTextarea.value)));
                outputTextarea.value = encoded;
            } catch (e) {
                outputTextarea.value = 'Error encoding text';
            }
        }
        
        function decode() {
            try {
                const decoded = decodeURIComponent(escape(atob(inputTextarea.value)));
                outputTextarea.value = decoded;
            } catch (e) {
                outputTextarea.value = 'Error decoding text. Please check if the input is valid Base64.';
            }
        }
        
        function convert() {
            if (encodeRadio && encodeRadio.checked) {
                encode();
            } else if (decodeRadio && decodeRadio.checked) {
                decode();
            }
        }
        
        function copyOutput() {
            if (outputTextarea.value) {
                outputTextarea.select();
                document.execCommand('copy');
                showNotification('Text copied to clipboard!', 'success');
            }
        }
        
        function clearAll() {
            inputTextarea.value = '';
            outputTextarea.value = '';
        }
        
        if (convertBtn) convertBtn.addEventListener('click', convert);
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
        document.addEventListener('DOMContentLoaded', initBase64Encoder);
    } else {
        initBase64Encoder();
    }
})();

