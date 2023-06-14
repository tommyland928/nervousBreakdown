#!/usr/local/bin/python

import sys
import io
import cgi
import cgitb
import pymysql
import random
import string
import datetime
import os
import json

cgitb.enable()
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')


#冒頭のhtmlメッセージのみ送信
print("Content-Type: text/html")
print()


try:
    with connection.cursor() as cursor:
        sql = "select openCard,get from battles"
        cursor.execute(sql)
        result = cursor.fetchall()
        openCardJson = ""
        getJson = ""
        for i in result:
            openCardJson = i[0]
            getJson = i[1]
        openCard = json.loads(openCardJson)
        get = json.loads(getJson)
        print(openCard)
        print(get)
finally:
    connection.close()

