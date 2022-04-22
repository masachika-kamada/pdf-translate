import streamlit as st
from lib.image_process import save_crop_image
from lib.image_process import pdf2images
from lib.ocr import AzureCV
from lib.translate import DeepL


def main():
    st.markdown('# PDF Translate')
    file = st.file_uploader('翻訳したいpdfファイルをアップロードしてください', type=['pdf'])
    azure_cv = AzureCV()
    deepl = DeepL()
    if file is not None:
        st.markdown(f'{file.name} をアップロードしました')
        with open("./pdf_files/src.pdf", "wb") as f:
            f.write(file.getvalue())

        imgs = pdf2images("./pdf_files/src.pdf")
        for img in imgs:
            img_paths = save_crop_image("./pdf_files/crop_imgs", img)

            for path in img_paths:
                block = open(path, "rb")
                text_en = azure_cv.ocr(block)
                print(text_en)
                # " ".joinだと改行による単語分割に対応できない
                # ブロックの途中で文が切れているものにも対応できない
                # TODO : translateに関数を追加
                text_ja = deepl.translate(" ".join(text_en))
                # st.write内の改行ができなかったので都度write
                st.write(" ".join(text_ja))


if __name__ == '__main__':
    main()
