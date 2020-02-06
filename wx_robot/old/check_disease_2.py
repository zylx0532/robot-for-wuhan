# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/6 18:21
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------


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