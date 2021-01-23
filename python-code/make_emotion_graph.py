# json 읽어서 감성 종합하고 날짜별 감성 수치 도출 + 그래프-- 최종마무리
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import json
tlist = []
for i in range(1,6):
    tlist.append("after"+str(i))
    tlist.append("before"+str(i))

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
        
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def append_dict(d1, d2):
    for d in d1.keys():
        if d in d2.keys(): 
            for i in d1[d]:
                d2[d][i] = d1[d][i]
        else: d2[d] = d1[d]
    return d2

import math
def make_graph_over(tablename, x, y, x2, y2, fig):
    average = [ round(float(np.mean(y)), 3) , round(float(np.mean(y2)), 3)  ]
    vsum=0
    for v in y: vsum = vsum + (v - average[0]) ** 2
    bunsan1 = round(vsum / len(y), 3)
    std1 = round(math.sqrt(bunsan1), 3)
    vsum=0
    for v in y2: vsum = vsum + (v - average[1]) ** 2
    bunsan2 = round(vsum / len(y2), 3)
    std2 = round(math.sqrt(bunsan2), 3)
    
    plt.figure(fig, figsize=(16, 5))
    font_name = font_manager.FontProperties(fname='./font/KoPubDotumMedium.ttf', size=20).get_name()
    rc('font', family=font_name)
    
    plt.title(dictName[tablename[-1]],fontsize=22)
    ee =0
    nx=[]
    for s in range(len(x)):
        nx.append(s)
        ee+=1
    nx = np.array(nx)
    ny = np.array(y)
    m, bb = np.polyfit(nx, ny, 1)
    plt.plot(nx, m*nx + bb, 'r--', color='#819FF7' , label="Before Trend Line")
    plt.plot(nx, y, 'bo', color='#04B404', label="Before Emotion" )

    nx2 = [ e+2 for e in range(ee-1, ee-1+len(x2)) ]
    nx2 = np.array(nx2)
    ny2 = np.array(y2)
    m2, bb2 = np.polyfit(nx2, ny2, 1)
    plt.plot(nx2, m2*nx2 + bb2, 'r--', color='#FAAC58' , label="After Trend Line" )
    plt.plot(nx2, y2, 'bo', color='#FF0080' , label="After Emotion" )
    month_list, temp, year_temp = [], "", ''
    for month in x:
        month, year = month.split("/")[1],  month.split("/")[0][2:]
        if temp != month : 
            temp = month
            month_list.append(month)
            if  year_temp != year: 
                month_list[-1] = year+"/"+ month_list[-1]
                year_temp = year
        else: month_list.append("")
    for month in x2:
        month, year = month.split("/")[1],  month.split("/")[0][2:]
        if temp != month : 
            temp = month
            month_list.append(month)
            if  year_temp != year: 
                month_list[-1] = year+"/"+ month_list[-1]
                year_temp = year
        else: month_list.append("")


    plt.ylim([0.0, 1.02]) 
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Emotion',fontsize=18)
    plt.xticks(rotation=6,fontsize=13)
    plt.yticks(fontsize=16)
    plt.xticks(range(0,len(month_list)), month_list)
    plt.legend()
    plt.savefig("../result-graph/emotion-flow/"+tablename+'-graph-emotion-flow.png', dpi=400) 
    

def makeValue(data):
    result = []
    ccount = 0
    table_emo_count, table_emo_sum= 0, 0.0 
    for date in data.keys():
        for art in data[date].keys():
            ccount += len(data[date][art][1])
            
    for data_date in data.keys():
        table_emo_sum += sum([ (sum(data[data_date][art][1])/(len(data[data_date][art][1])+1))*(len(data[data_date][art][1])/ccount)   for art in data[data_date].keys() ]) #날짜당 감성 평균
        table_emo_count += sum([ len(data[data_date][art][1]) for art in data[data_date].keys() ]) # 감성 개수
    table_avg = table_emo_sum 
    for date in data.keys(): #모든 날짜
        
        sumArticle = sum([len(data[date][artc][1]) for artc in data[date].keys()]) #날짜당 총 댓글 수
        if sumArticle ==0: continue
        emotion = 0
        isInput = True
        day_emo_count = sum([ len(data[date][art][1]) for art in data[date].keys() ]) #날짜당 총 댓글 수
        for article in data[date].keys(): #모든 기사
            if len(data[date])==1 and len(data[date][article][1]) <1: 
                isInput=False
                print("out")
                break
            emotionList= data[date][article][1]
            
            if emotionList == []: continue
            emotion_avg  =sum(emotionList) / len(emotionList) #감성 평균 / 기사당
            emotion += (len(emotionList)/sumArticle) * emotion_avg # 기사 가중 평균 / day
        least =10
        emotion_ = (sumArticle/(sumArticle+least))*emotion +  (least/(sumArticle+least))*table_avg #베이지안 평균
        
        d_y, d_m, d_d = int(date.split("/")[0]), int(date.split("/")[1]), int(date.split("/")[2])
        
        if isInput: result.append([date, round(emotion_, 6), d_y, d_m, d_d ])
    sresult = sorted(result, key = lambda x: (x[2], x[3], x[-1]))
    
    x,y = [],[]
    for val in sresult:
        x.append(val[0])
        y.append(val[1])
    
    return x, y


fig = 0
for tableList in tlist:
    data = []
    for tablename in tableList:
        temp = {}
        path = "../comment-emotion-predict/"
        with open(path+"finish-daum"+tablename+'-dict.json', encoding="utf-8") as json_file:
            data1 = json.load(json_file)
        with open(path+"finish-naver"+tablename+'-dict.json', encoding="utf-8") as json_file:
            data2 = json.load(json_file)

        temp = append_dict(data1, data2)
        
        data.append(makeValue(temp))
    print("tablename",tablename)
    x, y = data[0][0], data[0][1]
    x2, y2 = data[1][0], data[1][1]
    make_graph_over(tablename, x, y, x2, y2, fig)

    fig+=2
