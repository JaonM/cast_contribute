# -*- coding:utf-8 -*-
"""
利用lstm预测aspcet
利用cnn预测aspect对应sentiment
"""
import os
import pandas as pd
from model.preprocess.weibo_preprocess import preprocess
from pyltp import Segmentor
import codecs
import numpy as np
from gensim.models import KeyedVectors
from sklearn.model_selection import StratifiedKFold
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense, BatchNormalization, Dropout, Activation, Convolution2D, MaxPooling2D, Flatten
from keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

LTP_DATA_DIR = '../ltp'
INPUT_FILE = '../input/input.csv'
STOP_WORD_FILE = '../input/stopword.txt'
EMBEDDING_FILE = '../input/word2vec/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'


class LSTMAspect(object):
    """
    从文本中预测主创aspect

    Arguments:
        batch_size  每个batch的大小
        num_epoch   迭代计算趟数
        threshold   优化参数，输出概率大于阈值方可预测一类
    """
    EMBEDDING_DIMENSION = 64
    SEGMENT_PATH = os.path.join(LTP_DATA_DIR, 'cws.model')

    def __init__(self, batch_size=400, num_epoch=100, threshold=0.105):
        self.raw_data = None
        self.train_data = []
        self.segmentor = Segmentor()
        self.segmentor.load(self.SEGMENT_PATH)
        self.stops = []
        # 加载停用词
        stop_word_file = codecs.open(STOP_WORD_FILE, encoding='utf-8')
        for line in stop_word_file.readlines():
            if line != '':
                self.stops.append(line.strip())
        self.max_sequence_length = 0
        self.y_data = []
        self.buid_features()
        self.get_max_sequence_length()
        self.num_word = 0
        self.train_embedding = None  # 训练文本词向量
        self.batch_size = batch_size
        self.num_epoch = num_epoch

        self.out_dim = 17  # 输出维度(类别)
        self.threshold = threshold  # 输出概率大于阈值方可预测一类
        self.num_fold = 10

    def buid_features(self):
        """
        构建文本输入特征、输出特征
        :return:
        """
        df_data = pd.read_csv(INPUT_FILE, encoding='utf-8').fillna(0)
        self.raw_data = df_data['weibo'].values
        for index, item in df_data.iterrows():
            # 微博文本预处理
            raw_text = preprocess(item['weibo'])
            # 分词
            words = list(self.segmentor.segment(raw_text))
            # 去停用词
            _words = []
            for word in words:
                if word in self.stops:
                    continue
                _words.append(word)
            self.train_data.append(_words)
            y = []
            for value in item[
                ['audio', 'cg', 'movie_depth', 'advertisement', 'movie_total', 'movie_pace',
                 'character', 'director_total', 'acting', 'appearance', 'figure', 'voice',
                 'temperament', 'line_ability', 'actor', 'script', 'scenarist_total']].values:
                if value != 0:
                    y.append(1)
                else:
                    y.append(0)
            self.y_data.append(y)
        self.train_data = np.array(self.train_data)

    def get_max_sequence_length(self):
        """
        确定输入文本的最大长度
        :return:
        """
        max_length = 0
        num_word = 0
        for sentence in self.train_data:
            length = len(sentence)
            num_word += length
            if length > max_length:
                max_length = length
        self.max_sequence_length = max_length
        self.num_word = num_word

    def get_train_embedding(self):
        word_vectors = KeyedVectors.load_word2vec_format(EMBEDDING_FILE, binary=True)
        self.train_embedding = []
        for i in range(len(self.train_data)):
            # sentence = pad_sequences(self.train_data[i], maxlen=self.max_sequence_length, padding='post')
            sentence = self.train_data[i]
            print(sentence)
            sentence_embedding = []
            for word in sentence:
                try:
                    sentence_embedding.extend(word_vectors[word])
                except:
                    sentence_embedding.extend(np.zeros(self.EMBEDDING_DIMENSION))
            if len(self.train_data[i]) < self.max_sequence_length:
                sentence_embedding.extend(
                    np.zeros((self.max_sequence_length - len(self.train_data[i])) * self.EMBEDDING_DIMENSION))
            self.train_embedding.append(sentence_embedding)

    def train(self, num_fold=10):
        self.num_fold = num_fold
        skf = StratifiedKFold(n_splits=num_fold, shuffle=True)
        current_fold = 0
        for idx_train, idx_val in skf.split(self.y_data, self.y_data):
            X_train = self.train_embedding[idx_train]
            y_train = self.y_data[idx_train]

            X_val = self.train_embedding[idx_val]
            y_val = self.train_embedding[idx_val]

            clf = Sequential()
            clf.add(LSTM(self.EMBEDDING_DIMENSION, recurrent_dropout=0.2, dropout=0.2,
                         input_shape=(self.max_sequence_length, self.EMBEDDING_DIMENSION)))
            clf.add(BatchNormalization())
            clf.add(Dense(self.EMBEDDING_DIMENSION, activation='tanh'))
            clf.add(Dropout(rate=0.2))
            clf.add(BatchNormalization())
            clf.add(Dense(self.out_dim, activation='sigmoid'))

            clf.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

            early_stopping = EarlyStopping(monitor='val_loss', patience=5)

            # 保存最优模型
            checkpointer = ModelCheckpoint(filepath='./aspect_model_' + str(current_fold) + '.h5', save_best_only=True)

            hist = clf.fit(X_train, y_train, validation_data=(X_val, y_val), batch_size=self.batch_size,
                           epochs=self.num_epoch, verbose=1, callbacks=[early_stopping, checkpointer], shuffle=True)

            print(current_fold, "validation loss:", min(hist.history["val_loss"]))
            current_fold += 1

    def predict_prob(self, X_test):
        """
        K折平均预测新文本的aspect概率分布
        :param X_test:
        :return:
        """
        res = np.zeros((X_test.shape[0], self.out_dim))
        for i in range(self.num_fold):
            clf = Sequential()
            clf.load_weights('./apect_model_' + str(i) + '.h5')
            _res = clf.predict(X_test)
            res = res + _res
        return res / self.num_fold

    def adjust_threshold(self):
        X_train, X_test, y_train, y_test = train_test_split(self.train_embedding, self.y_data, test_size=0.3,
                                                            random_state=33)
        f1 = 0
        for threshold in np.arange(0, 1, 0.01):
            preds = self.predict_prob(X_test)
            preds[preds >= threshold] = 1
            preds[preds < threshold] = 0

            score = f1_score(y_test, preds, average='binary')
            if score > f1:
                f1 = score
                self.threshold = threshold
                print('update threshold: ' + str(threshold) + ', f1 score is ' + score)

    def predict_label(self, X_test):
        """
        K折平均预测新文本的标签
        :param X_test:
        :return:
        """
        res = np.zeros((X_test.shape[0], self.out_dim))
        for i in range(self.num_fold):
            clf = Sequential()
            clf.load_weights('./aspect_model_' + str(i) + '.h5')
            _res = clf.predict(X_test)
            res = res + _res
        res = res / self.num_fold
        res[res >= self.threshold] = 1
        res[res < self.threshold] = 0
        return res

    def train_cnn(self):
        X_train, X_test, y_train, y_test = train_test_split(self.train_embedding, self.y_data, test_size=0.2,
                                                            random_state=2)
        model = Sequential()
        model.add(Convolution2D(
            batch_input_shape=(64, 1, 28, 28),
            filters=32,
            kernel_size=5,
            strides=1,
            padding='same',  # Padding method
            data_format='channels_first',
        ))
        model.add(Activation('relu'))
        model.add(Convolution2D(64, 5, strides=1, padding='same', data_format='channels_first'))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(2, 2, 'same', data_format='channels_first'))
        model.add(Flatten())
        model.add(Dense(1024))
        model.add(Activation('relu'))
        model.add(Dense(10))
        model.add(Activation('softmax'))
        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(X_train, y_train, epoch=1, batch_size=32, )


if __name__ == '__main__':
    lstm = LSTMAspect()
    # print(lstm.train_data)
    # print(lstm.max_sequence_length)
    lstm.get_train_embedding()
    print(len(lstm.train_embedding))
    print(len(lstm.y_data))
