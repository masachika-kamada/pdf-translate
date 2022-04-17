import glob
import pyocr
import pyocr.builders
from PIL import Image

pyocr.tesseract.TESSERACT_CMD = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
tool = pyocr.get_available_tools()[0]

images = []
for img_path in glob.glob("./pdf_files/text_block/*.jpg"):
    img = Image.open(img_path)
    result = tool.image_to_string(
        img,
        lang="eng",
        builder=pyocr.builders.TextBuilder()
    )
    save_path = img_path.replace(".jpg", "_tesseract.txt")
    with open(save_path, mode="w", encoding="UTF-8") as f:
        f.write(result)
