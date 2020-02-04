# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/2 16:15
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from CONST_base import *
import logging

"""
修改以下代码，尤其是要监控的群组
"""
SEND_GREETING           = True
ENABLE_VERIFY_NEWS      = True          # 辟谣开关
ENABLE_CHECK_TRANSPORT  = True          # TODO 出行人开关
ENABLE_CHECK_DISEASE    = True          # TODO 疫情数据开关

WX_LOG_LEVEL = logging.DEBUG            # 默认log会发送给自己的文件助手，这里可以设置log的等级
WX_VERIFY_DEBUG = True                  # 是否打开辟谣的debug，打开之后将对每一条链接都返回消息结果
WX_VERIFY_GROUP_KEYS = [                # 辟谣所监控的消息群，直接输入关键字即可，一定要确保唯一，否则会报错
	"测试群",
	"机器人团队",
	"最帅气",
	"健康平安",
	"P.F.A"
]

ABOUT_ME = """==这里是疫情查询帮助==
{}
为配合WX的机制，请不要过度使用本API哦，感谢！
"""