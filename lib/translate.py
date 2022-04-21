import deepl
import json


class DeepL:
    def __init__(self):
        with open("./secret.json") as f:
            secret = json.load(f)
        KEY = secret["KEY"]
        self.translator = deepl.Translator(KEY)

    def translate(self, text):
        result = self.translator.translate_text(
            text, source_lang="EN", target_lang="JA")
        return result.text
