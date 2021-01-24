# Comment-Sentiment-Analysis
### Comment Sentiment Analysis using Deep Learning
---------------------------------------------------

- Author : Minku Koo
- Project Period : Dec/2020 ~ 21/Jan/2021
- E-Mail : corleone@kakao.com
- Keyword : "sentiment-analysis", "korean", "deep learning", "KoNLPy", "keras", "tensorflow"

---------------------------------------------------
---------------------------------------------------

## 1. Comment Data Scrap

- Python File Name : ./python-code/comment_crawling.py
- Target Place : Naver, Daum News Comment
- Scrap Data : Comment, Replay, Article Date (+ Title, Content)
- News Searching Keyword : "기독교", "불교", "천주교", "신천지", "종교"
- Data Save Place : Database (mysql or MariaDB)
- Database Data to Text file - path : ./comment/raw-comment/

* __Scrap Period per Religion__
![수집기간](https://user-images.githubusercontent.com/25974226/105630853-add95300-5e8e-11eb-9e23-37addf3c6904.JPG)

* __Scrap Data Result__
![수집결과](https://user-images.githubusercontent.com/25974226/105630851-aa45cc00-5e8e-11eb-9890-0e4e165ab8f5.JPG)

---------------------------------------------------

## 2. Comment Data Labeling

- path : ./train-data/
- Comment Handwork : comment-labeling.csv
- Naver Movie Review : naver-ratings.csv
- _( Data from https://github.com/e9t/nsmc )_

- 네이버 및 다음 뉴스 댓글 수작업 레이블링 데이터 :  ./train-data/comment-labeling.csv

---------------------------------------------------

## 3. Use KoNLPy Okt

```
okt.pos(comment)
remove 'Josa', 'Punctuation', 'Number'
save path : ./comment/after-okt-comment/
```

---------------------------------------------------

## 4. Build RNN Model with Keras

- Python File Name : ./python-code/make_rnn_model.py
- Train Data path : ./train-data/
- _Comment + Naver Movie Reivew => Transfer Learning_
- Comment text data convert to Vector __(using TextVectorization)__
- Accuracy : 0.95
- Val Accuracy : 0.83

![model-making](https://user-images.githubusercontent.com/25974226/105630839-9d28dd00-5e8e-11eb-8067-4e23fca24768.JPG)

---------------------------------------------------

## 5. After build RNN Model

1. make json file / dict[date][article] = [[comment list],[]]
1. Every Comment Labeling using RNN Model
1. update json file / dict[date][article] = [[comment list],[sentiment list]] (path: ./comment/json-okt-comment)
1. Calculate sentiment per date 
    + each Article sentiment : Weight Average _(article comment count / date comment count)_
    + each Date sentiment : using IMDb's rating system _(https://www.quora.com/How-does-IMDbs-rating-system-work)_
    ![계산하기2](https://user-images.githubusercontent.com/25974226/105633620-044d8e00-5e9d-11eb-92df-b4072a9d0ee2.JPG)

---------------------------------------------------

## 6. Make Graph

1. Average, Dispersion, Standard Deviation / Religion
![표준편차및분산표](https://user-images.githubusercontent.com/25974226/105630857-b3cf3400-5e8e-11eb-9439-81028d316b63.JPG)

1. Sentiment time flow graph  _(path : ./result-graph/emotion-flow/)_
   + __천주교__
   ![천주교-graph-emotion-flow](https://user-images.githubusercontent.com/25974226/105630885-e11be200-5e8e-11eb-8b03-94246ee73ca0.png)
   + __종교__
   ![종교-graph-emotion-flow](https://user-images.githubusercontent.com/25974226/105630878-d82b1080-5e8e-11eb-8941-1b89254813a7.png)
   
1. All Comment Count per Month / Religion  _(path : ./result-graph/comment-count/)_
![graph-month-comment-count](https://user-images.githubusercontent.com/25974226/105630892-e8db8680-5e8e-11eb-95f6-d35c6ebe7128.png)

1. Average Sentiment stick graph / Religion  _(path : ./result-graph/stick/)_
![종교별 평균 감성 지수-graph-avg-emotion](https://user-images.githubusercontent.com/25974226/105630900-f264ee80-5e8e-11eb-88d5-fab987e80766.png)

1. WordCloud / Religion  _(path : ./result-graph/word-cloud/)_
    + __Before COVID19, 기독교__
    ![기독교 이전-wordcloud](https://user-images.githubusercontent.com/25974226/105630935-19232500-5e8f-11eb-8f73-45b7342d06b0.png)
    + __After COVID19, 기독교__
    ![기독교 이후-wordcloud](https://user-images.githubusercontent.com/25974226/105630939-1a545200-5e8f-11eb-82fa-c1d5dca13034.png)

1. Top 20 Word / Religion  _(path : ./result-graph/top-word/)_
   + __Before COVID19, 신천지 __
    ![before1-graph](https://user-images.githubusercontent.com/25974226/105630930-1294ad80-5e8f-11eb-810f-24a8741f4513.png)
    + __After COVID19, 신천지__
    ![after1-graph](https://user-images.githubusercontent.com/25974226/105630911-fe50b080-5e8e-11eb-90bb-29e8fd9cfb16.png)
    




