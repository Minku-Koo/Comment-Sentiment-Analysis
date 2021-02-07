# 종교별로 시간 흐름에 따른 감성 쉬치 변화 그래프
# sentiment flow graph by time per religion

from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import json
import numpy as np
import math

tlist = [] # database table name
for i in range(1,6):  tlist.append(["before"+str(i),"after"+str(i)])

dictName = { # table index and name
        "1":"신천지",
        "2":"기독교",
        "3":"천주교",
        "4":"불교",
        "5":"종교" }
        
def append_dict(d1, d2): # dictionary + dictionary
    for d in d1.keys():
        if d in d2.keys(): 
            for i in d1[d]: d2[d][i] = d1[d][i]
        else: d2[d] = d1[d]
    return d2

# 시간 흐름에 따른 감성 지수 그래프
def make_graph_flow(tablename, x, y, x2, y2, fig):
    
    plt.figure(fig, figsize=(16, 5))
    font_name = font_manager.FontProperties(fname='./font/KoPubDotumMedium.ttf', size=20).get_name()
    rc('font', family=font_name)
    
    plt.title(dictName[tablename[-1]],fontsize=22)
    a =0
    nx=[]
    for s in range(len(x)):
        nx.append(s)
        a+=1
    nx = np.array(nx)
    ny = np.array(y)
    m, bb = np.polyfit(nx, ny, 1) # calculate trend line
    plt.plot(nx, m*nx + bb, 'r--', color='#819FF7' , label="Before Trend Line")
    plt.plot(nx, y, 'bo', color='#04B404', label="Before Emotion" )

    nx2 = [ e+2 for e in range(a-1, a-1+len(x2)) ]
    nx2 = np.array(nx2)
    ny2 = np.array(y2)
    m2, bb2 = np.polyfit(nx2, ny2, 1) # calculate trend line
    plt.plot(nx2, m2*nx2 + bb2, 'r--', color='#FAAC58' , label="After Trend Line" )
    plt.plot(nx2, y2, 'bo', color='#FF0080' , label="After Emotion" )
    
    # make month x label
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
    return 0
    
# json 파일 읽어서 자료구조 생성
def makeValue(data):
    result = []
    table_emo_count, table_emo_avg= 0, 0.0 # 감성 개수, 감성 총 합
    for date in data.keys():
        for art in data[date].keys():
            table_emo_count += len(data[date][art][1])
    
    for data_date in data.keys():
        table_emo_avg += sum([ (sum(data[data_date][art][1])/(len(data[data_date][art][1])+1))*(len(data[data_date][art][1])/ table_emo_count) \
                                for art in data[data_date].keys() ]) #날짜당 감성 평균, 가중 평균
    
    for date in data.keys(): #모든 날짜
        day_emo_count = sum([len(data[date][artc][1]) for artc in data[date].keys()]) #날짜당 총 댓글 수 / all comment per day
        if day_emo_count ==0: continue
        
        emotion, isInput = 0, True
        day_emo_count = sum([ len(data[date][art][1]) for art in data[date].keys() ]) #날짜당 총 댓글 수
        for article in data[date].keys(): #모든 기사
            if len(data[date])==1 and len(data[date][article][1]) <1: # 기사가 1개 and 댓글이 0개인 경우 > 입력 안함
                isInput=False
                break
                
            emotionList= data[date][article][1]
            if emotionList == []: continue
            
            emotion_avg  =sum(emotionList) / len(emotionList) #기사당 감성 평균 / emotion average per article
            emotion += (len(emotionList)/day_emo_count) * emotion_avg # 날짜당 기사 가중 평균 / article emotion weighted average per day
        least =10 # 최소 댓글 수 
        # 공식 참고 : https://www.quora.com/How-does-IMDbs-rating-system-work
        emotion_ = (day_emo_count/(day_emo_count+least))*emotion +  (least/(day_emo_count+least))*table_emo_avg 
        
        d_y, d_m, d_d = int(date.split("/")[0]), int(date.split("/")[1]), int(date.split("/")[2])
        
        if isInput: result.append([date, round(emotion_, 6), d_y, d_m, d_d ])
    result_sort_day = sorted(result, key = lambda x: (x[2], x[3], x[-1])) # 정렬 : 1순위 년도, 2순위 월, 3순위 일
    
    x,y = [],[]
    for val in result_sort_day:
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
    
    x, y = data[0][0], data[0][1]
    x2, y2 = data[1][0], data[1][1]
    make_graph_flow(tablename, x, y, x2, y2, fig)

    fig+=2
