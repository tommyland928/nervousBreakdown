#!/usr/bin/python3

import sys
import io
import cgi
import pymysql
import datetime
import os
import json 

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')

"""
試合中、クリックされたカードの座標情報の登録周りを担う
ここで登録された情報を元にbattleInfo.pyで盤面の情報をユーザに送る
"""

#cookieを格納
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
html = """Content-Type: text/html

{"ok": 1}
"""
print(html)


form = cgi.FieldStorage()
row = int(form.getvalue('row'))
column = int(form.getvalue('column'))


try:
    with connection.cursor() as cursor:

        #まず正規のユーザかを確認
        sql = "select count(*) from users where name=%s and sessid=%s"
        cursor.execute(sql,(cookieDic['name'],cookieDic['sessid']))
        result = cursor.fetchone()
        exist = result[0]

        #自分の番か
        sql = "select member,turn,get,tableCard,openCard from battles"
        cursor.execute(sql)
        result = cursor.fetchall()

        memberJson = ""
        turn = -1
        tableCardJson = ""
        openCardJson = ""
        getJson = ""

        for i in result:
            memberJson = i[0]
            turn = i[1]
            getJson = i[2]
            tableCardJson = i[3]
            openCardJson = i[4]

        member = json.loads(memberJson)
        get = json.loads(getJson)
        tableCard = json.loads(tableCardJson)
        openCard = json.loads(openCardJson)
        openCardNum = len(openCard)
        
        selectedCard = tableCard[row][column]
        turnName = member[turn]
        if exist == 1 and cookieDic["name"] == turnName and selectedCard[0] != -1 and openCardNum < 2:#正規のユーザであり　かつ　順番の人 かつ　選ばれたカードが背景画像じゃない　かつ　オープンされたカードが二枚より少ない
            
            #同じところをクリっくしていたら無効
            if openCardNum == 0:#登録 #データベース更新　//バトルの一番最初のみクリックされたら呼ばれる
                openCard.append([row,column])
                openCardJson = json.dumps(openCard)
                sql = f"update battles set openCard='{openCardJson}'"
                cursor.execute(sql)
                connection.commit()

                
            elif openCardNum == 1:
                alreadySelected = tableCard[openCard[0][0]][openCard[0][1]]
                if alreadySelected != selectedCard:#登録　#データベース更新
                    openCard.append([row,column])
                    openCardJson = json.dumps(openCard)
                    sql = f"update battles set openCard='{openCardJson}'"
                    cursor.execute(sql)
                    connection.commit()
                #二枚が同じならgetを変更 
                #tablecardを-1,-1に変更
                #ターンはここでは変更しない次の文で自動的に変更される
                firstCardLoc = openCard[0]#座標を示しているにすぎない
                secondCardLoc = openCard[1]
                firstCard = tableCard[firstCardLoc[0]][firstCardLoc[1]]
                secondCard = tableCard[secondCardLoc[0]][secondCardLoc[1]]
                
                if firstCard[1] == secondCard[1]:
                    tableCard[firstCardLoc[0]][firstCardLoc[1]] = [-1,-1]
                    tableCard[secondCardLoc[0]][secondCardLoc[1]] = [-1,-1]
                    #自分がgetのどっち側かを確認しなきゃいけない
                    get[turn] += 2

                    openCard = []
                    openCardJson = json.dumps(openCard)

                    tableCardJson = json.dumps(tableCard)
                    getJson = json.dumps(get)
                    sql = f"update battles set tableCard='{tableCardJson}',get='{getJson}',openCard='{openCardJson}'"
                    cursor.execute(sql)
                    connection.commit()

                
                
        elif exist == 1 and cookieDic["name"] != turnName and selectedCard[0] != -1 and openCardNum == 2:#相手のターンかつ二枚選ばれてるときは自分のターン
            #自分のターンにする
            if turn == 0:
                turn = 1
            elif turn == 1:
                turn = 0

            #openCardを二つとも削除する
            openCard = []
            #自分の値を追加するopenCardに追加する
            openCard.append([row,column])
            openCardJson = json.dumps(openCard)

            sql = f"update battles set turn={turn},openCard='{openCardJson}'"
            cursor.execute(sql)
            connection.commit()
            

finally:
    connection.close()



