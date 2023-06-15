#!/usr/local/bin/python

import cgi
import sys
import io
import cgitb
import pymysql
import time
import json
import urllib.parse
import os



cgitb.enable()
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

cookieDic["name"] = urllib.parse.unquote(cookieDic["name"])
########################################

html_body = """Content-Type: text/html

{
    "ok":"ok"
}
"""
print(html_body)


try:
    with connection.cursor() as cursor:
        sql = "select member from battles"
        cursor.execute(sql)
        result = cursor.fetchone()
        member = json.loads(result[0])
        print(member[1])

finally:
    connection.close()


