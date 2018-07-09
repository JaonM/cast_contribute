# -*- coding:utf-8 -*-

"""
训练线性回归模型预测票房
"""

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

import pandas as pd

df_data = pd.read_csv('../../input/movie_feature.csv')

df_train, df_test = train_test_split(df_data, test_size=0.1, random_state=23)

y_train = df_train['box_office']
X_train = df_train.drop(
    ['movie_id', 'box_office', 'movie_name', 'chinese', 'english','other_language','box_office_rate'], axis=1)

y_test = df_test['box_office']
X_test = df_test.drop(
    ['movie_id', 'box_office', 'movie_name', 'english', 'chinese','box_office_rate',
     'other_language'], axis=1)

# Normalization
min_max_scaler = preprocessing.MinMaxScaler()
# print(X_train['director_award_count'])
X_train['director_award_count'] = min_max_scaler.fit_transform(X_train['director_award_count'].reshape(-1, 1))
X_train['actor_award_count'] = min_max_scaler.fit_transform(X_train['actor_award_count'].reshape(-1, 1))
X_train['schedule_rate'] = min_max_scaler.fit_transform(X_train['schedule_rate'].reshape(-1, 1))
X_train['box_office_rate'] = min_max_scaler.fit_transform(X_train['box_office_rate'].reshape(-1, 1))
# print(X_train['director_award_count'].value_counts())

X_test['director_award_count'] = min_max_scaler.fit_transform(X_test['director_award_count'].reshape(-1, 1))
X_test['actor_award_count'] = min_max_scaler.fit_transform(X_test['actor_award_count'].reshape(-1, 1))
X_test['schedule_rate'] = min_max_scaler.fit_transform(X_test['schedule_rate'].reshape(-1, 1))
X_test['box_office_rate'] = min_max_scaler.fit_transform(X_test['box_office_rate'].reshape(-1, 1))

model = LinearRegression()
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
