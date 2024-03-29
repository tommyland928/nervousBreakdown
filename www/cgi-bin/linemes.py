
import requests
import json
import urllib.parse
import apikey

"""
lineにメッセージをline message APIを用いて送信する
送信内容は、誰と誰が遊んでくれたかである。
"""

def mes(memberArg):
    url = 'https://api.line.me/v2/bot/message/broadcast'
    
    apiKey = apikey.apiKey
    
    headers = {
        'Authorization': 'Bearer ' + apiKey,
        'Content-Type': 'application/json'
    }
    member1 = urllib.parse.unquote(memberArg[0])
    member2 = urllib.parse.unquote(memberArg[1])
    message =  member1 + "と" + member2 + "が遊んでくれました。"
    message_list = {
        'messages': [
            {
                'type': 'text',
                'text': message
            }
        ]
    }
    data = json.dumps(message_list)
    response = requests.post(url, headers=headers, data=data)
    return

