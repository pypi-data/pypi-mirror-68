# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/1/6 14:17
# @author  : Mo
# @function:


import random


def read_txt():
    import json
    ner_chiq_people = "D:/soft_install/dataset/corpus/segnment/chiq_acgn_2018/acgn_set.csv"
    fw = open("name.csv", 'w', encoding='utf-8')
    with open(ner_chiq_people, 'r', encoding='utf-8') as fo:
        while True:
            lines = fo.readline().split(",")
            line = lines[1].replace("，", ",")
            if "{" in line and "}" in line:
                json_line = json.loads(line)
                for tag in ["actor", "director", "role", "athlete"]: #, "singer"]:
                    if tag in json_line.keys():
                        if json_line[tag].split("，")[0] in lines[2]:
                            # print(lines)
                            fw.write(",".join(lines))
                            break


def change_json():
    import json
    ner_chiq_people = "name.csv"
    fw = open("name_tag.csv", 'w', encoding='utf-8')
    with open(ner_chiq_people, 'r', encoding='utf-8') as fo:
        while True:
            lines = fo.readline().split(",")
            line = lines[1].replace("，", ",")
            sent = lines[2]
            res = {}
            if "{" in line and "}" in line:
                json_line = json.loads(line)
                people = []
                for tag in ["actor", "director", "role", "athlete"]: #, "singer"]:
                    if tag in json_line.keys():
                        if json_line[tag].split("，")[0] in lines[2]:
                            people.append(json_line[tag])
                tags = ["O"] * len(sent)
                for peo in people:
                    names = peo.split("，")
                    for name in names:
                        sents = sent.split(name)
                        if len(name)==1:
                            continue
                        else:
                            index_name = sent.index(name)
                            tags[index_name] = "B-PER"
                            for i in range(len(name)-1):
                                tags[index_name+i+1] = "I-PER"

                res["question"]=list(sent)
                res["label"]=tags
                fw.write(json.dumps(res, ensure_ascii=False)+"\n")


# change_json()
fr = open("name_tag.csv", 'r', encoding='utf-8').readlines()
random.shuffle(fr)
fr_8000 = fr[0:8000]
with open("ner_tag_8000.csv", 'w', encoding='utf-8') as fo:
    fo.writelines(fr_8000)
gg = 0

