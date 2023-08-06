# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/3/6 15:11
# @author  : Mo
# @function:



# BIO标注(tag-pos, 词性标注), json-txt格式
# line[index:] 2014人民日报, 前21个数字不要
import codecs
import json


def character_tagging(input_file):
    """
        BIO标注数据(people_darily_data-1998-2014)
    :param input_file: 
    :return: 
    """
    input_data = codecs.open(input_file, 'r', 'utf-8')
    list_line = []
    label_set = set()
    for line in input_data.readlines():
        # line = "长城站/ns]/ns	、/w	中山站/ns	的/u	重力/n"
        # 移除字符串的头和尾的空格。strip()方法默认是移除空格的
        word_list = line.strip().split()
        line_word = ""
        label_seq = []
        for w in word_list:
            words = w.split("/")
            word = words[0]
            label = words[1].replace("]", "")
            # 即名语素Ng，动语素Vg，形容语素Ag，时语素Tg，副语素Dg等
            if len(word) == 1: # 一个字符的情况
                line_word += word
                label_tag = "B" # "O-" + label.upper()
                label_seq.append(label_tag)
                label_set.add(label)
            elif len(word) >= 2: # 大于等于2个字符的情况
                line_word += word[0]
                for w in word[1: len(word) - 1]:
                    line_word += w
                line_word += word[len(word) - 1]
                label_tag = "B" #+ label.upper()
                label_seq.append(label_tag)
                for i in range(len(word)-1):
                    label_tag = "I" # + label.upper()
                    label_seq.append(label_tag)
                label_set.add(label)
        ques_label_dict = {}
        ques_label_dict["question"] = list(line_word)
        ques_label_dict["label"] = label_seq
        ql_str = json.dumps(ques_label_dict, ensure_ascii=False) + "\n"
        if len(ques_label_dict["question"]) != len(ques_label_dict["label"]): #不等长数据输出
            print(ql_str)
        list_line.append(ql_str)
    input_data.close()
    return list_line, label_set


# segment
list_line, label_set = character_tagging("1998_jiayan.txt") # "199801.txt")
print(label_set)
print(len(label_set))
json_path = "199801.train.json"
with open(json_path, 'w', encoding='utf-8') as fj:
    fj.writelines(list_line)
fj.close()


