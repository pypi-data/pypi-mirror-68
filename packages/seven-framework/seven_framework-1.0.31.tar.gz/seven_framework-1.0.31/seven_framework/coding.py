# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-05-11 21:46:17
@LastEditTime: 2020-05-11 21:49:20
@LastEditors: ChenXiaolei
@Description: 
"""

from urllib.parse import quote, unquote


class CodingHelper():
    @classmethod
    def url_encode(self, text, coding='utf-8'):
        return quote(text, 'utf-8')

    @classmethod
    def url_decode(self, text, coding='utf-8'):
        return unquote(text, 'utf-8')
