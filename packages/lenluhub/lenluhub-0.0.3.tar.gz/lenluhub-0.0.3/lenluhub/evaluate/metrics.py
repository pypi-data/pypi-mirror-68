#!/usr/bin/python
#coding:utf-8

"""
@author: yangst2
@contact: yangst2@lenovo.com
@software: PyCharm
@file: metrics.py
@time: 2020/4/12 20:39
"""

from sklearn.metrics import f1_score, accuracy_score, recall_score
import tensorflow.keras as keras
import numpy as np
import json
import os


class MultiClassCallback(keras.callbacks.Callback):
    best_f1 = 0.0
    best_epoch = 0.0

    def __init__(self, model_save_dir, patience=5, test_data=None, id2label=None):
        self.model_save_dir = model_save_dir
        self.patience = patience
        self.test_data = test_data
        self.id2label = id2label
        self.metrics_score = dict()
        self.metrics_score.setdefault("f1", [])
        self.metrics_score.setdefault("precision", [])
        self.metrics_score.setdefault("recall", [])
        super().__init__()

    def on_epoch_end(self, epoch, logs=None):
        predict_result = self.model.predict(self.test_data[0])
        pred_label = [self.id2label[_] for _ in np.argmax(predict_result, -1)]
        real_label = [self.id2label[_] for _ in np.argmax(self.test_data[1], -1)]
        f1 = f1_score(real_label, pred_label, average="micro")
        precision = accuracy_score(real_label, pred_label)
        recall = recall_score(real_label, pred_label, average="micro")
        self.metrics_score["f1"].append(f1)
        self.metrics_score["precision"].append(precision)
        self.metrics_score["recall"].append(recall)
        print(" - Current Epoch: {} Validate F1: {} and the Best Validate F1:{}".format(epoch, f1, self.best_f1))
        if f1 > self.best_f1:
            self.best_f1 = f1
            self.best_epoch = epoch
            self.model.save_weights(self.model_save_dir + '/best_model.weights')
        else:
            if epoch - self.best_epoch >= self.patience:
                self.model.stop_training = True
                print("Early stopping at epoch {}, and final Validate F1: {}".format(epoch, self.best_f1))

    def on_train_end(self, logs=None):
        with open(os.path.join(self.model_save_dir, "train_log.txt"), "w", encoding="utf8") as f:
            f.write(json.dumps(self.metrics_score))
