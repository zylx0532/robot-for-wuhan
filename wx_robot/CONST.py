# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 13:48
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from settings_base import *

"""
消息尾巴
"""
TEMPLATE_RANDOM_MSG_TAIL_LIST   =  [
	"-------------------\n",
]

"""
一些控制命令模板，业务模板请去 wx_servers.CONST 修改
"""

TEMPLATE_API_FAILED             = "哎呀，服务器好像出错了，IT小哥正在赶在路上啦，我去催催他/她/它快来救我！"
TEMPLATE_NO_KEYWORD             = "您要查啥呢？不如试试查一些城市的疫情数据？比如 『查武汉』=.="

TEMPLATE_ROBOT_QUIT             = "收到退出命令，正在下线，bye bye ~"


"""
微信配置
"""
# 该文件夹内的数据是您自己的用户数据，不会上传到Github，但需要确保文件夹存在
WX_ROBOT_DATA_DIR         = os.path.join(WX_ROBOT_DIR, "data")
if not os.path.exists(WX_ROBOT_DATA_DIR):
	os.mkdir(WX_ROBOT_DATA_DIR)

WX_COOKIE_PATH      = os.path.join(WX_ROBOT_DATA_DIR, "cookie.pkl")
WX_PUID_PATH        = os.path.join(WX_ROBOT_DATA_DIR, "puid.pkl")
WX_QR_PATH          = os.path.join(WX_ROBOT_DATA_DIR, "QR.png")

WX_COOKIE_TIMEOUT   = 30 * 60 * 60    # 微信Cookie文件的过期时间，设置成30小时
WX_MSG_VERIFY_TIMEOUT = 60            # 微信辟谣的时间延迟，超过一分钟就不辟谣了
