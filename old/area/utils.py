

# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/6 2:02
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from common.json import read_json_file, write_json_file
import requests
import json
import re





def area_dict_tx2gb(tx_area_dict: dict, gb_area_dict: dict, cur_path=""):
	for tx_area_name, tx_area_dict in tx_area_dict.items():
		cur_path_new = cur_path + "/" + tx_area_name
		for gb_area_name, gb_area_dict in gb_area_dict.items():
			tx_area_name = re.sub("自治|州|县|区|市|行政区|特别|示范区", "", tx_area_name)
			if tx_area_name in gb_area_name:
				yield from area_dict_tx2gb(tx_area_dict, gb_area_dict, cur_path_new)
				break
		else:
			if re.search("外地来|待确认", tx_area_name):
				pass
			elif re.search("香港|澳门|台湾", tx_area_name):
				pass
			else:
				yield "Not Found {} in | {}".format(cur_path_new,  list(gb_area_dict))


def joined_area_dict_tx_gb(tx_area_dict: dict, gb_nested_area_dict: dict, joined_area_dict=None):

	joined_area_dict = joined_area_dict if joined_area_dict else dict()
	gb_area_name_set = set(gb_nested_area_dict)
	for tx_area_name, tx_area_value in tx_area_dict.items():
		#-----------  疫情专用 ------------------#
		if re.search("外地来|待确认", tx_area_name):
			joined_area_dict[tx_area_name] = tx_area_value
		#-----------  万能场合 ------------------#
		elif re.search("香港|澳门|台湾", tx_area_name):
			joined_area_dict[tx_area_name] = tx_area_value
		#-----------  遍历匹配 ------------------#
		else:
			for gb_area_name, gb_area_value in gb_nested_area_dict.items():
				if tx_area_name in gb_area_name:
					gb_area_name_set.remove(gb_area_name)
					joined_area_dict[gb_area_name] = joined_area_dict_tx_gb(tx_area_value, gb_area_value, dict())
					break
			else:
				tx_area_name_subbed = re.sub("自治|特别|示范|行政|县$|区$|市$|州$", "", tx_area_name)
				for gb_area_name, gb_area_value in gb_nested_area_dict.items():
					if tx_area_name_subbed in gb_area_name:
						gb_area_name_set.remove(gb_area_name)
						joined_area_dict[tx_area_name] = joined_area_dict_tx_gb(tx_area_value, gb_area_value, dict())
						break
				else:
					joined_area_dict[tx_area_name] = tx_area_value
	for gb_area_name_remaining in gb_area_name_set:
		joined_area_dict[gb_area_name_remaining] = gb_nested_area_dict[gb_area_name_remaining]
	return joined_area_dict


def gen_joined_area_dict():
	DATA_TX_AREA_DICT_PATH          = "tx_cn_area_dict.json"
	DATA_GB_NESTED_AREA_DICT_PATH   = "gb_nested_area_dict.json"
	DATA_JOINED_AREA_DICT_PATH      = "joined_area_dict.json"

	tx_area_dict            = read_json_file(DATA_TX_AREA_DICT_PATH)
	gb_nested_area_dict     = read_json_file(DATA_GB_NESTED_AREA_DICT_PATH)
	joined_area_dict        = joined_area_dict_tx_gb(tx_area_dict, gb_nested_area_dict)

	write_json_file(joined_area_dict, DATA_JOINED_AREA_DICT_PATH)
	return joined_area_dict


def area_dict2map(area_dict: dict) -> dict:

	def flat_dict(area_dict: dict, cur_tuple: tuple=(), area_map: dict=dict()):
		for area_name, area_children in area_dict.items():
			area_tuple = cur_tuple + (area_name, )
			area_map["".join(area_tuple)] = area_tuple
			flat_dict(area_children, area_tuple, area_map)
		return area_map

	area_map = flat_dict(area_dict)
	sorted_area_map = dict(sorted(area_map.items(), key=lambda x: len(x[1])))
	return sorted_area_map


