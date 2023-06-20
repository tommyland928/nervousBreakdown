#!/usr/local/bin/python

import sys
import io
import pymysql
import os 

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')

"""
バトルの最初の画面
キャッシュさせるためにこの時点ですべての画像を読み込ませる
"""

###


#クッキーを見てusersに乗っていない場合にはindex.pyに遷移

###
#cookieを確認,cookieDic["名前"]で値を参照
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

html = """Content-Type: text/html

<html>
    <head>
    	<meta charset='UTF-8'>
        <link rel="stylesheet" href="/battle.css">
    </head>
    <body>
        <div id="table">
            <div id="first">
                <img src = "/img/reverse.png" id="i00">
                <img src = "/img/reverse.png" id="i01">
                <img src = "/img/reverse.png" id="i02">
                <img src = "/img/reverse.png" id="i03">
                <img src = "/img/reverse.png" id="i04">
                <img src = "/img/reverse.png" id="i05">
            </div>
            <div id="second">
                <img src = "/img/reverse.png" id="i10">
                <img src = "/img/reverse.png" id="i11">
                <img src = "/img/reverse.png" id="i12">
                <img src = "/img/reverse.png" id="i13">
                <img src = "/img/reverse.png" id="i14">
                <img src = "/img/reverse.png" id="i15">
            </div>
            <div id="third">
                <img src = "/img/reverse.png" id="i20">
                <img src = "/img/reverse.png" id="i21">
                <img src = "/img/reverse.png" id="i22">
                <img src = "/img/reverse.png" id="i23">
                <img src = "/img/reverse.png" id="i24">
                <img src = "/img/reverse.png" id="i25">
            </div>
            <div id="forth">
                <img src = "/img/reverse.png" id="i30">
                <img src = "/img/reverse.png" id="i31">
                <img src = "/img/reverse.png" id="i32">
                <img src = "/img/reverse.png" id="i33">
                <img src = "/img/reverse.png" id="i34">
                <img src = "/img/reverse.png" id="i35">
            </div>
            <div id="score"></div>
            
        </div>
        <div id="ready">
            <form class="readyFetch">
                <input type="button" value="Ready" class="readyBtn" id="clicked">      
            </form>
        </div>
        <div hidden>
            <img src = "/reverseImg/s/1.png">
            <img src = "/reverseImg/s/2.png">
            <img src = "/reverseImg/s/3.png">
            <img src = "/reverseImg/s/4.png">
            <img src = "/reverseImg/s/5.png">
            <img src = "/reverseImg/s/6.png">
            <img src = "/reverseImg/s/7.png">
            <img src = "/reverseImg/s/8.png">
            <img src = "/reverseImg/s/9.png">
            <img src = "/reverseImg/s/10.png">
            <img src = "/reverseImg/s/11.png">
            <img src = "/reverseImg/s/12.png">
            <img src = "/reverseImg/s/13.png">
            <img src = "/reverseImg/c/1.png">
            <img src = "/reverseImg/c/2.png">
            <img src = "/reverseImg/c/3.png">
            <img src = "/reverseImg/c/4.png">
            <img src = "/reverseImg/c/5.png">
            <img src = "/reverseImg/c/6.png">
            <img src = "/reverseImg/c/7.png">
            <img src = "/reverseImg/c/8.png">
            <img src = "/reverseImg/c/9.png">
            <img src = "/reverseImg/c/10.png">
            <img src = "/reverseImg/c/11.png">
            <img src = "/reverseImg/c/12.png">
            <img src = "/reverseImg/c/13.png">
            <img src = "/reverseImg/h/1.png">
            <img src = "/reverseImg/h/2.png">
            <img src = "/reverseImg/h/3.png">
            <img src = "/reverseImg/h/4.png">
            <img src = "/reverseImg/h/5.png">
            <img src = "/reverseImg/h/6.png">
            <img src = "/reverseImg/h/7.png">
            <img src = "/reverseImg/h/8.png">
            <img src = "/reverseImg/h/9.png">
            <img src = "/reverseImg/h/10.png">
            <img src = "/reverseImg/h/11.png">
            <img src = "/reverseImg/h/12.png">
            <img src = "/reverseImg/h/13.png">
            <img src = "/reverseImg/d/1.png">
            <img src = "/reverseImg/d/2.png">
            <img src = "/reverseImg/d/3.png">
            <img src = "/reverseImg/d/4.png">
            <img src = "/reverseImg/d/5.png">
            <img src = "/reverseImg/d/6.png">
            <img src = "/reverseImg/d/7.png">
            <img src = "/reverseImg/d/8.png">
            <img src = "/reverseImg/d/9.png">
            <img src = "/reverseImg/d/10.png">
            <img src = "/reverseImg/d/11.png">
            <img src = "/reverseImg/d/12.png">
            <img src = "/reverseImg/d/13.png">
            <img src = "/reverseImg/back.png">
            <img src = "/reverseImg/jorker.png">
            <img src = "/reverseImg/reverse.png">
        </div>
        <div id="winner"></div>


        <script src="/battle.js" defer></script>
        <script src="/ready.js" defer></script>
        <script src="/clickCard.js" defer></script>
        <script src="/movePhase.js" defer></script>

    </body>
</html>

"""


try:
    with connection.cursor() as cursor:
        sql = "select name,sessid from users"
        cursor.execute(sql)
        result = cursor.fetchall()
        names = []
        sessids = []
        for i in result:
            if cookieDic["name"] == i[0] and cookieDic["sessid"] == i[1]:
                #クッキーがあるから表示させる
                print(html)
                break
        else:
            html = """Content-Type: text/html

            <html>
                <head>
                    <meta charset='UTF-8'>
                    <script>
                        window.location.href = "/cgi-bin/index.py"
                    </script>
                </head>
                <body>
                </body>
            </html>
            """
            print(html)
finally:
    connection.close()