import fitz  # PyMuPDF
import re

##################################################################
#            5.  Extract References    
##################################################################


REFERENCE_HEADINGS = [
    r'\bReferences\b',
    r'\bRefrences\b',
    r'\bBibliography\b',
    r'\bWorks Cited\b',
    r'\bمنابع\b',
    r'\bعبانم\b',
    r'\bمراجع\b'
    r'\bعجارم\b',
    r'\bمراجع\b',
    r'\bﻣﻨﺎﺑﻊ\b' 
]

END_REFERENCE_HEADINGS = [
    r'\bAppendix\b',
    r'\bAcknowledgements?\b',
    r'\bAbout the Author\b',
    r'\bSUPPLEMENTARY\b', 
    r'\bضمیمه\b',
    r'\bتشکر\b',
    r'\bقدردانی\b',
    r'\bمؤلف\b',
    r'\bAbstract\b',
    r'\bConclusion\b'
]

REFERENCE_ENTRY_PATTERNS = [
    r'^\[\d+\]',       # [1]
    r'^\d+\.',         # 1.
    r'^\(\d+\)',       # (1)
    r'^• ',            # •
    r'^\* '            # *
]

MAX_NON_REF_LINES = 5

def extract_references_from_pdf(path):
    doc = fitz.open(path)
    all_lines = []

    for page in doc:
        text = page.get_text()
        lines = text.splitlines()
        all_lines.extend(lines)

    # STEP 1: Find start of references
    refs_start = -1
    for i, line in enumerate(all_lines):
        for heading in REFERENCE_HEADINGS:
            if re.search(heading, line.strip(), flags=re.IGNORECASE):
                refs_start = i

    if refs_start == -1:
        return []  # No references found

    # STEP 2: Extract until known end
    ref_lines = []
    non_ref_line_count = 0
    for line in all_lines[refs_start + 1:]:
        if any(re.search(end_head, line.strip(), flags=re.IGNORECASE) for end_head in END_REFERENCE_HEADINGS):
            break  # hit appendix/acknowledgment/etc.
        if any(re.match(pat, line.strip()) for pat in REFERENCE_ENTRY_PATTERNS):
            ref_lines.append(line)
            non_ref_line_count = 0
        else:
            if line.strip() == "":
                non_ref_line_count += 1
            else:
                ref_lines.append(line)
                non_ref_line_count = 0
            if non_ref_line_count >= MAX_NON_REF_LINES:
                break  # likely done with references

    # STEP 3: Merge lines into reference entries
    entries = []
    current_entry = ""
    for line in ref_lines:
        if any(re.match(pat, line.strip()) for pat in REFERENCE_ENTRY_PATTERNS):
            if current_entry:
                entries.append(current_entry.strip())
            current_entry = line
        else:
            current_entry += " " + line

    if current_entry:
        entries.append(current_entry.strip())

    result = ""
    for ref in entries:
        result += ref
        #result += '\n'
        result += ' '

    return result