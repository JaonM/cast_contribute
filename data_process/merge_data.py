# -*- coding:utf-8 -*-
"""
抽取电影票房特征
"""

import pandas as pd
import math
import functools

left = pd.read_csv('./movie.csv')

right = pd.read_csv('./movie2.csv')

right = right.get(
    ['movie_id', 'want_count', 'score', 'english', 'chinese', 'other_language', '剧情', '动作', '爱情', '喜剧', '奇幻',
     '冒险', '犯罪', '悬疑', '惊悚'])

left = pd.merge(left=left, right=right, left_on='movie_id', right_on='movie_id')

production_company = dict()

for index, value in left['production_company'].iteritems():
    try:
        for comp in value.split(','):
            production_company[comp] = production_company.get(comp, 0) + 1
    except:
        continue

items = sorted(production_company.items(), key=lambda d: d[1], reverse=True)

companys = []
for i in range(5):
    companys.append(items[i][0])
companys.append('其他')
print(companys)


def extract_company_1(row, companys):
    try:
        if companys[0] in row['production_company'].split(','):
            return 1
        else:
            return 0
    except:
        return 0


def extract_company_2(row, companys):
    try:
        if companys[1] in row['production_company'].split(','):
            return 1
        else:
            return 0
    except:
        return 0


def extract_company_3(row, companys):
    try:
        if companys[2] in row['production_company'].split(','):
            return 1
        else:
            return 0
    except:
        return 0


def extract_company_4(row, companys):
    try:
        if companys[3] in row['production_company'].split(','):
            return 1
        else:
            return 0
    except:
        return 0


def extract_company_5(row, companys):
    try:
        if companys[4] in row['production_company'].split(','):
            return 1
        else:
            return 0
    except:
        return 0


def extract_company_6(row, companys):
    try:
        for comp in row['production_company'].split(','):
            if comp in companys:
                return 0
        return 1
    except:
        return 1


# 抽取电影制片公司

df_company = pd.DataFrame()
f = functools.partial(extract_company_1, companys=companys)
df_company['中国电影股份有限公司'] = left.apply(f, raw=True, axis=1)

f = functools.partial(extract_company_2, companys=companys)
df_company['华夏电影发行有限责任公司'] = left.apply(f, raw=True, axis=1)

f = functools.partial(extract_company_3, companys=companys)
df_company['中国电影集团公司'] = left.apply(f, raw=True, axis=1)

f = functools.partial(extract_company_4, companys=companys)
df_company['万达影视传媒有限公司'] = left.apply(f, raw=True, axis=1)

f = functools.partial(extract_company_5, companys=companys)
df_company['华谊兄弟传媒股份有限公司'] = left.apply(f, raw=True, axis=1)

f = functools.partial(extract_company_6, companys=companys)
df_company['其他'] = left.apply(f, raw=True, axis=1)

print(df_company)
# df_company['movie_id']=left['movie_id']
left = left.drop('production_company', axis=1)

left = pd.concat((left, df_company), axis=1)

left = left.drop(
    ['ypr_want_count', 'ypr_score', 'douban_want_count', 'douban_score', 'maoyan_want_count', 'maoyan_score',
     'taopiaopiao_want_count', 'taopiaopiao_score', 'nuomi_want_count', 'nuomi_score', 'shiguang_want_count',
     'shiguang_score','movie_type','languages'], axis=1)

left.to_csv('../input/movie_raw.csv', index=False, encoding='utf-8')
