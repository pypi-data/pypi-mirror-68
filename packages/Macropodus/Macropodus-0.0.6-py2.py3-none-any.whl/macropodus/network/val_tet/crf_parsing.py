# -*- coding:utf-8 -*-
# author: xiaojie
# datetime: 2020/4/15 14:58
# software: PyCharm


import CRFPP
import json
import os
import codecs


def read(file):

    with open(file, 'r', encoding='utf-8') as f:
        lines = json.load(f)
    res = {}
    for k, v in lines.items():
        v1 = v.replace('\n', '').replace('\r', '')
        text = list(v1)
        text1 = [[t, "0"] for t in text]
        if k not in res:
            res[k] = text1
    return res


def get_model(model_path):
    tagger = CRFPP.Tagger("-m {} -v 3 -n2".format(model_path))
    return tagger


def get_crf(text1, tagger):
    # tagger = CRFPP.Tagger("-m {} -v 3 -n2".format(model))
    # tagger = model
    tagger.clear()
    words0 = [s[0] for s in text1]
    for t in text1:
        t1 = [str(x) for x in t]
        t2 = ' '.join(t1)
        tagger.add(t2)
    ysize = tagger.ysize()
    tagger.parse()
    size = tagger.size()
    xsize = tagger.xsize()
    words1 = []
    tag1 = []
    prob1 = []
    sentence_prob = tagger.prob()
    for i in range(0, (size - 0)):
        www = []
        for j in range(0, (xsize-1)):
           www.append(tagger.x(i, j))

        words1.append(www)
        tag1.append(tagger.y2(i))

        p1 = []
        p2 = []
        for j in range(0, (ysize-0)):
            p1.append(tagger.yname(j))
            p2.append(tagger.prob(i, j))

        prob1.append([tag1[-1], p2[p1.index(tag1[-1])]])
    return words0, words1, tag1, prob1, sentence_prob


def jiexi(words0, tag1, prob1, sentence_prob):
    res = []
    ws = ''
    start_pos = 0
    end_pos = 0
    start_pos_1 = 0
    end_pos_1 = 0
    types = ''
    pr01 = 0.0
    sentence = ''
    for i in range(len(tag1)):
        if tag1[i].startswith('S_'):
            ws += words0[i]
            pr01 += prob1[i][1]
            start_pos_1 = i
            end_pos_1 = i
            start_pos = len(sentence)
            sentence += words0[i]
            end_pos = len(sentence) - 1
            types = tag1[i][2:]
            res.append([ws, start_pos, end_pos, types, pr01/(end_pos_1-start_pos_1+1)])
            ws = ''
            types = ''
            pr01 = 0.0
        if tag1[i].startswith('B_'):
            if len(ws) > 0:
                res.append([ws, start_pos, end_pos, types, pr01/(end_pos_1-start_pos_1+1)])
                ws = ''
                types = ''
                pr01 = 0.0
            if len(ws) == 0:
                ws += words0[i]
                pr01 += prob1[i][1]
                start_pos_1 = i
                end_pos_1 = i
                start_pos = len(sentence)
                sentence += words0[i]
                end_pos = len(sentence) - 1
                types = tag1[i][2:]

        elif tag1[i].startswith('I_'):
            if len(ws) > 0 and types == tag1[i][2:]:
                ws += words0[i]
                pr01 += prob1[i][1]
                sentence += words0[i]
                end_pos = len(sentence) - 1
                end_pos_1 = i
            elif len(ws) > 0 and types != tag1[i][2:]:
                res.append([ws, start_pos, end_pos, types, pr01/(end_pos_1-start_pos_1+1)])
                ws = ''
                types = ''
                pr01 = 0.0
            if len(ws) == 0:
                ws += words0[i]
                pr01 += prob1[i][1]
                start_pos_1 = i
                end_pos_1 = i
                start_pos = len(sentence)
                sentence += words0[i]
                end_pos = len(sentence) - 1
                types = tag1[i][2:]

        elif tag1[i].startswith('E_'):
            if len(ws) > 0 and types == tag1[i][2:]:
                ws += words0[i]
                pr01 += prob1[i][1]
                sentence += words0[i]
                end_pos = len(sentence) - 1
                end_pos_1 = i
                res.append([ws, start_pos, end_pos, types, pr01/(end_pos_1-start_pos_1+1)])
                ws = ''
                types = ''
                pr01 = 0.0
            if len(ws) > 0 and types != tag1[i][2:]:
                res.append([ws, start_pos, end_pos, types, pr01/(end_pos_1-start_pos_1+1)])
                ws = ''
                types = ''
                pr01 = 0.0
                ws += words0[i]
                pr01 += prob1[i][1]
                start_pos_1 = i
                end_pos_1 = i
                start_pos = len(sentence)
                sentence += words0[i]
                end_pos = len(sentence) - 1
                types = tag1[i][2:]
                res.append([ws, start_pos, end_pos, types, pr01/(end_pos_1-start_pos_1+1)])
                ws = ''
                types = ''
                pr01 = 0.0
        elif tag1[i] == 'O':
            sentence += words0[i]
        if i == len(tag1) - 1 and len(ws) > 0:
            res.append([ws, start_pos, end_pos, types, pr01/(end_pos_1-start_pos_1+1)])
            ws = ''
            types = ''
            pr01 = 0.0

    # for i in range(len(res)):
    #     s1 = res[i]
    #     length = len(s1[0]) - 1
    #     stand_pos = s1[1]
    #     if s1[1] == s1[2] and len(s1[0]) > 1:
    #         s1[2] = s1[1] + length
    #     res[i] = s1
    #     for j in range(len(res)):
    #         if i != j:
    #             s2 = res[j]
    #             if s2[1] > stand_pos:
    #                 s2[1] += length
    #                 s2[2] += length
    #                 res[j] = s2

    res1 = []
    for s in res:
        s1 = {}
        s1['word'] = s[0]
        s1['start_pos'] = s[1]
        s1['end_pos'] = s[2]
        s1['entity_type'] = s[3]
        s1['prob'] = s[4]
        res1.append(s1)
    res2 = {}
    textss = ''.join(words0)
    res2['text'] = textss
    res2['label_results'] = res1
    res2['sentence_prob'] = sentence_prob
    return res2


