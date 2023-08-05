# -*- coding: utf-8 -*-
"""
@Author: ChenXiaolei
@Date: 2020-05-09 20:39:20
@LastEditTime: 2020-05-09 20:41:19
@LastEditors: ChenXiaolei
@Description: 基础控制台类
"""

from seven_framework import *
import sys
global production
production = "--production" in sys.argv
sys.path.append(".local")  # 不可删除,置于其他import前
# 初始化配置,执行顺序需先于调用模块导入
config.init_config(
    "config{0}.json".format("" if production else "_dev"))  # 全局配置,只需要配置一次

logger_error = Logger.get_logger_by_name("log_error")
logger_info = Logger.get_logger_by_name("log_info")
