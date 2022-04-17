import cv2
import glob


def mouse_event(event, x, y, flags, param):
    global crds
    if event == cv2.EVENT_LBUTTONUP:
        crds.append((x, y))
        if len(crds) > 2:
            del crds[0]


def main():
    global crds
    crds = []
    img = cv2.imread("./pdf_files/imgs/page1.jpg")
    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("img", mouse_event)
    idx = len(glob.glob("./pdf_files/text_block/*.jpg"))

    while True:
        img_tmp = img.copy()
        if len(crds) == 2:
            cv2.rectangle(img_tmp, crds[0], crds[1], (255, 0, 0), 3)
        cv2.imshow("img", img_tmp)
        key = cv2.waitKey(10) & 0xFF
        if key == ord("s"):
            (xmin, ymin), (xmax, ymax) = crds
            dst = img[ymin:ymax, xmin:xmax]
            cv2.imwrite(f"./pdf_files/text_block/block{idx}.jpg", dst)
            idx += 1
        elif key == 27 or key == ord("q"):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    main()
