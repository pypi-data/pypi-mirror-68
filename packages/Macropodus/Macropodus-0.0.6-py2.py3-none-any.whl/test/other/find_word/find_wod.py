# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/1/10 15:36
# @author  : Mo
# @function:


import time
time_start = time.time()
from macropodus.preprocess.tools_common import txt_read
from macropodus import find
print('macropodus初始化耗时: ' + str(time.time()-time_start) + 's')

txts = txt_read("6_symptom_dataset.txt")
text = "".join(txts)
res = find(text)
print(list(res.keys()))


