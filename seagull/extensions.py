# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 10:19
# file: extensions.py
# IDE: PyCharm

import redis
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from seagull.settings import BaseConfig

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

# redis连接
redis_conn = redis.Redis(connection_pool=BaseConfig.POOL)
