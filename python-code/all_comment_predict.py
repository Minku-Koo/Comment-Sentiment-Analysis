
# json 읽어서 학습된 모델에 입력해서 댓글당 감성수치 받아서 딕셔너리 완성 > json file
# read json >input RNN model > predict comment sentiment > make dictionary > write json file

from tensorflow.keras import models
from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
import tensorflow as tf
import json
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] ='2'

tlist = [] # database table name list
for i in range(1,6):
    t = "daum"
    tlist.append(t+"after"+str(i))
    tlist.append(t+"before"+str(i))
for i in range(1,6):
    t = "naver"
    tlist.append(t+"after"+str(i))
    tlist.append(t+"before"+str(i))

# load RNN model
rnn_model = tf.keras.models.load_model("../comment_emotion_rnn-model/rnn_model", custom_objects={"TextVectorization":TextVectorization})

path = "../comment/json-okt-comment/" # comment  json file directory path
for tablename in tlist:
    with open(path+tablename+'-dict.json', encoding="utf-8") as json_file:
        data = json.load(json_file) # load json file
    
    for date in data.keys(): 
        print(date,"/",tablename)
        
        day_article = data[date]
        for article in day_article.keys():
            for comment in day_article[article][0]:
                if comment=="": # if comment is not include text
                    continue
                emotion = float(rnn_model.predict([comment])) # predict comment sentiment
                data[date][article][-1].append(round(emotion, 4)) # dictionary value append sentiment
    result_path = "../comment-emotion-predict/" #  result save json path
    with open(result_path+"finish-"+tablename+"-dict.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent="\t",ensure_ascii = False)
