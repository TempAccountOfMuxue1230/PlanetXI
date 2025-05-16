"""
File: helper/translator.py
File Version: 1.0
"""
import json
import os
import warnings


class Translator:
    """
    Translate special sign to correct language.
    """

    def __init__(self, assets_path="assets/", correct_lang="zh_cn"):
        self.lang_file_path = assets_path + "lang/"
        self.correct_lang = correct_lang
        self.default_lang = "en_us"
        self.dir_lang = os.listdir(self.lang_file_path)

        with open(self.lang_file_path + self.correct_lang + ".json", encoding="utf-8") as f:
            self.translate_dic = json.load(f)

    def use_lang(self, lang):
        if lang + ".json" in self.dir_lang:
            self.correct_lang = lang

            with open(self.lang_file_path + self.correct_lang + ".json", encoding="utf-8") as f:
                self.translate_dic = json.load(f)
        else:
            warnings.warn(
                "The target language translate file does not exist. Language has already replaced to default.",
                RuntimeWarning
            )
            self.correct_lang = self.default_lang

            with open(self.lang_file_path + self.correct_lang + ".json", encoding="utf-8") as f:
                self.translate_dic = json.load(f)

    def translate(self, text):
        target_clip = text.split(".")
        correct_clip = self.translate_dic
        for clip in target_clip:
            try:
                correct_clip = correct_clip[clip]
            except KeyError:
                return text

        return correct_clip
