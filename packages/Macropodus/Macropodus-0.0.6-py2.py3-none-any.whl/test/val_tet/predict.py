# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/6/3 10:51
# @author   :Mo
# @function :pred of text-cnn with baidu-qa-2019 in question title


# 适配linux
import pathlib
import sys
import os
project_path = str(pathlib.Path(os.path.abspath(__file__)).parent.parent.parent.parent)
sys.path.append(project_path)
# 地址
from macropodus.conf.path_config import path_model, path_fineture, path_model_dir, path_hyper_parameters, path_model_l2i_i2l
# 数据预处理, 删除文件目录下文件
from macropodus.preprocess.tools_common import load_json
from macropodus.network.preprocess.preprocess_generator import PreprocessGenerator
# 模型图
from macropodus.network.graph.bilstm_crf import BilstmCRFGraph as Graph
# 模型评估
from sklearn.metrics import classification_report
# 计算时间
import time

import numpy as np


def pred_input(path_hyper_parameter=path_hyper_parameters):
    # 输入预测
    # 加载超参数
    hyper_parameters = load_json(os.path.join(path_hyper_parameter, "params.json"))
    pt = PreprocessGenerator(os.path.join(path_hyper_parameters, "l2i_i2l.json"))
    # 模式初始化和加载
    graph = Graph(hyper_parameters)
    graph.load_model()
    ra_ed = graph.word_embedding
    ques = '北京是中国的首都，天安门，天安门广场，故宫，长城，天坛，水立方，鸟巢等这些地方我都想去'
    # str to token
    ques_embed = [ra_ed.sentence2idx(ques)]
    if hyper_parameters['embedding_type'] in ['bert', 'albert']:
        x_ = np.array(ques_embed)
        x_1 = np.array([x[0] for x in x_])
        x_2 = np.array([x[1] for x in x_])
        x_3 = np.array([x[2] for x in x_])
        # x_1 = np.array([x_[0]])
        # x_2 = np.array([x_[1]])
        # x_3 = np.array([x_[2]])
        if hyper_parameters['model']['crf_mode'] == 'pad':
            x_all = [x_1, x_2, x_3]
        elif hyper_parameters['model']['crf_mode'] == 'reg':
            x_all = [x_1, x_2]
        else:
            x_all = [x_1, x_2]
    else:
        x_ = np.array(ques_embed)
        x_1 = np.array([x[0] for x in x_])
        x_2 = np.array([x[1] for x in x_])
        if hyper_parameters['model']['crf_mode'] == 'pad':
            x_all = [x_1, x_2]
        elif hyper_parameters['model']['crf_mode'] == 'reg':
            x_all = x_1
        else:
            x_all = x_1
    # 预测
    pred = graph.predict(x_all)
    pred_arg = np.argmax(pred[0], axis=-1)
    len_ques = len(ques) + 2 if len(ques) + 2 < hyper_parameters["len_max"] else hyper_parameters["len_max"]
    pred_len = pred_arg[0:len_ques]
    # 取id to label and pred
    pre = pt.prereocess_i2l(pred_len)
    print(pre)
    while True:
        print("请输入: ")
        ques = input()
        ques_embed = [ra_ed.sentence2idx(ques)]
        print(ques_embed)
        # 通过两种方式处理: 1.嵌入类型(bert, word2vec, random), 2.条件随机场(CRF:'pad', 'reg')类型
        if hyper_parameters['embedding_type'] in ['bert', 'albert']:
            x_ = np.array(ques_embed)
            x_1 = np.array([x[0] for x in x_])
            x_2 = np.array([x[1] for x in x_])
            x_3 = np.array([x[2] for x in x_])
            # x_1 = np.array([x_[0]])
            # x_2 = np.array([x_[1]])
            # x_3 = np.array([x_[2]])
            if hyper_parameters['model']['crf_mode'] == 'pad':
                x_all = [x_1, x_2, x_3]
            elif hyper_parameters['model']['crf_mode'] == 'reg':
                x_all = [x_1, x_2]
            else:
                x_all = [x_1, x_2]
        else:
            x_ = np.array(ques_embed)
            x_1 = np.array([x[0] for x in x_])
            x_2 = np.array([x[1] for x in x_])
            if hyper_parameters['model']['crf_mode'] == 'pad':
                x_all = [x_1, x_2]
            elif hyper_parameters['model']['crf_mode'] == 'reg':
                x_all = x_1
            else:
                x_all = x_1
        # 预测
        pred = graph.predict(x_all)
        pred_arg = np.argmax(pred[0], axis=-1)
        len_ques = len(ques) + 2 if len(ques) + 2 < hyper_parameters["len_max"] else hyper_parameters["len_max"]
        pred_len = pred_arg[0:len_ques]
        # 取id to label and pred
        pre = pt.prereocess_i2l(pred_len)
        print(pre)


if __name__=="__main__":
    # 可输入 input 预测
    path_hyper_parameters = "D:/workspace/pythonMyCode/Macropodus/macropodus/data/model_ner_bilstm_crf"
    # path_hyper_parameters = "D:/workspace/pythonMyCode/Macropodus/macropodus/data/model/params.json"
    pred_input(path_hyper_parameters)


