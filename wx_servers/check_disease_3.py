# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/5 14:36
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

from area_converter.gbtx import GBTX


my_map = GBTX()

def msg_template(item):
	return """{area}今日新增确诊{t_c}人，去世{t_d}人，治愈{t_h}人；目前总计有{s_c}人确诊，去世{s_d}人，治愈{s_h}人。""".format(
		area=item["name"], t_c=item["today"]["confirm"], t_d=item["today"]["dead"], t_h=item["today"]["heal"],
		s_c=item["total"]["confirm"], s_d=item["total"]["dead"], s_h=item["total"]["heal"],
	)


def check_disease_by_area(search_key):
	status, data = my_map.search_disease_by_area(search_key)
	"""
	填入逻辑
	"""
	if data:
		msgs = list(map(msg_template, data))
		if len(msgs) == 1:
			return msgs[0]
		msg_all = ""
		for msg_seq, msg_content in enumerate(msgs):
			msg_all += "{}. {}\n".format(msg_seq+1, msg_content)
		return msg_all
	print(status)
	return status.msg
