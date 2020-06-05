# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 10:44
# file: common_utils.py
# IDE: PyCharm

import jwt
import datetime
from flask import jsonify, current_app
from webargs import ValidationError
from werkzeug.http import HTTP_STATUS_CODES
from seagull.models import Category


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')
    response = jsonify(code=code, message=message, **kwargs)
    response.status_code = code
    return response


def gen_token(user, operation, expire_in=None, **kwargs):
    """
    生成token函数
    :param operation: 操作类型
    :param expire_in: 超时时间
    :param user_id:
    :return:
    """
    if not expire_in:
        expire_in = current_app.config.get('AUTH_EXPIRE')
    data = {
        "user_id": user.id,
        "operation": operation,
        "exp": int(datetime.datetime.now().timestamp()) + expire_in  # 超时时间
    }
    data.update(**kwargs)
    token = jwt.encode(data, current_app.config.get("SECRET_KEY"), 'HS256').decode()

    return token


def validate_category_id(val):
    cid = Category.query.get(val)
    if not cid:
        raise ValidationError("分类不存在")
