# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2019/12/20 23:08
# @author  : Mo
# @function: predict(albert+bilstm)


# win10必须加，否则报错
import multiprocessing as mp
mp.freeze_support()
mp.set_start_method("spawn", force=True)


from macropodus.network.service.server_base import Streamer
from macropodus.preprocess.tools_ml import extract_chinese
from tensorflow.python.keras.models import model_from_json
from macropodus.preprocess.tools_common import load_json
from keras_bert import Tokenizer
import numpy as np
import macropodus
import codecs
import os

# flask
from flask import Flask, request, jsonify
import logging

# 常规
class AlbertBilstmPredict:
    def __init__(self, path_dir):
        self.path_dir = path_dir
        self.tokenizer_init()
        self.l2i_i2l_init()
        self.params_init()
        self.model_init()

    def model_init(self):
        """模型初始化"""
        path_graph = os.path.join(self.path_dir, "graph.json")
        path_model = os.path.join(self.path_dir, "model.h5")
        # 加载模型结构
        self.model = model_from_json(open(path_graph, "r", encoding="utf-8").read(),
                                custom_objects=macropodus.custom_objects)
        # 加载模型权重
        self.model.load_weights(path_model)

    def tokenizer_init(self):
        """字典"""
        # reader tokenizer
        token_dict = {}
        path_dict = os.path.join(self.path_dir, "vocab.txt")
        with codecs.open(path_dict, 'r', 'utf8') as reader:
            for line in reader:
                token = line.strip()
                token_dict[token] = len(token_dict)
        # vocab_size = len(token_dict)
        self.tokenizer = Tokenizer(token_dict)

    def params_init(self):
        """超参数初始化"""
        # params
        path_params = os.path.join(self.path_dir, "params.json")
        self.params = load_json(path_params)
        self.len_max = self.params["len_max"]

    def l2i_i2l_init(self):
        """类别与数字项目转化"""
        # l2i_i2l
        path_l2i_i2l = os.path.join(self.path_dir, "l2i_i2l.json")
        self.l2i_i2l = load_json(path_l2i_i2l)

    def sentence2idx(self, text, second_text=None):
        """数据预处理"""
        text = extract_chinese(str(text).upper())
        input_id, input_type_id = self.tokenizer.encode(first=text, second=second_text, max_len=self.len_max)
        input_mask = len([1 for ids in input_id if ids != 0])
        # return input_id, input_type_id, input_mask
        # x_ = np.array((input_id, input_type_id, input_mask))
        x = [[input_id, input_type_id, input_mask]]
        x_ = np.array(x)
        x_1 = np.array([x[0] for x in x_])
        x_2 = np.array([x[1] for x in x_])
        x_3 = np.array([x[2] for x in x_])
        return [x_1, x_2, x_3]

    def predict(self, ques):
        """预测"""
        mode_input = self.sentence2idx(ques)
        res = self.model.predict(mode_input)
        res_list = res.tolist()[0]
        res_idxs = [np.argmax(rl) for rl in res_list]
        res_label = [self.l2i_i2l["i2l"][str(ri)] if str(ri) in self.l2i_i2l["i2l"] else "O" for ri in  res_idxs]
        return res_label[1:len(ques)+1]

# 一个进程多个线程等
class ServiceNer:
    def __init__(self, path_model_dir, cuda_devices="0",
                       max_latency=0.01, worker_num=1, batch_size=32):
        self.path_model_dir = path_model_dir
        self.cuda_devices = cuda_devices
        self.max_latency = max_latency
        self.worker_num = worker_num
        self.batch_size = batch_size
        self.algorithm = 'albert-ner-bilstm-crf'
        self.streamer_init(self.path_model_dir, cuda_devices=self.cuda_devices,
                           max_latency=self.max_latency, worker_num=self.worker_num,
                           batch_size=self.batch_size)

    def streamer_init(self, path_abs, cuda_devices="0", max_latency=0.01,
                            worker_num=1, batch_size=32):
        """
            ner初始化
        :param path_abs: str, like "ner_model"
        :param batch_size: int, like 32
        :param max_latency: float, 0-1, like 0.01
        :param worker_num: int, like 2
        :param cuda_devices: str, like "0,1"
        :return: 
        """
        abp = AlbertBilstmPredict(path_abs)
        self.streamer = Streamer(predict_function_or_model=abp,
                                 cuda_devices=cuda_devices,
                                 max_latency=max_latency,
                                 worker_num=worker_num,
                                 batch_size=batch_size, )

        return self.streamer

    def streamer_predict(self, text):
        """
            预测返回
        :param text: str, like "桂林"
        :return: list, like ["B-LOC", "I-LOC"]
        """
        return self.streamer.predict(text)


def model_predict(streamer_real):
    """
        复合使函数方法通用
    :return: 
    """
    params = request.form if request.form else request.json
    sentences = params.get('texts', '')
    res00 = []
    try:
        res00 = streamer_real.predict(sentences)
    except Exception:
        gg = 0
    res = {'result_code': 0,
           'result_message': '调用成功',
           'prob_dist': res00  # 只打印top5类别
           }
    return res


# 模型加载
path = "D:/workspace/pythonMyCode/Macropodus/macropodus/data/ner_people_1998_mix_albert_1"
abp = AlbertBilstmPredict(path)
# streamer_11 = model_streamer(path_abs_11)
app = Flask(__name__)


@app.route('/text_classification/textcnn_cust_notval_11/predict', methods=["GET"])
def textcnn_cust_notval_11_predict():
    """
        催收11分类
    :return:
    """
    res = model_predict(abp)
    return jsonify(content=res,
                   content_type='application/json;charset = utf-8',
                   status='200',
                   reason='success',
                   charset='utf-8')


if __name__ == '__main__':
    # app.run()
    # app.run(port=8080, threaded=True, host='0.0.0.0', debug=False)
    while True:
        print("请输入:")
        ques = input()
        res = abp.predict(ques)
        print(res)

# if __name__ == '__main__':
#     path = "D:/workspace/pythonMyCode/Macropodus/macropodus/data/ner_people_1998_mix_albert_1"
#     # abp = AlbertBilstmPredict(path)
#     abp = ServiceNer(path)
#     while True:
#         print("请输入:")
#         ques = input()
#         res = abp.predict(ques)
#         print(res)


