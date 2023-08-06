# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/1/17 16:15
# @author  : Mo
# @function:


import re


MAX_LEN_SIZE = 126


def _parse_text(text: list):
    bises = []
    for line in text:
        # remove POS tag
        line, _ = re.subn('\\n', '', line)
        if line == '' or line == '\n':
            continue
        words = re.split('\s+', line)

        if len(words) > MAX_LEN_SIZE:
            texts = re.split('[。？！，.?!,]/w', line)
            if len(min(texts, key=len)) > MAX_LEN_SIZE:
                continue
            bises.extend(_parse_text(texts))
        else:
            bises.append(_tag(words))
    return bises


def _tag(words):
    """
    给指定的一行文本打上BIS标签
    :param line: 文本行
    :return:
    """
    bis = []
    # words = list(map(list, words))
    pre_word = None
    for word in words:
        pos_t = None
        tokens = word.split('/')
        if len(tokens) == 2:
            word, pos = tokens
        elif len(tokens) == 3:
            word, pos_t, pos = tokens
        else:
            continue

        word = list(word)
        pos = pos.upper()

        if len(word) == 0:
            continue
        if word[0] == '[':
            pre_word = word
            continue
        if pre_word is not None:
            pre_word += word
            if pos_t is None:
                continue
            elif pos_t[-1] != ']':
                continue
            else:
                word = pre_word[1:]
                pre_word = None
        # 即名语素Ng，动语素Vg，形容语素Ag，时语素Tg，副语素Dg等, yg,rg,bg,mg
        pos = pos.replace("NG", "g").replace("VG", "g").replace("AG", "g").replace("TG", "g").replace("DG", "g").replace("YG", "g").replace("RG", "g").replace("BG", "g").replace("MG", "g")
        if len(word) == 1:
            bis.append((word[0], 'O-' + pos.lower()))
        else:
            for i, char in enumerate(word):
                if i == 0:
                    bis.append((char, 'B-' + pos.lower()))
                else:
                    bis.append((char, 'I-' + pos.lower()))
    # bis.append(('\n', 'O'))
    return bis


if __name__ == '__main__':
    from macropodus.preprocess.tools_common import txt_write, txt_read
    ques = txt_read("199801.txt")
    ress = _parse_text(ques)
    import json
    qts = []
    for res in ress:
        qt_single = {}
        quess = []
        tagers = []
        for r in res:
            ques = r[0]
            tags = r[1]
            quess.append(ques)
            tagers.append(tags)
        qt_single["question"] = quess
        qt_single["label"] = tagers
        qt_single_dumps = json.dumps(qt_single, ensure_ascii=False) + "\n"
        qts.append(qt_single_dumps)
    txt_write(qts, "train.1998.json")

    all_tags = []
    single_tags = []
    for res in ress:
        for r in res:
            tagger = r[1]
            tags = tagger.split("-")
            tagg = tags[1]
            all_tags.append(tagger)
            single_tags.append(tagg)
    all_tags = list(set(all_tags))
    single_tags = list(set(single_tags))
    print(len(all_tags))
    print(all_tags)
    print(len(single_tags))
    print(single_tags)
    gg = 0



# yg,rg,bg,mg




