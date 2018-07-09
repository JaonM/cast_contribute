# -*- coding:utf-8 -*-
# -*- coding:utf-8 -*-
"""
用XGBoost预测电影票房
"""
import xgboost as xgb
import pandas as pd
from xgboost import plot_importance
from sklearn.model_selection import train_test_split
from matplotlib import pyplot

df_data = pd.read_csv('../../input/all_feature.csv')

# 填充缺失值
df_data.fillna(0, inplace=True)

y_data = df_data['box_office'] / 10000

features = ['director_influence', 'director_award_count', 'director_num_follow', 'director_num_fan', 'director_overall',
            'director_average_reports_count', 'director_average_comments_count', 'director_average_attitudes_count',
            'actor1_average_comments_count', 'actor1_average_reports_count', 'actor1_average_attitudes_count',
            'actor1_figure', 'actor1_overall', 'actor1_voice', 'actor1_influence', 'actor1_line_ability',
            'actor1_acting',
            'actor1_appearance', 'actor1_award_count', 'actor1_num_follow', 'actor1_num_fans',
            'actor2_influence', 'actor2_voice', 'actor2_line_ability', 'actor2_acting', 'actor2_appearance',
            'actor2_average_comments_count', 'actor2_average_reports_count', 'actor2_average_attitudes_count',
            'actor2_figure',
            'actor2_overall', 'actor2_num_follow', 'actor2_num_fans', 'actor3_influence', 'actor3_award_count',
            'actor3_overall', 'actor3_voice', 'actor3_acting', 'actor3_appearance', 'actor3_average_comments_count',
            'actor3_average_reports_count', 'actor3_figure', 'actor3_num_follow', 'actor3_average_attitudes_count',
            'actor3_num_fans', 'actor3_line_ability', 'actor4_influence', 'actor4_acting',
            'actor4_appearance', 'actor4_award_count', 'actor4_average_comments_count', 'actor4_average_reports_count',
            'actor4_overall', 'actor4_num_follow', 'actor4_voice', 'actor4_line_ability', 'actor4_num_fans',
            'actor4_figure',
            'actor4_average_attitudes_count', 'is_']

filter_features = [
    'is_hot_schedule', 'schedule_rate', 'is_series', 'score', '剧情',
    '动作', '爱情', '喜剧', '奇幻', '冒险', '犯罪', '悬疑', '惊悚', '中国电影股份有限公司', '华夏电影发行有限责任公司', '中国电影集团公司', '万达影视传媒有限公司',
    '华谊兄弟传媒股份有限公司', '其他'
]

X_data = df_data[features]

X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, random_state=23, test_size=0.05)

print(len(X_train))
print(len(y_train))

dTest = xgb.DMatrix(X_test, label=y_test)

params = {'eta': 0.1, 'objective': 'reg:linear', 'eval_metrics': 'rmse', 'colsample_bytree': 1, 'max_depth': 4,
          'subsample': 1}

num_round = 10000

dTrain = xgb.DMatrix(X_train, label=y_train)
# dVal = xgb.DMatrix(X_test)
eval_set = [(dTest, 'eval'), (dTrain, 'train')]


# bst = xgb.train(params=params, num_boost_round=num_round, dtrain=dTrain, evals=eval_set, early_stopping_rounds=50)

# bst.save_model('box_office_predict.model')
# plot_importance(bst)
# pyplot.show()

# y_preds = bst.predict(dTest)

# print(y_preds)
