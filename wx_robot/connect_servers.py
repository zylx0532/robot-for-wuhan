# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 15:53
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------


from wx_robot.utils import *
from wx_servers.verify_news import handle_msg
from wx_servers.check_disease_2 import check_disease_by_area
from database.db import my_db

import re
import random

"""
装饰器部分，你可以用它来收集各类信息
"""

def msg_record(func):
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


"""
功能函数部分，你可以设计各种不同的功能
"""

@msg_record
def command_quit(self, msg):
	if msg.sender == self.self and msg.text == "退出":
		self.my_log.info(TEMPLATE_ROBOT_QUIT)
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

@msg_record
def command_check_disease(self, msg):
	area_match = re.match("查(?:一查|查|询)?\s*([\u4e00-\u9fa5]*)", msg.text)
	if area_match:
		area_matched = area_match.group(1)
		if area_matched:
			area_info = check_disease_by_area(area_matched)
			if area_info["code"] != 0:
				# 如果返回不为0，则返回报错消息
				self.my_log.error(area_info)
				return TEMPLATE_API_FAILED
			# 如果返回码为0，则顺利返回消息
			return area_info["msg"] + random.choice(TEMPLATE_RANDOM_MSG_TAIL_LIST)
		# 如果没有匹配到任何信息，就给一个提示
		return TEMPLATE_NO_KEYWORD
	# 没有匹配，则不返回任何信息，且不阻塞消息管道



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