def search_map(search_key: str, sorted_area_map: dict) -> dict:

	SPECIAL_CASES = {
		"全国": "中国"
	}

	# 以下后缀，是通过扫描GB表的后缀汇成的集合，对后续的分词具有重要意义
	AREA_SLOGAN = {
		'县', '岭', '市', '园', '认', '沪', '门', '子', '师', '会', '州', '区',
		'城', '旗', '岛', '盟', '渠', '域', '省', '港', '特', '津', '京', '湾'
	}

	# 层数控制限制，为了提高检索的效率，限制返回的层级结果
	LEVEL_LIMIT = 99

	# 存储要返回的列表信息
	searched_list = []

	# 去除非中文
	search_key = re.sub("[^\u4e00-\u9fa5]*", "", search_key)
	if not search_key:
		return {
			"code": -1,
			"info": "请输入一个合适的中文地名哦~",
		}
	# 替换特例
	search_key = SPECIAL_CASES.get(search_key, search_key)

	####################    S T A R T   #######################
	# 第一遍遍历是全称匹配
	for area_key, area_tuple in sorted_area_map.items():
		# 设置层级退出标志
		if len(area_tuple) <= LEVEL_LIMIT:
			if search_key in area_key:
				searched_list.append(sorted_area_map[area_key])
				LEVEL_LIMIT = len(area_tuple)
		else:
			break

	if searched_list:
		return {
			"code": 1,
			"info": searched_list
		}

	# 第二遍遍历是切割匹配
	search_key_nested = re.sub("|".join(AREA_SLOGAN), "", search_key)

	print("Started nested search with key from {} to {}".format(search_key, search_key_nested))

	for area_key, area_tuple in sorted_area_map.items():
		if len(area_tuple) <= LEVEL_LIMIT:
			area_key_nested = re.sub("|".join(AREA_SLOGAN), "", area_key)
			if search_key_nested in area_key_nested:
				searched_list.append(sorted_area_map[area_key])
				LEVEL_LIMIT = len(area_tuple)
		else:
			break

	if searched_list:
		return {
			"code": 2,
			"info" : searched_list
		}
	else:
		return {
			"code": -2,
			"info" : "您输入的好像不是一个中国地名欸，要不换个关键词试试~"
		}




def gen_gbtx_area_map(tx_area_list: list, gb_area_dict: dict, gbtx_area_map: dict, cur_tuple: tuple):
	gb_area_name_set = set(gb_area_dict)
	# 先将腾讯地名与国标地名进行全称对比
	for tx_area_item in tx_area_list:
		tx_area_name = tx_area_item["name"]
		for gb_area_name in list(gb_area_dict):
			if tx_area_name in gb_area_name:
				gb_area_name_set.remove(gb_area_name)
				the_tuple = cur_tuple + (gb_area_name, )
				full_area_name = "".join(the_tuple)
				next_tx_area_list = tx_area_item.pop("children", [])
				gbtx_area_map[full_area_name] = dict(tx_area_item, **{"tuple": the_tuple})
				gen_gbtx_area_map(next_tx_area_list, gb_area_dict.get(gb_area_name, dict()), gbtx_area_map, the_tuple)
				break
		else:
			# 第一次匹配没有成功，就进行第二次模糊匹配
			tx_area_name_subbed = cls._re_sub_area_name(tx_area_name)
			for gb_area_name in list(gb_area_dict):
				gb_area_name_subbed = cls._re_sub_area_name(gb_area_name)
				if tx_area_name_subbed in gb_area_name_subbed:
					gb_area_name_set.remove(gb_area_name)
					the_tuple = cur_tuple + (gb_area_name,)
					full_area_name = "".join(the_tuple)
					next_tx_area_list = tx_area_item.pop("children", [])
					gbtx_area_map[full_area_name] = dict(tx_area_item, **{"tuple": the_tuple})
					gen_gbtx_area_map(next_tx_area_list, gb_area_dict.get(gb_area_name, dict()), gbtx_area_map, the_tuple)
					break
			else:
				# 否则，大概率是腾讯特有的地名，因此直接加上
				the_tuple = cur_tuple + (tx_area_name, )
				full_area_name = "".join(the_tuple)
				gbtx_area_map[full_area_name] = dict(tx_area_item, **{"tuple": the_tuple})
	# 接下来，进行剩余的国标地名遍历
	for gb_area_name_remaining in gb_area_name_set:
		the_tuple = cur_tuple + (gb_area_name_remaining, )
		full_area_name = "".join(the_tuple)
		gbtx_area_map[full_area_name] = dict(gb_area_dict[gb_area_name_remaining], **{"tuple": the_tuple})
	return gbtx_area_map