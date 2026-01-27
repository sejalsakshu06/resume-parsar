"""
This module provides functions for cleaning resume text.
"""

import re


def clean_text(text):
    """
    Cleans the input text by removing PDF artifacts, fixing hyphenated line breaks,
    and preserving line structure for section detection.
    """
    # Remove PDF artifacts like (cid:XXX)
    text = re.sub(r'\(cid:\d+\)', '', text)

    # Remove zero-width spaces and other invisible characters
    text = re.sub(r'[\U0001F300-\U0001F9FF\u200b\u200c\u200d\ufeff\r]', '', text)
    
    # Fix hyphenated line breaks that span across lines
    text = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', text)

    # Split into lines
    lines = text.split('\n')
    
    # Process each line individually, preserving structure
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            # Keep empty lines to preserve section structure
            cleaned_lines.append('')
            continue
        
        # Clean up spaces within the line
        line = re.sub(r'[ \t]+', ' ', line)
        cleaned_lines.append(line)
    
    # Join lines back with newlines
    text = '\n'.join(cleaned_lines)
    
    # Clean up multiple consecutive empty lines but preserve some structure
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()

    return text

def remove_contact_info(text):
    """Remove email, phone, location info, and links from text"""
    # Remove email addresses
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', text)
    # Remove phone numbers
    text = re.sub(r'(\+91[\s-]?)?[6-9]\d{9}', '', text)
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+|linkedin\.com/in/\S+', '', text)
    # Remove location patterns (City, State, Country) - multiple variations
    text = re.sub(r'[A-Z][a-z]+,\s*[A-Z][a-z]+\s+Pradesh,\s*India', '', text)
    text = re.sub(r'^[A-Z][a-z]+,\s*[A-Z][a-z]+.*India\s*$', '', text, flags=re.MULTILINE)
    # Remove section symbols and extra whitespace
    text = re.sub(r'[§]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

