# 종교별로 총 평균 감성 수치 그래프
# all sentiment average per religion

from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import json
import math


tlist = []
for i in range(1,6):
    tlist.append(["before"+str(i),"after"+str(i)])

dictName = { # index and religion name
        "1":"신천지",
        "2":"기독교",
        "3":"천주교",
        "4":"불교",
        "5":"종교" }

# dictionary + dictionary
def append_dict(d1, d2): #딕셔너리 합치기
    for d in d1.keys():
        if d in d2.keys(): 
            for i in d1[d]:
                d2[d][i] = d1[d][i]
        else: d2[d] = d1[d]
    return d2

# 댓글 수 카운트 count comment
def calc_comment_avg(dict, tablename ):
    emotion=[] 
    emotion_count = 0 # emotion count
    emotion_sum = 0.0 # emotion sum
    for day in dict.keys():
        for art in dict[day].keys():
            if len(dict[day][art][1]) <1: continue
            emotion.extend([a for a in dict[day][art][1]])
            emotion_count += len(dict[day][art][1])
            emotion_sum += sum(dict[day][art][1])
    
    mean = round(sum(emotion) / len(emotion) ,3) #평균 average
    
    vsum = 0.0
    for x in emotion:
        vsum = vsum + (x - mean) ** 2
    var = round(vsum / len(emotion),3) # 분산
    
    std = round(math.sqrt(var),3) #표준편차
    title = dictName[tablename[-1]] # title name
    filepath = "../result-graph/" # result graph save path
    with open(filepath +"statistics-history.txt","at",encoding="utf-8") as f:
        f.write(title+"  "+tablename+"\n") # data save to file
        f.write("avg: "+str(mean)+" 분산: "+str(var)+" 표준편차: "+str(std)+"\n")
    
    return mean
    
# 종교별 총 평균 그래프
# all average per religion graph
def make_graph(tablename, x, y):
    plt.figure(0, figsize=(16, 6))
    font_name = font_manager.FontProperties(fname='./font/KoPubDotumMedium.ttf', size=20).get_name()
    rc('font', family=font_name)
    
    wid = 0.3
    plt.ylim([0, 1])
    plt.title(tablename,fontsize=22)
    for i, v in enumerate([r for r in range(5)] ): # before value
        plt.text(v, y[i], y[i],    
             fontsize = 11, 
             color='black',
             horizontalalignment='center', 
             verticalalignment='bottom')
    for i, v in enumerate([r for r in range(5)] ): #after value
        plt.text(v-0.3, x[i], x[i],  
             fontsize = 11, 
             color='black',
             horizontalalignment='center', 
             verticalalignment='bottom')
    
    plt.bar(range(len(y)), y, color='#F7BE81' , label="After"  ,width=0.3)
    plt.bar( [i-wid for i in range(len(x))] , x, color='#58ACFA' , label="Before" ,width=wid )
    plt.ylim([0, 0.5]) 
    plt.xlabel('Religion',fontsize=20)
    plt.ylabel('Emotion',fontsize=20)
    plt.xticks(rotation=1,fontsize=16)
    plt.xticks([x-round(wid/2,2) for x in range(0,5)], [dictName[str(d)] for d in range(1,6)])
    plt.yticks(fontsize=16)
    plt.legend()
    plt.savefig(filepath +"/emotion-average-stick/"+tablename+'-graph-avg-emotion.png', dpi=400) 
    return 0

x,y = [],[]
for tableList in tlist:
    data =[]
    for tablename in tableList:
        temp = {}
        path = "../comment-emotion-predict/"
        with open(path+"finish-daum"+tablename+'-dict.json', encoding="utf-8") as json_file:
            data1 = json.load(json_file)
        with open(path+"finish-naver"+tablename+'-dict.json', encoding="utf-8") as json_file:
            data2 = json.load(json_file)
        print(tablename)
        temp = append_dict(data1, data2)
        data.append(calc_comment_avg(temp, tablename))
    
    x.append(data[0])
    y.append(data[1])
make_graph("종교별 평균 감성 지수", x, y )
    
    
    
    