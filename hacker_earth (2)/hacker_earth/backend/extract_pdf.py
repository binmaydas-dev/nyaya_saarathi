from __future__ import annotations

import fitz  # PyMuPDF
from loguru import logger

def extract_text_and_detect_scan(pdf_path: str) -> tuple[str, bool]:
    """
    Extracts text from a PDF and determines if it is primarily a scanned document.
    Returns:
        tuple (extracted_text: str, is_scanned: bool, num_pages: int)
    """
    logger.info(f"Analyzing PDF: {pdf_path}")
    text = ""
    is_scanned = False
    
    try:
        doc = fitz.open(pdf_path)
        num_pages = len(doc)
        total_chars = 0
        
        for page_num in range(num_pages):
            page = doc.load_page(page_num)
            page_text = page.get_text("text")
            text += page_text + "\n\n"
            total_chars += len(page_text.strip())
            
        doc.close()
        
        # Heuristic for scanned PDF detection
        # If the average number of characters per page is very low, it's likely scanned.
        avg_chars_per_page = total_chars / num_pages if num_pages > 0 else 0
        logger.info(f"Extracted {total_chars} total characters across {num_pages} pages. Avg: {avg_chars_per_page:.2f} chars/page.")
        
        # Threshold: Less than 100 characters per page typically means the page is mostly an image
        if avg_chars_per_page < 100 and num_pages > 0:
            is_scanned = True
            logger.warning("PDF appears to be scanned/image-based. OCR fallback may be required.")
            
        return text, is_scanned, num_pages
        
    except Exception as e:
        logger.error(f"Error reading PDF with PyMuPDF: {e}")
        return "", True, 0 # Assume OCR is needed if standard extraction totally fails
