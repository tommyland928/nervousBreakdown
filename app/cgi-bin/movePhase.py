#!/usr/local/bin/python

import sys
import io
import pymysql
import random
import string
import datetime
import os
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')

cookieString = os.environ['HTTP_COOKIE']
cookiesStringList = cookieString.split(';')
cookieDic = {}
for i in cookiesStringList:
    tmp = i.split('=')
    cookieDic[tmp[0].replace(' ','')] = tmp[1] 

#冒頭のhtmlメッセージのみ送信
html = """Content-Type: text/html

{"ok": 1}
"""
print(html)

def randomCard():
    while True:
        suit = random.randint(1,4)
        num = random.randint(1,13)
        #card = int(str(suit)+str(num))
        #重複チェック重複が無ければ代入
        kind = ""
        if suit ==1:
            kind = "spades"
        if suit ==2:
            kind = "clovers"
        if suit ==3:
            kind = "hearts"
        if suit ==4:
            kind = "dias"

        sql = f"SELECT count(room1) FROM {kind} WHERE room1 = {num}"
        cursor.execute(sql)
                    
        if cursor.fetchone()[0] != 0:
            sql = f"DELETE FROM {kind} WHERE room1 = {num}"
            cursor.execute(sql)
            connection.commit()
            return [suit,num]



try:
    with connection.cursor() as cursor:
        #最初にいろんなDBの取り出し
        #roomsの情報 roomナンバー,　phaseを格納
        sql = "select * from rooms"
        cursor.execute(sql)
        rooms = cursor.fetchall()
        room = 0
        phase = 0
        for i in rooms:
            room = i[1]
            phase = i[2]
        #member情報を格納
        sql = "select * from users"
        cursor.execute(sql)
        result = cursor.fetchall()
        users = []
        sessids = []

        for i in result:
            users.append(i[1])
            sessids.append(i[2])
        
        #もしphase==0 and readyボタンを押してる人が二人いるなら次のフェーズへ
        sql = "select count(*) from users where ready=1"
        cursor.execute(sql)
        result = cursor.fetchone()
        readyNum = result[0]

        if (phase==0 and readyNum==2) or (phase==2 and readyNum==2):
            #カードの作成
            
            sql = "insert into hearts (room1) values (1),(3),(7),(9),(12),(13)"
            cursor.execute(sql)
            sql = "insert into spades (room1) values (1),(3),(7),(9),(12),(13)"
            cursor.execute(sql)
            sql = "insert into dias (room1) values (1),(3),(7),(9),(12),(13)"
            cursor.execute(sql)
            sql = "insert into clovers (room1) values (1),(3),(7),(9),(12),(13)"
            cursor.execute(sql)
            

            #tableデータベースの作成
            member = []
            sql = "select name from users where ready=1"
            cursor.execute(sql)
            result = cursor.fetchall()
            for i in result:
                member.append(i[0])
            memberJson = json.dumps(member)
            get = [0,0]
            getJson = json.dumps(get)
            tableCard = [[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]]]
            #ランダムでテーブルカードを取り出す
            for i in range(0,4):
                for j in range(0,6):
                    card = randomCard()
                    tableCard[i][j] = card
            openCard = []
            openCardJson = json.dumps(openCard)
            tableCardJson = json.dumps(tableCard)
            sql =f"delete from battles"
            cursor.execute(sql)
            connection.commit()
            sql = f"insert into battles (member,turn,get,tableCard,openCard,winner) values ('{memberJson}',0,'{getJson}','{tableCardJson}','{openCardJson}','')"
            cursor.execute(sql)

            #phaseを前に進める
            sql = "update rooms set phase=1 where id=1"
            cursor.execute(sql)
            connection.commit()
        
        if phase == 1:
            sql = "select * from battles"
            cursor.execute(sql)
            result = cursor.fetchall()
            memberJson = ""
            member = []
            getJson = ""
            get = []
            for i in result:
                memberJson = i[1]
                getJson = i[3]

            member = json.loads(memberJson)
            get = json.loads(getJson)
            if get[0]+get[1] == 24:
                #試合終了
                #誰が勝ったかを教える

                winner = ""
                if get[0] > get[1]:
                    winner = member[0]
                elif get[0] < get[1]:
                    winner = member[1]
                elif get[0] == get[1]:
                    winner = "引き分け"
                
                #テーブルのカードをすべて0に戻す
                tableCard = [[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]],[[],[],[],[],[],[]]]
                for i in range(0,4):
                    for j in range(0,6):
                        tableCard[i][j] = [0,0]
                tableCardJson = json.dumps(tableCard)
                openCard = []
                openCardJson = json.dumps(openCard)
                sql = f"update battles set winner='{winner}',tableCard='{tableCardJson}',openCard='{openCardJson}'"
                cursor.execute(sql)
                connection.commit()
                
                #roomsのphaseを0に戻す
                sql = "update rooms set phase=2"
                cursor.execute(sql)
                #usersのreadyを下げる
                sql = "update users set ready=0"
                cursor.execute(sql)
                #カード情報をすべて消すroom1
                sql = "delete from dias"
                cursor.execute(sql)
                sql = "delete from hearts"
                cursor.execute(sql)
                sql = "delete from spades"
                cursor.execute(sql)
                sql = "delete from clovers"
                cursor.execute(sql)
                connection.commit()

finally:
    connection.close()