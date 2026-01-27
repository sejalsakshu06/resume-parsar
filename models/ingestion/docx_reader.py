"""
This module provides functions for reading text from DOCX files.
"""
import docx


def read_docx(path):
    """
    Reads text from a DOCX file.
    """
    try:
        doc = docx.Document(path)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception as e:
        raise ValueError(f"Failed to read DOCX file {path}: {e}")

