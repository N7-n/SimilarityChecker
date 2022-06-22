import requests
import logging
import os
import urllib.request
import json
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    for message_event in json.loads(event['body'])['events']:
        text = message_event['message']['text']
        reply_token = message_event['replyToken']
        
    input_event = {
        "body": text,
    }
    Payload = json.dumps(input_event) # jsonシリアライズ
    
    response = boto3.client('lambda').invoke(
        FunctionName='n7QandA-dev-learn',
        InvocationType='RequestResponse',
        Payload=Payload
    )


    data = json.loads(response['Payload'].read())["body"]
    
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ['ACCESSTOKEN']
    }
    body = {
        'replyToken': reply_token,
        'messages': [
            {
                "type": "text",
                "text": data,
            }
        ]
    }

    req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), method='POST', headers=headers)
    with urllib.request.urlopen(req) as res:
        logger.info(res.read().decode("utf-8"))


    return {
        'statusCode': 200,
        'body': json.dumps('Success!')
    }