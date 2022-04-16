import pyocr
import pyocr.builders
import pdf2image
import os

pyocr.tesseract.TESSERACT_CMD = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
tool = pyocr.get_available_tools()[0]

# pdf->image
images = pdf2image.convert_from_path(
    "./pdf_files/src.pdf",
    poppler_path="C:/poppler-22.01.0/Library/bin",
    dpi=200,
    fmt='jpg')

os.makedirs("./pdf_files/imgs", exist_ok=True)
for i, image in enumerate(images):
    image.save(f"./pdf_files/imgs/page{i + 1}.jpg", "JPEG")

# image->text
dst = ""
for image in images:
    text = tool.image_to_string(
        image,
        lang="eng",
        builder=pyocr.builders.TextBuilder()
    )
    dst += text + "\n"

with open("./pdf_files/ocr_tesseract.txt", mode="w", encoding="UTF-8") as f:
    f.write(dst)
