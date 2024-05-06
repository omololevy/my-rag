from PyPDF2 import PdfReader
from io import BytesIO

def extract_text_from_pdf(file):
    text = ""
    reader = PdfReader(file)
    num_pages = len(reader.pages)
    for page_number in range(num_pages):
        page = reader.pages[page_number]
        text += page.extract_text()
    return text


if __name__ == "__main__":
    pdf_path = "example.pdf"  # Change this to the path of your PDF file
    extracted_text = extract_text_from_pdf(pdf_path)
    print(extracted_text)
