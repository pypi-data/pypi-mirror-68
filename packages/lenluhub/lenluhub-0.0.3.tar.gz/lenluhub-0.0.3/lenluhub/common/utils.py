#!/usr/bin/python
#coding:utf-8

"""
@author: yangst2
@contact: yangst2@lenovo.com
@software: PyCharm
@file: utils.py
@time: 2020/4/11 19:48
"""

import re
import numpy as np
from typing import Tuple, List


def sequence_padding(inputs, length=None, padding=0):
    if length is None:
        length = max([len(x) for x in inputs])
    pad_width = [(0, 0) for _ in np.shape(inputs[0])]
    outputs = []
    for x in inputs:
        x = x[:length]
        pad_width[0] = (0, length - len(x))
        x = np.pad(x, pad_width, 'constant', constant_values=padding)
        outputs.append(x)
    return np.array(outputs)


def remove_multi_blank(text):
    return re.sub(r"\s+", " ", text).lstrip().rstrip()


def read_plain_text(file_path, split_tag=None) -> Tuple[List[str], List[str]]:
    data_x, data_y = [], []
    with open(file_path, encoding="utf8") as f:
        for line in f.readlines()[0:]:
            line = line.strip("\n")
            if split_tag is None:
                split_tag = "\t"
            parts = line.split(split_tag)
            if len(parts) == 2:
                data_x.append(parts[0])
                data_y.append(str(parts[1]).lower())
    return list(data_x), list(data_y)


def build_mapping(label_vocab, add_one=False):
    label2id = dict()
    id2label = dict()
    for index, label in enumerate(label_vocab):
        if add_one:
            index += 1
        label2id[label] = index
        id2label[index] = label
    return label2id, id2label

def main():

    train_file_path = "../demo_data/train.txt"
    test_file_path = "../demo_data/train.txt"

    import os

    print(os.path.split(train_file_path))

    x, y = read_plain_text(train_file_path)
    for i in range(len(x)):
        print(x[i], y[i])


if __name__ == "__main__":
    main()