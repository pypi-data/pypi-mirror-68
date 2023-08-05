from logging.config import dictConfig
import os

import pymysql
from DBUtils.PooledDB import PooledDB


def config_log():
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            "gunicorn.error": {
                "level": "INFO",
                "handlers": ["error_file"],
                "propagate": 1,
                "qualname": "gunicorn.error"
            },
            "gunicorn.access": {
                "level": "INFO",
                "handlers": ["access_file"],
                "propagate": 0,
                "qualname": "gunicorn.access"
            }
        },
        'handlers': {
            "error_file": {
                "class": 'concurrent_log.ConcurrentTimedRotatingFileHandler',
                'backupCount': 14,
                'when': 'midnight',
                'delay': False,
                "formatter": "generic",
                "filename": os.path.join(os.path.dirname(__file__), '../logs/gunicorn.log')
            },
            "access_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "maxBytes": 1024 * 1024 * 1024,
                "backupCount": 1,
                "formatter": "generic",
                "filename": os.path.join(os.path.dirname(__file__), '../logs/gunicorn.access.log'),
            }
        },
        'formatters': {
            "generic": {
                "format": "[process=%(process)d] [timestamp=%(asctime)s] [tx_id=] [level=%(levelname)s] "
                          " [bu_id=JT_AILab] [app_id=AI_Folder Recommendation]  %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S]",
                "class": "logging.Formatter"
            },
            "access": {
                "format": "'[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'",
                "class": "logging.Formatter"
            }
        }
    })


class G:
    pass


class BaseConfig:
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]axx/'
    DEBUG = False
    TESTING = False
    __POOL = None

    @classmethod
    def pool(cls, *, db_host, db_port=3306, db_user, db_pwd, db_database):
        if cls.__POOL is None:
            cls.__POOL = PooledDB(
                creator=pymysql,  # 使用链接数据库的模块
                maxconnections=50,  # 连接池允许的最大连接数，0和None表示不限制连接数
                mincached=10,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
                maxcached=10,  # 链接池中最多闲置的链接，0和None不限制
                maxshared=5,
                blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
                maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
                setsession=[],  # 开始会话前执行的命令列表。
                ping=4,
                host=db_host,
                port=db_port,
                user=db_user,
                password=db_pwd,
                database=db_database,
                charset='utf8'
            )
        return cls.__POOL


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    __db_host = '127.0.0.1'
    __db_port = 3306
    __db_user = 'root'
    __db_pwd = 'danzhenyu'
    __db_database = 'test'
    POOL = BaseConfig.pool(db_host=__db_host, db_port=__db_port, db_user=__db_user, db_pwd=__db_pwd,
                           db_database=__db_database)


class TestingConfig(DevelopmentConfig):
    pass


class ProductionConfig(BaseConfig):
    __db_host = '127.0.0.1'
    __db_port = 3306
    __db_user = 'root'
    __db_pwd = 'danzhenyu'
    __db_database = 'test'
    POOL = BaseConfig.pool(db_host=__db_host, db_port=__db_port, db_user=__db_user, db_pwd=__db_pwd,
                           db_database=__db_database)


config = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prd': ProductionConfig,
    'default': DevelopmentConfig
}
