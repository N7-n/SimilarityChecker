import json
import boto3

s3 = boto3.resource("s3")


def lambda_handler(event, context):

    s3_record = event["Records"][0]["s3"]
    inputKey = s3_record["object"]["key"]
    inputBucket = s3_record["bucket"]["name"]

    object = s3.Object(inputBucket, inputKey)
    body = object.get()["Body"].read()

    #アウトプット用のkey作成
    count = inputKey.find("/")
    output_keyName = "learn" + inputKey[count:]

    #S3に書き出し
    bucket = s3.Bucket(inputBucket)
    obj = bucket.Object(output_keyName)
    obj.put(Body=body)
