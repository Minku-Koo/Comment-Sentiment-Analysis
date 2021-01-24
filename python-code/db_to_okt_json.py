# 디비에서 댓글 꺼내서 날짜순으로 작성하고 KoNLPy okt 돌리기
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
                
ok = Okt() # KoNLPy Okt
cursor = db.cursor()
for tablename in tlist:
    sql  = "select year, month, day, url, comment from "+tablename+" ;"
    cursor.execute(sql)
    result = {} # json에 넣을 dictionary
    for info in cursor.fetchall():
        article_date = str(info[0])+"/"+str(info[1])+"/"+str(info[2]) #날짜 합치기
        
        if article_date not in result.keys(): result[article_date] = {} # 날짜 초기화
        
        url = info[3]
        result[article_date][url] = [[],[]] # 날짜[기사 링크] 초기화
        
        for comment in info[-1].split("/%**+%/"): # database 모든 댓글 구분하여 리스트화
            konlp = ok.pos(comment) #okt 적용
            comment_temp = [] #댓글 리스트 초기화
            for i in konlp: 
                # 조사, 구두점, 숫자 제거
                if i[1] !='Josa' and i[1] !='Punctuation' and i[1] !='Number' : 
                    comment_temp.append(i[0])
            result[article_date][url][0].append(" ".join(comment_temp)) # 딕셔너리[날짜][기사] 에 댓글 리스트 추가
    # 테이블 이름 별로 json 작성
    with open("../comment/json-comment/"+tablename+"-dict.json", "w") as json_file:
        json.dump(result, json_file, indent="\t", ensure_ascii = False)

db.close() 
