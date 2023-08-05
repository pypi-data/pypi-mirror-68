#!/usr/bin/python
#coding:utf-8

"""
@author: yangst2
@contact: yangst2@lenovo.com
@software: PyCharm
@file: ClassificationTask.py
@time: 2020/4/12 11:59
"""

import json, os, shutil
import tensorflow.keras as keras
from lenluhub.dataset.classification_dataset import BertClsDataSet
from bert4keras.models import build_transformer_model
from lenluhub.evaluate import metrics
from collections import defaultdict
import keras


class Classifier:

    def __init__(self):
        pass

    def predict(self, tmp_input, top_k=1):
        raise NotImplementedError


class BertClassifier(Classifier):

    def __init__(self, config: defaultdict):
        self.task_name = config["task_name"]
        self.bot_id = config["bot_id"]
        self.model_save_dir = config["model_save_dir"]
        self.id2label = config.get("id2label", None)
        self.multi_label = config.get("multi_label", False)
        self.max_len = config.get("max_len", 0)
        self.label_num = config.get("label_num", 0)
        self.bert_config_path = config.get("bert_config_path", None)
        self.bert_checkpoint_path = config.get("bert_checkpoint_path", None)
        self.train_data, self.test_data = None, None
        self.tokenizer = None
        self.model = None
        super().__init__()

    def load_config_from_data_set(self, data_set: BertClsDataSet):
        """根据DataSet确定构建模型所需要的部分参数"""
        self.id2label = data_set.id2label
        self.max_len = data_set.tokenizer.max_len
        self.multi_label = data_set.multi_label
        self.label_num = data_set.label_num
        self.train_data = data_set.train_data
        self.test_data = data_set.test_data

    def build_model(self):
        bert = build_transformer_model(
            config_path=self.bert_config_path,
            checkpoint_path=self.bert_checkpoint_path,
            model='bert',
            return_keras_model=False
        )
        output = keras.layers.Lambda(lambda x: x[:, 0])(bert.model.output)
        output = keras.layers.Dense(units=self.label_num, activation=keras.activations.softmax,)(output)
        self.model = keras.models.Model(bert.model.inputs, output)
        self.model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(lr=0.0001), metrics=["acc"])

    def fit(self, batch_size=64, epochs=15):
        callback = metrics.MultiClassCallback(self.model_save_dir, test_data=self.test_data, id2label=self.id2label)
        train_history = self.model.fit(x=self.train_data[0], y=self.train_data[1], batch_size=batch_size, epochs=epochs, callbacks=[callback])
        return train_history

    def predict(self, tmp_input, top_k=1):
        probability = self.model.predict([[tmp_input[0]], [tmp_input[1]]])[0]
        label_props = dict()
        for i in range(len(probability)):
            label_props[self.id2label[i]] = probability[i]
        items = [item for item in label_props.items()]
        items.sort(key=lambda x: x[1], reverse=True)
        result = []
        for item in items[:top_k]:
            tmp = dict()
            tmp[self.task_name] = item[0]
            tmp["confidence"] = float(item[1])
            tmp["procMethod"] = "model"
            result.append(tmp)
        return json.dumps(result, ensure_ascii=False)

    def save(self, model_save_dir):
        params = dict()
        params["bot_id"] = self.bot_id
        params["task_name"] = self.task_name
        params["max_len"] = self.max_len
        params["label_num"] = self.label_num
        params["multi_label"] = self.multi_label
        params["id2label"] = self.id2label
        (_, config_file_name) = os.path.split(self.bert_config_path)
        shutil.copyfile(self.bert_config_path, dst=os.path.join(model_save_dir, config_file_name))
        params["bert_config_path"] = config_file_name
        params["model_save_dir"] = self.model_save_dir
        with open("{}/model_config.json".format(model_save_dir), "w", encoding="utf8") as f:
            f.write(json.dumps(params, ensure_ascii=False)+"\n")

    @staticmethod
    def load_model(save_path):
        """
        根据Config自动创建模型，加载相应的权重
        :param model_config_path:
        :return:
        """
        with open("{}/model_config.json".format(save_path), "r", encoding="utf8") as f:
            params = json.loads(f.read())
            new_id2label = dict()
            if "id2label" in params.keys():
                for item in params["id2label"].items():
                    new_id2label[int(item[0])] = item[1]
            params["id2label"] = new_id2label
            if "bert_config_path" in params.keys():
                params["bert_config_path"] = os.path.join(save_path, params["bert_config_path"])
        model = BertClassifier(params)
        model.build_model()
        model.model.load_weights("{}/best_model.weights".format(save_path))
        return model

    def summary(self):
        self.model.summary()
