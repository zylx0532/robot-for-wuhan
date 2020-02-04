# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 15:53
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from wx_robot.utils import *
from wx_servers.check_disease import init_area_dict, check_area_info

import re


def start_servers(self):
	"""

	:param self:
	:return:
	"""


	"""
	以下是全部控制命令
	"""
	self.commands_dict = {
		"辟谣": "enable_verify_news",
		"疫情": "enable_check_disease",
	}
	self.ENABLE_COMMAND_PREFIX = "打开"
	self.DISABLE_COMMAND_PREFIX = "关闭"


	@self.register(chats=self.target_groups + [self.my_fh], msg_types=[TEXT], except_self=False)
	def func_control(msg: Message):
		if msg.text == "帮助":
			return ABOUT_ME.format(
				"目前可选功能有: {}\n启动命令为： {}\n关闭命令为： {}".format(
					list(self.commands_dict),
					self.ENABLE_COMMAND_PREFIX,
					self.DISABLE_COMMAND_PREFIX,
			))

		command_open = re.match("打开(.*)", msg.text)
		if command_open:
			command = command_open.group(1).strip()
			if command in self.commands_dict:
				setattr(self, self.commands_dict[command], True)
				return "已{} {} by {}".format(self.ENABLE_COMMAND_PREFIX, command, real_sender(msg))

		command_close = re.match("关闭(.*)", msg.text)
		if command_close:
			command = command_close.group(1).strip()
			if command in self.commands_dict:
				setattr(self, self.commands_dict[command], False)
				return "已{} {} by {}".format(self.DISABLE_COMMAND_PREFIX, command, real_sender(msg))


		"""
		辟谣
		"""
		if self.enable_verify_news:
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

			chase_msg_match = re.match("追\s*(\d+)", msg.text)
			if chase_msg_match:
				msg_id = chase_msg_match.group(1)
				msg_info = self.verified_msgs_dict.get(msg_id, None)
				return "@{} 答: {}".format(real_sender(msg), msg_info)

		"""
		疫情数据查询
		"""
		if self.enable_check_disease:
			# 匹配查字后面连续的字符串
			area_match = re.match("查(.*)", msg.text)
			if area_match:
				area_matched = area_match.group(1)
				# 特例
				if area_matched == "全国":
					area_matched = "中国"
				if area_matched:
					area_info = check_area_info(area_matched)
					return area_info["msg"]
				else:
					return "您要查啥呢？不如试试查一些城市的疫情数据？比如 『查武汉』"

