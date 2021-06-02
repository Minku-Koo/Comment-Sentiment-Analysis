#-*- coding:utf-8 -*-

# using kobert
# start : 21.05.17
# update : 21.05.xx

# https://github.com/SKTBrain/KoBERT
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] ='2'
import torch
from kobert.utils import get_tokenizer
from kobert.pytorch_kobert import get_pytorch_kobert_model
# from gluonnlp.data import SentencepieceTokenizer


'''
https://moondol-ai.tistory.com/241
https://ebbnflow.tistory.com/151
BERT를 사용하지 않은 일반 모델과정은,
: 분류를 원하는 데이터 -> LSTM, CNN 등의 머신러닝 모델 -> 분류

BERT를 사용한 모델링 과정,
: 관련 대량 코퍼스 -> BERT -> 분류를 원하는 데이터 -> LSTM, CNN 등의 머신러닝 모델 -> 분류
https://drive.google.com/file/d/1fR2VsROYiCunp3BxcXJJNMlK4h51Nkey/view?usp=sharing

# test
!wget "https://drive.google.com/uc?export=download&id=1PWcT5ucCWPPefzJVLBjC1KszKamn_vyR" -O datatest.tsv
https://drive.google.com/file/d/1PWcT5ucCWPPefzJVLBjC1KszKamn_vyR/view?usp=sharing
# train
!wget "https://drive.google.com/uc?export=download&id=13xxABWzRT0mjoPEKWApezhX96XPH58sk" -O datatrain.tsv
https://drive.google.com/file/d/13xxABWzRT0mjoPEKWApezhX96XPH58sk/view?usp=sharing
'''

print("sstart")


input_ids = torch.LongTensor([[31, 51, 99], [15, 5, 0]])
input_mask = torch.LongTensor([[1, 1, 1], [1, 2, 0]])
token_type_ids = torch.LongTensor([[0, 0, 1], [0, 2, 0]])
print("do get_pytorch_kobert_model")
model, vocab  = get_pytorch_kobert_model()
print("do model")
sequence_output, pooled_output = model(input_ids, input_mask, token_type_ids)

# 버트를 사용하기에 앞서 가장 기초에 속하는 tokenizer 사용 방법에 대해서 잠시 배워보도록 하겠습니다.
# tokenizer.encode => 문장을 버트 모델의 인풋 토큰값으로 바꿔줌
# tokenizer.tokenize => 문장을 토큰화
# print(tokenizer.encode("보는내내 그대로 들어맞는 예측 카리스마 없는 악역"))
# print(tokenizer.tokenize("보는내내 그대로 들어맞는 예측 카리스마 없는 악역"))
# print(tokenizer.encode("전율을 일으키는 영화. 다시 보고싶은 영화", max_length=64, pad_to_max_length=True))


# bertmodel, vocab = get_pytorch_kobert_model()

unseen_test = pd.DataFrame([['음식, 발열, 구토, 복통, 설사', 7]], columns = [['질문 내용', '질병명']]) 

unseen_values = ["그러니까 제발 그러지마 ㅠㅜ완전 싫다고","맞아맞아 나는 그게 제일 좋아!! 사랑해"]
test_set = BERTDataset(unseen_values, 0, 1, tok, max_len, True, False) 
test_input = torch.utils.data.DataLoader(test_set, batch_size=batch_size, num_workers=5) 

for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(tqdm_notebook(test_input)): 
    token_ids = token_ids.long().to(device) 
    segment_ids = segment_ids.long().to(device) 
    valid_length= valid_length 
    out = model(token_ids, valid_length, segment_ids) 
    print(out)



