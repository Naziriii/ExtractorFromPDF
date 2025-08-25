import fitz

##################################################################
#            1.  Extract Title    
##################################################################


def extract_title_lines(pdf_path):
    doc = fitz.open(pdf_path)
    title_lines = []

    max_font_size = 0
    line_info = []  # Store (y, line_text, has_max_font)

    for page in doc:
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

        break  # only first page

    # Second pass: extract lines with at least one word of max font size
    for y, text, sizes in line_info:
        if max_font_size in sizes:
            title_lines.append(text)

    return "".join(title_lines)