
import pymysql
import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] ='2'
import numpy as np
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras import metrics
import tensorflow as tf
from keras.preprocessing.sequence import pad_sequences
import csv
import numpy as np
import urllib
import time
import pandas as pd

from tensorflow.keras import Input, Model
from tensorflow.keras.layers import (
    Dense,
    Embedding,
    GRU
)
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import tensorflow_transform as tft
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras.layers import LSTM

print(tf.__version__)


#     csv 파일 읽어서 x y 리스트 저장
x, y = [],[]
path = "../train-data/"
fname = "comment-labeling.csv"
fnamee = "ratings.csv"
f = open(path +fname, 'r', encoding='utf-8')
rdr = csv.reader(f)
p,n = 0,0
for line in rdr:
    flt = float(line[-1])
    if flt ==0.0:  n+=1
    else:  p+=1
    x.append(line[0])
    y.append(flt)
    
f.close()

nx, ny = [],[]
f = open(path +fnamee, 'r', encoding='utf-8') #
rdr = csv.reader(f)
p,n = 0,0
for line in rdr:
    flt = float(line[-1])
    
    if flt ==0.0:   n+=1
    else:  p+=1
     
    ny.append(flt)
    nx.append(line[0])
    
f.close()

pp = 0.2
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=pp)
a,b,c,d =  train_test_split(nx, ny, test_size=pp)

x_train += a
x_test += b
y_train += c
y_test += d


from tensorflow.keras.layers import Dense, Embedding, Flatten

def build_model(train_data):
    train_data = tf.data.Dataset.from_tensor_slices(train_data)
    model = Sequential()
    model.add(Input(shape=(1,), dtype="string"))

    max_tokens = 15000
    max_len = 50
    vectorize_layer = TextVectorization(
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

from keras.optimizers import SGD
rnn_model =build_model(x_train)
rnn_model.compile(
        optimizer=  "adam",
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

history = rnn_model.fit(x_train,y_train,
                   epochs = 5,  batch_size = 128  , validation_data = (x_test, y_test) )
rnn_model.summary()


import time

thepath = "../mmm/"
name ="rnn-model"
tf.saved_model.save(rnn_model, thepath+name)


import matplotlib.pyplot as plt
def make_graph(history_dict):
    acc = history_dict['accuracy']
    val_acc = history_dict['val_accuracy']
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']

    epochs = range(1, len(acc) + 1)

    plt.plot(epochs, loss, 'bo', label = "Training Loss")
    plt.plot(epochs, val_loss, 'b', label='Validation Loss')
    plt.title("Training and validation loss")
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig("../mmm/train.png", dpi=400) 
    plt.show()


    plt.plot(epochs, acc, 'bo', label = "Training val_acc")
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title("Training and validation acc")
    plt.xlabel('Epochs')
    plt.ylabel('acc')
    plt.legend()
    plt.savefig("../mmm/val.png", dpi=400) 
    plt.show()
    
history_dict = history.history
make_graph(history_dict)








