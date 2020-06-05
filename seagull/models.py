# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 11:56
# file: models.py
# IDE: PyCharm

import datetime
from seagull.extensions import db
from flask_avatars import Identicon


class User(db.Model):
    """用户表"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(48), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))

    # posts = db.relationship('Post', back_populates='author')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_avatar()

    def generate_avatar(self):
        avatar = Identicon(cols=7, bg_color=(125, 125, 125))
        filenames = avatar.generate(text=self.username)
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


class Category(db.Model):
    """分类表"""
    __tablename__ = 'category'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True, comment="分类名称")
    posts = db.relationship('Post', back_populates='category')


class Post(db.Model):
    """文章表"""
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60), nullable=False, comment="文章标题")
    body = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment="更新时间")
    # 与分类表关联
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
    # 作者
    # author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # author = db.relationship('User', back_populates='posts')
