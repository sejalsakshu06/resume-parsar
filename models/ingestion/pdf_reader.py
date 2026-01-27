"""
This module provides functions for reading text from PDF files.
"""
from pdfminer.high_level import extract_text


def read_pdf(path):
    """
    Reads text from a PDF file.
    """
    try:
        return extract_text(path)
    except Exception as e:
        raise ValueError(f"Failed to read PDF file {path}: {e}")
