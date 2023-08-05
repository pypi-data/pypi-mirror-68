#!/usr/bin/python
#coding:utf-8

"""
@author: yangst2
@contact: yangst2@lenovo.com
@software: PyCharm
@file: Tokenizer.py
@time: 2020/4/11 19:50
"""

import json
import shutil, os
from collections import defaultdict
from lenluhub.common.utils import remove_multi_blank, sequence_padding
from bert4keras.tokenizers import Tokenizer


class BertTokenizer(Tokenizer):

    def __init__(self, config: defaultdict):
        self.config = config
        self.token_dict_path = config.get("token_dict_path", None)
        self.max_len = config.get("max_len", 512)
        self.lower_case = config.get("lower_case", False)
        self.remove_multi_blank = config.get("remove_multi_blank", False)
        super().__init__(self.token_dict_path)

    def pre_process(self, text):
        """针对训练样本进行预处理"""
        if text is None:
            return None
        if self.lower_case:
            text = text.lower()
        if self.remove_multi_blank:
            text = remove_multi_blank(text)
        return text

    def encode(
        self,
        first_text,
        second_text=None,
        max_length=None,
        first_length=None,
        second_length=None
    ):
        first_text = self.pre_process(first_text)
        if second_text is not None:
            second_text = self.pre_process(second_text)
        enc = super().encode(first_text=first_text, second_text=second_text, max_length=self.max_len)
        enc = sequence_padding(enc, length=self.max_len)
        return enc[0].tolist(), enc[1].tolist()

    def save_config_to_file(self, save_path):
        """
        保存配置，便于重新加载部署服务
        :param save_path:
        :return:
        """
        with open("{}/tokenizer_config.json".format(save_path), "w", encoding="utf8") as f:
            print(self.token_dict_path)
            (_, config_file_name) = os.path.split(self.token_dict_path)
            shutil.copyfile(self.token_dict_path, dst=os.path.join(save_path, config_file_name))
            self.config["token_dict_path"] = config_file_name
            content = json.dumps(self.config, ensure_ascii=False)
            f.write(content+"\n")

    @staticmethod
    def load(save_path: str):
        """
        根据Config加载得到Tokenizer
        :param save_path:
        :return:
        """
        with open("{}/tokenizer_config.json".format(save_path), "r", encoding="utf8") as f:
            config = json.loads(f.read())
            if "token_dict_path" in config.keys():
                config["token_dict_path"] = os.path.join(save_path, config["token_dict_path"])
            return BertTokenizer(config)


if __name__ == '__main__':

    config = defaultdict()
    config["token_dict_path"] = "../../en_bert_resource_uncased/vocab.txt"
    config["max_len"] = 10
    config["lower_case"] = False
    config["remove_multi_blank"] = False

    tokenizer = BertTokenizer(config)
    print(tokenizer.encode("i am a boyd"))

