import cv2
from cv2 import imwrite


def main():
    img = cv2.imread("./blur.jpg", 0)
    ret, img_bi = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
    imwrite("bi.jpg", img_bi)
    cv2.imshow("img", img_bi)
    cv2.waitKey()


if __name__ == "__main__":
    main()
