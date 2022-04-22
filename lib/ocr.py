from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time
import json


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
            read_result = self.computervision_client.get_read_result(operation_id)
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
                    # TODO : 数式の認識系
                    # line_words = ""
                    # for word in line.words:
                    #     line_words += word.text + " "
                    #     text.append([word.text, word.confidence])
        return text
