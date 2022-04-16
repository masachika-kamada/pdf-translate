import cv2


def nothing(x):
    pass


if __name__ == "__main__":
    img = cv2.imread("./pdf_files/imgs/page1.jpg")
    cv2.namedWindow("params")
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.namedWindow("dst", cv2.WINDOW_NORMAL)
    cv2.namedWindow("blur", cv2.WINDOW_NORMAL)
    cv2.namedWindow("bin", cv2.WINDOW_NORMAL)
    cv2.createTrackbar("blur", "params", 5, 20, nothing)
    cv2.createTrackbar("sigma", "params", 5, 20, nothing)
    cv2.createTrackbar("bocho", "params", 5, 20, nothing)
    cv2.createTrackbar("thresh", "params", 5, 255, nothing)

    while True:
        img_copy = img.copy()
        ksize = cv2.getTrackbarPos("blur", "params")
        ksize = 2 * ksize + 1
        thresh = cv2.getTrackbarPos("thresh", "params")
        sigma = cv2.getTrackbarPos("sigma", "params")
        bocho = cv2.getTrackbarPos("bocho", "params")
        gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (ksize, ksize), sigma)
        dilation = cv2.dilate(blur, (bocho, bocho), iterations=1)
        ret, thresh = cv2.threshold(dilation, thresh, 255, cv2.THRESH_BINARY)
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
            cv2.imwrite("blur.jpg", blur)
            cv2.imwrite("dst.jpg", img_copy)
            break

    cv2.destroyAllWindows()
