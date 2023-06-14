#!/usr/local/bin/python

import cgi
import sys
import io
import cgitb
import pymysql
import time
import json

import os



cgitb.enable()
connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')
###クッキー情報を辞書型に変換 cookieDic###
cookieString = os.environ['HTTP_COOKIE']
cookiesStringList = cookieString.split(';')
cookieDic = {}
for i in cookiesStringList:
    tmp = i.split('=')
    cookieDic[tmp[0].replace(' ','')] = tmp[1] 
########################################

html_body = """Content-Type: text/html

{
    "ok":"ok"
}
"""
print(html_body)


try:
    with connection.cursor() as cursor:
        list1 = [[1,2]]
        list1Json = json.dumps(list1)
        sql = f"UPDATE battles set openCard='{list1Json}'"
        cursor.execute(sql)
        connection.commit()
finally:
    connection.close()


