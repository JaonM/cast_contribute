# -*- coding:utf-8 -*-
"""
微博文本预处理
"""
import re
import pandas as pd


def preprocess(text):
    text = re.sub(r'#.*?#', '', text)
    text = re.sub(r'@.*\?\??', '', text)
    text = re.sub(r'@.*?\s', '', text)
    text = text.replace('?', '')
    return text


if __name__ == '__main__':
    df = pd.read_csv('../../input/芳华.csv')
    df.columns = ['movie_name', 'id', 'weibo', 'audio', 'cg', 'movie_depth', 'advertisement', 'movie_overall',
                  'movie_pace', 'character', 'director_overall', 'acting', 'appearance', 'figure', 'voice',
                  'temperament','line_ability', 'actor_overall', 'script', 'scenarist_overall']
    df.to_csv('../../input/input.csv', index=False, encoding='utf-8')
    result = []
    for index, item in df.iterrows():
        result.append({'id': item['id'], 'content': preprocess(item['weibo'])})
    new_df = pd.DataFrame(result, columns=['id', 'content'])
    new_df.to_csv('../../input/test.csv', encoding='utf-8', index=False)
    print(preprocess('#ads#sadasdas#@@@#'))
