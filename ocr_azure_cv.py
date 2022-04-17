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
        read_response = self.computervision_client.read_in_stream(img, raw=True)
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
                    print(line.text)
                    text.append(line.text)
                    # print(line.bounding_box)
        return text


print("===== Read File - local =====")
img_path = "./pdf_files/imgs/page1.jpg"
img = open(img_path, "rb")
azure_cv = AzureCV()
result = azure_cv.ocr(img)
