# -*- coding:utf-8 -*-
"""
主创姓名去重
"""
import codecs

file = codecs.open('../model/word_bank/key.txt', encoding='utf-8')

l1 = []
l2 = []
for line in file.readlines():
    if line == '\n':
        continue
    line = line.strip()
    if line not in l2:
        l1.append(line)
    l2.append(line)

file = codecs.open('../model/word_bank/key.txt', encoding='utf-8',mode='w')
for l in l1:
    file.write(l + '\n')
