#!/usr/local/bin/python

import sys
import io
import pymysql
import time
import os
import urllib.parse

connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')
###クッキー情報を辞書型に変換 cookieDic###
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
        
            
        if ready == 0: 
            sql = f"UPDATE users SET ready=1 WHERE name='{cookieDic['name']}' AND sessid='{cookieDic['sessid']}'"
            cursor.execute(sql)
            connection.commit()
finally:
    connection.close()







