from __future__ import annotations

import re
from loguru import logger

def generate_summary(text: str, clauses: dict) -> list[str]:
    """
    Generates a 4-part legal summary using extractive heuristics.
    (Interpretation, Explanation, Actionable Outcome, Next Step)
    """
    logger.info("Generating smart legal summary...")
    
    # 1. Interpretation
    interpretation = "This document appears to be a standard legal order or judgment."
    if clauses.get("orders") and len(clauses["orders"]) > 0:
        text_val = clauses["orders"][0]["text"] if isinstance(clauses["orders"][0], dict) else str(clauses["orders"][0])
        text_val = re.sub(r'\s+', ' ', text_val).strip()
        interpretation = f"The court has issued directives regarding: {text_val[:120]}{'...' if len(text_val) > 120 else ''}"
        
    # 2. Explanation
    explanation = "The legal text details the proceedings and positions of the involved parties."
    if clauses.get("observations") and len(clauses["observations"]) > 0:
        text_val = clauses["observations"][0]["text"] if isinstance(clauses["observations"][0], dict) else str(clauses["observations"][0])
        text_val = re.sub(r'\s+', ' ', text_val).strip()
        explanation = f"The authority observed that: {text_val[:120]}{'...' if len(text_val) > 120 else ''}"
    
    # 3. Actionable Outcome
    outcome = "Review the document for any specific compliance requirements."
    text_lower = text.lower()
    if "mandatory" in text_lower or "forthwith" in text_lower or "immediate" in text_lower:
        outcome = "Immediate compliance is required as per the explicit instructions in the text. Failure to act may lead to penalties."
        
    # 4. Next Step
    next_step = "Consult legal counsel to determine the appropriate follow-up actions."
    if "dismissed" in text_lower:
        next_step = "Consider filing an appeal if grounds exist, as the current petition was dismissed."
    elif "allowed" in text_lower:
        next_step = "Ensure the execution of the allowed petition and monitor for any opposing appeals."
        
    return [
        f"INTERPRETATION: {interpretation}",
        f"EXPLANATION: {explanation}",
        f"ACTIONABLE OUTCOME: {outcome}",
        f"NEXT STEP: {next_step}"
    ]

def generate_voice_narration(extracted_data: dict, insights: dict) -> str:
    """
    Generates a short, 1-2 sentence spoken summary for demo/accessibility purposes.
    """
    logger.info("Generating Voice-Ready Narration...")
    
    tags = insights.get("tags", [])
    primary_tag = tags[0] if tags else "legal issue"
    
    petitioner = extracted_data.get("petitioner", {}).get("value", "a petitioner")
    respondent = extracted_data.get("respondent", {}).get("value", "a respondent")
    
    deadlines = extracted_data.get("deadlines", [])
    
    narration = f"This case involves a {primary_tag} dispute between {petitioner} and {respondent}. "
    
    if extracted_data.get("orders"):
        if deadlines:
            dl_text = deadlines[0].get("raw", "shortly")
            narration += f"The court has issued an order requiring compliance {dl_text}."
        else:
            narration += "The court has issued a final order regarding the matter."
    else:
        narration += "The matter is currently under observation."
        
    return narration

def generate_executive_report(text: str, clauses: dict, insights: dict) -> dict:
    """
    Generates a high-level executive AI report section.
    """
    logger.info("Generating executive report...")
    
    tags = insights.get("tags", [])
    primary_issue = tags[0] if tags else "General legal dispute"
    
    court_direction = "Standard legal observations without explicit binding directives."
    if clauses.get("orders") and len(clauses["orders"]) > 0:
        text_val = clauses["orders"][0]["text"] if isinstance(clauses["orders"][0], dict) else str(clauses["orders"][0])
        text_val = re.sub(r'\s+', ' ', text_val).strip()
        court_direction = text_val[:200] + "..."
        
    risk_assessment = "High risk detected due to severe language or short deadlines." if insights.get("risk_score", 0) > 60 else "Moderate to low risk assessment based on standard legal terminology."
    
    return {
        "case_overview": "This AI-generated report outlines a legal proceeding requiring professional review and potential compliance.",
        "primary_issue": primary_issue,
        "court_direction": court_direction,
        "risk_assessment": risk_assessment,
        "recommended_next_step": "Ensure the legal team reviews all noted deadlines and prepares required documentation."
    }
