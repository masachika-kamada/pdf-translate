import cv2


def crop_image(img, thresh=250, blur=12, display=False):
    img_copy = img.copy()
    img_h, img_w = img.shape[:2]
    ksize = 2 * blur + 1
    sigma = 20
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (ksize, ksize), sigma)
    _, thresh = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    blocks = []
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < 20 or h < 20:
            continue
        elif h + 5 > img_h and w + 5 > img_w:
            continue
        blocks.append([y, y + h, x, x + w])

    for i in range(len(blocks)):
        if blocks[i] is None:
            continue
        ymin_i, ymax_i, xmin_i, xmax_i = blocks[i]
        for j in range(len(blocks)):
            if i == j or blocks[j] is None:
                continue
            ymin_j, ymax_j, xmin_j, xmax_j = blocks[j]
            if (ymin_i <= ymin_j and ymax_i >=
                    ymax_j and xmin_i <= xmin_j and xmax_i >= xmax_j):
                blocks[j] = None
    blocks = [block for block in blocks if block is not None]
    # OCRする順番に整列させないといけない

    dst = []
    for ymin, ymax, xmin, xmax in blocks:
        dst.append(img[ymin:ymax, xmin:xmax])
    if display:
        img_copy = img.copy()
        for ymin, ymax, xmin, xmax in blocks:
            cv2.rectangle(img_copy, (xmin, ymin), (xmax, ymax), (0, 0, 255), 4)
        cv2.namedWindow("dst", cv2.WINDOW_NORMAL)
        cv2.imshow("dst", img_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return dst
