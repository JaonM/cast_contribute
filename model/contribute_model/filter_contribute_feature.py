# -*- coding:utf-8 -*-

import pandas as pd

df = pd.read_csv('../../input/contribute_feature.csv')

df = df[df['schedule_rate'].notnull()]
df = df[df['want_count'].notnull()]
df = df[df['score'].notnull()]

df.to_csv('../../input/contribute_feature.csv', index=False, encoding='utf-8')
print(df['schedule_rate'].value_counts())
