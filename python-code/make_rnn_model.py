
# 학습 데이터를 통해 RNN 딥러닝 모델 생성
# build RNN model from train data

import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] ='2'

import numpy as np
from tensorflow.keras import models, layers, optimizers, losses, metrics
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences
import csv
import pandas as pd

from tensorflow.keras.layers import Dense, Embedding, Flatten
from tensorflow.keras import Input, Model

from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization

#   csv 파일 읽어서 x y 리스트 저장
# read csv and make list
x, y = [],[]
path = "../train-data/"
file1 = "comment-labeling.csv" # train data 1
file2 = "naver-ratings.csv" # train data 2

# make train data .csv 
f = open(path +file1, 'r', encoding='utf-8')
read = csv.reader(f)
for line in read:
    emotion = float(line[-1])
    x.append(line[0])
    y.append(emotion)
    
f.close()

x2, y2 = [],[]
f = open(path +file2, 'r', encoding='utf-8') #
read = csv.reader(f)
for line in read:
    emotion = float(line[-1])
    y2.append(emotion)
    x2.append(line[0])
    
f.close()

test_percent = 0.2 # test data percent
# make train and test data usin train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_percent)
a,b,c,d =  train_test_split(x2, y2, test_size=test_percent)

# train and test data append
x_train += a
x_test += b
y_train += c
y_test += d


def build_model(train_data): # to make rnn model
    train_data = tf.data.Dataset.from_tensor_slices(train_data)
    model = Sequential()
    model.add(Input(shape=(1,), dtype="string")) # input one string data (comment)
    max_tokens = 15000 # dictionary size
    max_len = 50 # comment to vectorize size
    vectorize_layer = TextVectorization( # make textvectorization 
      max_tokens=max_tokens,
      output_mode="int",
      output_sequence_length=max_len,
    )
    
    vectorize_layer.adapt(train_data.batch(64))
    model.add(vectorize_layer)
    model.add(layers.Embedding(max_tokens + 1,output_dim= 200))
    model.add(Flatten())
    model.add(Dense(8, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))
    return model

rnn_model =build_model(x_train)
rnn_model.compile( # rnn model compile
        optimizer=  "adam",
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

# model training
history = rnn_model.fit(x_train, y_train,
                   epochs = 5,  batch_size = 128  , validation_data = (x_test, y_test) )
rnn_model.summary()

model_save_path = "../comment_emotion_rnn-model/" # model save path
model_name ="rnn-model" #model save file name
tf.saved_model.save(rnn_model, model_save_path+model_name)

