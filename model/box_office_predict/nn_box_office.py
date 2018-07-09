# -*- coding:utf-8 -*-
"""
神经网络预测票房
"""

from keras.layers import Dense, BatchNormalization, Dropout, Input
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.callbacks import EarlyStopping
import numpy as np

df_data = pd.read_csv('../../input/mainland_movie.csv', encoding='utf-8')
# df_data = pd.read_csv('../../input/contribute/feature.csv', encoding='utf-8')

BATCH_SIZE = df_data.size
NUM_EPOCH = 10000000

features = [
    'director_influence', 'director_award_count', 'director_num_follow', 'director_num_fan', 'director_overall',
    'director_average_reports_count', 'director_average_comments_count', 'director_average_attitudes_count',
    'actor1_average_comments_count', 'actor1_average_reports_count', 'actor1_average_attitudes_count',
    'actor1_figure', 'actor1_overall', 'actor1_voice', 'actor1_influence', 'actor1_line_ability', 'actor1_acting',
    'actor1_appearance', 'actor1_award_count', 'actor1_num_follow', 'actor1_num_fans',
    'actor2_influence', 'actor2_voice', 'actor2_line_ability', 'actor2_acting', 'actor2_appearance',
    'actor2_average_comments_count', 'actor2_average_reports_count', 'actor2_average_attitudes_count', 'actor2_figure',
    'actor2_overall', 'actor2_num_follow', 'actor2_num_fans', 'actor3_influence', 'actor3_award_count',
    'actor3_overall', 'actor3_voice', 'actor3_acting', 'actor3_appearance', 'actor3_average_comments_count',
    'actor3_average_reports_count', 'actor3_figure', 'actor3_num_follow', 'actor3_average_attitudes_count',
    'actor3_num_fans', 'actor3_line_ability', 'actor4_influence', 'actor4_acting',
    'actor4_appearance', 'actor4_award_count', 'actor4_average_comments_count', 'actor4_average_reports_count',
    'actor4_overall', 'actor4_num_follow', 'actor4_voice', 'actor4_line_ability', 'actor4_num_fans', 'actor4_figure',
    'actor4_average_attitudes_count'
]

X_data = df_data[features]
X_data.fillna(0, inplace=True)

y_data = np.array(df_data['box_office'].tolist())/10000

X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.1, random_state=2)

X_train = X_train.as_matrix()
X_test = X_test.as_matrix()

regr = Sequential()
regr.add(BatchNormalization(input_shape=(len(features),)))
regr.add(Dense(units=30, activation='relu', input_dim=len(features)))
# regr.add(BatchNormalization())
regr.add((Dense(units=10, activation='tanh',)))
# regr.add((Dropout(rate=0.1)))
# regr.add(BatchNormalization())
# regr.add(Dense(units=10,activation='relu'))
regr.add(Dense(units=1, activation='linear'))

early_stopping = EarlyStopping(patience=10)
regr.compile(optimizer='adam', loss='mse', metrics=['mse'])
regr.fit(X_train, y_train, batch_size=BATCH_SIZE, validation_data=(X_test, y_test), epochs=NUM_EPOCH, shuffle=True,
         callbacks=[early_stopping])

regr.save('nn_box_office.model.h5')
