#!/usr/bin/env python
# encoding: utf-8

"""
@version: v1.0
@author: YangST
@software: PyCharm Community Edition
@file: cnn_online.py
@time: 2017/8/30 9:43
"""
from abc import ABC

import logging
import asyncio
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado.web import RequestHandler
from typing import Type
from lenluhub.web.handlers import SingleInputHandler


class Service:

    def __init__(self):
        pass



class HttpsService(Service):

    def __init__(self, handler: RequestHandler, service_port=9001, service_url=""):
        tornado.options.parse_command_line()
        self.service_port = service_port
        self.service_url = service_url
        self.handler = handler
        define("port", default=self.service_port, help="run on the given port", type=int)
        self.app = tornado.web.Application([(r"/{}".format(self.service_url), self.handler)])
        self.app.listen(options.port)
        self.__ioloop = tornado.ioloop.IOLoop.instance()
        super().__init__()

    def start_service(self):
        self.__ioloop.start()

    def stop_service(self):
        self.__ioloop.stop()

