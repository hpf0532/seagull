# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 22:44
# file: wsgi.py
# IDE: PyCharm

from seagull import create_app

# from backend.extensions import celery_ext

app = create_app('production')
