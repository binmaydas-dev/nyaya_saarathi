from extractor import normalize_deadline, extract_legal_information

def test_normalize_deadline():
    assert normalize_deadline("within two weeks") == 14
    assert normalize_deadline("within 30 days") == 30
    assert normalize_deadline("immediately") == 0
    assert normalize_deadline("forthwith") == 0
    assert normalize_deadline("within one month") == 30
    assert normalize_deadline("something random") == None

def test_extract_legal_information():
    sample_text = """
    IN THE HIGH COURT OF DELHI
    W.P.(C) 9999/2024
    Dated: 12th August 2024
    
    JOHN DOE ... Petitioner
    vs
    STATE ... Respondent
    
    The respondent is directed to file a counter affidavit within two weeks.
    """
    
    result = extract_legal_information(sample_text)
    
    assert result["case_number"]["value"] == "W.P.(C) 9999/2024"
    assert result["court_name"]["value"] == "HIGH COURT OF DELHI"
    assert "12th August 2024" in result["date"]["value"]
    
    # Check deadlines
    assert len(result["deadlines"]) == 1
    assert result["deadlines"][0]["normalized_days"] == 14
    
    # Check Important Clauses (should contain the 'directed' keyword)
    assert len(result["important_clauses"]) > 0
    assert "directed" in result["important_clauses"][0]["text"].lower()
    assert "start" in result["important_clauses"][0]
