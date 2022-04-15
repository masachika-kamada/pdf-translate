from pdfminer.high_level import extract_text


def main():
    FILE_PATH = "./pdf_files/src.pdf"
    text = extract_text(FILE_PATH)

    with open("./pdf_files/read_pdfminer.txt", mode="w", encoding='UTF-8') as f:
        f.write(text)


if __name__ == '__main__':
    main()
