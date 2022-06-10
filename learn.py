import json
import boto3
import MeCab
import dill
import zipfile
import os
from pprint import pprint
import sys
import io
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer 


s3 = boto3.resource("s3")
# MeCabの初期化
mecab = MeCab.Tagger()
mecab.parse('')


sents = []
labels = []

def lambda_handler(event, context):
#    zip_ref = zipfile.ZipFile('/tmp/scipy.zip', 'r')
#   zip_ref = zipfile.ZipFile('/tmp/numpy.zip', 'r')
#    zip_ref = zipfile.ZipFile('/tmp/dill.zip', 'r')
#    zip_ref = zipfile.ZipFile('/tmp/sklearn.zip', 'r')
#    zip_ref.extractall('/tmp')
#    zip_ref.close()
#    os.remove("/tmp/scipy.zip")
#    os.remove("/tmp/numpy.zip")
#    os.remove("/tmp/dill.zip")
#    os.remove("/tmp/sklearn.zip")


    s3_record = event["Records"][0]["s3"]
    inputKey = s3_record["object"]["key"]
    inputBucket = s3_record["bucket"]["name"]

    object = s3.Object(inputBucket, inputKey)
    body = object.get()["Body"].read()

    #デコード
    body = body.decode()

    bodyList = body.splitlines()


    for line in bodyList:
        line = line.rstrip()
        co = line.find(" ")
        da = line[0:co-1]
        utt = line[co+1:]
        words = []
        for line in mecab.parse(utt).splitlines():
            if line == "EOS":
                break
            else:
                word, feature_str = line.split("\t")
                words.append(word)
        sents.append(" ".join(words))
        labels.append(da)

    # TfidfVectorizerを用いて，各文をベクトルに変換
    vectorizer = TfidfVectorizer(tokenizer=lambda x:x.split(), ngram_range=(1,3))
    X = vectorizer.fit_transform(sents)

    #    LabelEncoderを用いて，ラベルを数値に変換
    label_encoder = LabelEncoder()
    Y = label_encoder.fit_transform(labels)

    # SVMでベクトルからラベルを取得するモデルを学習
    svc = SVC(gamma="scale")
    svc.fit(X,Y)

    f = io.BytesIO()
    dill.dump(vectorizer, f)
    dill.dump(label_encoder, f)
    dill.dump(svc, f)


    #アウトプット用のkey作成
    output_keyName = "learn/svc.model"

    #S3に書き出し
    bucket = s3.Bucket(inputBucket)
    bucket.upload_fileobj(f, output_keyName)
        
