# Comment-Sentiment-Analysis
### Comment Sentiment Analysis using Deep Learning
---------------------------------------------------

- Author : Minku Koo
- Project Period : Dec/2020 ~ 21/Jan/2021
- E-Mail : corleone@kakao.com
- Keyword : "sentiment-analysis", "korean", "deep learning", "KoNLPy", "keras", "tensorflow"

---------------------------------------------------

## 1. Comment Data Scrap

- Python File Name : ./python-code/comment_crawling.py
- Target Place : Naver, Daum News Comment
- Scrap Data : Comment, Replay, Article Date (+ Title, Content)
- News Searching Keyword : "기독교", "불교", "천주교", "신천지", "종교"
- Data Save Place : Database (mysql or MariaDB)
- Database Data to Text file - path : ./comment/raw-comment/

- Scrap Period per Religion
![수집기간](https://user-images.githubusercontent.com/25974226/105630853-add95300-5e8e-11eb-9e23-37addf3c6904.JPG)

- Scrap Data Result
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

> okt.pos(comment) <br>
> remove 'Josa', 'Punctuation', 'Number'<br>
> save path : ./comment/after-okt-comment/

---------------------------------------------------

## 4. Build RNN Model with Keras

- Python File Name : ./python-code/make_rnn_model.py
- Train Data path : ./train-data/
- _Comment + Naver Movie Reivew => Transfer Learning_
- Comment text data convert to Vector (using TextVectorization)
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
  ![계산하기](https://user-images.githubusercontent.com/25974226/105630843-a31ebe00-5e8e-11eb-880c-dc426ceced4c.JPG)


---------------------------------------------------

## 6. Make Graph

- 

