# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 10:21
# file: settings.py
# IDE: PyCharm

import os
import redis
import secrets
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


# token操作类型
class Operations:
    LOGIN = 'login'
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    BACK_LOCALES = ['en_US', 'zh_Hans_CN']
    BACK_ITEM_PER_PAGE = 10
    UPLOAD_PATH = os.path.join(basedir, 'uploads')
    secret = secrets.token_urlsafe(nbytes=15)
    '''
    # 旧版本
    import random
    import string
    ''.join(random.choices(string.ascii_letters + string.digits, k=15))
    # py3.6+
    import secrets
    secrets.token_urlsafe(nbytes=15)
    '''
    SECRET_KEY = os.getenv('SECRET_KEY', secret)
    AUTH_EXPIRE = 60 * 60 * 8

    AVATARS_IDENTICON_ROWS = 7
    AVATARS_SAVE_PATH = os.path.join(UPLOAD_PATH, 'avatars')
    AVATARS_SIZE_TUPLE = (30, 100, 200)

    REDIS_ADDR = os.getenv('REDIS_ADDR')
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_PD = os.getenv('REDIS_PD')
    REDIS_DB = 2

    # redis连接池
    POOL = redis.ConnectionPool(host=REDIS_ADDR, port=REDIS_PORT, password=REDIS_PD, db=REDIS_DB)


class MySQLConfig:
    MYSQL_USERNAME = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DATABASE = 'seagull'
    MYSQL_CHARSET = 'utf8mb4'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MySQLConfig.MYSQL_USERNAME}:{MySQLConfig.MYSQL_PASSWORD}' \
        f'@{MySQLConfig.MYSQL_HOST}/{MySQLConfig.MYSQL_DATABASE}?charset={MySQLConfig.MYSQL_CHARSET}'


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MySQLConfig.MYSQL_USERNAME}:{MySQLConfig.MYSQL_PASSWORD}' \
        f'@{MySQLConfig.MYSQL_HOST}/{MySQLConfig.MYSQL_DATABASE}?charset={MySQLConfig.MYSQL_CHARSET}'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MySQLConfig.MYSQL_USERNAME}:{MySQLConfig.MYSQL_PASSWORD}' \
        f'@{MySQLConfig.MYSQL_HOST}/{MySQLConfig.MYSQL_DATABASE}?charset={MySQLConfig.MYSQL_CHARSET}'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
