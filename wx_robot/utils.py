# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/3 20:43
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from .CONST import *

import os
import time
from wxpy import *


def clear_cookie() -> None:
	"""
	该函数主要为删除过期的微信Cookie文件，以保证微信Cookie的有效性
	[python获取文件修改时间与创建时间_u014717398的博客-CSDN博客](https://blog.csdn.net/u014717398/article/details/72627125 )
	:return:
	"""
	if os.path.exists(WX_COOKIE_PATH):
		if os.stat(WX_COOKIE_PATH).st_mtime < time.time() - WX_COOKIE_TIMEOUT:
			os.remove(WX_COOKIE_PATH)

def real_sender(msg: Message) -> Chat:
	"""
	该函数可以返回消息的直接发送人
	:param msg:
	:return:
	"""
	return msg.member if msg.member else msg.sender



