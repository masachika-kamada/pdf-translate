import streamlit as st
from lib.image_process import save_crop_image
from lib.translate import DeepL
from lib.ocr import pdf2images
from lib.ocr import AzureCV


def main():
    st.markdown('# PDF Translate')
    file = st.file_uploader('翻訳したいpdfファイルをアップロードしてください', type=['pdf'])
    deepl = DeepL()
    azure_cv = AzureCV()
    if file is not None:
        st.markdown(f'{file.name} をアップロードしました')
        with open("./pdf_files/src.pdf", "wb") as f:
            f.write(file.getvalue())

        dst = ""

        imgs = pdf2images("./pdf_files/src.pdf")
        for img in imgs:
            img_paths = save_crop_image("./pdf_files/crop_imgs", img)

            for path in img_paths:
                block = open(path, "rb")
                text_en = azure_cv.ocr(block)
                print(text_en)
                text_ja = deepl.translate(text_en)
                dst += text_ja

        st.write(dst)


if __name__ == '__main__':
    main()
