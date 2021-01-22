from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import json
import math
import pandas as pd
import numpy as np


tlist = []
for i in range(1,6):
    tlist.append(["before"+str(i),"after"+str(i)])
print(tlist)
dictName = {
        "1":"신천지",
        "2":"기독교",
        "3":"천주교",
        "4":"불교",
        "5":"종교" }


def append_dict(d1, d2): #딕셔너리 합치기
    for d in d1.keys():
        if d in d2.keys(): 
            for i in d1[d]:
                d2[d][i] = d1[d][i]
        else: d2[d] = d1[d]
    return d2
import math
# 댓글 수 카운트
def calc_comment_avg(dict, tablename ):
# def make_comment_avg(dict, fig):
    data = {}
    emotion=[]
    emotion_count = 0
    emotion_sum = 0.0
    for day in dict.keys():
        for art in dict[day].keys():
            if len(dict[day][art][1]) <1: continue
            emotion.extend([a for a in dict[day][art][1]])
            emotion_count += len(dict[day][art][1])
            emotion_sum += sum(dict[day][art][1])
    
    mean = round(sum(emotion) / len(emotion) ,3) #평균
    
    vsum = 0.0
    for x in emotion:
        vsum = vsum + (x - mean) ** 2
    var = round(vsum / len(emotion),3) # 분산
    
    std = round(math.sqrt(var),3) #표준편차
    title = dictName[tablename[-1]]
    with open("etc.txt","at",encoding="utf-8") as f:
        f.write(title+"  "+tablename+"\n")
        f.write("Before/ avg: "+str(mean)+" 분산: "+str(var)+" 표준편차: "+str(std)+"\n")
    
    return mean
    
# 날짜별 기사 평균 댓글 수  선 그래프
def make_graph(tablename, x, y,  fig):
    plt.figure(fig, figsize=(16, 6))
    font_name = font_manager.FontProperties(fname='KoPubDotumMedium.ttf', size=20).get_name()
    rc('font', family=font_name)
    
    plt.ylim([0, 1]) 
    plt.title(tablename,fontsize=22)
    for i, v in enumerate([r for r in range(5)] ):  #[dictName[str(d)] for d in range(1,6)]
        print(i)
        print(v)
        print("**")
        plt.text(v, y[i], y[i],                 # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
             fontsize = 11, 
             color='black',
             horizontalalignment='center',  # horizontalalignment (left, center, right)
             verticalalignment='bottom')
    for i, v in enumerate([r for r in range(5)] ):  #[dictName[str(d)] for d in range(1,6)]
        plt.text(v-0.3, x[i], x[i],                 # 좌표 (x축 = v, y축 = y[0]..y[1], 표시 = y[0]..y[1])
             fontsize = 11, 
             color='black',
             horizontalalignment='center',  # horizontalalignment (left, center, right)
             verticalalignment='bottom')
    wid = 0.3
    plt.bar(range(len(y)), y, color='#F7BE81' , label="After"  ,width=0.3)
    plt.bar( [i-wid for i in range(len(x))] , x, color='#58ACFA' , label="Before" ,width=0.3 )
    
    # plt.text()
    plt.ylim([0, 0.5]) 
    plt.xlabel('Religion',fontsize=20)
    plt.ylabel('Emotion',fontsize=20)
    plt.xticks(rotation=1,fontsize=16)
    plt.xticks([x-0.15 for x in range(0,5)], [dictName[str(d)] for d in range(1,6)])
    plt.yticks(fontsize=16)
    plt.legend()
    # plt.show()
    plt.savefig("./result/"+tablename+'-graph-avg-emotion.png', dpi=400) 
    return 0

fig = 0
x,y = [],[]
for tableList in tlist:
    data =[]
    for tablename in tableList:
        temp = {}
        path = "./comment/jjson/okt-emo/"
        with open(path+"finish-daum"+tablename+'-dict.json', encoding="utf-8") as json_file:
            data1 = json.load(json_file)
        with open(path+"finish-naver"+tablename+'-dict.json', encoding="utf-8") as json_file:
            data2 = json.load(json_file)
        print(tablename)
        temp = append_dict(data1, data2)
        data.append(calc_comment_avg(temp, tablename))
    
    x.append(data[0])
    y.append(data[1])
make_graph("종교별 평균 감성 지수", x, y ,1)
    
    
    
    