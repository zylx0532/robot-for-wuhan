# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/6 16:02
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from .CONST import *

def gen_nested_gb_area_dict(DATA_CN_AREA_DICT_PATH, DATA_CN_NESTED_AREA_DICT_PATH):
	"""
	该函数用于生成一份自定义的国标字典数据，注意没有港澳台
	该字典信息已在目标位置下，不用重新运行
	原国标字典数据是从china_region这个repo上download下来处理的
	:return:
	"""

	def _nest_gb_area_dict(area_dict: dict, nested_area_dict=None):
		for k, v in area_dict.items():
			if not re.match(".*省直辖.*|.*市辖区.*|.*直辖县.*|县", k):
				nested_area_dict[k] = _nest_gb_area_dict(v, dict())
			else:
				for i, j in v.items():
					nested_area_dict[i] = _nest_gb_area_dict(j, dict())
		return nested_area_dict

	gb_area_dict = json.load(open(DATA_CN_AREA_DICT_PATH, "r", encoding="utf-8"))
	nested_gb_area_dict = _nest_gb_area_dict(gb_area_dict, dict())
	write_json_file(nested_gb_area_dict, DATA_CN_NESTED_AREA_DICT_PATH)
	return nested_gb_area_dict
