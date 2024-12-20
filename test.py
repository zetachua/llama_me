import PyPDF2
def extract_pdf_text(pdf_path):
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

if __name__ == "__main__":
    text=extract_pdf_text('./data/personal_statement_zeta.pdf')
    print(text)
    