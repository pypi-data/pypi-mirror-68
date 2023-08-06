# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/1/9 10:03
# @author  : Mo
# @function:


import json


def txt_read(path_file, encode_type='utf-8'):
    """
        读取txt文件，默认utf8格式, 不能有空行
    :param file_path: str, 文件路径
    :param encode_type: str, 编码格式
    :return: list
    """
    list_line = []
    try:
        file = open(path_file, 'r', encoding=encode_type)
        while True:
            line = file.readline().strip()
            if not line:
                break
            list_line.append(line)
        file.close()
    except Exception as e:
        print(str(e))
    finally:
        return list_line


def txt_write(list_line, file_path, type='w', encode_type='utf-8'):
    """
      txt写入list文件
    :param listLine:list, list文件，写入要带"\n" 
    :param filePath:str, 写入文件的路径
    :param type: str, 写入类型, w, a等
    :param encode_type: 
    :return: 
    """
    try:
        file = open(file_path, type, encoding=encode_type)
        file.writelines(list_line)
        file.close()
    except Exception as e:
        print(str(e))


def seq_tag_cut_len_max(infile, outfile, len_max, split_syboml="，"):
    """
         
    :param infile: str, 输入文件地址
    :param outfile: str, 输出文件地址
    :param len_max: int, 最大长度
    :param split_syboml: str, 切分符号,如逗号等
    :return: None
    """
    dev_json = txt_read(infile)

    res = []
    for dj in dev_json:
        dj_js = json.loads(dj)
        question = "".join(dj_js["question"])
        label_seq = dj_js["label"]
        ques_label_dict = {}
        if len(question) > len_max: # 大于126长度的len_max
            seq_index = 0
            questions = question.split(split_syboml)
            for ques in questions:
                if ques:
                    len_ques = len(ques)
                    if len_ques > len_max:
                        print(ques)
                    if ques != questions[-1]: # 不是最后一句话
                        question_ = ques + split_syboml
                    else: #最后一句话不加符号
                        question_ = ques
                    label_seq_ = label_seq[seq_index:seq_index + len_ques + 1]
                    ques_label_dict["question"] = list(question_)
                    ques_label_dict["label"] = label_seq_
                    ql_str = json.dumps(ques_label_dict, ensure_ascii=False) + "\n"
                    if len(ques_label_dict["question"]) != len(ques_label_dict["label"]):
                        print(ql_str)
                    res.append(ql_str)
                    if ques != questions[-1]:
                        seq_index += len_ques + 1
                    else:
                        seq_index += len_ques
        else:
            ql_str = dj + "\n"
            res.append(ql_str)
    print(len(res))
    res = list(set(res))
    print(len(res))
    txt_write(res, outfile)


symbols = ["", "。", "；", "，", ";", ",", "、", "[","”", "）", "／", "的", "一", "团", ".126"]
base = "dev.json"
for i in range(len(symbols)-1):
    infile = base + symbols[i]
    outfile = base + symbols[i+1]
    len_max = 126
    split_syboml=symbols[i+1]
    print("#########################################\n"
          "#########################################"+split_syboml)
    seq_tag_cut_len_max(infile, outfile, len_max, split_syboml)


