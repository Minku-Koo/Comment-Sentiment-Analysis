
# 종교별로 월별 총 댓글 수 그래프
# all comment count by month per religion
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import json
import math

tlist = [] # database table name
for i in range(1,6):
    tlist.append(["before"+str(i),"after"+str(i)])

dictName = { # table index and name
        "1":"신천지",
        "2":"기독교",
        "3":"천주교",
        "4":"불교",
        "5":"종교" }


def append_dict(d1, d2): #딕셔너리 합치기 dictionary + dictionary
    for d in d1.keys():
        if d in d2.keys(): 
            for i in d1[d]:
                d2[d][i] = d1[d][i]
        else: d2[d] = d1[d]
    return d2

# 댓글 수 카운트 count comment
def calc_comment_count(dict ):
    data = {}
    for day in dict.keys():
        comment_count = 0
        article_count = 0
        for art in dict[day].keys():
            comment_count += len(dict[day][art][1])
            article_count+=1
        if article_count <1 : continue
        
        d_y, d_m, d_d = day.split("/")[0], day.split("/")[1], day.split("/")[2]
        date = d_y+"/"+d_m # year/month
        if d_y+"/"+d_m in data.keys(): 
            data[date][0] += comment_count
            data[date][1] += article_count
        else:  data[date] = [comment_count, article_count, d_y, d_m]
        
    result =[]
    for d in data.keys():
        result.append([d, data[d]])
    # list sort order by date
    result = sorted(result, key = lambda x: (int(x[1][2]), int(x[1][3])))
    
    x,y = [],[]
    for val in result:
        x.append(val[0])
        # average per article
        # y.append(round(val[1][0]/val[1][1],3))
        # all count
        y.append(val[1][0])
        # all article count
        # y.append(val[1][1])
    return x, y 

# make graph
def sum_graph(tablename, x, y, x2, y2, plots, colors):
    a =0
    nx=[]
    for s in range(len(x)):
        nx.append(s)
        a+=1
    nx2 = [ e for e in range(a, a+len(x2)) ]
    month_list, temp, year_temp = [], "", ''
    for month in x:
        month, year = month.split("/")[1],  month.split("/")[0][2:]
        if temp != month : # if month change
            temp = month
            month_list.append(month)
            if  year_temp != year: 
                month_list[-1] = year+"/"+ month_list[-1]
                year_temp = year
        else: month_list.append("") # if same month
    
    for month in x2:
        month, year = month.split("/")[1],  month.split("/")[0][2:]
        if temp != month :  # if month change
            temp = month
            month_list.append(month)
            if  year_temp != year: 
                month_list[-1] = year+"/"+ month_list[-1]
                year_temp = year
        else: month_list.append("")
    
    plt.xticks(range(0,len(month_list)), month_list)
    ax = nx + nx2
    ay = y + y2
    
    plots.plot(ax, ay, 'b', color=colors , label=dictName[tablename[-1]] , marker='o')
    plots.legend()
    return pp
    
# 날짜별 기사 평균 댓글 수  선 그래프
def make_graph(tablename, x, y, x2, y2, fig):
    plt.figure(fig, figsize=(16, 6))
    font_name = font_manager.FontProperties(fname='./font/KoPubDotumMedium.ttf', size=20).get_name()
    rc('font', family=font_name)
    
    a =0
    nx=[]
    for s in range(len(x)):
        nx.append(s)
        a+=1
    nx2 = [ e for e in range(a, a+len(x2)) ]
    
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
    
    ax = nx + nx2
    ay = y + y2
    plt.ylim([0, 70000]) 
    plt.title("월별 댓글 수",fontsize=22)
    plt.plot(ax, ay, 'b', color='#2E9AFE' , label=dictName[tablename[-1]] , marker='o')
    plt.xlabel('Date',fontsize=20)
    plt.ylabel('Comment',fontsize=20)
    plt.xticks(rotation=6,fontsize=16)
    plt.legend()
    plt.yticks(fontsize=16)
    plt.xticks(range(0,len(month_list)), month_list)
    
    return plt

colorlist = ['#F78181','gray','#FACC2E','#AC58FA'] # line color list
fig = 0
for tableList in tlist:
    data =[]
    for tablename in tableList:
        temp = {}
        path = "../comment-emotion-predict/"
        with open(path+"finish-daum"+tablename+'-dict.json', encoding="utf-8") as json_file:
            data1 = json.load(json_file)
        with open(path+"finish-naver"+tablename+'-dict.json', encoding="utf-8") as json_file:
            data2 = json.load(json_file)

        temp = append_dict(data1, data2)
        data.append(calc_comment_count(temp))
    
    x, y = data[0][0], data[0][1]
    x2, y2 = data[1][0], data[1][1]
    if fig==0:
        plt = make_graph(tablename, x, y, x2, y2,fig)
        fig+=1
    else: 
        plt = sum_graph(tablename, x, y, x2, y2, plt, colorlist[fig-1])
        fig+=1
        
        
plt.savefig("../result-graph/comment-count/graph-month-comment-count.png", dpi=400) 
    
    
    
    