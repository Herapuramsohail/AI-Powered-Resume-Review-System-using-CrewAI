import os
import docx

def extract_text_from_docx(docx_path: str) -> str:
    """
    Extracts text from a .docx file including paragraphs and tables.
    """
    if not os.path.exists(docx_path):
        raise FileNotFoundError(f"DOCX file not found at: {docx_path}")
        
    try:
        doc = docx.Document(docx_path)
        full_text = []
        
        # Read all elements sequentially (paragraphs and tables)
        for element in doc.element.body:
            if element.tag.endswith('p'):  # Paragraph
                p = docx.text.paragraph.Paragraph(element, doc)
                if p.text.strip():
                    full_text.append(p.text)
            elif element.tag.endswith('tbl'):  # Table
                table = docx.table.Table(element, doc)
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        # Get cell paragraphs text
                        cell_p_text = " ".join([p.text.strip() for p in cell.paragraphs if p.text.strip()])
                        if cell_p_text:
                            row_text.append(cell_p_text)
                    if row_text:
                        full_text.append(" | ".join(row_text))
                        
        return "\n".join(full_text)
    except Exception as e:
        raise RuntimeError(f"Failed to parse DOCX: {e}")

if __name__ == "__main__":
    # Test script if run directly
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        try:
            parsed = extract_text_from_docx(path)
            print(f"Successfully extracted {len(parsed)} characters.")
            print(parsed[:500])
        except Exception as err:
            print(f"Error: {err}")
    else:
        print("Please provide a DOCX file path to test.")
