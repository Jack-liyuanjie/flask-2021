import hashlib

import pymysql
from pymysql.cursors import DictCursor

CONFIG = {
    'host': '116.62.193.152',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'db': 'User',
    'charset': 'utf8',
    'cursorclass': DictCursor
}


class DB():
    def __init__(self):
        self.conn = pymysql.Connect(**CONFIG)

    def __enter__(self):
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None


class BaseDao():
    def __init__(self):
        self.db = DB()

    def query(self, sql, args=None):
        # 支持原生的sql语句查询
        with self.db as c:
            c.execute(sql, args)
            result = c.fetchall()
        return result

    # 查找功能
    def find_all(self, table, where=None, *whereArgs):
        sql = "select *from %s" % table
        if where:
            sql += where

        with self.db as c:
            c.execute(sql, whereArgs)
            result = list(c.fetchall())
        return result

    # 添加功能
    def save(self, table, **data):
        sql = "insert into %s(%s) value(%s)"
        colnames = ','.join([key for key in data])
        colplaceholdes = ','.join(['%%(%s)s' % key for key in data])
        with self.db as c:
            c.execute(sql % (table, colnames, colplaceholdes), data)
            if c.rowcount > 0:
                return True

        return False

    # 更新功能
    def update(self, table, id, **data):
        # 要求：每一个表都有主键id
        sql = "update %s set %s where id=%s"
        update_cols = ','.join(["%s=%%(%s)s" % (key, key) for key in data])
        with self.db as c:
            c.execute(sql % (table, update_cols, id), data)
            if c.rowcount > 0:
                return True

        return False

# if __name__ == '__main__':
#     dao = BaseDao()
#     # 如果密码时哈希码的话需要转码操作
#     # psd = hashlib.md5('123456'.encode('utf-8').hex())
#     result = dao.find_all('user',' where name=%s and password=%s', '李元杰', '123456')
#     print(result)
