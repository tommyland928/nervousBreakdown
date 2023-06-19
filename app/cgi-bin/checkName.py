#!/usr/local/bin/python

import sys
import io
import cgi
import pymysql
import random
import string
import datetime
import urllib.parse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#払いだすクッキーを決定。名前一致が無ければ実際に払い出される
sendCookie = ''
number_of_strings = 5
length_of_string = 16
for x in range(number_of_strings):
  sendCookie = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))

#POTSされた値を格納
form = cgi.FieldStorage()
formNameBeforeEncoding = form.getvalue('name')
formName = urllib.parse.quote(formNameBeforeEncoding)

connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')

#冒頭のhtmlメッセージのみ送信
print("Content-Type: text/html")
print()

try:
  with connection.cursor() as cursor:
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
    
    if phase != 0 and phase !=2:
      #試合中につき入室禁止
      html = """<body>
        battle has started already
      </body>
      """
      print(html)
    else:#試合前
      for i in users:#既に存在していないか
        if i == formName:#一致していた時
          html = """<html>
            <head>
              <meta charset="utf-8">
            </html>
            <body>
              exist
            </body>
          </html>
          """
          print(html)
          break
      else:#一致が無かったとき
        #データベースに登録
        JST = datetime.timezone(datetime.timedelta(hours=+9),'JST')
        JSTnow = datetime.datetime.now(JST)
        now = JSTnow.strftime("%Y-%m-%d %H:%M:%S")
        sql = f"insert into users (name,sessid,ready,lastuse) values (%s,'{sendCookie}',0,'{now}')"
        cursor.execute(sql,formName)
        connection.commit()
    
        #SSIDを払い出し
        html = f"""<html>
          <head>
            <meta charset="utf-8">
            <script>
              document.cookie = 'name={formName}; path=/;'
              document.cookie = 'sessid={sendCookie}; path=/;'
              window.location.href = '/cgi-bin/battle.py';
            </script>
          </head>
          <body>
            登録完了
          </body>
        </html>
        """
        print(html)


finally:
  connection.close()



    
