import streamlit as st
import deepl
import json


def main():
    st.markdown('# PDF Translate')
    file = st.file_uploader('翻訳したいpdfファイルをアップロードしてください', type=['pdf'])
    text = "Brushless DC motors are widely used in industrial applications and computer peripheral devices, because of no brush and commutator, wide speed range, and relatively high efficiency"
    if file is not None:
        st.markdown(f'{file.name} をアップロードしました')
        with open("./pdf_files/src.pdf", "wb") as f:
            f.write(file.getvalue())

        with open("./secret.json") as f:
            secret = json.load(f)

        KEY = secret["KEY"]
        translator = deepl.Translator(KEY)
        result = translator.translate_text(text, source_lang="EN", target_lang="JA")
        translated_text = result.text
        st.write(translated_text)


if __name__ == '__main__':
    main()
