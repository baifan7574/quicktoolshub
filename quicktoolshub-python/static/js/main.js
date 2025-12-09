// 主要 JavaScript 功能

// 文件上传处理
function handleFileUpload(formId, endpoint, onSuccess, onError) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        
        // 显示加载状态
        submitBtn.disabled = true;
        submitBtn.textContent = '处理中...';
        
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                // 下载文件
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = response.headers.get('Content-Disposition')?.split('filename=')[1] || 'download';
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                if (onSuccess) onSuccess();
            } else {
                const error = await response.json();
                if (onError) onError(error.error || '处理失败');
                else alert(error.error || '处理失败');
            }
        } catch (error) {
            if (onError) onError(error.message);
            else alert('处理失败: ' + error.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });
}

// 初始化文件上传
document.addEventListener('DOMContentLoaded', () => {
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
});

