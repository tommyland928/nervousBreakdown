import pymysql
import datetime


"""
データベースを操作するための関数をまとめる
"""

class OperateDb:
    
    def removeNoSessionUser(self):
        self.connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')
        self.cursor = self.connection.cursor()
        try:
            sql = "select name,lastuse from users"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            JST = datetime.timezone(datetime.timedelta(hours=+9),'JST')
            JSTnow = datetime.datetime.now(JST)
            nowStr = JSTnow.strftime("%Y-%m-%d %H:%M:%S")
            now = datetime.datetime.strptime(nowStr,"%Y-%m-%d %H:%M:%S")
            for i in result:
                deltaTime = now - i[1]
                if deltaTime.seconds > 15:
                    sql = f"delete from users where name='{i[0]}'"
                    self.cursor.execute(sql)
                    self.connection.commit()

        finally:
            self.connection.close()


    def renewSession(self,name,sessid):
        self.connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')
        self.cursor = self.connection.cursor()
        try:
            sql = "select name from users where name=%s and sessid=%s"
            if self.cursor.execute(sql,(name,sessid)) == 1:
                JST = datetime.timezone(datetime.timedelta(hours=+9),'JST')
                JSTnow = datetime.datetime.now(JST)
                nowStr = JSTnow.strftime("%Y-%m-%d %H:%M:%S")
                sql = f"update users set lastuse = %s where name = %s"
                self.cursor.execute(sql,(nowStr,name))
                self.connection.commit()


        finally:
            self.connection.close()
    

    def checkIfTwoPeople(self):
        self.connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')
        self.cursor = self.connection.cursor()
        try:
            sql = "select name from users where ready=1"
            if self.cursor.execute(sql) == 2:
                return False
            else:
                return True
                
        finally:
            self.connection.close()

    def removeBattle(self):
        self.connection = pymysql.connect(host='db',user='root',password='pwd',db='nur')
        self.cursor = self.connection.cursor()
        try:
            sql = "select name from users"
            if self.cursor.execute(sql) == 0:
                sql = "delete from battles"
                self.cursor.execute(sql)
                self.connection.commit()
                sql = "update rooms set phase=0"
                self.cursor.execute(sql)
                self.connection.commit()
        finally:
            self.connection.close()
