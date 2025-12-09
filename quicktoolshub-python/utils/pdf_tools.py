from PyPDF2 import PdfReader, PdfWriter
from pdf2docx import Converter
import os
from config import Config

def compress_pdf(input_path):
    """压缩 PDF 文件"""
    output_path = os.path.join(Config.UPLOAD_FOLDER, f'compressed_{os.path.basename(input_path)}')
    
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)
    
    # 压缩设置
    writer.compress_metadata = True
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    return output_path

def pdf_to_word(input_path):
    """将 PDF 转换为 Word"""
    output_path = os.path.join(Config.UPLOAD_FOLDER, f'{os.path.splitext(os.path.basename(input_path))[0]}.docx')
    
    cv = Converter(input_path)
    cv.convert(output_path)
    cv.close()
    
    return output_path

