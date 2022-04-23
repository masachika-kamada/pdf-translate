import streamlit as st
from lib.image_process import save_crop_image
from lib.image_process import pdf2images
from lib.image_process import save_formula_image
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
        formula_dict_dst = {}
        for img in imgs:
            img_paths, img_widths = save_crop_image("./pdf_files/crop_imgs", img)
            for path, width in zip(img_paths, img_widths):
                text_en, formula_dict = azure_cv.ocr(path, width)
                save_formula_image("./pdf_files/formulas", path, formula_dict)
                print(text_en)
                text_ja = deepl.translate(text_en)
                # st.write内の改行ができなかったので都度write
                for print_text in text_ja.split("\n"):
                    st.write(print_text)
                formula_dict_dst.update(formula_dict)
        st.write(formula_dict_dst)


if __name__ == '__main__':
    main()
