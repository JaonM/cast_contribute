# -*- coding:utf-8 -*-
"""
通过规则匹配语料
计算出主创正面负面评论数量(比例)
"""

import jieba
import codecs
import pandas as pd


class weibo_analysis:
    # keyword bank
    keywords_file = "../word_bank/key.txt"
    # stopword bank
    stopword_file = "../word_bank/stopword.txt"
    # 指定自己自定义的词典，以便包含jieba词库里没有的词，提高jieba分词的精度
    self_built_wordbank_file = "../word_bank/ciku.txt"
    # positive word bank
    posword_file = '../word_bank/pos_key.txt'
    # negative word bank
    negword_file = '../word_bank/neg_key.txt'
    # set word distance
    distance = 5

    def __init__(self, keyword_file=keywords_file, stopword_file=stopword_file,
                 selfbuilt_wordbank=self_built_wordbank_file, pos_file=posword_file, neg_file=negword_file):
        self.keywords = self.load_keywords(keyword_file)
        self.stopwords = self.load_stopwords(stopword_file)
        self.pos_words = self.load_poswords(pos_file)
        self.neg_words = self.load_negwords(neg_file)
        self.selfbuilt_words = selfbuilt_wordbank

    def set_word_distance(self, distance):
        self.distance = distance

    def load_keywords(self, filename):
        keywords = [line.strip() for line in codecs.open(filename, encoding='utf-8')]
        return keywords

    def load_stopwords(self, filename):
        stopwords = [line.strip() for line in codecs.open(filename, encoding='utf-8')]
        return stopwords

    def load_poswords(self, filename):
        pos_word = []
        pos_file = codecs.open(filename, encoding='utf-8')
        lines = pos_file.readlines()
        for line in lines:
            # if line.strip() != u''.encode('utf8'):
            pos_word.append(line.strip())
        return pos_word

    def load_negwords(self, filename):
        neg_word = []
        neg_file = codecs.open(filename, encoding='utf-8')
        for line in neg_file.readlines():
            # if line.strip() != u''.encode('utf8'):
            neg_word.append(line.strip())
        return neg_word

    # add keywords
    def add_keyword(self, keyword):
        self.keywords.append(keyword)

    def add_posword(self, word):
        self.pos_words.append(word)

    def add_negword(self, word):
        self.neg_words.append(word)

    """
    # word segmentation
    Input: the original comments
    Output: a keyword list

    """

    def segment_jieba(self, text):

        jieba.load_userdict(self.selfbuilt_words)

        default_mode = jieba.cut(text)
        seg_text = []
        for seg in default_mode:
            if seg not in self.stopwords:
                seg_text.append(seg)

        notags = ' '.join(seg_text)
        # print notags
        return seg_text

    """
    # sentiment analysis
    Input: the word list from comment pretreated by Jieba
    Output: positive keyword list and negative keyword list

    """

    def analyse_sentiment(self, comment):

        distance = self.distance
        neg_word = []
        pos_word = []
        distance_list = []

        comment_word = self.segment_jieba(comment)

        for i in range(1, distance + 1):
            distance_list.append(-i)
            distance_list.append(i)

        for i in range(len(comment_word)):
            word = comment_word[i]
            for j in range(len(self.keywords)):
                if word == self.keywords[j]:
                    idx_f = i
                    flag = False
                    for dist in distance_list:
                        idx = idx_f + dist
                        if 0 < idx < len(comment_word):
                            e_word = comment_word[idx]
                            # e_word = e_word.encode('utf-8')
                            for pos in self.pos_words:
                                if e_word == pos:
                                    pos_word.append(word)
                                    flag = True
                                    break
                            for neg in self.neg_words:
                                if e_word == neg:
                                    neg_word.append(word)
                                    flag = True
                                    break
                            if flag:
                                break
        return pos_word, neg_word


if __name__ == '__main__':
    analysis = weibo_analysis()
    df_weibo = pd.read_csv('../../input/weibo.csv')
    for weibo in df_weibo['content'].values:
        print(analysis.analyse_sentiment(weibo))
