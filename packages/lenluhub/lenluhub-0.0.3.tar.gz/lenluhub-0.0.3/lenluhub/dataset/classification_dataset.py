#!/usr/bin/python
#coding:utf-8

"""
@author: yangst2
@contact: yangst2@lenovo.com
@software: PyCharm
@file: ClassificationDataset.py
@time: 2020/4/12 9:45
"""

import logging
import numpy as np
from lenluhub.common.utils import read_plain_text, build_mapping
from lenluhub.processor.tokenizer import BertTokenizer
from lenluhub.dataset import dataset_utils


class BertClsDataSet:

    def __init__(self, train_data_path, test_data_path=None,
                 tokenizer: BertTokenizer = None, multi_label=False,
                 max_training_case_num=10):
        """
        :param train_data_path: 训练数据路径
        :param test_data_path: 测试数据路径
        :param tokenizer: 分词器
        :param multi_label: 是否为多标签
        """
        self.train_data_path = train_data_path
        self.test_data_path = test_data_path
        self.tokenizer = tokenizer
        self.multi_label = multi_label
        self.max_training_case_num = max_training_case_num

        # 以下属性仅初始化，通过加载数据重新赋值
        self.train_data, self.test_data = None, None
        self.train_case_num, self.test_case_num, self.label_num = 0.0, 0.0, 0.0
        self.label2id, self.id2label = None, None
        self.load_data_set(train_data_path, test_data_path)
        self.label_vocab = None
        self.feature_num = 0

    def load_data_set(self, train_data_path, test_data_path):
        """
        处理数据集
        """
        logging.info("self: " + str(self))
        train_data_x, train_data_y = read_plain_text(train_data_path, split_tag="\t")
        test_data_x, test_data_y = read_plain_text(test_data_path, split_tag="\t")
        train_token_x, train_segment_x, test_token_x, test_segment_x = [], [], [], []
        for row in train_data_x:
            row_enc = self.tokenizer.encode(row)
            train_token_x.append(row_enc[0])
            train_segment_x.append(row_enc[1])
        train_token_x = np.array(train_token_x)
        train_segment_x = np.array(train_segment_x)
        for row in test_data_x:
            row_enc = self.tokenizer.encode(row)
            test_token_x.append(row_enc[0])
            test_segment_x.append(row_enc[1])
        test_token_x = np.array(test_token_x)
        test_segment_x = np.array(test_segment_x)

        train_label_vocab = dataset_utils.build_label_vocab(train_data_y, multi_label=self.multi_label)

        tmp_train_data_y, tmp_test_data_y = [], []
        label2id, id2label = build_mapping(train_label_vocab)
        for row_labels in train_data_y:
            tmp_train_data_y.append(dataset_utils.to_category(row_labels, label2id=label2id, multi_label=self.multi_label))
        for row_labels in test_data_y:
            tmp_test_data_y.append(dataset_utils.to_category(row_labels, label2id=label2id, multi_label=self.multi_label))

        train_token_x = np.array(train_token_x)[:self.max_training_case_num]
        train_segment_x = np.array(train_segment_x)[:self.max_training_case_num]
        train_data_y = np.array(tmp_train_data_y)[:self.max_training_case_num]
        test_token_x = np.array(test_token_x)[:self.max_training_case_num]
        test_segment_x = np.array(test_segment_x)[:self.max_training_case_num]
        test_data_y = np.array(tmp_test_data_y)[:self.max_training_case_num]

        self.train_data = [[train_token_x, train_segment_x], train_data_y]
        self.test_data = [[test_token_x, test_segment_x], test_data_y]
        self.label_vocab = train_label_vocab
        self.label_num = len(train_label_vocab)
        self.id2label = id2label

