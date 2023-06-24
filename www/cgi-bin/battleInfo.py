#!/usr/bin/python3
import sys
import io
import pymysql
import datetime
import os
import json 

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')

"""
ユーザからのリクエストに応じて盤面の情報をユーザに送る
battle.jsと連携
"""

#cookieを確認,cookieDic["名前"]で値を参照
try:
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
except KeyError:
    cookieDic = {}
    cookieDic["name"] = ""
    cookieDic["sessid"] = ""

#冒頭のhtmlメッセージのみ送信
print("Content-Type: text/html")
print()

try:
    with connection.cursor() as cursor:
        #member情報を格納
        sql = "select name,sessid from users"
        cursor.execute(sql)
        result = cursor.fetchall()
        users = []
        sessids = []
        for i in result:
            users.append(i[0])
            sessids.append(i[1])
        
        #同じセッションIDが無ければindexにリダイレクト
        """
        for i in result:
            if cookieDic["name"] == i[0] and cookieDic["sessid"] == i[1]:
                break
        else:
            html = <html>
                <head>
                    <meta charset='UTF-8'>
                    <script>
                        window.location.href = "/cgi-bin/index.py"
                    </script>
                </head>
                <body>
                </body>
            </html>
            
            print(html)
            sys.exit()
            """

        sql = "select room,phase from rooms"
        cursor.execute(sql)
        result = cursor.fetchall()
        room = ""
        phase = 0
        for i in result:
            room = i[0]
            phase = i[1]
        
        #phase=0(試合前)の時にはまだデータベースから参照するものがないから、すべての値を初期化
        memberJson = ""
        turn = -1
        getJson = ""
        tableCardJson = ""
        openCardJson = ""
        member = []
        get = []
        tableCard = [[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]]
        sendOpenCard = [[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]]
        openCard=[]
        winner = ""
        if phase != 0: #試合後は上の初期化をデータベースの値で上書き
            sql = "select member,turn,get,tableCard,openCard,winner from battles"
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in result:
                memberJson = i[0]
                turn = i[1]
                getJson = i[2]
                tableCardJson = i[3]
                openCardJson = i[4]
                winner = i[5]

            member = json.loads(memberJson)
                
            get = json.loads(getJson)
            tableCard = json.loads(tableCardJson)
            openCard = json.loads(openCardJson)

            onlyOpenCard = []
            for i in openCard:
                sendOpenCard[i[0]][i[1]] = tableCard[i[0]][i[1]]
            
            for i in range(0,4):
                for j in range(0,6):
                    if tableCard[i][j][0] == -1:
                        sendOpenCard[i][j] = tableCard[i][j]
        #tablesも呼び出す

        if phase == 0: #試合前に送るJSON
            #この時点ではまだbattlesレコードが作られてない
            sendDic = {}
            sendDic["member"] = []
            sendDic["turn"] = -1 #-1でフロントの開始前の合図に使う
            sendDic["get"] = [0,0]
            sendDic["tableCard"] = sendOpenCard
            sendDic["winner"] = ""
            sendJson = json.dumps(sendDic)
            print(sendJson)
        if phase == 1: #試合中に送るJSON
            sendDic = {}
            sendDic["member"] = member
            sendDic["turn"] = turn 
            sendDic["get"] = get
            sendDic["tableCard"] = sendOpenCard
            sendDic["winner"] = ""
            sendJson = json.dumps(sendDic)
            print(sendJson)
        #phase=2の時はwinnerを渡す
        if phase==2: #試合後に送るJSON（正直phase==1の時との統合が可能）
            sendDic = {}
            sendDic["member"] = member
            sendDic["turn"] = turn 
            sendDic["get"] = get
            sendDic["tableCard"] = sendOpenCard
            sendDic["winner"] = winner
            sendJson = json.dumps(sendDic)
            print(sendJson)

finally:
    connection.close()
