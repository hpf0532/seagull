# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 16:44
# file: post.py
# IDE: PyCharm

from sqlalchemy import text
from flask import jsonify, current_app, url_for, request
from flask.views import MethodView
from webargs.flaskparser import use_args, use_kwargs
from seagull.api.v1 import api_v1
from seagull.extensions import db
from seagull.decorators import auth_required
from seagull.schema import category_schema, categorys_schema, post_schema, posts_schema, PostSchema
from seagull.models import Category, Post
from seagull.utils.common_utils import api_abort


class CategoryAPI(MethodView):
    decorators = [auth_required]

    def get(self, category_id):
        """获取单条分类信息"""
        category = Category.query.get_or_404(category_id)
        return jsonify(category_schema.dump(category))

    @use_kwargs(category_schema, location="json")
    def put(self, category_id, name):
        """编辑分类"""
        category = Category.query.get_or_404(category_id)
        category.name = name
        try:
            db.session.add(category)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return api_abort(400, "数据保存失败")
        return jsonify(category_schema.dump(category))


class CategorysAPI(MethodView):
    decorators = [auth_required]

    def get(self):
        """获取所有分类接口"""
        categorys = Category.query.all()
        return jsonify({
            "items": categorys_schema.dump(categorys),
            "self": url_for('api_v1.categorys', _external=True),
            "count": len(categorys)
        })

    @use_args(category_schema, location="json")
    def post(self, args):
        """
        创建新分类
        :param args:
        :return:
        """
        category = Category(name=args['name'])
        try:
            db.session.add(category)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return api_abort(400, "数据保存失败")
        response = jsonify(category_schema.dump(category))
        response.status_code = 201
        return response


class PostAPI(MethodView):
    # decorators = [auth_required]

    def get(self, post_id):
        """
        文章详细接口
        :param post_id: 文章
        :return:
        """
        doc = Post.query.get_or_404(post_id)
        return jsonify(post_schema.dump(doc))

    @use_args(PostSchema(), location="json")
    def put(self, args, post_id):
        """
        编辑文章接口
        :param args: 请求数据
        :param post_id: 文章ID
        :return:
        """
        doc = Post.query.get_or_404(post_id)

        doc.title = args["title"]
        doc.category_id = args["category_id"]
        doc.body = args["body"]

        try:
            db.session.add(doc)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            return api_abort(400, "数据保存失败")
        return jsonify(post_schema.dump(doc))

    def delete(self, post_id):
        """删除文章接口"""
        doc = Post.query.get_or_404(post_id)
        db.session.delete(doc)
        db.session.commit()
        return '', 204


class PostsAPI(MethodView):
    # decorators = [auth_required]

    def get(self):
        """
        分页获取文章列表
        :return:
        """
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', type=int)
        category_id = request.args.get('category_id', type=int)
        title = request.args.get('title')

        per_page = limit or current_app.config['BACK_ITEM_PER_PAGE']
        pagination = Post.query.filter(
            # 查询搜索条件
            Post.category_id == category_id if category_id else text(''),
            Post.title.like("%" + title + "%") if title else text(''),
        ).order_by(text('-update_time')).paginate(page, per_page)
        items = pagination.items
        current = url_for('.posts', page=page, _external=True)
        prev = None
        if pagination.has_prev:
            prev = url_for('.posts', page=page - 1, _external=True)
        next = None
        if pagination.has_next:
            next = url_for('.posts', page=page + 1, _external=True)
        return jsonify(
            {
                "items": posts_schema.dump(items),
                "prev": prev,
                "first": url_for('api_v1.posts', page=1, _external=True),
                "last": url_for('api_v1.posts', page=pagination.pages, _external=True),
                "next": next,
                "count": pagination.total
            }
        )

    @use_args(post_schema, location="json")
    def post(self, args):
        """
        新建文章
        :param args:
        :return:
        """

        doc = Post()
        doc.title = args["title"]
        doc.category_id = args["category_id"]
        doc.body = args["body"]
        doc.published = True
        try:
            db.session.add(doc)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            return api_abort(400, "数据保存失败")
        response = jsonify(post_schema.dump(doc))
        response.status_code = 201
        return response


# 路由规则
api_v1.add_url_rule('/category/<int:category_id>', view_func=CategoryAPI.as_view('category'),
                    methods=['GET', 'PUT', 'DELETE'])
api_v1.add_url_rule('/categorys', view_func=CategorysAPI.as_view('categorys'), methods=['GET', 'POST'])
api_v1.add_url_rule('/post/<int:post_id>', view_func=PostAPI.as_view('post'), methods=['GET', 'PUT', 'DELETE'])
api_v1.add_url_rule('/posts', view_func=PostsAPI.as_view('posts'), methods=['GET', 'POST'])
