# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/1/2 20:51
# @author  : Mo
# @function:


# 适配linux
import pathlib
import sys
import os
project_path = str(pathlib.Path(os.path.abspath(__file__)).parent.parent.parent)
sys.path.append(project_path)
# network
from macropodus.conf.path_config import path_model, path_fineture, path_model_dir, path_hyper_parameters, path_model_l2i_i2l
from macropodus.preprocess.tools_common import load_json, save_json, txt_read, txt_write
from macropodus.network.preprocess.preprocess_generator import PreprocessGenerator
from macropodus.conf.path_config import path_embedding_albert
from macropodus.preprocess.tools_ml import extract_chinese
from tensorflow.python.keras.models import model_from_json
from macropodus.preprocess.tools_common import load_json
from keras_bert import Tokenizer
import numpy as np
import macropodus
import pickle
import codecs
import json
import os
# 模型图
from macropodus.network.graph.bilstm_crf import BilstmCRFGraph as Graph
# 模型评估
from sklearn.metrics import classification_report
# 计算时间
import time


path_model_dir = "D:/workspace/pythonMyCode/Macropodus/macropodus/data/model_ner_bilstm_crf/params.json"

def pred_input(path_hyper_parameter=path_model_dir):
    # 输入预测
    # 加载超参数
    hyper_parameters = load_json(path_hyper_parameter)
    pt = PreprocessGenerator(path_model_l2i_i2l)
    # 模式初始化和加载
    graph = Graph(hyper_parameters)
    graph.load_model()
    ra_ed = graph.word_embedding
    ques = '我要打王者荣耀'
    # str to token
    ques_embed = ra_ed.sentence2idx(ques)
    if hyper_parameters['embedding_type'] == 'bert':
        x_val_1 = np.array([ques_embed[0]])
        x_val_2 = np.array([ques_embed[1]])
        x_val = [x_val_1, x_val_2]
    else:
        x_val = ques_embed[0]
    # 预测
    pred = graph.predict([x_val])
    # 取id to label and pred
    pre = pt.prereocess_idx2label(pred[0])
    print(pre)
    while True:
        print("请输入: ")
        ques = input()
        ques_embed = ra_ed.sentence2idx(ques)
        print(ques_embed)
        if hyper_parameters['embedding_type'] == 'bert':
            x_val_1 = np.array([ques_embed[0]])
            x_val_2 = np.array([ques_embed[1]])
            x_val = [x_val_1, x_val_2]
        else:
            x_val = ques_embed
        pred = graph.predict(x_val)
        pre = pt.prereocess_idx2label(pred[0])
        print(pre)


if __name__=="__main__":
    # 可输入 input 预测
    pred_input()