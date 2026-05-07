from __future__ import annotations

import re
try:
    import spacy
except ImportError:
    spacy = None
from loguru import logger


class EmptyDoc:
    def __init__(self):
        self.ents = []


# Lazy load spaCy model
nlp = None
def get_nlp():
    global nlp
    if nlp is None:
        if spacy is None:
            logger.warning("spaCy module not installed. Proceeding with regex only.")
            nlp = lambda text: EmptyDoc()
            return nlp
        try:
            logger.info("Loading spaCy model 'en_core_web_sm'...")
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Proceeding with regex only for entity extraction.")
            nlp = lambda text: EmptyDoc()
    return nlp

def extract_field_with_confidence(pattern: str, text: str, base_confidence: float = 0.8) -> dict:
    match = re.search(pattern, text)
    if match:
        # Higher confidence if found early in the document
        pos_factor = 1.0 - (match.start() / len(text) if len(text) > 0 else 0)
        confidence = min(0.99, base_confidence + (pos_factor * 0.1))
        return {"value": match.group(1 if len(match.groups()) > 0 else 0).strip().replace('\n', ' '), "confidence": round(confidence, 2)}
    return {"value": "", "confidence": 0.0}

def normalize_deadline(deadline_str: str) -> int | None:
    deadline_str = deadline_str.lower()
    if "immediately" in deadline_str or "forthwith" in deadline_str or "immediate effect" in deadline_str:
        return 0
        
    if "before next hearing" in deadline_str:
        return 14
        
    num_map = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
        "eighteen": 18, "nineteen": 19, "twenty": 20
    }
    
    # Extract number
    num_match = re.search(r'(\d+)', deadline_str)
    num = int(num_match.group(1)) if num_match else None
    
    if not num:
        for word, val in num_map.items():
            if word in deadline_str:
                num = val
                break
                
    if num is not None:
        if "week" in deadline_str:
            return num * 7
        if "month" in deadline_str:
            return num * 30
        if "day" in deadline_str:
            return num
            
    return None

