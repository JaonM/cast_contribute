# -*- coding:utf-8 -*-
"""
提取编剧平均票房信息
"""
import pymongo
import pandas as pd

# df = pd.read_csv('../input/all_feature.csv', encoding='utf-8')
mainland_movie = pd.read_csv('../input/mainland_movie.csv', encoding='utf-8')
#
# mainland_movie = pd.merge(df, mainland_movie, how='inner', left_on='movie_name', right_on='movie_name')
#
# mainland_movie.to_csv('../input/mainland_movie.csv', encoding='utf-8', index=False)

new = pd.read_csv('../input/new_mainland_movie.csv', encoding='utf-8')

mainland_movie = pd.merge(left=mainland_movie, right=new, how='inner', left_on='movie_name', right_on='movie_name')
mainland_movie.to_csv('../input/mainland_movie.csv', encoding='utf-8', index=False)
