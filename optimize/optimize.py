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

def lambda_handler(event, context):

    #mecab初期化
    mecab = MeCab.Tagger()
    mecab.parse("")

    #s3からsvc.modelの取得
    s3.Bucket("putlambdan7chat").download_file("svc.model", "/tmp/svc.model")
    s3.Bucket("putlambdan7chat").download_file("label.model", "/tmp/label.model")
    s3.Bucket("putlambdan7chat").download_file("vector.model", "/tmp/vector.model")
    #テキストの取得
    text = event['body']

    with open("/tmp/vector.model","rb") as f:
        vectorizer = f.read()
    with open("/tmp/label.model","rb") as ff:
        label_encoder = ff.read()
    with open("/tmp/svc.model","rb") as fff:
        svc = fff.read()

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