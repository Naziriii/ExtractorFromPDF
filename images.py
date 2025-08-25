import fitz
from io import BytesIO

##################################################################
#            3.  Extract Images    
##################################################################


def extract_images(uploaded_file):
    #pdf_document = fitz.open(pdf_path)
    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    image_bytes_list = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            # store as BytesIO object
            image_bytes_io = BytesIO(image_bytes)
            image_bytes_list.append(image_bytes_io)

    return image_bytes_list