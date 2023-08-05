import os

import pymysql
from config import config


class MySQLTemplate:

    @staticmethod
    def open(cursor):
        env = os.environ.get('AI_ENV', 'default')
        pool = config.get(env).POOL
        conn = pool.connection()
        cursor = conn.cursor(cursor=cursor)
        return conn, cursor

    @staticmethod
    def close(conn, cursor):
        # conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def fetch_one(cls, sql, args=(), cursor=pymysql.cursors.DictCursor):
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
