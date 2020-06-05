# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 10:41
# file: errors.py
# IDE: PyCharm

from flask import jsonify
from seagull.api.v1 import api_v1


# 定义webargs错误处理函数
@api_v1.errorhandler(422)
def handle_error(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid request."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code


@api_v1.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": e.description}), 429


class SqlOperationError(ValueError):
    pass
