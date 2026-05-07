import re
from loguru import logger

def clean_text(text: str) -> str:
    """
    Cleans raw extracted text from a PDF.
    - Normalizes whitespace.
    - Removes common header/footer artifacts like standalone page numbers.
    - Preserves legal paragraph structure.
    """
    logger.info("Starting text preprocessing...")
    
    if not text:
        return ""

    # Remove typical standalone page numbers (e.g., "- 1 -", "Page 1 of 10", just numbers on their own line)
    text = re.sub(r'^\s*-\s*\d+\s*-\s*$', '\n', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*Page\s+\d+\s+of\s+\d+\s*$', '\n', text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r'^\s*\d+\s*$', '\n', text, flags=re.MULTILINE)

    # Normalize newlines: replace 3 or more newlines with exactly 2 (paragraph break)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove trailing/leading whitespaces on each line
    lines = [line.strip() for line in text.split('\n')]
    
    # Rejoin preserving double newlines for paragraphs, single for regular breaks
    cleaned_lines = []
    for line in lines:
        if line:
            cleaned_lines.append(line)
        else:
            if cleaned_lines and cleaned_lines[-1] != "":
                cleaned_lines.append("") # paragraph break
                
    text = '\n'.join(cleaned_lines)
    
    # Final cleanup of any lingering multiple spaces
    text = re.sub(r'[ \t]{2,}', ' ', text)

    logger.info(f"Preprocessing complete. Text length: {len(text)} characters.")
    return text
