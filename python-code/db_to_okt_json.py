# 디비에서 댓글 꺼내서 날짜순으로 작성하고 okt 돌리기
# database comment order by date > konlpy (okt) > make json 
import pymysql
import json
from konlpy.tag import Okt

tlist = [] #테이블 이름 리스트
for i in range(1,6):
    t = "daum"
    tlist.append(t+"after"+str(i))
    tlist.append(t+"before"+str(i))
for i in range(1,6):
    t = "naver"
    tlist.append(t+"after"+str(i))
    tlist.append(t+"before"+str(i))

db = pymysql.connect( #연결할 디비 정보
                user='root', 
                passwd='', 
                host='localhost',
                db='',
                charset="utf8mb4"
                )
ok = Okt()
cursor = db.cursor()
for tablename in tlist:
    sql  = "select year, month, day, url, comment from "+tablename+" ;"
    cursor.execute(sql)
    result = {}
    for info in cursor.fetchall():
        article_date = str(info[0])+"/"+str(info[1])+"/"+str(info[2])
        
        if article_date not in result.keys():result[article_date] = {}
        
        url = info[3]
        result[article_date][url] = [[],[]]
        comment_temp = []
        for comment in info[-1].split("/%**+%/"):
            konlp = ok.pos(comment)
            temp=[]
            for i in konlp:
                if i[1] !='Josa' and i[1] !='Punctuation' and i[1] !='Number' : 
                    temp.append(i[0])
            result[article_date][url][0].append(" ".join(temp))
            
    with open("../comment/json-comment/"+tablename+"-dict.json", "w") as json_file:
        json.dump(result, json_file, indent="\t", ensure_ascii = False)

    
db.close() 
