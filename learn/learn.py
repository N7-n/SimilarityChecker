import boto3
import MeCab
from pprint import pprint
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
    mecab = MeCab.Tagger()
    mecab.parse("")

    inputKey = "text/learn.txt"
    inputBucket = "n7chatdata"

    text = event['body']

    object = s3.Object(inputBucket, inputKey)
    body = object.get()["Body"].read()

    body = body.decode()
    bodyList = body.splitlines()

    for line in bodyList:
        line = line.rstrip()
        co = line.find(" ")
        da = line[0:co]
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

    vectorizer = TfidfVectorizer(tokenizer=lambda x:x.split(), ngram_range=(1,3))
    X = vectorizer.fit_transform(sents)

    label_encoder = LabelEncoder()
    Y = label_encoder.fit_transform(labels)

    svc = SVC(gamma="scale")
    svc.fit(X,Y)

    words = []
    for line in mecab.parse(text).splitlines():
        if line == "EOS":
            break
        else:
            word, feature_str = line.split("\t")
            words.append(word)
    str = " ".join(words)
    X = vectorizer.transform([str])
    Y = svc.predict(X)

    da = label_encoder.inverse_transform(Y)[0]
    return {
        "body": da
    }
