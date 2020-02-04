# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/3 20:43
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from .CONST import *

# 通过链接wx_servers库来提供wx_robots的服务
from wx_servers.verify_news import verify_news
from wx_servers.check_disease import search_area_partial

import os
import time
from datetime import datetime

from wx_robot import *




def clear_cookie() -> None:
	"""
	# 该函数主要为删除过期的微信Cookie文件，以保证微信Cookie的有效性
	# [python获取文件修改时间与创建时间_u014717398的博客-CSDN博客](https://blog.csdn.net/u014717398/article/details/72627125 )
	:return:
	"""
	if os.path.exists(WX_COOKIE_PATH):
		if os.stat(WX_COOKIE_PATH).st_mtime < time.time() - WX_COOKIE_TIMEOUT:
			os.remove(WX_COOKIE_PATH)

def real_sender(msg: Message) -> str:
	return msg.member.name if msg.member else msg.sender.name

def pre_verify_news(msg: Message):
	msg_dict = {
		"id": msg.id,
		"sender": real_sender(msg),
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
				return True, "@{} {}".format(real_sender(msg), verified_res)
			else:
				return True, verified_res
		else:
			msg_dict["reason"] = verified_res

	return False, msg_dict

