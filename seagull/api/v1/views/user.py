# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 20:35
# file: user.py
# IDE: PyCharm

from flask import g, jsonify, url_for, send_from_directory, current_app
from seagull.api.v1 import api_v1
from seagull.decorators import auth_required


@api_v1.route('/user/info', methods=['GET'])
@auth_required
def userinfo():
    print(212)
    return jsonify({
        "id": g.user.id,
        "name": g.user.username,
        "avatar": url_for("api_v1.get_avatar", filename=g.user.avatar_s, _external=True)
    })


@api_v1.route('/avatars/<path:filename>', methods=['GET'])
def get_avatar(filename):
    """用户头像"""
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)
