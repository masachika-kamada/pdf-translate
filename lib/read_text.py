from PyPDF2 import PdfFileReader
from pdfminer.high_level import extract_text


def read_pypdf2(file_path):
    text = ""
    with open(file_path, "rb") as input:
        reader = PdfFileReader(input)
        for i in range(reader.getNumPages()):
            page = reader.getPage(i)
            text += page.extractText()
        return text


def read_pdfminer(file_path):
    return extract_text(file_path)
