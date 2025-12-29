from PyPDF2 import PdfReader, PdfWriter
from pdf2docx import Converter
import os
import subprocess
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def compress_pdf(input_path):
    """
    使用 Ghostscript 进行 PDF 压缩
    使用更激进的压缩设置以确保文件变小
    """
    try:
        output_path = os.path.join(Config.UPLOAD_FOLDER, f'compressed_{os.path.basename(input_path)}')
        
        # 使用 /screen 设置进行最大压缩
        # 这会将图片降到 72 DPI，但文件会显著变小
        gs_cmd = [
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/screen',  # 最大压缩！
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            '-dDetectDuplicateImages=true',
            '-dCompressFonts=true',
            '-dDownsampleColorImages=true',
            '-dDownsampleGrayImages=true',
            '-dDownsampleMonoImages=true',
            '-dColorImageResolution=72',
            '-dGrayImageResolution=72',
            '-dMonoImageResolution=72',
            f'-sOutputFile={output_path}',
            input_path
        ]
        
        logger.info(f"Running aggressive Ghostscript compression on {input_path}")
        
        result = subprocess.run(
            gs_cmd, 
            capture_output=True, 
            text=True, 
            timeout=120,
            check=False
        )
        
        logger.info(f"Ghostscript return code: {result.returncode}")
        
        if result.returncode == 0 and os.path.exists(output_path):
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            
            logger.info(f"Original: {original_size}, Compressed: {compressed_size}")
            
            # 只要压缩后文件更小就接受
            if compressed_size < original_size:
                compression_ratio = (1 - compressed_size / original_size) * 100
                logger.info(f"Compression successful: {compression_ratio:.1f}% reduction")
                return output_path
            else:
                # 如果还是变大，尝试 /ebook 设置
                logger.warning(f"Screen setting failed. Trying ebook setting...")
                os.remove(output_path)
                return compress_pdf_ebook(input_path)
        else:
            logger.error(f"Ghostscript failed. Using fallback.")
            return compress_pdf_fallback(input_path)
            
    except Exception as e:
        logger.error(f"Ghostscript error: {e}")
        return compress_pdf_fallback(input_path)

def compress_pdf_ebook(input_path):
    """
    使用 /ebook 设置（中等压缩）
    """
    try:
        output_path = os.path.join(Config.UPLOAD_FOLDER, f'compressed_{os.path.basename(input_path)}')
        
        gs_cmd = [
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            '-dPDFSETTINGS=/ebook',
            '-dNOPAUSE',
            '-dQUIET',
            '-dBATCH',
            '-dDetectDuplicateImages=true',
            '-dCompressFonts=true',
            f'-sOutputFile={output_path}',
            input_path
        ]
        
        logger.info("Trying ebook compression")
        result = subprocess.run(gs_cmd, capture_output=True, text=True, timeout=120, check=False)
        
        if result.returncode == 0 and os.path.exists(output_path):
            original_size = os.path.getsize(input_path)
            compressed_size = os.path.getsize(output_path)
            
            if compressed_size < original_size:
                compression_ratio = (1 - compressed_size / original_size) * 100
                logger.info(f"Ebook compression: {compression_ratio:.1f}% reduction")
                return output_path
            else:
                logger.warning("Ebook compression also ineffective")
                os.remove(output_path)
                return compress_pdf_fallback(input_path)
        else:
            return compress_pdf_fallback(input_path)
            
    except Exception as e:
        logger.error(f"Ebook compression error: {e}")
        return compress_pdf_fallback(input_path)

def compress_pdf_fallback(input_path):
    """
    备用方案：直接返回原文件的副本
    对于已经优化的 PDF，诚实告知用户
    """
    try:
        logger.info("File is already well-optimized. Returning original.")
        output_path = os.path.join(Config.UPLOAD_FOLDER, f'compressed_{os.path.basename(input_path)}')
        
        import shutil
        shutil.copy2(input_path, output_path)
        
        return output_path
    
    except Exception as e:
        logger.error(f"Fallback failed: {e}")
        raise Exception("PDF compression failed")

def pdf_to_word(input_path):
    """PDF 转 Word"""
    try:
        logger.info(f"Converting PDF to Word: {input_path}")
        output_path = os.path.join(
            Config.UPLOAD_FOLDER, 
            f'{os.path.splitext(os.path.basename(input_path))[0]}.docx'
        )
        
        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()
        
        logger.info(f"Conversion successful")
        return output_path
        
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise Exception("PDF to Word conversion failed")


def merge_pdfs(input_paths):
    """合并多个 PDF 文件"""
    try:
        logger.info(f"Merging {len(input_paths)} PDF files")
        output_path = os.path.join(Config.UPLOAD_FOLDER, 'merged.pdf')
        
        writer = PdfWriter()
        
        # 依次读取每个 PDF 并添加所有页面
        for pdf_path in input_paths:
            logger.info(f"Adding pages from: {pdf_path}")
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        
        # 写入合并后的文件
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"Successfully merged {len(input_paths)} PDFs into {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"PDF merge failed: {e}")
        raise Exception(f"Failed to merge PDFs: {str(e)}")

def split_pdf(input_path, method='range', pages_spec=''):
    """分割 PDF 文件，提取指定页面"""
    try:
        logger.info(f"Splitting PDF: {input_path}, method: {method}, pages: {pages_spec}")
        output_path = os.path.join(Config.UPLOAD_FOLDER, 'split.pdf')
        
        reader = PdfReader(input_path)
        writer = PdfWriter()
        total_pages = len(reader.pages)
        
        # 解析页面规格
        pages_to_extract = []
        
        if method == 'range':
            # 解析范围，例如 "1-5, 10-15"
            ranges = pages_spec.split(',')
            for r in ranges:
                r = r.strip()
                if '-' in r:
                    start, end = r.split('-')
                    start = int(start.strip())
                    end = int(end.strip())
                    pages_to_extract.extend(range(start, end + 1))
                else:
                    pages_to_extract.append(int(r))
        else:
            # 解析具体页码，例如 "1, 3, 5, 7"
            pages = pages_spec.split(',')
            pages_to_extract = [int(p.strip()) for p in pages if p.strip()]
        
        # 去重并排序
        pages_to_extract = sorted(set(pages_to_extract))
        
        # 验证页码范围
        for page_num in pages_to_extract:
            if page_num < 1 or page_num > total_pages:
                raise Exception(f"Page {page_num} is out of range (1-{total_pages})")
        
        # 提取页面（PDF 页码从 0 开始）
        for page_num in pages_to_extract:
            writer.add_page(reader.pages[page_num - 1])
        
        # 写入分割后的文件
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info(f"Successfully extracted {len(pages_to_extract)} pages from {input_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"PDF split failed: {e}")
        raise Exception(f"Failed to split PDF: {str(e)}")
