// 主要 JavaScript 功能

// 显示通知
function showNotification(message, type = 'info') {
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
        max-width: 400px;
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// 创建进度条
function createProgressBar(container) {
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    progressBar.innerHTML = '<div class="progress-bar-fill" style="width: 0%"></div>';
    container.appendChild(progressBar);
    return progressBar.querySelector('.progress-bar-fill');
}

// 文件上传处理（增强版）
function handleFileUpload(formId, endpoint, onSuccess, onError) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    const fileInput = form.querySelector('input[type="file"]');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (!fileInput || !submitBtn) return;
    
    // 创建文件上传区域
    const uploadArea = document.createElement('div');
    uploadArea.className = 'file-upload-area';
    uploadArea.innerHTML = `
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-bottom: 1rem; color: #6b7280;">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
            <polyline points="17 8 12 3 7 8"></polyline>
            <line x1="12" y1="3" x2="12" y2="15"></line>
        </svg>
        <p style="margin-bottom: 0.5rem; font-weight: 500;">点击选择文件或拖拽文件到此处</p>
        <p style="font-size: 0.875rem; color: #6b7280;">支持拖拽上传</p>
    `;
    
    // 替换文件输入
    fileInput.style.display = 'none';
    fileInput.parentNode.insertBefore(uploadArea, fileInput);
    
    // 点击上传区域选择文件
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // 拖拽上传
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            updateFileDisplay(uploadArea, e.dataTransfer.files[0]);
        }
    });
    
    // 文件选择后更新显示
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            updateFileDisplay(uploadArea, e.target.files[0]);
        }
    });
    
    // 更新文件显示
    function updateFileDisplay(area, file) {
        const fileSize = (file.size / 1024 / 1024).toFixed(2);
        area.innerHTML = `
            <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem; background: white; border-radius: 8px; border: 1px solid #e5e7eb;">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="color: #2563eb;">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                    <polyline points="14 2 14 8 20 8"></polyline>
                </svg>
                <div style="flex: 1; text-align: left;">
                    <p style="font-weight: 500; margin-bottom: 0.25rem;">${file.name}</p>
                    <p style="font-size: 0.875rem; color: #6b7280;">${fileSize} MB</p>
                </div>
                <button type="button" onclick="this.closest('form').querySelector('input[type=file]').value=''; this.closest('.file-upload-area').innerHTML='点击选择文件或拖拽文件到此处';" style="background: none; border: none; color: #ef4444; cursor: pointer; padding: 0.5rem;">
                    ✕
                </button>
            </div>
        `;
    }
    
    // 表单提交
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        if (!fileInput.files || fileInput.files.length === 0) {
            showNotification('请先选择文件', 'error');
            return;
        }
        
        const formData = new FormData(form);
        const originalText = submitBtn.innerHTML;
        
        // 显示加载状态
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> 处理中...';
        
        // 创建进度条
        const progressContainer = document.createElement('div');
        progressContainer.style.marginTop = '1rem';
        form.appendChild(progressContainer);
        const progressFill = createProgressBar(progressContainer);
        
        try {
            // 模拟进度（实际应该使用 XMLHttpRequest 获取真实进度）
            let progress = 0;
            const progressInterval = setInterval(() => {
                progress += 10;
                if (progress <= 90) {
                    progressFill.style.width = progress + '%';
                }
            }, 200);
            
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });
            
            clearInterval(progressInterval);
            progressFill.style.width = '100%';
            
            if (response.ok) {
                // 下载文件
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                
                // 从响应头获取文件名
                const contentDisposition = response.headers.get('Content-Disposition');
                if (contentDisposition) {
                    const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
                    if (filenameMatch) {
                        a.download = filenameMatch[1].replace(/['"]/g, '');
                    }
                }
                
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                showNotification('处理成功！文件已下载', 'success');
                
                // 重置表单
                setTimeout(() => {
                    form.reset();
                    uploadArea.innerHTML = '点击选择文件或拖拽文件到此处';
                    progressContainer.remove();
                }, 1000);
                
                if (onSuccess) onSuccess();
            } else {
                const error = await response.json().catch(() => ({ error: '处理失败' }));
                const errorMsg = error.error || '处理失败';
                showNotification(errorMsg, 'error');
                if (onError) onError(errorMsg);
            }
        } catch (error) {
            showNotification('处理失败: ' + error.message, 'error');
            if (onError) onError(error.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
            progressContainer.remove();
        }
    });
}

// 添加 CSS 动画
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; transform: translateX(0); }
        to { opacity: 0; transform: translateX(100px); }
    }
`;
document.head.appendChild(style);

// 初始化文件上传
document.addEventListener('DOMContentLoaded', () => {
    // 添加淡入动画
    document.body.classList.add('fade-in');
    
    // PDF 压缩
    if (document.getElementById('compress-pdf-form')) {
        handleFileUpload('compress-pdf-form', '/api/compress-pdf');
    }
    
    // PDF 转 Word
    if (document.getElementById('pdf-to-word-form')) {
        handleFileUpload('pdf-to-word-form', '/api/pdf-to-word');
    }
    
    // 背景移除
    if (document.getElementById('remove-background-form')) {
        handleFileUpload('remove-background-form', '/api/remove-background');
    }
    
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

