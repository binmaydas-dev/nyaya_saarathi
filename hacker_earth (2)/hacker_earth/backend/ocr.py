from __future__ import annotations

import fitz  # PyMuPDF
import numpy as np
from loguru import logger

try:
    import cv2
except ImportError:
    cv2 = None
    logger.warning("OpenCV not installed. OCR image preprocessing disabled.")

# Safe PaddleOCR import
try:
    from paddleocr import PaddleOCR
except ImportError:
    PaddleOCR = None
    logger.warning("PaddleOCR not installed. OCR features disabled.")

# Lazy loading of OCR engines
ocr_engines = {}


def get_ocr_engine(lang='en'):
    """
    Lazy loads PaddleOCR engine safely.
    """
    global ocr_engines

    # If PaddleOCR unavailable
    if PaddleOCR is None:
        logger.warning("PaddleOCR unavailable in current environment.")
        return None

    # Load engine only once
    if lang not in ocr_engines:
        logger.info(f"Initializing PaddleOCR Engine for lang='{lang}'")

        try:
            ocr_engines[lang] = PaddleOCR(
                use_angle_cls=True,
                lang=lang,
                show_log=False
            )

        except Exception as e:
            logger.error(f"Failed to initialize PaddleOCR: {e}")
            return None

    return ocr_engines[lang]


def perform_ocr(pdf_path: str, lang: str = 'en') -> tuple[str, float]:
    """
    Performs OCR on scanned PDFs safely.

    Returns:
        tuple:
            extracted_text (str)
            average_confidence (float)
    """

    logger.info(f"Starting OCR process for: {pdf_path}")

    # Safe fallback if PaddleOCR unavailable
    engine = get_ocr_engine(lang)

    if engine is None:
        logger.warning("OCR skipped because PaddleOCR is unavailable.")

        return (
            "OCR unavailable in current environment.",
            0.0
        )

    if cv2 is None:
        logger.warning("OCR skipped because OpenCV is unavailable.")

        return (
            "OCR unavailable in current environment.",
            0.0
        )

    extracted_text = ""
    total_confidence = 0.0
    text_blocks_count = 0

    try:
        doc = fitz.open(pdf_path)

        num_pages = len(doc)

        logger.info(f"Rendering {num_pages} pages for OCR")

        for page_num in range(num_pages):

            page = doc.load_page(page_num)

            # High-resolution rendering
            zoom = 2.0
            mat = fitz.Matrix(zoom, zoom)

            pix = page.get_pixmap(
                matrix=mat,
                alpha=False
            )

            # Convert pixmap to numpy array
            img = np.frombuffer(
                pix.samples,
                dtype=np.uint8
            ).reshape(
                pix.h,
                pix.w,
                pix.n
            )

            # Convert color space
            if pix.n == 4:
                img = cv2.cvtColor(
                    img,
                    cv2.COLOR_RGBA2BGR
                )

            elif pix.n == 3:
                img = cv2.cvtColor(
                    img,
                    cv2.COLOR_RGB2BGR
                )
                
            elif pix.n == 1:
                img = cv2.cvtColor(
                    img,
                    cv2.COLOR_GRAY2BGR
                )

            # OCR processing
            result = engine.ocr(img, cls=True)

            if result and result[0]:

                for line in result[0]:

                    try:
                        text = line[1][0]
                        confidence = line[1][1]

                        extracted_text += text + "\n"

                        total_confidence += confidence
                        text_blocks_count += 1

                    except Exception:
                        continue

            extracted_text += "\n\n"

            logger.info(
                f"OCR completed for page "
                f"{page_num + 1}/{num_pages}"
            )

        doc.close()

        avg_confidence = (
            total_confidence / text_blocks_count
            if text_blocks_count > 0
            else 0.0
        )

        logger.info(
            f"OCR Complete | "
            f"Chars: {len(extracted_text)} | "
            f"Confidence: {avg_confidence:.2f}"
        )

        return extracted_text, avg_confidence

    except Exception as e:

        logger.error(f"OCR Processing Error: {e}")

        # Safe fallback response
        return (
            "OCR processing failed safely.",
            0.0
        )
