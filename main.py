import streamlit as st
import deepl
import json
from PyPDF2 import PdfFileReader


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
    # deepl = DeepL()
    if file is not None:
        st.markdown(f'{file.name} をアップロードしました')
        with open("./pdf_files/src.pdf", "wb") as f:
            f.write(file.getvalue())
        with open("./pdf_files/src.pdf", "rb") as input:
            reader = PdfFileReader(input)

        pages = reader.getNumPages()
        print(pages)
        # st.write(f"pdf has {reader.getNumPages()} pages")

        # page = reader.getPage(0)
        # # 読み込んだページのテキストを抽出
        # text = page.extractText()
        # st.write(text)


if __name__ == '__main__':
    main()
