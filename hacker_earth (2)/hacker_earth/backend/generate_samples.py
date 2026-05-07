import os
import fitz  # PyMuPDF
from loguru import logger

SAMPLE_DIR = "sample_cases"

CASES = {
    "compensation_case.pdf": """
    IN THE HIGH COURT OF DELHI
    W.P.(C) 4455/2023
    Dated: 15th January 2024
    
    RAMESH KUMAR ... Petitioner
    vs
    STATE OF DELHI ... Respondent
    
    The petitioner seeks compensation for land acquisition.
    The court observes that the compensation amount was incorrectly calculated by the tribunal.
    The respondent is directed to recalculate and disperse the compensation amount of Rs 50,00,000 within 30 days.
    Failure to comply will result in contempt of court proceedings.
    """,
    "property_dispute.pdf": """
    IN THE SUPREME COURT OF INDIA
    Civil Appeal No. 112/2022
    Date: 02/03/2023
    
    ANITA SHARMA ... Appellant
    vs
    SURESH SHARMA ... Respondent
    
    This is an ongoing property dispute regarding the ancestral home.
    We note that both parties have agreed to a settlement.
    The court orders that the property be divided equally.
    Parties must vacate the disputed premises forthwith.
    """,
    "environmental_order.pdf": """
    NATIONAL GREEN TRIBUNAL
    Dated: 10th October 2023
    
    ECO WARRIORS NGO ... Petitioner
    vs
    ABC CHEMICALS LTD ... Respondent
    
    The petitioner alleges severe environmental pollution by the respondent factory.
    It is strictly mandatory for the respondent to halt all industrial discharge immediately.
    The factory is ordered to close operations pending a full environmental audit.
    Compliance report must be filed before 20th October 2023.
    """,
    "labor_issue.pdf": """
    INDUSTRIAL COURT
    Dated: 05-05-2023
    
    WORKMEN UNION ... Petitioner
    vs
    XYZ CORP ... Respondent
    
    Dispute regarding unpaid wages.
    We suggest the management hold talks with the union within two weeks.
    The respondent is directed to pay the pending arrears within one month.
    """,
    "criminal_bail_scanned_mock.pdf": """
    IN THE HIGH COURT
    Crl.A. 789/2023
    Date: 12-12-2023
    
    JOHN DOE ... Petitioner
    vs
    STATE ... Respondent
    
    Bail application for the accused.
    The court finds no prima facie evidence of flight risk.
    Bail is granted. The petitioner shall report to the local station weekly.
    """
}

def generate_pdfs():
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    logger.info(f"Generating 5 mock legal PDFs in {SAMPLE_DIR}/...")
    
    for filename, content in CASES.items():
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text(fitz.Point(50, 50), content.strip(), fontsize=11, fontname="helv")
        
        if "scanned" in filename:
            # Convert the text page to an image to simulate a scanned PDF
            pix = page.get_pixmap(dpi=150)
            img_pdf = fitz.open()
            img_page = img_pdf.new_page(width=page.rect.width, height=page.rect.height)
            img_page.insert_image(img_page.rect, stream=pix.tobytes("png"))
            
            filepath = os.path.join(SAMPLE_DIR, filename)
            img_pdf.save(filepath)
            img_pdf.close()
            doc.close()
            logger.info(f"Created (Scanned): {filepath}")
        else:
            filepath = os.path.join(SAMPLE_DIR, filename)
            doc.save(filepath)
            doc.close()
            logger.info(f"Created: {filepath}")

if __name__ == "__main__":
    generate_pdfs()
    logger.info("Mock PDFs generated successfully.")
