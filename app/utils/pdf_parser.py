import fitz  # PyMuPDF


def parse_pdf(path: str) -> str:
    """Extracts text from a PDF file using PyMuPDF."""
    doc = fitz.open(path)
    return "\n".join(page.get_text() for page in doc)
