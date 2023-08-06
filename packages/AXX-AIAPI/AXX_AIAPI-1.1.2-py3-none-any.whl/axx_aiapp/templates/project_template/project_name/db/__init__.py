import os

import pymysql
from config import config


class MySQLTemplate:
    """
    简单封装了几个方法，其余方法可根据实际情况自行封装
    """

    @staticmethod
    def open(cursor):
        """
        创建-打开链接方法
        :param cursor:
        :return:
        """
        env = os.environ.get('AI_ENV', 'default')
        pool = config.get(env).POOL
        conn = pool.connection()
        cursor = conn.cursor(cursor=cursor)
        return conn, cursor

    @staticmethod
    def close(conn, cursor):
        """
        关闭链接方法
        :param conn:
        :param cursor:
        :return:
        """
        # conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def fetch_one(cls, sql, args=(), cursor=pymysql.cursors.DictCursor):
        """
        查询单个数据
        :param sql: SQL语句
        :param args: 对应参数
        :param cursor:
        :return:成功返回数据，失败返回false
        """

        conn, cursor = cls.open(cursor)
        try:
            cursor.execute(sql, args)
            obj = cursor.fetchone()
            return obj
        except Exception as e:
            return False
        finally:
            cls.close(conn, cursor)

    @classmethod
    def fetch_all(cls, sql, args=(), cursor=pymysql.cursors.DictCursor):
        """
        查询所有复合条件的
        :param sql: SQL语句
        :param args: 参数
        :param cursor:
        :return: 成功返回数据，失败返回false
        """
        conn, cursor = cls.open(cursor)
        try:
            cursor.execute(sql, args)
            obj = cursor.fetchall()
            return obj
        except Exception as e:
            return False
        finally:
            cls.close(conn, cursor)

    @classmethod
    def insert(cls, sql, args=(), cursor=pymysql.cursors.DictCursor):
        """
        插入数据
        :param sql:
        :param args:
        :param cursor:
        :return: 成功返回ID 失败返回false
        """
        conn, cursor = cls.open(cursor)
        try:
            conn.begin()
            cursor.execute(sql, args)
            _id = cursor.lastrowid
            conn.commit()
            return _id
        except Exception as e:
            conn.rollback()
            return False
        finally:
            cls.close(conn, cursor)

    @classmethod
    def delete(cls, sql, args=(), cursor=pymysql.cursors.DictCursor):
        """
        删除数据 ， 建议采用逻辑删除，即数据库字段标志位，而非物理闪出去
        :param sql:
        :param args:
        :param cursor:
        :return: 成功返回true 失败返回false
        """
        conn, cursor = cls.open(cursor)
        try:
            conn.begin()
            cursor.execute(sql, args)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            cls.close(conn, cursor)

    @classmethod
    def update(cls, sql, args=(), cursor=pymysql.cursors.DictCursor):
        """
        更新数据
        :param sql:
        :param args:
        :param cursor:
        :return: 成功返回true 失败返回false
        """
        conn, cursor = cls.open(cursor)
        try:
            conn.begin()
            cursor.execute(sql, args)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            cls.close(conn, cursor)
