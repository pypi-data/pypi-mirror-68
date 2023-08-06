# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/1/14 20:11
# @author  : Mo
# @function:



def data_process():
    zh_punctuation = ['，', '。', '？', '；', '！', '……']
    with open('BosonNLP_NER_6C_process.txt', 'w', encoding='utf-8') as fw:
        with open('D:/soft_install/dataset/corpus/ner/BosonNLP_NER_6C/BosonNLP_NER_6C.txt', 'r', encoding='utf-8') as fr:
            for line in fr.readlines():
                line = ''.join(line.split()).replace('\\n', '')  # 去除文本中的空字符

                i = 0
                while i < len(line):
                    word = line[i]

                    if word in zh_punctuation:
                        fw.write(word + '/O')
                        fw.write('\n')
                        i += 1
                        continue

                    if word == '{':
                        i += 2
                        temp = ''
                        while line[i] != '}':
                            temp += line[i]
                            i += 1
                        i += 2

                        type_ne = temp.split(':')
                        etype = type_ne[0]
                        entity = type_ne[1]
                        fw.write(entity[0] + '/B_' + etype.replace("", "").replace("", "") + ' ')
                        for item in entity[1:]:
                            fw.write(item + '/I_' + etype.replace("", "").replace("", "") + ' ')
                    else:
                        fw.write(word + '/O ')
                        i += 1

def to_json():
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
            # 移除字符串的头和尾的空格。strip()方法默认是移除空格的
            word_list = line.strip().split()
            line_word = ""
            label_seq = []
            for w in word_list:
                words = w.split("/")
                if len(words)==2:
                    word = words[0]
                    label = words[1]
                else:
                    word = "/"
                    label = words[2]
                    print(words)
                try:
                    line_word += word
                    label_tag = label.replace("B_time", "O").replace("I_time", "O").replace("B_location", "B-LOC").replace("I_location", "I-LOC")\
                        .replace("B_person_name", "B-PER").replace("I_person_name", "I-PER")\
                        .replace("B_org_name", "B-ORG").replace("I_org_name", "I-ORG")\
                        .replace("B_company_name", "B-ORG").replace("I_company_name", "I-ORG")\
                        .replace("B_product_name", "O").replace("I_product_name", "O")
                    label_seq.append(label_tag)
                    for i in range(len(word) - 1):
                        label_tag = label.upper()
                        label_seq.append(label_tag)
                    label_set.add(label)
                except:
                    gg = 0
            ques_label_dict = {}
            ques_label_dict["question"] = list(line_word)
            ques_label_dict["label"] = label_seq
            ql_str = json.dumps(ques_label_dict, ensure_ascii=False) + "\n"
            if len(ques_label_dict["question"]) != len(ques_label_dict["label"]):  # 不等长数据输出
                print(ql_str)
            gg = 0
            list_line.append(ql_str)
        input_data.close()
        return list_line, label_set

    # segment
    list_line, label_set = character_tagging("BosonNLP_NER_6C.txt")
    print(label_set)
    print(len(label_set))
    json_path = "BosonNLP_NER_6C.train.json"
    with open(json_path, 'w', encoding='utf-8') as fj:
        fj.writelines(list_line)
    fj.close()



if __name__ == '__main__':
    # data_process()
    to_json()

