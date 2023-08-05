# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-04-16 14:38:22
@LastEditTime: 2020-04-26 09:50:49
@LastEditors: ChenXiaolei
@Description: json 帮助类
"""
import json
import datetime


class JsonEncoder(json.JSONEncoder):
    """
    继承json.JSONEncoder
    
    使用方法:json.dumps(json_obj, ensure_ascii=False, cls=JsonEncoder)
    """
    def default(self, obj):  # pylint: disable=E0202
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, bytes):
            return ord(obj)
        else:
            return json.JSONEncoder.default(self, obj)