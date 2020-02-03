# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/3 20:43
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from advanced.CONST import *
from servers.verify_news import verify_news

import os
import time
from datetime import datetime

from wxpy import Message, SHARING

"""
微信配置
"""
WX_COOKIE_PATH      = os.path.join(WX_PATH, "cookie.pkl")
WX_PUID_PATH        = os.path.join(WX_PATH, "puid.pkl")
WX_QR_PATH          = os.path.join(WX_PATH, "QR.png")

WX_COOKIE_TIMEOUT   = 30 * 60 * 60    # 微信Cookie文件的过期时间，设置成30小时
WX_MSG_VERIFY_TIMEOUT = 60            # 微信辟谣的时间延迟，超过一分钟就不辟谣了


def clear_cookie() -> None:
	"""
	# 该函数主要为删除过期的微信Cookie文件，以保证微信Cookie的有效性
	# [python获取文件修改时间与创建时间_u014717398的博客-CSDN博客](https://blog.csdn.net/u014717398/article/details/72627125 )
	:return:
	"""
	if os.path.exists(WX_COOKIE_PATH):
		if os.stat(WX_COOKIE_PATH).st_mtime < time.time() - WX_COOKIE_TIMEOUT:
			os.remove(WX_COOKIE_PATH)

def real_sender(msg: Message):
	return msg.member if msg.member else msg.sender

def pre_verify_news(msg: Message):
	msg_dict = {
		"id": msg.id,
		"sender": real_sender(msg).name,
		"text": msg.text,
	}
	if (datetime.now() - msg.create_time).seconds > WX_MSG_VERIFY_TIMEOUT:
		msg_dict.update({
			"code": -1,
			"reason": "超过预设时间，本AI不打算给你辟谣了！"
		})

	# 竟然不支持isinstance(msg, SHARING)
	elif msg.type == "Sharing":
		msg_dict.update({
			"code": 0,
			"reason": "SUCCESS ~"
		})
	else:
		msg_dict.update({
			"code": -2,
			"reason": "暂不支持此类消息类型的辟谣！",
		})
	return msg_dict


def handle_msg(msg: Message):
	msg_dict = pre_verify_news(msg)
	if msg_dict["code"] == 0:
		verified_status, verified_res = verify_news(msg.text)
		if verified_status:
			if msg.member:
				return True, "@{} {}".format(real_sender(msg).name, verified_res)
			else:
				return True, verified_res
		else:
			msg_dict["reason"] = verified_res

	return False, msg_dict