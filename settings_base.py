# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/2 16:15
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

import os
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

import logging

"""
修改以下代码，尤其是要监控的群组
"""
ENABLE_VERIFY_NEWS = True              # 辟谣开关
ENABLE_CHECK_TRANSPORT = False         # TODO 出行人开关
ENABLE_CHECK_DISEASE = False           # TODO 疫情数据开关

WX_LOG_LEVEL = logging.DEBUG            # 默认log会发送给自己的文件助手，这里可以设置log的等级
WX_VERIFY_DEBUG = True                  # 是否打开辟谣的debug，打开之后将对每一条链接都返回消息结果
WX_DEFAULT_FILE_HELPER = True           # TODO 该控制开关还没实现，目前是默认的，所有消息默认抄一份给自己的文件传输助手
WX_VERIFY_GROUP_KEYS = [                # 辟谣所监控的消息群，直接输入关键字即可，一定要确保唯一，否则会报错
	"测试群",
	"开发组",
	"机器人组"
]
