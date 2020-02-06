# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/2 16:15
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from CONST_base import *


"""
修改以下代码，尤其是要监控的群组
"""
WX_TARGET_GROUP_KEYS    = [                 # 辟谣所监控的消息群，直接输入关键字即可，一定要确保唯一，否则会报错
	"测试群",
	"XBRL",
	"机器人团队",
	"健康平安",
	"P.F.A",
	"统计建模",
]



SEND_GREETING           = False             # 是否在启动和关闭的时候群发祝福语
ENABLE_CHECK_DISEASE    = True              # 疫情数据开关
ENABLE_VERIFY_NEWS      = True              # 辟谣开关
WX_VERIFY_DEBUG         = True              # 是否打开辟谣的debug，打开之后将对每一条链接都返回消息结果
ENABLE_CHECK_TRANSPORT  = True              # TODO 出行人开关

WX_LOG_LEVEL            = logging.DEBUG     # 默认log会发送给自己的文件助手，这里可以设置log的等级


REGISTER_COMMANDS = [
	"command_check_disease",            # 【查】疫情
	"command_verify_shared_msg",        # 自动辟谣
	"command_enable_some_func",         # 【启动】功能
	"command_disable_some_func",        # 【关闭】功能
	"command_quit",                     # 【退出】
]


ABOUT_ME = """==这里是疫情查询帮助==
{}
为配合WX的机制，请不要过度使用本API哦，感谢！
"""


"""
以下是数据库存储部分，默认是MongoDB，多种数据库开启会优先使用程序预设的
"""

USE_MONGODB             = True
MONGO_HOST              = "localhost"
MONGO_PORT              = 27017
DB_NAME                 = "robot-for-wuhan"
COLL_NAME               = datetime.today().strftime("%Y-%m-%d")

USE_LOCAL               = True      # TODO 本地的消息缓存暂时未实现成功
MSG_HISTORY_DIR         = os.path.join(LOG_DIR, "history")
MSG_HISTORY_PATH        = os.path.join(MSG_HISTORY_DIR, "{}.log".format(COLL_NAME))