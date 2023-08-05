# -*- coding: utf-8 -*-
"""
    :author: jiegemena
    :url: http://jieguone.top
    :copyright: © jieguone.top
    :license: none
"""
import sqlite3


class db_sqlite3:

    # SQL_CONN = 'appdata/web.db'
    def __init__(self, sql_conn_str):
        print('''conn database''')
        self.conn = sqlite3.connect(sql_conn_str)
        self.cursor = None
        self.total_changes = 0
        self.dowork = False

    # 开启事务
    def setDoWork(self):
        print('db_sqlite3.setDoWork')
        self.dowork = True

    def commitWork(self):
        print('db_sqlite3.commitWork')
        self.conn.commit()

    def backWork(self):
        print('db_sqlite3.backWork')
        self.conn.rollback()

    def __del__(self):
        self.close()

    def exec(self, sql_str, sql_par=()):
        print(sql_str)
        print(sql_par )
        try:
            self.get_db().execute(sql_str, sql_par)
            if self.dowork is False:
                print('exec.commit')
                self.conn.commit()
                # 返回影响数
                changes = self.conn.total_changes
                cha = changes - self.total_changes
                self.total_changes = changes
                return cha
            else:
                return 1
        except Exception as e:
            if self.dowork is False:
                self.conn.rollback()
            print('db_sqlite3.exec:', e)
            raise e

    def query(self, sql_str, sql_par=()):
        print(sql_str)
        print(sql_par)
        return self.get_db().execute(sql_str, sql_par)

    def query_all(self, sql_str, sql_par=()):
        cur = self.query(sql_str=sql_str, sql_par=sql_par)
        que = cur.fetchall()
        cols = cur.description
        tmp = []
        for v in que:
            row = {}
            for v2 in range(0, len(cols)):
                row[cols[v2][0]] = v[v2]
            tmp.append(row)
        return tmp

    def query_one(self, sql_str, sql_par=()):
        cur = self.query(sql_str=sql_str, sql_par=sql_par)
        que = cur.fetchone()
        if que is None:
            return None
        cols = cur.description
        row = {}
        for v2 in range(0, len(cols)):
            row[cols[v2][0]] = que[v2]
        return row

    def get_db(self):
        if self.cursor is None:
            self.cursor = self.conn.cursor()
        return self.cursor

    def close(self):
        self.cursor = None
        self.conn.close()
        print('''close database''')

    def add(self, obj, tableName):
            sql = "INSERT INTO `"+ tableName +"` "
            par = []
            bval = '('
            eval = '('
            for key in obj:
                bval = bval + str(key) + ','
                eval = eval + '?,'
                par.append(obj[key])

            bval = bval[0:-1] + ')'
            eval = eval[0:-1] + ') '
            sql = sql + bval + ' VALUES ' + eval
            bak = self.exec(sql_str=sql, sql_par=par)
            return bak

    def delById(self, id,tableName):
        if id <= 0:
            raise Exception("id < 0")
        sql = 'DELETE FROM `' + tableName + '` WHERE id = ?'
        par = [id]

        bak = self.exec(sql_str=sql, sql_par=par)
        return bak

    def findById(self, id,tableName):
        if id <= 0:
            raise Exception("id < 0")
        sql = 'SELECT * FROM `' + tableName + '` where id = ?'
        par = [id]

        bak = self.query(sql_str=sql, sql_par=par).fetchone()
        return bak
