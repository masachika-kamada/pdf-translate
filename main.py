import streamlit as st
from lib.image_process import save_crop_image
from lib.image_process import pdf2images
from lib.image_process import save_formula_image
from lib.image_process import make_formula_pairs
from lib.ocr import AzureCV
from lib.translate import DeepL


def main():
    st.set_page_config(layout="wide")
    st.title("PDF Translate")
    file = st.file_uploader("翻訳したいpdfファイルをアップロードしてください", type=['pdf'])
    azure_cv = AzureCV()
    deepl = DeepL()
    if file is not None:
        st.write(f"#### {file.name} をアップロードしました")
        with open("./pdf_files/src.pdf", "wb") as f:
            f.write(file.getvalue())

        cols = st.columns([2, 1])
        cols[0].write("### 翻訳文")
        cols[1].write("### 数式対応表")
        cols[1].write(" ")

        imgs = pdf2images("./pdf_files/src.pdf")
        formula_dict_dst = {}
        for img in imgs:
            img_paths, img_widths = save_crop_image("./pdf_files/crop_imgs", img)
            for path, width in zip(img_paths, img_widths):
                text_en, formula_dict = azure_cv.ocr(path, width)
                save_formula_image("./pdf_files/formulas", path, formula_dict)
                # タイトルに対応
                if text_en[0:2] == "##":
                    text_en = text_en.replace("##", "")
                    bold = True
                else:
                    bold = False
                text_ja = deepl.translate(text_en)
                text_ja = text_ja.replace("xxxx", "<")
                text_ja = text_ja.replace("xxx", ">")
                if bold:
                    text_ja = "## " + text_ja
                # st.write内の改行ができなかったので都度write
                for print_text in text_ja.split("\n"):
                    cols[0].write(print_text)
                formula_dict_dst.update(formula_dict)
        print(formula_dict_dst)
        formula_path = make_formula_pairs("./pdf_files/formulas", formula_dict_dst)
        cols[1].image(formula_path, use_column_width=True)


if __name__ == '__main__':
    main()
