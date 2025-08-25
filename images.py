import fitz
from io import BytesIO

##################################################################
#            3.  Extract Images    
##################################################################


def extract_images(uploaded_file):
    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    image_list = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)

            # Convert CMYK or grayscale images to RGB
            if pix.n - pix.alpha >= 4:  # CMYK
                pix = fitz.Pixmap(fitz.csRGB, pix)
            elif pix.n == 1:  # grayscale
                pix = fitz.Pixmap(fitz.csRGB, pix)

            img_bytes = pix.tobytes("png")  # get PNG bytes
            image_list.append(BytesIO(img_bytes))
            pix = None  # free memory

    return image_list



# import fitz
# from io import BytesIO
# from PIL import Image


# def extract_images(uploaded_file):
#     uploaded_file.seek(0)
#     doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
#     image_list = []

#     for page_num in range(len(doc)):
#         page = doc[page_num]
#         images = page.get_images(full=True)

#         for img_index, img in enumerate(images):
#             xref = img[0]
#             base_image = doc.extract_image(xref)
#             image_bytes = base_image["image"]

#             try:
#                 # Ensure PIL can read and convert to RGB
#                 image = Image.open(BytesIO(image_bytes)).convert("RGB")
#                 image_list.append(image)
#             except Exception as e:
#                 # Skip images that can't be read
#                 print(f"Skipping image {page_num}-{img_index}: {e}")

#     return image_list


# def extract_images(uploaded_file):
#     #pdf_document = fitz.open(pdf_path)
#     uploaded_file.seek(0)
#     doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
#     image_list = []

#     for page_num in range(len(doc)):
#         page = doc[page_num]
#         images = page.get_images(full=True)

#         for img_index, img in enumerate(images):
#             xref = img[0]
#             base_image = doc.extract_image(xref)
#             image_bytes = base_image["image"]
#             image_ext = base_image["ext"]

#             # Convert to PIL Image
#             image = Image.open(BytesIO(image_bytes))
#             image_list.append(image)

#     return image_list


# def extract_images(uploaded_file):
#     #pdf_document = fitz.open(pdf_path)
#     uploaded_file.seek(0)
#     doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
#     image_bytes_list = []

#     for page_num in range(len(doc)):
#         page = doc[page_num]
#         images = page.get_images(full=True)

#         for img_index, img in enumerate(images):
#             xref = img[0]
#             base_image = doc.extract_image(xref)
#             image_bytes = base_image["image"]
#             # store as BytesIO object
#             image_bytes_io = BytesIO(image_bytes)
#             image_bytes_list.append(image_bytes_io)

#     return image_bytes_list