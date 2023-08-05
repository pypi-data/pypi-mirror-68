#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on 2020/4/16

from tornado.escape import json_decode
from tornado.web import RequestHandler
from lenluhub.tasks.classification_task import Classifier, BertClassifier
from lenluhub.processor.tokenizer import BertTokenizer
from lenluhub.common.errors import ErrorMessage
from typing import List
from abc import ABC

# 为了解决一个bot需要多个服务的情况，这里将服务和handlder进行绑定，即一个handler 这样新增model服务的时候 只需要增加一个hanlder
# 然后所有的handlder注册到一个server下面


class SingleInputHandler(RequestHandler, ABC):

    def __init__(self, application, request):
        super().__init__(application, request)

    def set_predict_model(self, model: Classifier, tokenizer: BertTokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def predict_label(self, sentence):
        """
        :param sentence:
        :return:
        """
        enc = self.tokenizer.encode(sentence)
        result = self.model.predict([enc[0], enc[1]])
        return result

    def post(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        try:
            data_rec = json_decode(self.request.body)
            if data_rec is None or len(data_rec) == 0 or "query" not in data_rec.keys():
                self.write(ErrorMessage.reques_parameter_error)
            else:
                source_sentence = data_rec["query"]
                result = self.predict_label(source_sentence)
                self.write(result)
        except Exception as e:
            print(e)
            self.write(ErrorMessage.server_inner_error)


if __name__ == '__main__':

    pass