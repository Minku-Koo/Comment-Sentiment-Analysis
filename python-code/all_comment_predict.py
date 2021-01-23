
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] ='2'

import numpy as np
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras import losses
from tensorflow.keras import metrics
import csv
import numpy as np
import os
import urllib
import time
import pandas as pd
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import (
    Dense,
    Embedding,
    GRU
)
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical

# json 읽어서 모델에 입력해서 댓글당 감성수치 받아서 딕셔너리 완성
import tensorflow as tf
import json
tlist = []
for i in range(1,6):
    t = "daum"
    tlist.append(t+"after"+str(i))
    tlist.append(t+"before"+str(i))
for i in range(1,6):
    t = "naver"
    tlist.append(t+"after"+str(i))
    tlist.append(t+"before"+str(i))
print(tlist)

rnn_model = tf.keras.models.load_model("../comment_emotion_rnn-model/rnn_model", custom_objects={"TextVectorization":TextVectorization})
n=0
path = "../comment/json-okt-comment/"
for tablename in tlist:
    with open(path+tablename+'-dict.json', encoding="utf-8") as json_file:
        data = json.load(json_file)
    
    for date in data.keys():
        print(date,"/",tablename)
        
        day_article = data[date]
        for article in day_article.keys():
            for comment in day_article[article][0]:
                n+=1
                if comment=="": 
                    continue
                emotion = float(rnn_model.predict([comment]))
                data[date][article][-1].append(round(emotion, 4))
    result_path = "../comment-emotion-predict/"
    with open(result_path+"finish-"+tablename+"-dict.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent="\t",ensure_ascii = False)
