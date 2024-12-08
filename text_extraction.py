import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text

# Example usage
pdf_path = "data/personal_statement.pdf"  # Your uploaded PDF file
pdf_text = extract_text_from_pdf(pdf_path)
print(pdf_text[:500])  # Print the first 500 characters for verification
