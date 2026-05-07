from __future__ import annotations

import re
from loguru import logger

ORDER_KEYWORDS = [r'\bdirected\b', r'\border(ed|s)?\b', r'\bshall\b', r'\bmust\b', r'\bcommand(ed)?\b', r'\bdecree\b']
OBSERVATION_KEYWORDS = [r'\bobserves?\b', r'\bobserved\b', r'\bnoted?\b', r'\bview\b', r'\bclear\b', r'\bopinion\b', r'\bfind(s|ing)?\b']
SUGGESTION_KEYWORDS = [r'\bsuggest(s|ed|ion)?\b', r'\brecommend(s|ed|ation)?\b', r'\bmay\b', r'\badvise(d)?\b']
DIRECTIVE_ACTION_KEYWORDS = {
    "compensation": [r'\bcompensation\b', r'\bdamages\b', r'\bcompensate\b'],
    "compliance_report": [r'\bcompliance\s+report\b', r'\bstatus\s+report\b', r'\bcounter\s+affidavit\b'],
    "land_restoration": [r'\brestore\b.*\bland\b', r'\brestoration\b', r'\bvacate\b', r'\bpossession\b'],
    "payment": [r'\bpay\b', r'\bdeposit\b', r'\brelease\b.*\b(fund|amount|sum)\b'],
}

def classify_clauses(clauses: list[dict]) -> dict:
    """
    Classifies a list of extracted legal clauses (dicts with 'text', 'start', 'end') 
    into Orders, Observations, and Suggestions.
    """
    logger.info(f"Classifying {len(clauses)} clauses...")
    
    classified = {
        "orders": [],
        "observations": [],
        "suggestions": []
    }
    
    for clause_obj in clauses:
        if not isinstance(clause_obj, dict):
            continue
        clause_text = clause_obj.get("text", "")
        if not isinstance(clause_text, str):
            clause_text = ""
        clause_text = clause_text.lower()
        
        # Scoring mechanisms
        order_score = sum(1 for kw in ORDER_KEYWORDS if re.search(kw, clause_text))
        obs_score = sum(1 for kw in OBSERVATION_KEYWORDS if re.search(kw, clause_text))
        sug_score = sum(1 for kw in SUGGESTION_KEYWORDS if re.search(kw, clause_text))
        
        # Assign type and keep original spans
        annotated_clause = {**clause_obj}
        matched_directives = [
            name
            for name, patterns in DIRECTIVE_ACTION_KEYWORDS.items()
            if any(re.search(pattern, clause_text) for pattern in patterns)
        ]
        if matched_directives:
            annotated_clause["directive_categories"] = matched_directives
        
        if order_score > 0 and order_score >= obs_score and order_score >= sug_score:
            annotated_clause["type"] = "order"
            classified["orders"].append(annotated_clause)
        elif obs_score > 0 and obs_score >= sug_score:
            annotated_clause["type"] = "observation"
            classified["observations"].append(annotated_clause)
        elif sug_score > 0:
            annotated_clause["type"] = "suggestion"
            classified["suggestions"].append(annotated_clause)
        else:
            annotated_clause["type"] = "observation"
            classified["observations"].append(annotated_clause)
            
    logger.info(f"Classification complete: {len(classified['orders'])} orders, {len(classified['observations'])} observations, {len(classified['suggestions'])} suggestions.")
    return classified
