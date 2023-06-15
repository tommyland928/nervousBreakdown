#!/usr/local/bin/python

import sys
import io
import cgi
import pymysql
import random
import string

connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
print("Content-Type: text/html")
print()

try:
    with connection.cursor() as cursor:
        sql = "delete from battles"
        sql1 = "delete from dias"
        sql2 = "delete from hearts"
        sql3 = "delete from clovers"
        sql4 = "delete from spades"
        sql5 = "update rooms set phase=0"
        sql6 = "update users set ready=0"
        
        cursor.execute(sql)
        connection.commit()
        cursor.execute(sql1)
        connection.commit()
        cursor.execute(sql2)
        connection.commit()
        cursor.execute(sql3)
        connection.commit()
        cursor.execute(sql4)
        connection.commit()
        cursor.execute(sql5)
        connection.commit()
        cursor.execute(sql6)
        connection.commit()

finally:
    connection.close()

