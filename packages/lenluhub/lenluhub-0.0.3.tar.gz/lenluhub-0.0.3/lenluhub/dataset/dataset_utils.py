#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on 2020/5/6

from typing import List


def build_label_vocab(labels: List[str], multi_label=False):
    """
    根据标签值，构造标签集合
    :param labels: 标签序列
    :param multi_label: 是否为多标签
    :return:
    """
    label_vocab = set()
    if not multi_label:
        label_vocab = set(labels)
    else:
        for ll in labels:
            ll = ll.split("|")
            label_vocab.update(ll)
    return label_vocab


def to_category(row_labels: str, label2id: dict, multi_label=False):
    tmp = [0] * len(label2id)
    if not multi_label:
        tmp[label2id[row_labels]] = 1
        return tmp
    else:
        for l in row_labels.split("|"):
            tmp[label2id[l]] = 1
        return tmp

