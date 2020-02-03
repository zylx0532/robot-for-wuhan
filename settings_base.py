# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/2 16:15
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

import os
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

import logging

ENABLE_VERIFY_NEWS = True
ENABLE_CHECK_TRANSPORT = False
ENABLE_CHECK_DISEASE = False

WX_DEFAULT_FILE_HELPER = True         # 所有消息默认抄一份给自己的文件传输助手
WX_VERIFY_GROUP_KEYS = ["测试群", "开发组", "机器人组"]       # 辟谣所监控的消息群，直接输入关键字即可，一定要确保唯一，否则会报错
WX_LOG_LEVEL = logging.DEBUG
WX_VERIFY_DEBUG = True