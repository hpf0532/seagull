# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 10:37
# file: __init__.py.py
# IDE: PyCharm


from flask import Blueprint
from flask_cors import CORS

api_v1 = Blueprint('api_v1', __name__)

CORS(api_v1)

from seagull.api.v1 import views
from seagull.api.v1 import errors
