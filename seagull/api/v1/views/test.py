# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 10:47
# file: test.py
# IDE: PyCharm

from seagull.api.v1 import api_v1


@api_v1.route("/test", methods=["GET"])
def hello():
    return {"status": 200}
