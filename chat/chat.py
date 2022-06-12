import json
import boto3
import MeCab
import dill
import os
from pprint import pprint
import sys
import io
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer 

s3 = boto3.resource("s3")

#s3からlearn.pyの取得
s3.Bucket("putlambdan7chat").download_file("learn.py", "/tmp/learn.py")

from tmp import learn
sys.modules['learn'] = learn

def lambda_handler(event, context):

    #mecab初期化
    mecab = MeCab.Tagger()
    mecab.parse("")

    #s3からsvc.modelの取得
    s3.Bucket("putlambdan7chat").download_file("data.dill", "/tmp/data.dill")
    #テキストの取得
    text = event['body']

    with open("/tmp/data.dill","rb") as f:
        vectorizer = dill.load(f)
        label_encoder = dill.load(f)
        svc = dill.load(f)

    da =  decide_da(text)
    return {
        "body": da
    }

def decide_da(utt):
    words = []
    for line in mecab.parse(utt).splitlines():
        if line == "EOS":
            break
        else:
            word, feature_str = line.split("\t")
            words.append(word)
    str = " ".join(words)
    X = vectorizer.transform([str])
    Y = svc.predict(X)

    da = labal_encoder.inverse_transform(Y)[0]

    return da