// JSON Formatter Tool - 纯前端实现
(function() {
    'use strict';
    
    function initJSONFormatter() {
        const container = document.getElementById('json-formatter-tool');
        if (!container) return;
        
        const inputTextarea = container.querySelector('#json-input');
        const outputTextarea = container.querySelector('#json-output');
        const indentSelect = container.querySelector('#indent');
        const formatBtn = container.querySelector('.format-btn');
        const minifyBtn = container.querySelector('.minify-btn');
        const validateBtn = container.querySelector('.validate-btn');
        const copyBtn = container.querySelector('.copy-btn');
        const clearBtn = container.querySelector('.clear-btn');
        const errorDiv = container.querySelector('.error-message');
        
        if (!inputTextarea || !outputTextarea) return;
        
        function showError(message) {
            if (errorDiv) {
                errorDiv.textContent = message;
                errorDiv.style.display = 'block';
            }
        }
        
        function hideError() {
            if (errorDiv) {
                errorDiv.style.display = 'none';
            }
        }
        
        function formatJSON() {
            hideError();
            if (!inputTextarea.value.trim()) {
                outputTextarea.value = '';
                return;
            }
            
            try {
                const parsed = JSON.parse(inputTextarea.value);
                const indent = indentSelect ? parseInt(indentSelect.value) : 2;
                const formatted = JSON.stringify(parsed, null, indent);
                outputTextarea.value = formatted;
            } catch (e) {
                showError(e.message || 'Invalid JSON');
                outputTextarea.value = '';
            }
        }
        
        function minifyJSON() {
            hideError();
            if (!inputTextarea.value.trim()) {
                outputTextarea.value = '';
                return;
            }
            
            try {
                const parsed = JSON.parse(inputTextarea.value);
                const minified = JSON.stringify(parsed);
                outputTextarea.value = minified;
            } catch (e) {
                showError(e.message || 'Invalid JSON');
                outputTextarea.value = '';
            }
        }
        
        function validateJSON() {
            hideError();
            if (!inputTextarea.value.trim()) {
                showError('Please enter JSON to validate');
                return;
            }
            
            try {
                JSON.parse(inputTextarea.value);
                showNotification('✅ Valid JSON!', 'success');
            } catch (e) {
                showError(`❌ Invalid JSON: ${e.message}`);
            }
        }
        
        function copyOutput() {
            if (outputTextarea.value) {
                outputTextarea.select();
                document.execCommand('copy');
                showNotification('JSON copied to clipboard!', 'success');
            }
        }
        
        function clearAll() {
            inputTextarea.value = '';
            outputTextarea.value = '';
            hideError();
        }
        
        if (formatBtn) formatBtn.addEventListener('click', formatJSON);
        if (minifyBtn) minifyBtn.addEventListener('click', minifyJSON);
        if (validateBtn) validateBtn.addEventListener('click', validateJSON);
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
        document.addEventListener('DOMContentLoaded', initJSONFormatter);
    } else {
        initJSONFormatter();
    }
})();

