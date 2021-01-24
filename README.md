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
- ( Data from https://github.com/e9t/nsmc )

---------------------------------------------------

## 3. Build RNN Model with Keras




