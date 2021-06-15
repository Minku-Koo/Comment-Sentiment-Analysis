# Comment-Sentiment-Analysis
### Comment Sentiment Analysis using Deep Learning


📌 Author : [Minku Koo](https://github.com/Minku-Koo)    

📌 Project Period : Dec/2020 ~ Jan/2021    

📌 Contact : corleone@kakao.com    

📌 Main Library : tensorflow, keras, KoNLPy

📌 Keyword : "Sentiment Analysis", "Machine Learning", "Korean", "Deep Learning"    


## 1. Scrapping Comment Data

- Python Crawler : ./python-code/comment_crawling.py
- Target Place : Naver, Daum News Comment
- Scrapped Data : Comment, Replay, Article Date (+ Title, Content)
- News Searching Keyword : "기독교", "불교", "천주교", "신천지", "종교"
- Data Saved Place : Database (MariaDB)
- Database Data to Text file - path : ./comment/raw-comment/

### 🔍 Scrapping Period per Religion 
|검색 키워드|수집 시작 기간|기준 날짜|수집 종료 기간|
|:--------:|:-----------:|:------:|:-----------:|
| 신천지 | 19.09.17 | 20.02.17 | 20.07.18 |
| 기독교 |19.08.20| 20.01.20 | 20.10.20 |
| 천주교 | 19.08.20 | 20.01.20 | 20.08.20 |
| 불교 | 19.08.20 | 20.01.20 | 20.08.20 |
| 종교 | 19.08.20 | 20.01.20 | 20.10.10 |

### 🔍 Scrapped Data Result

<table>
    <thead>
        <tr>
        <th rowspan="2">검색 키워드</th>
        <th colspan="2">이전 기간</th>
        <th colspan="2">이후 기간</th>
        </tr>
        <tr>
        <th>Article</th>
        <th>Comment</th>
        <th>Article</th>
        <th>Comment</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>신천지</td>
            <td>211</td>
            <td>22,658</td>
            <td>2,974</td>
            <td>262,840</td>
        </tr>
        <tr>
            <td>기독교</td>
            <td>1,771</td>
            <td>94,405</td>
            <td>1,186</td>
            <td>85,443</td>
        </tr>
        <tr>
            <td>천주교</td>
            <td>1,899</td>
            <td>37,010</td>
            <td>1,685</td>
            <td>56,881</td>
        </tr>
        <tr>
            <td>불교</td>
            <td>833</td>
            <td>6,465</td>
            <td>420</td>
            <td>7,585</td>
        </tr>
        <tr>
            <td>종교</td>
            <td>1,939</td>
            <td>52,527</td>
            <td>2,373</td>
            <td>122,206</td>
        </tr>
    </tbody>
</table>

## 2. Labeling Comment Data

- path : ./train-data/
- Comment Human Inspection : ./train-data/comment-labeling.csv
- Naver Movie Review Data : naver-ratings.csv
- _( Data from [Here](https://github.com/e9t/nsmc) )_

## 3. Using KoNLPy Okt

#### Text Data Preprocessing
```
okt.pos(comment)
remove 'Josa', 'Punctuation', 'Number'
save path : ./comment/after-okt-comment/
```


## 4. Build Deep Learning Network using Keras

- Python File Name : ./python-code/make_rnn_model.py
- Train Data path : ./train-data/
- Crawled Comment + Naver Movie Reivew => Transfer Learning
- Comment text data convert to Vector (using TextVectorization)
- Accuracy : 0.95
- Val Accuracy : 0.83

![model-making](https://user-images.githubusercontent.com/25974226/105630839-9d28dd00-5e8e-11eb-8067-4e23fca24768.JPG)


## 5. After build RNN Model

1) make json file / dict[date][article] = [[comment list],[]]
1) Every Comment Labeling using RNN Model
1) update json file / dict[date][article] = [[comment list],[sentiment value list]] (path: ./comment/json-okt-comment)
1) Calculate sentiment per date 
    + each Article sentiment : Weight Average _(article comment count / date comment count)_
    + each Date sentiment : using IMDb's rating system _(https://www.quora.com/How-does-IMDbs-rating-system-work)_
    ![계산하기2](https://user-images.githubusercontent.com/25974226/105633620-044d8e00-5e9d-11eb-92df-b4072a9d0ee2.JPG)


## 6. RESULT (Make Graph)

### 📍 Average, Standard Deviation / Religion ###
![표준편차및분산표](https://user-images.githubusercontent.com/25974226/105630857-b3cf3400-5e8e-11eb-9439-81028d316b63.JPG)

### 📍 Sentiment time flow graph  ###
*(path : ./result-graph/emotion-flow/)*


   - Before COVID19 : color green
   - After COVID19 : color red
   - y axis
       + close to 1 : Positive
       + close to 0 : Negative
    <br><br>
   ✔ **천주교**
     ![천주교-graph-emotion-flow](https://user-images.githubusercontent.com/25974226/105630885-e11be200-5e8e-11eb-8b03-94246ee73ca0.png)
   ✔ **종교**
     ![종교-graph-emotion-flow](https://user-images.githubusercontent.com/25974226/105630878-d82b1080-5e8e-11eb-8941-1b89254813a7.png)
   
### 📍 All Comment Count per Month / Religion   ###
*(path : ./result-graph/comment-count/)*
![graph-month-comment-count](https://user-images.githubusercontent.com/25974226/105630892-e8db8680-5e8e-11eb-95f6-d35c6ebe7128.png)

### 📍 Sentiment Average stick graph / Religion   ###
*(path : ./result-graph/emotion-average-stick/)*
![종교별 평균 감성 지수-graph-avg-emotion](https://user-images.githubusercontent.com/25974226/105630900-f264ee80-5e8e-11eb-88d5-fab987e80766.png)


### 📍 WordCloud / Religion  ###
*(path : ./result-graph/word-cloud/)*


   ✔ Before COVID19, 기독교
     ![기독교 이전-wordcloud](https://user-images.githubusercontent.com/25974226/105630935-19232500-5e8f-11eb-8f73-45b7342d06b0.png)
   ✔ After COVID19, 기독교
     ![기독교 이후-wordcloud](https://user-images.githubusercontent.com/25974226/105630939-1a545200-5e8f-11eb-82fa-c1d5dca13034.png)

### 📍 Top 30 Word / Religion  ###
*(path : ./result-graph/word-cloud/)*


   ✔ __Before COVID19, 신천지__
     ![before1-graph](https://user-images.githubusercontent.com/25974226/105630930-1294ad80-5e8f-11eb-810f-24a8741f4513.png)
   ✔ __After COVID19, 신천지__
     ![after1-graph](https://user-images.githubusercontent.com/25974226/105630911-fe50b080-5e8e-11eb-90bb-29e8fd9cfb16.png)
    




