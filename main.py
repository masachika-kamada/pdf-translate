import streamlit as st
import deepl
import json
import cv2

from lib.image_process import crop_image


class DeepL:
    def __init__(self):
        with open("./secret.json") as f:
            secret = json.load(f)
        KEY = secret["KEY"]
        self.translator = deepl.Translator(KEY)

    def translate(self, text):
        result = self.translator.translate_text(
            text, source_lang="EN", target_lang="JA")
        return result.text


def main():
    st.markdown('# PDF Translate')
    file = st.file_uploader('翻訳したいpdfファイルをアップロードしてください', type=['pdf'])
    deepl = DeepL()
    if file is not None:
        st.markdown(f'{file.name} をアップロードしました')
        with open("./pdf_files/src.pdf", "wb") as f:
            f.write(file.getvalue())

        img = cv2.imread("./pdf_files/imgs/page1.jpg")
        res = crop_image(img)

        # read text from pdf
        text = "I am happy."

        st.write(deepl.translate(text))


if __name__ == '__main__':
    main()
