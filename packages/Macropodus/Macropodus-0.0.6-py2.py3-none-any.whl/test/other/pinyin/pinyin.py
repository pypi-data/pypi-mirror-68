# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/1/7 21:17
# @author  : Mo
# @function:


def count_replace_time():
    """
        统计'replace'方法耗时
    :return: 
    """
    import time
    time_start = time.time()
    text = "macropodus是一种中国产的淡水鱼，广泛分布于两广地区，abcdefghijklmnopqrstuvwxyz"
    for i in range(10000):
        text_i = text + str(i)
        wordsspot = text_i.replace("点", ".")
        wordsmark = wordsspot.replace("分之", "fenzhi")
        wordsin = wordsmark.replace("正切", "zheng切").replace("正弦", "zheng弦").replace("正割", "zheng割").replace("正矢", "zheng矢")
        wordsadd = wordsin.replace("加上", "+").replace("加到", "+").replace("加", "+").replace("＋", "+").replace("正", "+")
        wordsminus = wordsadd.replace("减去", "-").replace("减", "-").replace("－", "-").replace("负", "-")
        wordsmult = wordsminus.replace("阶乘", "jiecheng的").replace("乘上", "*").replace("乘以", "*").replace("乘于", "*").replace(
            "乘", "*").replace("×", "*")
        wordsdivis01 = wordsmult.replace("除去", "/").replace("除以", "/").replace("除于", "/").replace("除", "/").replace("÷",
                                                                                                                    "/")
        wordsdivis02 = wordsdivis01.replace("从", "").replace("再", "").replace("在", "").replace("然后", "").replace("直",
                                                                                                                 "").replace(
            "到", "")
        wordbrackets = wordsdivis02.replace("（", "(").replace("）", ")").replace("=", "").replace("=", "")
        formula = wordbrackets.replace("左括号", "(").replace("右括号", "(").replace("的和", "").replace("的差", "").replace("的商",
                                                                                                                   "").replace(
            "的积", "")
        myformula_1 = formula.replace("*-", "*(-1)*").replace("\\*\\+", "*").replace("\\/\\-", "/(-1)/")
        myformula_2 = myformula_1.replace(" ", "").replace("\\+\\-", "\\-").replace("\\+\\+", "\\+").replace("\\-\\+",
                                                                                                             "\\-").replace(
            "\\-\\-", "\\+")
    print(time.time()-time_start)


def tet_pypinyin():
    from pypinyin import pinyin, lazy_pinyin, Style
    dc0 = pinyin('中心1234567890ABCDEFG')
    dc01 = pinyin('中心', heteronym=True)  # 启用多音字模式
    dc02 = pinyin('中心', style=Style.FIRST_LETTER)  # 设置拼音风格
    pinyin('中心', style=Style.TONE2, heteronym=True)
    pinyin('中心', style=Style.TONE3, heteronym=True)
    pinyin('中心', style=Style.BOPOMOFO)  # 注音风格
    dc03 = lazy_pinyin('中心')  # 不考虑多音字的情况


def read_and_save_pinyin():
    path_pinyin_google = "D:/soft_install/dataset/corpus/segnment/words_dict/google_pinyin_ime_dict-master/谷歌拼音词库"
    from macropodus.preprocess.tools_common import get_dir_files, txt_write, txt_read, save_json, load_json
    from macropodus.conf.path_config import path_dict_macropodus
    macropodus_json = load_json(path_dict_macropodus)[0]
    path_files = get_dir_files(path_pinyin_google)
    pinyin_dict = {}
    for path_file in path_files:
        res = txt_read(path_file)
        for r in res:
            r_sp = r.split("\t")
            if len(r_sp) == 3:
                chinese = r_sp[0]
                pinyin = r_sp[2]
                if chinese in macropodus_json:
                    pinyin_dict[chinese] = pinyin.split(" ")

    res = txt_read(path_pinyin_google+"/snow_pinyin.txt")
    for r in res:
        r_sp = r.split(" ")
        if len(r_sp) == 2:
            chinese = r_sp[0]
            pinyin = r_sp[1]
            pinyin_dict[chinese] = pinyin.split(" ")

    save_json([pinyin_dict], "pinyin.dict")


import json
def load_json(path):
    """
      获取json, json存储为[{}]格式, like [{'大漠帝国':132}]
    :param path: str
    :return: json
    """
    with open(path, 'r', encoding='utf-8') as fj:
        model_json = json.load(fj)
    return model_json

res = load_json("D:/workspace/pythonMyCode/Macropodus/macropodus/data/dict/user.dict")

with open("pinyin.dict", 'w', encoding='utf-8') as fj:
    fj.write(json.dumps(res, ensure_ascii=False, indent=0))
fj.close()