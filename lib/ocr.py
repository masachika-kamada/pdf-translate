import pyocr
import pyocr.builders
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import pdf2image
import time
import json


def pdf2images(file_path):
    images = pdf2image.convert_from_path(
        file_path,
        poppler_path="C:/poppler-22.01.0/Library/bin",
        dpi=200,
        fmt='jpg')
    return images


class AzureCV:
    def __init__(self):
        with open("./secret.json") as f:
            secret = json.load(f)
        subscription_key = secret["SUBSCRIPTION_KEY"]
        endpoint = secret["ENDPOINT"]
        self.computervision_client = ComputerVisionClient(
            endpoint, CognitiveServicesCredentials(subscription_key))

    def ocr(self, img):
        """azureのcomputer vision clientでOCR

        Args:
            img: バイナリで読み込み

        Returns:
            text: listで読んだ文字を出力
        """
        read_response = self.computervision_client.read_in_stream(
            img, raw=True)
        read_operation_location = read_response.headers["Operation-Location"]
        operation_id = read_operation_location.split("/")[-1]

        while True:
            read_result = self.computervision_client.get_read_result(
                operation_id)
            if read_result.status.lower() not in ['notstarted', 'running']:
                break
            print('Waiting for result...')
            time.sleep(3)

        text = []
        if read_result.status == OperationStatusCodes.succeeded:
            for text_result in read_result.analyze_result.read_results:
                for line in text_result.lines:
                    # print(line.text)
                    text.append(line.text)
                    # print(line.bounding_box)
                    # 数式の認識系
                    # line_words = ""
                    # for word in line.words:
                    #     line_words += word.text + " "
                    #     text.append([word.text, word.confidence])
        return text


class Tesseract:
    def __init__(self):
        pyocr.tesseract.TESSERACT_CMD = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
        self.tool = pyocr.get_available_tools()[0]

    def ocr(self, img):
        """tesseractでOCR

        Args:
            img: np.ndarrayで入力、Pillow形式だがモノクロなのでそのままでOK

        Returns:
            text: 改行込みの文字列を出力
        """
        result = self.tool.image_to_string(
            img,
            lang="eng",
            builder=pyocr.builders.TextBuilder()
        )
        return result
