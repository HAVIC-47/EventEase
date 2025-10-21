import PyPDF2

def extract_pdf_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += f"\n--- Page {page_num + 1} ---\n"
            text += page.extract_text()
        return text

if __name__ == "__main__":
    pdf_path = "CSE-410 Lecture -01.pdf"
    content = extract_pdf_text(pdf_path)
    print(content)