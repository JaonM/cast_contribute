# -*- coding:utf-8 -*-
"""
随机森林预测评分
"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

import pandas as pd


def random_forest_score():
    df_data = pd.read_csv('../../input/contribute_feature.csv')
    df_data.fillna(0, inplace=True)

    features = [
        'director_influence', 'actor4_influence', 'director_overall', 'actor1_line_ability', 'actor1_figure',
        'actor3_acting', 'actor2_influence', 'actor2_voice', 'actor1_voice', 'actor3_influence', 'actor4_appearance',
        'actor1_influence', 'actor4_line_ability', 'actor3_voice', 'actor4_figure', 'actor2_acting', 'actor3_figure',
        'actor2_line_ability', 'actor2_figure', 'actor4_acting', 'actor1_acting', 'actor2_appearance',
        'actor3_line_ability', 'actor1_appearance', 'actor4_voice', 'actor3_appearance', 'actor1_award_count',
        'actor3_award_count', 'actor4_award_count'
    ]

    X_data = df_data[features]
    # print(X_data)
    y_data = df_data['score']
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.1, random_state=12)

    regr = RandomForestRegressor(max_depth=2, random_state=0)
    regr.fit(X_train, y_train)
    print(regr.score(X_test, y_test))
    return regr


random_forest_score()
