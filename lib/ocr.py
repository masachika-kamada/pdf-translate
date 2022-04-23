from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time
import json
import copy


class AzureCV:
    formula_idx = 0

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
        formula_dict = {}
        if read_result.status == OperationStatusCodes.succeeded:
            # copyでアクセス制限の回避
            read_result_cp = copy.copy(read_result)
            for text_result in read_result_cp.analyze_result.read_results:
                for line in text_result.lines:
                    from icecream import ic
                    line_text = []
                    ic(line.bounding_box)
                    line_bbox = reshape_bbox(line.bounding_box)
                    line_bbox_width = line_bbox[-1] - line_bbox[-2]
                    # TODO : 数式の認識系
                    formula_width = 0
                    formula_dict_tmp = {}
                    for word in line.words:
                        if word.confidence > 0.8 or word.txt == ".":
                            line_text.append(word.text)
                        else:
                            formula_bbox = reshape_bbox(word.bounding_box)
                            ic(formula_bbox)
                            ic(len(formula_bbox))
                            ic(formula_bbox[-1])
                            formula_width += formula_bbox[-1] - formula_bbox[-2]
                            formula_text = "xxxxxx" + word.text
                            line_text.append(formula_text)
                            formula_dict_tmp[formula_text] = reshape_bbox(word.bounding_box)
                    if formula_width > line_bbox_width * 0.5:
                        line_text = [f"<formula{self.formula_idx}>"]
                        self.formula_idx += 1
                        formula_dict_tmp = {line_text[0]: line_bbox}
                    dst = " ".join(line_text)
                    text.append(dst)
                    formula_dict.update(formula_dict_tmp)
                    ic(line_text)
        return text, formula_dict


def reshape_bbox(azure_bbox):
    return [
        azure_bbox[1],
        azure_bbox[5],
        azure_bbox[0],
        azure_bbox[4]]
