# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 14:06
# file: decorators.py
# IDE: PyCharm


import jwt, redis
from flask import request, current_app, g
from jwt import ExpiredSignatureError
from functools import wraps
from seagull.utils.common_utils import api_abort
from seagull.models import User
from seagull.extensions import redis_conn
from seagull.settings import Operations


# 判断元素是否在有序集合中
def zexist(name, value):
    index = redis_conn.zrank(name, value)
    # print(index)
    if index == 0 or index:
        return True
    return False


def auth_required(view):
    """登录保护装饰器"""

    @wraps(view)
    def wrapper(*args, **kwargs):
        token = request.headers.get('X-Token')

        # 没有token
        if not token:
            return api_abort(401, "token缺失")

        # 黑名单token
        if zexist("token_blacklist", token):
            return api_abort(401, "token非法")

        # 验证token
        try:
            data = jwt.decode(token, current_app.config.get("SECRET_KEY"), algorithms=['HS256'])
        except ExpiredSignatureError as e:
            current_app.logger.error("token超时: {}".format(e))
            return api_abort(401, "token超时")
        except Exception as e:
            current_app.logger.error("token非法: {}".format(e))
            return api_abort(401, "token非法")

        # 验证token类型为LOGIN
        if data.get('operation') != Operations.LOGIN:
            return api_abort(401, "token非法")

        # token验证通过，将当前用户挂载到g变量中
        try:
            user_id = data.get("user_id", -1)
            user = User.query.filter_by(id=user_id).one()
            g.user = user
            g.token = token
        except Exception as e:
            current_app.logger.error(e)
            return api_abort(401, "token非法")

        # 执行视图函数
        return view(*args, **kwargs)

    return wrapper
