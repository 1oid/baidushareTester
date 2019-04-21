import pymysql


class BaiduShareDb(object):

    def __init__(self, db_server, db_user, db_pwd, db_select):
        self.db_server = db_server
        self.db_user = db_user
        self.db_pwd = db_pwd
        self.db_select = db_select
        self.conn = self.connect()

    def connect(self):
        return pymysql.connect(self.db_server, self.db_user, self.db_pwd, self.db_select)

    def insert(self, appkey, times=10):
        cursor = self.conn.cursor()
        print("[+] Insert appkey({}) times({}) into {}".format(appkey, times, self.db_select))
        sql = "insert into appkeys(appkey, count) values ('{}', {})".format(appkey, times)
        cursor.execute(sql)
        self.conn.commit()

    def fetchone_id_not_zero(self):
        cursor = self.conn.cursor()
        # 查询不为 0
        cursor.execute("select id from appkeys where count > 0 order by count desc")

        rs = cursor.fetchone()
        if rs:
            appkey_id = rs[0]
            cursor.execute("update appkeys set count=count-1 where id={}".format(appkey_id))
            self.conn.commit()
            return appkey_id
        return None

    def fetch_appkey(self):
        cursor = self.conn.cursor()
        appkey_id = self.fetchone_id_not_zero()

        if appkey_id:
            cursor.execute("select appkey from appkeys where id={}".format(appkey_id))

            rs = cursor.fetchone()
            if rs:
                return rs[0]
            return None
        return None
