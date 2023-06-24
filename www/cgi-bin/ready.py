#!/usr/bin/python3

import sys
import io
import pymysql
import os

"""
readyボタンを押されたときの処理を記述
ready.jsと連携
この情報を元にmovePhase.pyにて試合前→試合中への遷移が行われる
"""
connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')
###クッキー情報を辞書型に変換 cookieDic###
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

########################################

html_body = """Content-Type: text/html

{
    "ok":"ok"
}
"""
print(html_body)


try:
    with connection.cursor() as cursor:
        #readyボタンを既に二人押していれば変更できないようにする
        sql = f"SELECT * FROM users WHERE name='{cookieDic['name']}' and sessid='{cookieDic['sessid']}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        name = ""
        sessid = ""
        ready = -1
        for i in result:
            name = i[1]
            sessid = i[2]
            ready = i[3]
        
        sql = "select count(*) from users where ready=1"
        cursor.execute(sql)
        result = cursor.fetchone()
        if ready == 0 and result[0] <= 1: 
            sql = f"UPDATE users SET ready=1 WHERE name='{cookieDic['name']}' AND sessid='{cookieDic['sessid']}'"
            cursor.execute(sql)
            connection.commit()
finally:
    connection.close()







