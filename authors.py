import fitz  # PyMuPDF
import re

##################################################################
#            4.  Extract Authors    
##################################################################

def title_to_flexible_regex(raw_title):
    compact_title = re.sub(r'\s+', '', raw_title)
    # Match optional whitespace between every character
    pattern = r'\s*'.join(map(re.escape, compact_title))
    return re.compile(pattern, re.IGNORECASE)

def extract_title_and_following_text(uploaded_file, title_variation, page_num):
    pattern = title_to_flexible_regex(title_variation)

    skip_flag = False

    if(page_num == 1):
        skip_flag = True

    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page_number, page in enumerate(doc, start=1):
        if (skip_flag):
            skip_flag = False
            continue
        text = page.get_text()
        match = pattern.search(text)
        
        if match:
            matched_raw = match.group()
            # Normalize matched title
            matched_normalized = re.sub(r'\s+', ' ', matched_raw).strip()
            # Get text after match
            remaining_text = text[match.end():].strip()

            return {
                "page": page_number,
                "matched_title": matched_normalized,
                "text_after_title": remaining_text
            }

    return None  # Not found

def normalize_farsi_text(text):
    # Remove all whitespace (spaces, newlines, tabs, etc.)
    return re.sub(r'\s+', '', text)


def get_text_before_abstract_from_following_text(text, lang):
    if(lang == "fa"):
        match = match = re.search(r'چ\s*ک\s*ی\s*د\s*ه', text)
        if not match:
            match = re.search(r'\bچکیده\b[:\-]?', text)
            if not match:
                match = re.search(r'\bﭼﻜﻴﺪﻩ\b[:\-]?', text)
    else:
        match = re.search(r'\babstract\b[:\-]?', text, re.IGNORECASE)  # matches "abstract", "abstract:", "abstract-"
    if match:
        return text[:match.start()].strip()
    else:
        return None  # 'abstract' not found