# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/1/10 11:11
# @author  : Mo
# @function:


## TODO 编写word_segment_viterbi函数来实现对输入字符串的分词
import math

def word_segment_viterbi(input_str, word_prob):
    """
    1. 基于输入字符串，词典，以及给定的unigram概率来创建DAG(有向图）。
    2. 编写维特比算法来寻找最优的PATH
    3. 返回分词结果

    input_str: 输入字符串   输入格式：“今天天气好”
    best_segment: 最好的分词结果  输出格式：["今天"，"天气"，"好"]
    """

    # TODO: 第一步：根据词典，输入的句子，以及给定的unigram概率来创建带权重的有向图（Directed Graph）
    #      有向图的每一条边是一个单词的概率（只要存在于词典里的都可以作为一个合法的单词），这些概率在 word_prob，如果不在word_prob里的单词但在
    #      词典里存在的，统一用概率值1e-100。
    # 图是为了直观起见，边表示字或词及其概率，节点存储状态，图有没有其实无所谓，从本质上讲其实就是个状态转移算法
    # 每个节点的状态包含-log(P)和当前最优切分
    memory = [[0, []] for _ in range(len(input_str)+1)]

    # TODO： 第二步： 利用维特比算法来找出最好的PATH， 这个PATH是P(sentence)最大或者 -log P(sentence)最小的PATH。
    # TODO: 第三步： 根据最好的PATH, 返回最好的切分
    for i in range(1, len(input_str)+1):
        for j in range(i):
            # 这里偷个懒，默认没有形成词的单字可以在词典中找到（如果不成立事实上会返回完整句子，因为-log(1e-100)必然小于该值加某个非负数
            word = input_str[j:i]
            prob = word_prob[word] if word in word_prob else 1e-100

            score = memory[j][0] - math.log(prob)
            # 状态更新
            if memory[i][0] == 0:
                memory[i][0] = score
                memory[i][1] = memory[j][1] + [word]
            else:
                if score < memory[i][0]:
                    memory[i][0] = score
                    memory[i][1] = memory[j][1] + [word]

    return memory[-1][1]


if __name__ == '__main__':
    from macropodus.conf.path_config import path_dict_macropodus
    from macropodus.preprocess.tools_common import load_json
    word_prob = load_json(path_dict_macropodus)
    text = "Macropodus是一个以Albert+BiLSTM+CRF网络架构为基础，用大规模中文语料训练的自然语言处理工具包。将提供中文分词、命名实体识别、关键词抽取、文本摘要、新词发现、文本相似度、计算器、数字转换、拼音转换、繁简转换等常见NLP功能。"
    res = word_segment_viterbi(text, word_prob)
    print(res)
    while True:
        print("请输入:")
        ques = input()
        print(word_segment_viterbi(ques, word_prob))