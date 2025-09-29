import fitz
from langdetect import detect

##################################################################
#            1.  Extract Title    
##################################################################


def lang(pagee):
    text_blocks = []
    blocks = pagee.get_text("blocks")  # returns list of (x0, y0, x1, y1, text, block_no, block_type)
    page_text_info = []
    for block in blocks:
        x0, y0, x1, y1, text, *_ = block
        if text.strip():  # ignore empty blocks
            page_text_info.append({
                "text": text.strip(),
                "x0": x0,
                "y0": y0,
                "x1": x1,
                "y1": y1
            })
    text_blocks.append(page_text_info)



    full_text = " ".join(
        block["text"] for page in text_blocks for block in page
    )
    try:
        return detect(full_text)
    except Exception as e:
        return f"Language detection failed: {e}"


def extract_title_lines(uploaded_file, languagee):
    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    title_lines = []

    max_font_size = 0
    line_info = []  # Store (y, line_text, has_max_font)

    for page in doc:
        if(lang(page) != languagee):
            continue
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                line_text = ""
                line_font_sizes = []

                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    line_text += text# + " "
                    size = span["size"]
                    line_font_sizes.append(size)
                    max_font_size = max(max_font_size, size)

                if line_text.strip():
                    y = line["bbox"][1]
                    line_info.append((y, line_text.strip(), line_font_sizes))
                    line_info.append((line_info[-1][0], " ", line_info[-1][2]))

        break 

    # Second pass: extract lines with at least one word of max font size
    for y, text, sizes in line_info:
        if max_font_size in sizes:
            title_lines.append(text)
        if max_font_size-2 in sizes: 
            title_lines.append(text) 

    return "".join(title_lines)