import cv2


def nothing(x):
    pass


def main():
    img = cv2.imread("./pdf_files/imgs/page1.jpg")
    cv2.namedWindow("params")
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.namedWindow("dst", cv2.WINDOW_NORMAL)
    cv2.namedWindow("blur", cv2.WINDOW_NORMAL)
    cv2.namedWindow("bin", cv2.WINDOW_NORMAL)
    cv2.createTrackbar("blur", "params", 12, 20, nothing)
    cv2.createTrackbar("sigma", "params", 20, 20, nothing)
    cv2.createTrackbar("erode", "params", 5, 20, nothing)
    cv2.createTrackbar("thresh", "params", 250, 255, nothing)

    while True:
        img_copy = img.copy()
        ksize = cv2.getTrackbarPos("blur", "params")
        ksize = 2 * ksize + 1
        thresh = cv2.getTrackbarPos("thresh", "params")
        sigma = cv2.getTrackbarPos("sigma", "params")
        erode = cv2.getTrackbarPos("erode", "params")
        gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (ksize, ksize), sigma)
        ret, thresh = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)
        # erosion = cv2.erode(thresh, (erode, erode), iterations=1)
        # 3---輪郭抽出
        contours = cv2.findContours(
            thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        # 4---抽出した数分処理
        for moji in contours:
            x, y, w, h = cv2.boundingRect(moji)
            if h < 20:
                continue
            red = (0, 0, 255)
            cv2.rectangle(img_copy, (x, y), (x + w, y + h), red, 2)

        cv2.imshow("img", img)
        cv2.imshow("dst", img_copy)
        cv2.imshow("blur", blur)
        cv2.imshow("bin", thresh)
        if cv2.waitKey(10) == 27:
            # cv2.imwrite("blur.jpg", blur)
            # cv2.imwrite("dst.jpg", img_copy)
            break

    cv2.destroyAllWindows()


def test():
    from lib.image_process import crop_image
    img = cv2.imread("./pdf_files/imgs/page1.jpg")
    res = crop_image(img, display=True)
    for i, item in enumerate(res):
        cv2.imwrite(f"./pdf_files/crop_block/{i}.jpg", item)
        cv2.imshow("img", item)
        cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # main()
    test()
