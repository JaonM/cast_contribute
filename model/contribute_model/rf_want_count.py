# -*- coding:utf-8 -*-
"""
随机森林预测想看数量
"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

import pandas as pd


def random_forest_want_count():
    df_data = pd.read_csv('../../input/contribute_feature.csv')
    df_data.fillna(0, inplace=True)

    features = ['director_influence', 'director_award_count', 'director_num_follow',
                'director_num_fan', 'director_overall', 'director_average_reports_count',
                'director_average_comments_count', 'director_average_attitudes_count',
                'actor1_average_comments_count', 'actor1_average_reports_count',
                'actor1_average_attitudes_count', 'actor1_figure', 'actor1_overall', 'actor1_voice',
                'actor1_influence', 'actor1_line_ability', 'actor1_acting', 'actor1_appearance',
                'actor1_award_count', 'actor1_num_follow', 'actor1_num_fans', 'actor2_influence',
                'actor2_voice', 'actor2_acting', 'actor2_appearance',
                'actor2_average_comments_count', 'actor2_average_reports_count',
                'actor2_average_attitudes_count', 'actor2_figure', 'actor2_overall',
                'actor2_line_ability', 'actor2_num_follow',
                'actor2_num_fans', 'actor3_influence', 'actor3_award_count',
                'actor3_overall', 'actor3_voice', 'actor3_acting', 'actor3_appearance',
                'actor3_average_comments_count', 'actor3_average_reports_count', 'actor3_figure',
                'actor3_num_follow', 'actor3_average_attitudes_count',
                'actor3_num_fans', 'actor3_line_ability',
                'actor4_influence', 'actor4_acting', 'actor4_appearance',
                'actor4_award_count',
                'actor4_average_comments_count', 'actor4_average_reports_count', 'actor4_overall',
                'actor4_num_follow', 'actor4_voice', 'actor4_line_ability',
                'actor4_num_fans', 'actor4_figure',
                'actor4_average_attitudes_count']

    X_data = df_data[features]
    # print(X_data)
    y_data = df_data['want_count']
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.1, random_state=12)

    regr = RandomForestRegressor(max_depth=2, random_state=0)
    regr.fit(X_train, y_train)
    print(regr.score(X_test, y_test))
    return regr


random_forest_want_count()
