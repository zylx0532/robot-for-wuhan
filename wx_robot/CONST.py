# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 13:48
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from settings_base import *


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
