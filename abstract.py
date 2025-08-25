import fitz
from langdetect import detect

##################################################################
#            2.  Extract Abstract    
##################################################################

HDR_EN = ["keywords", "introduction", "keyword"]

HDR_FA = ["کلیدواژه", "کلیدواژه‌ها", "واژگان", "مقدمه", "کلید"]

def extract_text_blocks(uploaded_file):
    #doc = fitz.open(pdf_path)
    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    all_pages_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("blocks")  # returns list of (x0, y0, x1, y1, text, block_no, block_type)
        
        page_text_info = []
        for block in blocks:
            x0, y0, x1, y1, text, *_ = block
            if text.strip():  # ignore empty blocks
                page_text_info.append({
                    "text": text.strip(),
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "page": page_num + 1
                })
        all_pages_text.append(page_text_info)
    return all_pages_text

def is_bold_font(font_name):
    """Check if the font name indicates boldness."""
    return "Bold" in font_name or "bold" in font_name

def extract_abstract_lines(uploaded_file, lang):
    #doc = fitz.open(pdf_path)
    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    abstarct_lines = []

    counter = 0
    abs_flag = 0
    end_flag = 0
    size_check_flag = 0
    first_abstract_size = 0
    abstract_size = 0
    abstract_counter = 0
    
    page_number_ = 0
    

    abstract_bold = False
    first_abstract_bold = False
    bold_check_flag = 0

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            temp_txt = ""
            for line in block["lines"]:
                line_text = ""
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    line_text += text# + " "
                    temp_txt += text
                    if(lang == "fa"):
                        if(("چکیده" in temp_txt) or ("ﭼﻜﻴﺪﻩ" in temp_txt)):
                            abs_flag = 1
                    else:
                        if("abstract" in temp_txt.lower()):
                            abs_flag = 1
                    if(abs_flag):
                        if(lang == "fa"):
                            for word in HDR_FA:
                                if(word in temp_txt):
                                    end_flag = 1
                                    break
                        else:
                            for word in HDR_EN:
                                if(word in temp_txt.lower()):
                                    end_flag = 1
                                    break
                        if(size_check_flag):
                            if(span["size"] > first_abstract_size+1):
                                end_flag = 1
                        if(bold_check_flag):
                            if(is_bold_font(span["font"])):
                                end_flag = 1
                        if(end_flag):
                            page_number_ = page.number
                            break
                    if(abs_flag):
                        if(abstract_counter > 0):
                            abstarct_lines.append(text.strip())
                        size = span["size"]
                        if(abstract_counter == 0):
                            abstract_size = size
                            if(is_bold_font(span["font"])):
                                abstract_bold = True
                        if(abstract_counter == 1):
                            first_abstract_size = size
                            if(is_bold_font(span["font"])):
                                first_abstract_bold = True
                        if(abstract_counter > 1):
                            if(abstract_size > first_abstract_size):
                                size_check_flag = 1
                            if(abstract_bold != first_abstract_bold):
                                bold_check_flag = 1
                        abstract_counter += 1
                if(end_flag):
                    break
                if(abs_flag):
                    abstarct_lines.append(" ")
            if(end_flag):
                break
        if(end_flag):
            break
        counter = counter + 1
        if(counter == 2):
            break

    return "".join(abstarct_lines), page_number_

def detect_document_language(text_blocks):
    full_text = " ".join(
        block["text"] for page in text_blocks for block in page
    )
    try:
        return detect(full_text)
    except Exception as e:
        return f"Language detection failed: {e}"