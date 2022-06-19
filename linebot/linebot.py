import json
import requests
import os
def lambda_handler(event, context):
    for message_event in json.loads(event['body'])['events']:
        text = message_event['message']['text']
    url = 'https://3qpdobwt1e.execute-api.ap-northeast-1.amazonaws.com/dev/posts/create'
    data = {
        "body": text,
    }
    r = requests.post(url, json=data)
    tag = r.content

    if tag == "mail":
        result = "迷惑メールフォルダを確認してください"
    elif tag == "account":
        result = "アカウント作成はこちらから"
    else:
        result = "abc"

    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ['ACCESSTOKEN']
    }
    data = {
        'replyToken': message_event['replyToken'],
        'messages': [
            {
                "type": "text",
                "text": result,
            }
        ]
    }