def extract_legal_information(text: str) -> dict:
    """
    Extracts structured legal information with confidence scores and character spans.
    """
    logger.info("Extracting structured legal information...")
    
    data = {
        "case_number": {"value": "", "confidence": 0.0},
        "court_name": {"value": "", "confidence": 0.0},
        "date": {"value": "", "confidence": 0.0},
        "petitioner": {"value": "", "confidence": 0.0},
        "respondent": {"value": "", "confidence": 0.0},
        "orders": [], 
        "deadlines": [],
        "important_clauses": []
    }
    
    if not text:
        return data

    # 1. Regex Extraction with Confidence
    case_no_pattern = r'(?i)((?:W\.P\.\s*\(C\)|Civil Appeal|Crl\.A\.|S\.L\.P\.|No\.)\s*[0-9]+(?:/[0-9]+)?)'
    data["case_number"] = extract_field_with_confidence(case_no_pattern, text, 0.85)
        
    court_pattern = r'(?i)(?:IN\s+THE\s+)?(HIGH\s+COURT\s+OF\s+[A-Z ]+|SUPREME\s+COURT\s+OF\s+INDIA)'
    data["court_name"] = extract_field_with_confidence(court_pattern, text, 0.90)

    date_pattern = r'(?i)(?:Dated|Date)[:\s]*(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+(?:,\s*|\s+)\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    data["date"] = extract_field_with_confidence(date_pattern, text, 0.88)

    # 2. NLP Entity Extraction (spaCy) for Parties
    _nlp = get_nlp()
    doc = _nlp(text[:5000]) 
    
    lines = text.split('\n')
    petitioner_lines = []
    respondent_lines = []
    current_party = "petitioner"
    
    for line in lines[:50]: 
        lower_line = line.lower()
        if re.search(r'\bv\.?\b|\bvs\.?\b|\bversus\b', lower_line):
            current_party = "respondent"
            continue
            
        if "petitioner" in lower_line or "appellant" in lower_line: continue
        if "respondent" in lower_line or "defendant" in lower_line:
            current_party = "respondent"
            continue
            
        clean_l = re.sub(r'^\d+\.?\s*', '', line.strip())
        if len(clean_l) > 3 and len(clean_l) < 100:
            if current_party == "petitioner": petitioner_lines.append(clean_l)
            else: respondent_lines.append(clean_l)

    if petitioner_lines:
        data["petitioner"] = {"value": petitioner_lines[0], "confidence": 0.75}
    if respondent_lines:
        data["respondent"] = {"value": respondent_lines[0], "confidence": 0.75}

    # 3. Clauses and Deadlines with Character Spans
    deadline_pattern = r'(?i)(within\s+(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:days?|weeks?|months?)|before\s+\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+|not later than\s+.*|on or before\s+.*|immediately|forthwith|immediate effect|before next hearing)'
    
    important_keywords = [r'\bdirect', r'\bshall\b', r'\bobserv', r'\bnoted', r'\bdecree', r'\bdismissed\b', r'\ballowed\b', r'\bdispose']
    
    # Iterate over text to find exact clause spans
    # We approximate paragraphs by double newlines
    for match in re.finditer(r'(?:\n\n|^)(.+?)(?=\n\n|$)', text, re.DOTALL):
        para = match.group(1).strip()
        if len(para) < 30: continue
        
        start_idx = match.start(1)
        end_idx = match.end(1)
        
        # Check for deadlines
        for dl_match in re.finditer(deadline_pattern, para):
            deadline_text = dl_match.group(0)
            data["deadlines"].append({
                "raw": deadline_text,
                "normalized_days": normalize_deadline(deadline_text),
                "context": para[:200] + "..." if len(para) > 200 else para
            })
            
        # Check for important clauses
        para_lower = para.lower()
        if any(re.search(kw, para_lower) for kw in important_keywords):
            data["important_clauses"].append({
                "text": para,
                "start": start_idx,
                "end": end_idx
            })

    # Deduplicate based on text
    unique_clauses = {c["text"]: c for c in data["important_clauses"]}
    data["important_clauses"] = list(unique_clauses.values())
    
    # 4. Timeline Extraction
    data["timeline"] = extract_timeline(text)
    
    # Fallback for date
    if not data["date"]["value"]:
        dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
        if dates:
            data["date"] = {"value": dates[-1], "confidence": 0.60}
            
    logger.info("Extraction complete.")
    return data

def extract_timeline(text: str) -> list[dict]:
    """
    Extracts a chronological timeline of legal events from the text.
    Looks for dates near action verbs.
    """
    timeline = []
    
    # Common date formats in legal texts
    date_regex = r'(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\s*,\s*\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    
    # Context window around dates to find events
    for match in re.finditer(date_regex, text):
        date_str = match.group(1).strip()
        
        # Get context: 50 chars before and after the date
        start_ctx = max(0, match.start() - 60)
        end_ctx = min(len(text), match.end() + 60)
        context = text[start_ctx:end_ctx].replace('\n', ' ')
        
        event_desc = "Mentioned date"
        context_lower = context.lower()
        
        if "filed" in context_lower or "petition" in context_lower:
            event_desc = "Petition/Document filed"
        elif "hearing" in context_lower or "listed" in context_lower:
            event_desc = "Case listed for hearing"
        elif "order" in context_lower or "directed" in context_lower:
            event_desc = "Order/Direction issued"
        elif "judgment" in context_lower:
            event_desc = "Judgment delivered"
        elif "dated" in context_lower:
            event_desc = "Document dated"
            
        # Avoid exact duplicates in the timeline
        if not any(item['date'] == date_str and item['event'] == event_desc for item in timeline):
            timeline.append({
                "date": date_str,
                "event": event_desc
            })
            
    return timeline
