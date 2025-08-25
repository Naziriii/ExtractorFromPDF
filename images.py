import fitz

##################################################################
#            3.  Extract Images    
##################################################################


def extract_images(uploaded_file, output_folder):
    #pdf_document = fitz.open(pdf_path)
    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    image_files = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_path = f'{output_folder}/image_p{page_num+1}_{img_index+1}.{image_ext}'
            with open(image_path, 'wb') as img_file:
                img_file.write(image_bytes)
            
            image_files.append(image_path)
    return image_files