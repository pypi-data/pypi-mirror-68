# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/1/14 20:46
# @author  : Mo
# @function:


def read_conll_format_file(file_path: str,
                           text_index: int = 0,
                           label_index: int = 1):
    """
    Read conll format data_file
    Args:
        file_path: path of target file
        text_index: index of text data, default 0
        label_index: index of label data, default 1

    Returns:

    """
    x_data, y_data = [], []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        x, y = [], []
        for line in lines:
            rows = line.split('\t')
            if len(rows) == 1:
                x_data.append(x)
                y_data.append(y)
                x = []
                y = []
            else:
                x.append(rows[text_index])
                y.append(rows[label_index])
    return x_data, y_data

import json
file_path1 = "D:/soft_install/dataset/corpus/ner/NER_corpus_chinese-master/MSRA/BIO_train.txt"
file_path2 = "D:/soft_install/dataset/corpus/ner/NER_corpus_chinese-master/MSRA/BIO_test.txt"
x1, y1 = read_conll_format_file(file_path1)
x2, y2 = read_conll_format_file(file_path2)
x=x1+x2
y=y1+y2
res = []
for i in range(len(y)):
    ques_label_dict = {}
    ques_label_dict["question"] = x[i]
    ques_label_dict["label"] = y[i]
    ql_str = json.dumps(ques_label_dict, ensure_ascii=False) + "\n"
    res.append(ql_str)

from macropodus.preprocess.tools_common import txt_write
txt_write(res, "ner_msra.txt")


