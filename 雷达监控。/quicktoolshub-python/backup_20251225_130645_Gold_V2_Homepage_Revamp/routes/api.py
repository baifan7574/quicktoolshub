from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from config import Config
from utils.pdf_tools import compress_pdf, pdf_to_word
from utils.image_tools import remove_background

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/health')
def health():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': __import__('datetime').datetime.now().isoformat()
    })

@bp.route('/compress-pdf', methods=['POST'])
def compress_pdf_api():
    """PDF 压缩 API"""
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    try:
        # 保存上传的文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # 压缩 PDF
        compressed_filepath = compress_pdf(filepath)
        
        # 返回压缩后的文件
        return send_file(compressed_filepath, as_attachment=True, download_name=f'compressed_{filename}')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/pdf-to-word', methods=['POST'])
def pdf_to_word_api():
    """PDF 转 Word API"""
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    try:
        # 保存上传的文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # 转换 PDF 到 Word
        word_filepath = pdf_to_word(filepath)
        
        # 返回 Word 文件
        return send_file(word_filepath, as_attachment=True, download_name=f'{os.path.splitext(filename)[0]}.docx')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/remove-background', methods=['POST'])
def remove_background_api():
    """背景移除 API"""
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    try:
        # 保存上传的文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # 移除背景
        result_filepath = remove_background(filepath)
        
        # 返回处理后的文件
        return send_file(result_filepath, as_attachment=True, download_name=f'no_bg_{filename}')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({'error': 'Content required'}), 400
    
    req_type = data.get('type', 'issue')
    content = data.get('content')
    tool_slug = data.get('tool_slug')
    contact = data.get('contact')
    
    from utils.supabase_client import get_supabase
    supabase = get_supabase()
    if not supabase:
        return jsonify({'error': 'DB not configured'}), 500
    
    try:
        supabase.table('user_feedback').insert({
            'type': req_type,
            'content': content,
            'tool_slug': tool_slug,
            'contact': contact
        }).execute()
        return jsonify({'message': 'Feedback received!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

