import pyocr
import pyocr.builders
import cv2
from PIL import Image


pyocr.tesseract.TESSERACT_CMD = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
tool = pyocr.get_available_tools()[0]

res = tool.image_to_string(
    Image.open("./pdf_files/imgs/page1.jpg"), lang="eng",
    # builder=pyocr.builders.WordBoxBuilder(tesseract_layout=6))
    builder=pyocr.builders.LineBoxBuilder(tesseract_layout=6))

# draw result
out = cv2.imread("./pdf_files/imgs/page1.jpg")
for d in res:
    print(d.content)
    print(d.position)
    cv2.rectangle(out, d.position[0], d.position[1], (0, 0, 255), 2)

cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.imshow("img", out)
cv2.waitKey(0)
cv2.destroyAllWindows()