if __name__ == '__main__':
    model_path = './data/model'
    file = "./data/validate_data.json"
    tagger = get_model(model_path)
    test_data = read(file)
    res = {}
    for k, v in test_data.items():
        words0, words1, tag1, prob1, sentence_prob = get_crf(v, tagger)
        re1 = jiexi(words0, tag1, prob1, sentence_prob)
        d = []
        for s in re1["label_results"]:
            d.append({
                "label_type": s["entity_type"],
                "overlap": 0,
                "start_pos": s["start_pos"]+1,
                "end_pos": s["end_pos"]+1
            })
        res[k] = d

        # re1 = {'text': '美国国防部作战试验鉴定局2017财年年度报告指出,F-35战斗机整体上存在诸多问题:一是F-35战斗机系统存在技术缺陷,'
        #                '包括F-35B战斗机轮胎性能低于需求,F-35B和F-35C战斗机的空中受油头锥破损过于频繁,以及F-35A战斗机的机炮射击精'
        #                '度仍有缺陷等;二是F-35项目技术成熟时的大部分可靠性指标都不太可能达到联合攻击战斗机《作战需求文件》的门槛需求'
        #                ';三是机队整体可用率偏低?',
        #        'label_results': [{'word': 'F-35战斗机整', 'start_pos': 25, 'end_pos': 32, 'entity_type': '试验要素', 'prob': 0.7809006955537907},
        #                          {'word': 'F-35战斗机系统存', 'start_pos': 44, 'end_pos': 53, 'entity_type': '试验要素', 'prob': 0.8840784884711885},
        #                          {'word': 'F-35A战斗机的', 'start_pos': 109, 'end_pos': 117, 'entity_type': '试验要素', 'prob': 0.8946230685677085},
        #                          {'word': '机炮射击精度仍有缺陷等', 'start_pos': 118, 'end_pos': 128, 'entity_type': '试验要素', 'prob': 0.3535722265606375}],
        #        'sentence_prob': 0.013246911734375534}

    with codecs.open("./data/result.json", 'w', encoding='utf-8') as fd:
        json.dump(res, fd, indent=4, ensure_ascii=False)

