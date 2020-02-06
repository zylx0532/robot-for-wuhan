# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 15:53
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------


from wx_robot.utils import *
from wx_servers.verify_news import handle_msg
from wx_servers.check_disease_3 import check_disease_by_area
from database.db import my_db

import re
import random

"""
装饰器部分
"""

def msg_record(func):
	"""
	这是一个统计管道，可以收集各类信息
	:param func:
	:return:
	"""
	def decorator(self: Bot, msg: Message, *args, **kwargs):
		result = func(self, msg, *args, **kwargs)
		item = {
			"func_name"     : func.__name__,
			"user_name"     : real_sender(msg).name,
			"group_name"    : msg.sender.name if msg.member else None,
			"msg_raw"       : msg.raw,
		}
		if result:  # 只在确实进入管道的时候才加
			my_db.insert_one(item)
		return result
	return decorator



def msg_tail(func):
	"""
	这是小尾巴的函数
	:param tail:
	:return:
	"""
	def wrapper(self, msg):
		res = func(self, msg)
		if isinstance(res, str):
			res += "\n-----------\n"
			res += random_tail()
		return res
	return wrapper


"""
功能函数部分，你可以设计各种不同的功能
"""

@msg_record
def command_quit(self, msg):
	if msg.sender == self.self and msg.text == "退出":
		self.my_log.info(TEMPLATE_LOG_OUT_GREETING)
		self.logout()
		return True

@msg_record
def command_enable_some_func(self, msg):
	command_open = re.match("打开(.*)", msg.text)
	if command_open:
		command = command_open.group(1).strip()
		if command in self.commands_dict:
			setattr(self, self.commands_dict[command], True)
			return "已{} {} by {}".format(self.ENABLE_COMMAND_PREFIX, command, real_sender(msg))

@msg_record
def command_disable_some_func(self, msg):
	command_close = re.match("关闭(.*)", msg.text)
	if command_close:
		command = command_close.group(1).strip()
		if command in self.commands_dict:
			setattr(self, self.commands_dict[command], False)
			return "已{} {} by {}".format(self.DISABLE_COMMAND_PREFIX, command, real_sender(msg))

@msg_record
def command_verify_shared_msg(self, msg):
	if msg.type == "Sharing":
		# TODO 以下逻辑还没有完全和 utils中解耦，后续再优化
		msg_status, msg_info = handle_msg(msg)
		if msg_status:
			self.my_log.info(msg_info)
			return msg_info
		else:
			self.verified_msgs_dict.update({msg_info["id"]: msg_info})
			if WX_VERIFY_DEBUG:
				return msg_info


# @msg_tail
@msg_record
def command_check_disease(self, msg):
	"""
	这个版本，把服务的逻辑带到业务上来了，不应该都这么多种返回的!
	:param self:
	:param msg:
	:return:
	"""
	area_match = re.match("查(?:一查|查|询)?\s*([\u4e00-\u9fa5]*)", msg.text)
	if area_match:
		area_matched = area_match.group(1)
		return check_disease_by_area(area_matched)



"""
全局控制逻辑，最好不要修改，除非你知道你在做什么！
"""
def start_servers(self):

	monitor_chats = self.target_groups + [self.my_fh]

	@self.register(chats=monitor_chats, msg_types=[TEXT, SHARING], except_self=False)
	def func_control(msg: Message):

		for command in REGISTER_COMMANDS:
			res = eval(command)(self, msg)
			if res:
				return res

