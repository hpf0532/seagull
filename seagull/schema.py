# -*- coding:utf-8 -*-
# author: hpf
# create time: 2020/6/5 16:24
# file: schema.py
# IDE: PyCharm

from marshmallow import fields
from seagull.extensions import ma
from seagull.utils.common_utils import validate_category_id


class CategorySchema(ma.Schema):
    name = fields.Str(validate=lambda p: len(p) > 0 and p != 'Default', required=True, error_messages=dict(
        required="分类名称为必填项", validator_failed="分类名不合法", invalid="请输入字符串"
    ))

    class Meta:
        fields = ("id", "name")


class PostSchema(ma.Schema):
    title = fields.Str(validate=lambda p: len(p) > 0, required=True, error_messages=dict(
        required="标题为必填项", validator_failed="标题不能为空", invalid="请输入字符串"
    ))
    body = fields.Str(validate=lambda p: len(p) > 0, required=True, error_messages=dict(
        required="正文必填项", validator_failed="内容不能为空", invalid="请输入字符串"
    ))
    category_id = fields.Int(required=True, validate=validate_category_id, load_only=True)
    create_time = fields.Function(lambda obj: int(obj.create_time.timestamp()))
    update_time = fields.Function(lambda obj: int(obj.update_time.timestamp()))
    category = fields.Function(lambda obj: obj.category.name, dump_only=True)

    class Meta:
        fields = ("id", "title", "body", "create_time", "update_time", "category_id", "category")


category_schema = CategorySchema()
categorys_schema = CategorySchema(many=True)

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
