from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time
import json
import copy


class AzureCV:
    formula_idx = 0
    text = []
    formula_dict = {}

    def __init__(self):
        with open("./secret.json") as f:
            secret = json.load(f)
        subscription_key = secret["SUBSCRIPTION_KEY"]
        endpoint = secret["ENDPOINT"]
        self.computervision_client = ComputerVisionClient(
            endpoint, CognitiveServicesCredentials(subscription_key))

    def ocr(self, path, width):
        self.text = []
        self.formula_dict = {}
        self.width = width
        img = open(path, "rb")
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

        if read_result.status == OperationStatusCodes.succeeded:
            # copyでアクセス制限の回避
            read_result_cp = copy.copy(read_result)
            if "_" in path.split("/")[-1]:
                self.reshape_ocr_result(read_result_cp, False)
            else:
                self.reshape_ocr_result(read_result_cp)
        return " ".join(self.text), self.formula_dict

    def reshape_ocr_result(self, ocr_result, formula=True):
        for text_result in ocr_result.analyze_result.read_results:
            for line in text_result.lines:
                line_text = []
                line_bbox = reshape_bbox(line.bounding_box)
                # 題名を拡大表示
                line_height = line_bbox[1] - line_bbox[0]
                if line_height > 45:
                    self.text.append("##")
                # 数式の認識系
                n_formula = 0
                formula_dict_tmp = {}
                n_word = len(line.words)
                for word in line.words:
                    if word.confidence > 0.8 or word.text == "." or formula is False:
                        line_text.append(word.text)
                    else:
                        n_formula += 1
                        formula_bbox = reshape_bbox(word.bounding_box)
                        formula_text = f"xxx{word.text}xxx"
                        line_text.append(formula_text)
                        formula_dict_tmp[formula_text] = formula_bbox
                if n_formula >= (n_word - n_formula) * 0.45:
                    line_text = [f"xxxformula{self.formula_idx}xxx"]
                    self.formula_idx += 1
                    formula_dict_tmp = {line_text[0]: line_bbox}
                dst = " ".join(line_text)
                # インデントや改行に対応
                if line_bbox[-2] > 50 and line_height < 45:
                    dst = "\n" + dst
                if line_bbox[-1] < self.width - 50 and line_height < 45:
                    dst = dst + "\n"
                self.text.append(dst)
                self.formula_dict.update(formula_dict_tmp)


def reshape_bbox(azure_bbox):
    bbox = [
        int(azure_bbox[1]),
        int(azure_bbox[5]),
        int(azure_bbox[0]),
        int(azure_bbox[4])]
    return bbox
