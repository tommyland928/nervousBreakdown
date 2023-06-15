#!/usr/local/bin/python

import sys
import io
import pymysql
import random
import string
import datetime
import os
import urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')

cookieString = os.environ['HTTP_COOKIE']
cookieDic = {}
if cookieString != "":
    cookiesStringList = cookieString.split(';')
    
    for i in cookiesStringList:
        tmp = i.split('=')
        cookieDic[tmp[0].replace(' ','')] = tmp[1] 
else:
    cookieDic["name"] = ""
    cookieDic["sessid"] = ""


#冒頭のhtmlメッセージのみ送信
print("Content-Type: text/html")
print()

#セッション登録済みのものならばbattleサイトへ誘導
try:
    with connection.cursor() as cursor:
        #member情報を格納
        sql = "select * from users"
        cursor.execute(sql)
        result = cursor.fetchall()
        users = []
        sessids = []
        for i in result:
            users.append(i[1])
            sessids.append(i[2])

        sql = "select * from rooms"
        cursor.execute(sql)
        result = cursor.fetchall()
        room = ""
        phase = 0
        for i in result:
            room = i[1]
            phase = i[2]

        for i in range(0,len(users)):
            if users[i] == cookieDic["name"] and sessids[i] == cookieDic["sessid"] and phase == 0:
                html = """<html>
                    <head>
                        <meta charset='UTF-8'>
                        <script>
                            window.location.href = "http://192.168.11.140:8000/cgi-bin/battle.py"
                        </script>
                    </head>
                    <body>
                    </body>
                </html>
                """
                print(html)
        else:
            html = """<html>
	            <head>
	                <meta charset='UTF-8'>
                </head>
                <body>
                    <h1>ポーカー対戦</h1>
                     <h2>名前を入力してください</h2>
                    <form action="/cgi-bin/checkName.py" method="POST">
                        <input type="text" name="name"/>
                        <input type="submit" name="submit"/>
                    </form>
                    <div id="test"></div>
                </body>
            </html>
            """
            print(html)
finally:
    connection.close()
