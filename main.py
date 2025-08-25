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

    text_blocks = extract_text_blocks(pdf_file)
    language = detect_document_language(text_blocks)
    abstract, page_number_ = extract_abstract_lines(pdf_file, language)
    title = extract_title_lines(pdf_file)
    images = extract_images(pdf_file)
    result = extract_title_and_following_text(pdf_file, title, page_number_)
    authors = get_text_before_abstract_from_following_text(result['text_after_title'], language)
    title = result['matched_title']
    refs = extract_references_from_pdf(pdf_file)

    lang = language

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
    for img_bytes in images:
        st.image(img_bytes)
