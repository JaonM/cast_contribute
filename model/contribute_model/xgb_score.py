# -*- coding:utf-8 -*-
"""
用XGBoost预测评分
"""
import xgboost as xgb
import pandas as pd
from xgboost import plot_importance
from sklearn.model_selection import train_test_split
from matplotlib import pyplot

df_data = pd.read_csv('../../input/contribute_feature.csv')

# 填充缺失值
df_data.fillna(0, inplace=True)

y_data = df_data['score'].tolist()

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

filter_features = [
    'director_influence', 'actor1_figure', 'director_overall', 'actor4_influence', 'actor2_voice',
    'actor2_line_ability', 'actor2_acting', 'actor1_influence', 'actor1_acting', 'actor4_acting', 'actor3_figure',
    'actor3_appearance', 'actor1_voice', 'actor3_voice', 'actor4_appearance', 'actor1_line_ability', 'actor2_figure',
    'actor4_figure', 'actor2_appearance', 'actor4_line_ability', 'actor3_acting', 'actor4_voice', 'actor1_appearance',
    'actor3_line_ability', 'actor3_influence'
]

X_data = df_data[filter_features]

X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, random_state=23, test_size=0.1)

print(len(X_train))
print(len(y_train))

dTest = xgb.DMatrix(X_test, label=y_test)

params = {'eta': 0.08, 'objective': 'reg:linear', 'eval_metrics': 'rmse', 'colsample_bytree': 0.8, 'max_depth': 4,
          'subsample': 0.8}

num_round = 3000

dTrain = xgb.DMatrix(X_train, label=y_train)
# dVal = xgb.DMatrix(X_test)
eval_set = [(dTest, 'eval'), (dTrain, 'train')]

bst = xgb.train(params=params, num_boost_round=num_round, dtrain=dTrain, evals=eval_set, early_stopping_rounds=5)

bst.save_model('score_predict.model')
plot_importance(bst)
pyplot.show()
