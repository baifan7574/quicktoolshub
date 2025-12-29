from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from config import Config
from utils.pdf_tools import compress_pdf, pdf_to_word, merge_pdfs, split_pdf
from utils.image_tools import remove_background, compress_image, resize_image, convert_image

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

@bp.route('/merge-pdf', methods=['POST'])
def merge_pdf_api():
    """PDF 合并 API"""
    if 'files' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    files = request.files.getlist('files')
    if len(files) < 2:
        return jsonify({'error': '至少需要上传 2 个 PDF 文件'}), 400
    
    try:
        # 保存所有上传的文件
        filepaths = []
        for file in files:
            if file.filename != '':
                filename = secure_filename(file.filename)
                filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
                file.save(filepath)
                filepaths.append(filepath)
        
        if len(filepaths) < 2:
            return jsonify({'error': '至少需要 2 个有效的 PDF 文件'}), 400
        
        # 合并 PDF
        merged_filepath = merge_pdfs(filepaths)
        
        # 返回合并后的文件
        return send_file(merged_filepath, as_attachment=True, download_name='merged.pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/split-pdf', methods=['POST'])
def split_pdf_api():
    """PDF 分割 API"""
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    method = request.form.get('method', 'range')
    pages_spec = request.form.get('pages', '')
    
    if not pages_spec:
        return jsonify({'error': '请指定要提取的页面'}), 400
    
    try:
        # 保存上传的文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # 分割 PDF
        split_filepath = split_pdf(filepath, method, pages_spec)
        
        # 返回分割后的文件
        return send_file(split_filepath, as_attachment=True, download_name='split.pdf')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/compress-image', methods=['POST'])
def compress_image_api():
    """图片压缩 API"""
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    # 获取压缩质量参数
    quality = int(request.form.get('quality', 85))
    
    try:
        # 保存上传的文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # 压缩图片
        compressed_filepath = compress_image(filepath, quality)
        
        # 返回压缩后的文件
        return send_file(compressed_filepath, as_attachment=True, download_name=f'compressed_{filename}')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/resize-image', methods=['POST'])
def resize_image_api():
    """图片调整尺寸 API"""
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    # 获取尺寸参数
    width = request.form.get('width')
    height = request.form.get('height')
    maintain_aspect = request.form.get('maintain_aspect', 'true').lower() == 'true'
    
    # 转换为整数
    width = int(width) if width and width.strip() else None
    height = int(height) if height and height.strip() else None
    
    if not width and not height:
        return jsonify({'error': '必须指定宽度或高度'}), 400
    
    try:
        # 保存上传的文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # 调整尺寸
        resized_filepath = resize_image(filepath, width, height, maintain_aspect)
        
        # 返回调整后的文件
        return send_file(resized_filepath, as_attachment=True, download_name=os.path.basename(resized_filepath))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/convert-image', methods=['POST'])
def convert_image_api():
    """图片格式转换 API"""
    if 'file' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    # 获取目标格式和质量参数
    output_format = request.form.get('format', 'jpg').lower()
    quality = int(request.form.get('quality', 95))
    
    # 验证格式
    if output_format not in ['jpg', 'jpeg', 'png', 'webp']:
        return jsonify({'error': '不支持的格式。支持: jpg, png, webp'}), 400
    
    try:
        # 保存上传的文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # 转换格式
        converted_filepath = convert_image(filepath, output_format, quality)
        
        # 返回转换后的文件
        return send_file(converted_filepath, as_attachment=True, download_name=os.path.basename(converted_filepath))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
