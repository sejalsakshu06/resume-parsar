from pdfminer.high_level import extract_text

def read_pdf(path):
    return extract_text(path)
