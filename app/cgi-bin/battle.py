#!/usr/local/bin/python

import sys
import io
import pymysql
import random
import string
import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')

#冒頭のhtmlメッセージのみ送信

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
            <img src = "/img/s/1.png">
            <img src = "/img/s/2.png">
            <img src = "/img/s/3.png">
            <img src = "/img/s/4.png">
            <img src = "/img/s/5.png">
            <img src = "/img/s/6.png">
            <img src = "/img/s/7.png">
            <img src = "/img/s/8.png">
            <img src = "/img/s/9.png">
            <img src = "/img/s/10.png">
            <img src = "/img/s/11.png">
            <img src = "/img/s/12.png">
            <img src = "/img/s/13.png">
            <img src = "/img/c/1.png">
            <img src = "/img/c/2.png">
            <img src = "/img/c/3.png">
            <img src = "/img/c/4.png">
            <img src = "/img/c/5.png">
            <img src = "/img/c/6.png">
            <img src = "/img/c/7.png">
            <img src = "/img/c/8.png">
            <img src = "/img/c/9.png">
            <img src = "/img/c/10.png">
            <img src = "/img/c/11.png">
            <img src = "/img/c/12.png">
            <img src = "/img/c/13.png">
            <img src = "/img/h/1.png">
            <img src = "/img/h/2.png">
            <img src = "/img/h/3.png">
            <img src = "/img/h/4.png">
            <img src = "/img/h/5.png">
            <img src = "/img/h/6.png">
            <img src = "/img/h/7.png">
            <img src = "/img/h/8.png">
            <img src = "/img/h/9.png">
            <img src = "/img/h/10.png">
            <img src = "/img/h/11.png">
            <img src = "/img/h/12.png">
            <img src = "/img/h/13.png">
            <img src = "/img/d/1.png">
            <img src = "/img/d/2.png">
            <img src = "/img/d/3.png">
            <img src = "/img/d/4.png">
            <img src = "/img/d/5.png">
            <img src = "/img/d/6.png">
            <img src = "/img/d/7.png">
            <img src = "/img/d/8.png">
            <img src = "/img/d/9.png">
            <img src = "/img/d/10.png">
            <img src = "/img/d/11.png">
            <img src = "/img/d/12.png">
            <img src = "/img/d/13.png">
            <img src = "/img/back.png">
            <img src = "/img/jorker.png">
        </div>
        <div id="winner"></div>

        <script src="/battle.js" defer></script>
        <script src="/ready.js" defer></script>
        <script src="/clickCard.js" defer></script>
        <script src="/movePhase.js" defer></script>
    </body>


</html>

"""
print(html)