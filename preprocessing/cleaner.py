import re

def clean_text(text):
    # Remove PDF artifacts like (cid:XXX)
    text = re.sub(r'\(cid:\d+\)', '', text)
    
    # Fix hyphenated line breaks (e.g., "Accred- ited" -> "Accredited")
    text = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', text)
    
    # Remove extra spaces within lines but preserve line breaks
    lines = text.split('\n')
    cleaned_lines = [re.sub(r'\s+', ' ', line).strip() for line in lines]
    # Remove empty lines
    cleaned_lines = [line for line in cleaned_lines if line.strip()]
    return '\n'.join(cleaned_lines)

def remove_contact_info(text):
    """Remove email, phone, location info, and links from text"""
    # Remove email addresses
    text = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', text)
    # Remove phone numbers
    text = re.sub(r'(\+91[\s-]?)?[6-9]\d{9}', '', text)
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+|github\.com/\S+|linkedin\.com/\S+', '', text)
    # Remove location patterns (City, State, Country) - multiple variations
    text = re.sub(r'[A-Z][a-z]+,\s*[A-Z][a-z]+\s+Pradesh,\s*India', '', text)
    text = re.sub(r'^[A-Z][a-z]+,\s*[A-Z][a-z]+.*India\s*$', '', text, flags=re.MULTILINE)
    # Remove section symbols and extra whitespace
    text = re.sub(r'[§•]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text
