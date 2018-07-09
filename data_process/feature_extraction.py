# -*- coding:utf-8 -*-
"""
清洗原生电影票房特征数据 movie_raw.csv
"""
import pandas as pd

movie_raw = pd.read_csv('../input/movie_raw.csv')

print(movie_raw.isnull().any())
# 填补缺失值
movie_raw['english'].fillna(0, inplace=True)
movie_raw['chinese'].fillna(0, inplace=True)
movie_raw['other_language'].fillna(1, inplace=True)
movie_raw['schedule_rate'].fillna(movie_raw['schedule_rate'].mean(), inplace=True)
movie_raw['box_office_rate'].fillna(movie_raw['box_office_rate'].mean(), inplace=True)

print(movie_raw.isnull().any())

df_feature = movie_raw.drop(['director', 'actors'], axis=1)
# df_feature = movie_raw.drop(movie_raw['box_office'] == '-', axis=0)
df_feature.drop(df_feature[df_feature['box_office'] == '-'].index, inplace=True, axis=0)
# print(df_feature[df_feature['box_office'] == '-'].index)
df_feature.to_csv('../input/movie_feature.csv', index=False, encoding='utf-8')
