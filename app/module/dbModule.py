# file name : dbModule.py
# pwd : /testMariaDB/app/module/dbModule.py

import pymysql


class Database():
    def __init__(self):
        self.db = pymysql.connect(host='',
                                  port=,
                                  user='',
                                  password='',
                                  db='',
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def executeOne(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def executeAll(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def executeSp(self, pname, args={}):
        result_args = self.cursor.callproc(pname, args)
        # print(result_args[0] + ' ' + result_args[1])
        # self.cursor.execute('SELECT @_sp_upsert_monitoring_info_0, @_sp_upsert_monitoring_info_1, '
        #                     '@_sp_upsert_monitoring_info_2')
        row = self.cursor.fetchall()
        return row

    def commit(self):
        self.db.commit()