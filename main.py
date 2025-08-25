import streamlit as st
from title import extract_title_lines
from abstract import extract_text_blocks, detect_document_language, extract_abstract_lines
from images import extract_images
from authors import extract_title_and_following_text, get_text_before_abstract_from_following_text
from references import extract_references_from_pdf

##################################################################
#                Main Program    
##################################################################

labels = {
    "title": {"en": "Title", "fa": "عنوان"},
    "abstract": {"en": "Abstract", "fa": "چکیده"},
    "authors": {"en": "Authors", "fa": "نویسنده ها"},
    "images": {"en": "Images", "fa": "تصاویر"},
    "upload": {"en": "Upload PDF", "fa": "بارگذاری PDF"},
    "refs": {"en": "References", "fa": "منابع"}
}

st.title(labels["upload"]["en"])

pdf_file = st.file_uploader(labels["upload"]["en"], type="pdf")

if pdf_file:
    pdf_name = pdf_file.name

    text_blocks = extract_text_blocks(pdf_name)
    language = detect_document_language(text_blocks)
    abstract, page_number_ = extract_abstract_lines(pdf_name, language)
    title = extract_title_lines(pdf_name)
    images = extract_images(pdf_name, 'images')
    result = extract_title_and_following_text(pdf_name, title, page_number_)
    authors = get_text_before_abstract_from_following_text(result['text_after_title'], language)
    title = result['matched_title']
    refs = extract_references_from_pdf(pdf_name)

    lang = language

    #with open(("title" + pdf_name[0:len(pdf_name)-4] + ".txt"), "w", encoding="utf-8") as file:
    #    file.write(abstract)
    #with open(("title" + pdf_name[0:len(pdf_name)-4] + ".txt"), "w", encoding="utf-8") as file:
    #    file.write(title)

    # Display extracted information
    st.header(labels["title"][lang])
    st.write(title)

    st.header(labels["authors"][lang])
    st.write(authors)

    st.header(labels["abstract"][lang])
    st.write(abstract)

    st.header(labels["refs"][lang])
    st.text(refs)

    st.header(labels["images"][lang])
    for img_path in images:
        st.image(img_path)
