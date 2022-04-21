import cv2
import numpy as np


def pil2cv(img):
    img = np.array(img, dtype=np.uint8)
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


def save_crop_image(dir_save, img, min_size=50, thresh=250, blur=12):
    debug = False
    img = pil2cv(img)
    img_copy = img.copy()
    img_h, img_w = img.shape[:2]
    ksize = 2 * blur + 1
    sigma = 20
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (ksize, ksize), sigma)
    _, thresh = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)
    cnts = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]

    blocks = []
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        # ブロックの大きさでフィルタ
        if w < min_size or h < min_size:
            continue
        elif h + 5 > img_h and w + 5 > img_w:
            continue
        # 横方向のブロックの位置を補正
        x_pos = (x + w / 2) / img_w
        if 0.2 < x_pos < 0.3:
            x_pos = 1
        elif 0.45 < x_pos < 0.55:
            x_pos = 0
        elif 0.7 < x_pos < 0.8:
            x_pos = 2
        else:
            continue
        blocks.append([y, y + h, x, x + w, x_pos])

    # 内側のブロックを削除
    for i in range(len(blocks)):
        if blocks[i] is None:
            continue
        ymin_i, ymax_i, xmin_i, xmax_i, _ = blocks[i]
        for j in range(len(blocks)):
            if i == j or blocks[j] is None:
                continue
            ymin_j, ymax_j, xmin_j, xmax_j, _ = blocks[j]
            if (ymin_i <= ymin_j and ymax_i >=
                    ymax_j and xmin_i <= xmin_j and xmax_i >= xmax_j):
                blocks[j] = None
    blocks = [block for block in blocks if block is not None]

    # OCRする順番に整列
    blocks = sorted(blocks, key=lambda x: (x[-1], x[0]))

    img_paths = []
    for i, (ymin, ymax, xmin, xmax, _) in enumerate(blocks):
        img_out = img[ymin:ymax, xmin:xmax]
        h, s, v = cv2.split(cv2.cvtColor(img_out, cv2.COLOR_BGR2HSV))
        print(f"img_s.mean: {s.mean()}")
        if s.mean() > 0.5:
            continue
        save_path = f"{dir_save}/{i}.jpg"
        cv2.imwrite(save_path, img_out)
        img_paths.append(save_path)

    if debug:
        img_copy = img.copy()
        for ymin, ymax, xmin, xmax, _ in blocks:
            cv2.rectangle(img_copy, (xmin, ymin), (xmax, ymax), (0, 0, 255), 4)
        cv2.namedWindow("dst", cv2.WINDOW_NORMAL)
        cv2.imshow("dst", img_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return img_paths
