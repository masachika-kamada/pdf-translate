from PyPDF2 import PdfFileReader


def main():
    text = ""
    with open("./pdf_files/YOLOv4.pdf", "rb") as input:
        reader = PdfFileReader(input)

        pages = reader.getNumPages()
        print(pages)

        for i in range(pages):
            page = reader.getPage(i)
            text += page.extractText()

    with open("./pdf_files/read_pypdf2.txt", mode="w", encoding='UTF-8') as f:
        f.write(text)


if __name__ == '__main__':
    main()
