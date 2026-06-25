import os
import pdfplumber
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts raw text from a PDF file using pdfplumber, falling back to PyPDF2.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")
        
    text = ""
    
    # Try pdfplumber first
    try:
        with pdfplumber.open(pdf_path) as pdf:
            pages_text = []
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text(layout=True) or page.extract_text()
                if page_text:
                    pages_text.append(page_text)
            text = "\n\n--- Page Break ---\n\n".join(pages_text)
    except Exception as e:
        print(f"pdfplumber failed: {e}. Falling back to PyPDF2...")
        text = ""

    # Fallback to PyPDF2 if text is empty or pdfplumber failed
    if not text.strip():
        try:
            reader = PdfReader(pdf_path)
            pages_text = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    pages_text.append(page_text)
            text = "\n\n--- Page Break ---\n\n".join(pages_text)
        except Exception as e:
            raise RuntimeError(f"Failed to parse PDF with both pdfplumber and PyPDF2: {e}")
            
    return text

if __name__ == "__main__":
    # Test script if run directly
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        try:
            parsed = extract_text_from_pdf(path)
            print(f"Successfully extracted {len(parsed)} characters.")
            print(parsed[:500])
        except Exception as err:
            print(f"Error: {err}")
    else:
        print("Please provide a PDF file path to test.")
