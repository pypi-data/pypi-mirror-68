#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on 2020/4/17

import logging
import asyncio
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado.web import RequestHandler
from typing import Type
from lenluhub.web.handlers import SingleInputHandler
from tornado.escape import json_decode
from lenluhub.common.errors import ErrorMessage
from lenluhub.processor.tokenizer import BertTokenizer
from lenluhub.tasks.classification_task import BertClassifier
from lenluhub.web.service import HttpsService
import asyncio

class MainHandler(RequestHandler):

    def __init__(self, application, request):
        super().__init__(application, request)

    def post(self, *args, **kwargs):
        param_format = """
        {
           "query":"how to update my phone"
        }
        """
        print(self.request.body)

        data_rec = json_decode(self.request.body)
        print(data_rec)
        if data_rec is None or len(data_rec) == 0 or "bot_id" not in data_rec.keys() or "task_name" not in data_rec.keys():
            self.write(ErrorMessage.reques_parameter_error)
        else:
            task_name = data_rec["task_name"]
            service_url = ""
            if "service_url" in data_rec.keys():
                service_url = data_rec["service_url"]
            model_save_dir = "../../demo/demo_model"
            tokenizer = BertTokenizer.load(model_save_dir)
            model = BertClassifier.load_model(model_save_dir)
            hanlder = type("{}_service_handler".format(task_name), (SingleInputHandler,), {"model": model, "tokenizer": tokenizer})
            self.application.add_handlers(r".*", [("/{}".format(service_url), hanlder)])
            self.write("模型训练完成，服务已启动，请访问:http://127.0.0.1:{}/{}\n进行验证，访问参数要求：\n{}".format(9001, service_url, param_format))

if __name__ == "__main__":

    app = tornado.web.Application(handlers=[(r"/", MainHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(9001)
    tornado.ioloop.IOLoop.instance().start()
