
"""
- News crawler
- Target Web Page : Naver and Daum News
- Kinds of Scrap Data : Title, Content, Date, all of comment and reply

Author : Minkuk Koo
E-Mail : corleone@kakao.com
"""

'''
DATABASE TABLE INFO

CREATE TABLE news(
    no int(6) NOT NULL AUTO_INCREMENT,
    keyword varchar(20) NOT NULL,
    title varchar(100) NOT NULL,
    content mediumtext NOT NULL,
    year int(4) NOT NULL,
    month int(2) NOT NULL,
    day int(2) NOT NULL,
    url varchar(200) NOT NULL,
    comment longtext,
    PRIMARY KEY (no)
);

'''
import pymysql
import requests
from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
import selenium
import requests
from selenium.webdriver.support.ui import WebDriverWait
import time

class newsCrawler:
    def __init__(self, tablename, start, end, keyword, includeKeyword=""):
        # ex> newsCrawler("table","20201231","20210209""키워드", "포함 키워드(default=없음)")
        self.tablename = tablename
        self.keyword = keyword
        self.includeKeyword = includeKeyword
        self.startDate = start
        self.endDate = end
        
        #크롬 드라이버 옵션
        self.options = webdriver.ChromeOptions() 
        self.options.add_argument('headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('lang=ko_KR')

        self.linkSet = []  #링크 저장할 리스트

        self.db = pymysql.connect( #연결할 디비 정보
                user='root', 
                passwd='', 
                host='localhost', 
                db='',
                charset="utf8mb4"
                )
        # selenium 크롤링을 위한 크롬 드라이버 생성
        self.driver = webdriver.Chrome('./driver/chromedriver.exe', chrome_options=self.options)
        self.driver.implicitly_wait(5)

    def naverNews(self): #네이버 뉴스
        url = "https://search.naver.com/search.naver?where=news&query="
        url = url + self.keyword

        self.driver.get(url) # selenium으로 url 접속
        self.driver.implicitly_wait(10)
        time.sleep(1)

        # 검색 옵션 클릭
        self.driver.find_element_by_id("search_option_button").click()
        #기간 설정 클릭
        self.driver.find_elements_by_class_name("_tab_option_")[1].click()
        self.driver.implicitly_wait(5)
        # 기간 설정하기
        startDate = self.driver.find_element_by_id("news_input_period_begin")
        endDate = self.driver.find_element_by_id("news_input_period_end")

        startDate.send_keys(self.startDate)
        endDate.send_keys(self.endDate)
        
        #기간 적용
        dateBox = self.driver.find_element_by_class_name("_search_option_period_")
        dateBox.find_element_by_class_name("_btn_submit_").click()
        self.driver.implicitly_wait(10)
        
        #다음 버튼 클릭
        nextButton = self.driver.find_element_by_class_name("btn_next")
        while True: #기사 링크 수집, 다음 버튼 없을때 까지
            for article in self.driver.find_elements_by_class_name("info_group"):
                try:
                    #네이버 뉴스로 볼 수 있는 곳 링크
                    link = article.find_elements_by_tag_name("a")[1].get_attribute("href")
                    print(link)
                    self.linkSet.append(link)
                except(IndexError): #네이버 뉴스가 없는 경우
                    print("Index Error!!")
            #다음 페이지 넘어가기 위해 다음 버튼 클릭
            nextButton = self.driver.find_element_by_class_name("btn_next")
            if nextButton.get_attribute("href")==None:
                # 다음 버튼 없는 경우(=기사 마지막) 종료
                break
            else: nextButton.click()
        
        self.cursor = self.db.cursor()  # DB 연결
        self.naverArticle(self.linkSet) #기사별 데이터 수집
        self.db.commit() #디비 저장
        self.db.close() #디비 연결 종료
        return 0
    
    # 링크 리스트를 통해 기사 정보 추출
    def naverArticle(self, linkSet): #파라미터:페이지 링크 리스트
        link_count = len(linkSet)
        count = 1
        for link in linkSet: #모든 링크 데이터 수집
            self.driver.get(link) # selenium으로 기사 url 접속
            self.driver.implicitly_wait(3)
            time.sleep(0.01)
            count+=1 #진행 상황 알기 위한 변수
            
            try:
                #기사 본문 스크랩
                content = self.driver.find_element_by_id("articleBodyContents").text.replace("'","")
                #본문에 포함 키워드 없는 경우
                if self.includeKeyword not in content: continue
                
                #기사, 날짜, 댓글 링크 추출
                title = self.driver.find_element_by_id("articleTitle").text.replace("'","")
                article_info = self.driver.find_element_by_class_name("article_info")
                date = article_info.find_element_by_class_name("t11").text
                dateList = date.split(".")
                year, month, day = int(dateList[0]), int(dateList[1]), int(dateList[2])
                commentLink = self.driver.find_element_by_id("articleTitleCommentCount").get_attribute("href")
                
                allCommentBox = self.driver.find_element_by_class_name("u_cbox_comment_count_wrap")
                allComment = int(allCommentBox.find_element_by_class_name("u_cbox_info_txt").text.replace(",",""))

            #올바른 element 찾지 못한 경우
            except selenium.common.exceptions.NoSuchElementException:
                print("select error !!")
                continue

            self.driver.get(commentLink) # 댓글 화면으로 이동
            self.driver.implicitly_wait(3)
            time.sleep(0.1)
            try:
                for i in range( min( int(allComment/20), 100)): # 기사당 댓글 더보기 클릭, 최대 100회
                    self.driver.find_element_by_class_name("u_cbox_btn_more").click()
            except: #더이상 더보기 클릭이 불가능한 경우
                print("댓글 더보기 없음")
            
            try: #답글 보기 전부 클릭
                for i in self.driver.find_elements_by_class_name("u_cbox_reply_cnt"): 
                    if i.text != "0":  #답글이 있는 경우
                        i.click()
                        print("답글 클릭")
            except: #더이상 더보기 클릭이 불가능한 경우
                print("대댓글 없음")

            commentSet = ""  #댓글 리스트
            for comment in self.driver.find_elements_by_class_name("u_cbox_contents"):
                #기사별 모든 댓글 구분하여 저장
                commentSet += ( "/%**+%/" + comment.text.replace("'","") )
                
            # sql 쿼리문 작성
            sql = "INSERT INTO "+self.tablename+" (keyword, title, content, year, month, day, url, comment) VALUES ("
            sql += ("'"+self.keyword+"', '"+title+"',")
            sql += "'%s',%d,%d,%d,'%s','%s')" %( content, year, month, day ,link, commentSet)
            #디비에 입력
            self.cursor.execute(sql)
            
            
        print("Data finished")
        return 0

    def daumNews(self): #다음 뉴스
        url = "https://search.daum.net/search?w=news&nil_search=btn&DA=STC&enc=utf8&cluster=y&cluster_page=1&q="
        url += self.keyword

        self.linkSet = []
        self.driver.get(url) # selenium으로 url 접속
        self.driver.implicitly_wait(10)
        time.sleep(1)

        #검색 기간 설정 클릭
        self.driver.find_element_by_class_name("tit_menu").click()
        #시작 종료일 입력
        datePicker = self.driver.find_elements_by_class_name("hasDatepicker")
        datePicker[0].clear() #기간 설정값 초기화
        datePicker[1].clear()
        datePicker[0].send_keys(self.startDate) #기간 설정 입력
        datePicker[1].send_keys(self.endDate)
        self.driver.find_element_by_class_name("btn_confirm").click()
        self.driver.implicitly_wait(5)

        while True: #다음 페이지 없을때까지 반복
            for daum in self.driver.find_elements_by_class_name("f_nb"):
                if daum.text == "다음뉴스": #다음 뉴스 버튼인 경우만 
                    print(daum.get_attribute("href"))
                    self.linkSet.append(daum.get_attribute("href"))
                else: print("다음 뉴스 없음")
            
            #다음 버튼
            nextBtn = self.driver.find_element_by_class_name("btn_next")
            if nextBtn.get_attribute("data-paging-active") =="true": #다음 버튼이 존재하면
                nextBtn.click() #클릭
            else: break #반복 종료
        
        self.cursor = self.db.cursor()  # DB 연결
        self.daumArticle(self.linkSet) #기사별 데이터 수집
        self.db.commit() #디비 저장
        self.db.close() #디비 연결 종료
        return 0
    
    def daumArticle(self, linkSet):
        link_count = len(linkSet)
        count = 1
        for link in linkSet: #모든 링크 데이터 수집
            self.driver.get(link) # selenium으로 기사 url 접속
            self.driver.implicitly_wait(3)
            time.sleep(0.1)
            count+=1

            try:
                #기사 본문 스크랩
                content = self.driver.find_element_by_class_name("article_view").text.replace("'","")
                #본문에 포함 키워드 없는 경우
                if self.includeKeyword not in content: continue
                
                #기사, 날짜, 댓글 링크 추출
                title = self.driver.find_element_by_class_name("tit_view").text.replace("'","")
                date = self.driver.find_element_by_class_name("num_date").text
                dateList = date.split(".")
                year, month, day = int(dateList[0]), int(dateList[1]), int(dateList[2])

                commentCount = self.driver.find_element_by_class_name("alex-count-area").text
            except selenium.common.exceptions.NoSuchElementException:
                print("select error !!")
                continue

            #찬반순 댓글 정렬 클릭
            if int(commentCount) >5: #댓글이 5개 이상일 경우, 정렬 / 그 이하면 정렬 굳이 필요 없음
                self.driver.find_elements_by_class_name("link_cate")[1].click()
                # 최대 100회, 댓글 더보기 클릭
                for i in range( min(int(int(commentCount)/10), 100) ):
                    time.sleep(0.03)
                    try:
                        more = self.driver.find_element_by_class_name("link_fold")
                        self.driver.execute_script("window.scrollTo(0, 10);")
                        if more.text =="더보기": #더보기 있는 경우
                            more.click()
                            self.driver.implicitly_wait(2)
                    except:
                        time.sleep(0.05)
                        print("전체 댓글 더보기 클릭에서 에러")
                        continue
            
            self.driver.implicitly_wait(1)
            commentSet = ""  #댓글 리스트
            
            for comment in self.driver.find_elements_by_class_name("desc_txt"):
                #기사별 모든 댓글 구분하여 저장
                try:
                    commentSet += ( "/%**+%/" + comment.text.replace("'","") )
                except: continue
            
            #답글 있는 경우
            for i in  self.driver.find_elements_by_class_name("box_reply"):
                try:
                    if "작성" not in i.text: #답글 작성이 아닌 경우 == 답글 달린 경우
                        i.find_element_by_class_name("num_txt").click() #답글 보기 클릭
                        replay_count = int(i.find_element_by_class_name("num_txt").text.replace(",",""))
                        reply_box = self.driver.find_element_by_class_name("reply_wrap")
                        for a in range( int(replay_count/10)): #답글 보기 클릭 횟수
                            time.sleep(0.03)
                            try:
                                reply_box.find_element_by_class_name("alex_more").click()  #답글 더보기 클릭
                                self.driver.implicitly_wait(5)
                            except: time.sleep(0.05)
                            
                        time.sleep(0.25)
                        reply_box = self.driver.find_element_by_class_name("reply_wrap")
                        #답글 수집
                        for comment in reply_box.find_elements_by_class_name("desc_txt"):
                            try:
                                commentSet += ( "/%**+%/" + comment.text.replace("'","") )
                            except: 
                                print("답글 입력 오류")
                                continue
                except :
                    time.sleep(0.1)
                    print("댓글 수집에서 에러 발생함")
                    continue

            # sql 쿼리문 작성
            sql = "INSERT INTO "+self.tablename+" (keyword, title, content, year, month, day, url, comment) VALUES ("
            sql += ("'"+self.keyword+"', '"+title+"',")
            sql += "'%s',%d,%d,%d,'%s','%s')" %( content, year, month, day ,link, commentSet)
            #디비에 입력
            self.cursor.execute(sql)
            print(self.keyword,">>",count,"/",link_count)
            
        return 0

if __name__ == "__main__":
    crawler = newsCrawler("db_table_name", "Start_Date","End_Date", "KEYWORD")
    # ex> newsCrawler("table","20201231","20210209""deep learning", "keras")
    crawler.naverNews()
    crawler.daumNews()
    
    
    