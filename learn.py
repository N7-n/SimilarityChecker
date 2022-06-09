import json
import boto3
import MeCab
import zipfile
import os
from pprint import pprint
import sys

s3 = boto3.resource("s3")
# MeCabの初期化
mecab = MeCab.Tagger()
mecab.parse('')


sents = []
labels = []

def lambda_handler(event, context):

    pprint(os.listdir("/tmp/site-packages/"))
    sys.path.append('/tmp/site-packages')

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
        da, utt = line.split('\t')
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

    # 学習されたモデル等一式を svc.modelに保存
    with open("svc.model","wb") as f:
        dill.dump(vectorizer, f)
        dill.dump(label_encoder, f)
        dill.dump(svc, f)

    #アウトプット用のkey作成
    count = inputKey.find("/")
    output_keyName = "learn" + inputKey[count:]

    #S3に書き出し
    bucket = s3.Bucket(inputBucket)
    with svc.model.open('rb') as f:
        bucket.upload_fileobj(f, output_keyName)
