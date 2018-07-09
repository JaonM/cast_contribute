# -*- coding:utf-8 -*-
"""
回归树预测评分
"""

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

import pandas as pd

df_data = pd.read_csv('../../input/contribute_feature.csv')
df_data.fillna(-999, inplace=True)

features = [
    'director_influence', 'director_award_count', 'director_weibo_pos',
    'director_num_follow', 'director_num_tweets', 'director_num_fan',
    'actor1_influence', 'actor1_award_count', 'actor1_weibo_pos', 'actor1_num_follow',
    'actor1_num_tweets', 'actor1_num_fans', 'actor2_influence',
    'actor2_award_count', 'actor2_weibo_pos', 'actor2_num_follow', 'actor2_num_tweets',
    'actor2_num_fans', 'actor3_influence', 'actor3_award_count',
    'actor3_weibo_pos', 'actor3_num_follow', 'actor3_num_tweets', 'actor3_num_fans',
    'actor4_influence', 'actor4_award_count', 'actor4_weibo_pos',
    'actor4_num_follow', 'actor4_num_tweets', 'actor4_num_fans']

X_data = df_data[features]
# print(X_data)
y_data = df_data['score']
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.1, random_state=12)

regr = DecisionTreeRegressor(random_state=0)
regr.fit(X_train, y_train)
print(regr.score(X_test, y_test))
