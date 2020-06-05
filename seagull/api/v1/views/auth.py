# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 10:40
# file: auth.py
# IDE: PyCharm

import bcrypt, datetime
from flask import request, current_app, jsonify, g
from seagull.api.v1 import api_v1
from seagull.utils.common_utils import api_abort, gen_token
from seagull.models import User
from seagull.settings import Operations
from seagull.decorators import auth_required
from seagull.extensions import redis_conn


# 登录视图
@api_v1.route('/user/login', methods=["POST"])
def login():
    payload = request.json

    try:
        email = payload["username"]
        password = payload["password"]
        user = User.query.filter_by(email=email).first()

        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return api_abort(401, "用户名或密码错误")

        # 验证通过，生成token
        token = gen_token(user, Operations.LOGIN)
        response = {
            'code': 20000,
            'user': {
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            },
            'token': token
        }
        current_app.logger.info("用户{}登录成功".format(user.username))
        return jsonify(response)
    except AttributeError as e:
        current_app.logger.error("{}".format(e))
        return api_abort(401, "用户名或密码错误")
    except Exception as e:
        current_app.logger.error("{}".format(e))
        return api_abort(401, "登录失败")


@api_v1.route('/user/logout', methods=['POST'])
@auth_required
def logout():
    # r = redis.Redis(connection_pool=POOL)
    # 用户注销，将token加入到黑名单中
    redis_conn.zadd("token_blacklist", {g.token: int(datetime.datetime.now().timestamp())})
    return '', 204
