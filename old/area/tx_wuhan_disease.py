# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/6 16:14
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

from .CONST import *


def gen_tx_area_dict():
	import requests
	"""
	这个函数可以获得腾讯的疫情数据，是第三方的一套地理信息字典
	该函数运行后会在本地生成一份json文件
	:return:
	"""

	API_TX_DISEASE_DATA = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"

	def _convert_tx_area_tree(area_list, cur_dict=None):
		for area_item in area_list:
			if area_item.get("children"):
				cur_dict[area_item["name"]] = _convert_tx_area_tree(area_item["children"], dict())
			else:
				cur_dict[area_item["name"]] = dict()
		return cur_dict

	res = requests.get(API_TX_DISEASE_DATA)
	data = json.loads(res.json()["archive"])
	area_list = data["areaTree"][0]["children"]
	area_dict = _convert_tx_area_tree(area_list)
	write_json_file(area_dict, DATA_TX_CN_WUHAN_DISEASE_PATH)
	return area_dict

def _match_contains(cls, search_key: str, iterator: [set, dict, tuple], nest: bool) -> [bool, str]:
		"""
		必须要两遍搜索，主要是解决集合过滤的问题
		:param search_key:
		:param iterator:
		:param nest:
		:return:
		"""
		if not nest:
			for key in iterator:
				if search_key == key:
					return True, key
			for key in iterator:
				if key in search_key:
					return True, key
			return False, search_key
		if nest:
			search_key_nested = cls._re_sub_area_name(search_key)
			for key in iterator:
				key_nested = cls._re_sub_area_name(key)
				if key_nested == search_key_nested:
					return True, key
			for key in iterator:
				key_nested = cls._re_sub_area_name(key)
				if key_nested in search_key_nested:
					return True, key
			return False, search_key



@write_json_decorator()
def shadow_path_map(from_dict_like_gb: dict, to_dict_like_tx: dict, output_map=None, cur_path_from=(),
                    cur_path_to=()):

	def search_key_try(from_key, to_key_set, choose_nest):
		status, to_key_matched = _match_contains(from_key, to_key_set, choose_nest)
		if status:
			to_key_set.remove(to_key_matched)
			new_path_to = cur_path_to + (to_key_matched,)
			output_map[from_full_name] = {
				"path_from": new_path_from,
				"path_to": new_path_to,
			}
			shadow_path_map(from_dict_like_gb[from_key], to_dict_like_tx[to_key_matched], output_map,
			                new_path_from,
			                new_path_to)
			return True

	output_map = output_map if output_map else dict()
	to_key_set = set(to_dict_like_tx)

	for from_key in list(from_dict_like_gb):
		# assert from_key != "湖北省恩施土家族苗族自治州"
		new_path_from = cur_path_from + (from_key,)
		from_full_name = "".join(new_path_from)

		if not search_key_try(from_key, to_key_set, False):
			if not search_key_try(from_key, to_key_set, True):
				output_map[from_full_name] = {"path_from": new_path_from, "path_to": ()}
				shadow_path_map(from_dict_like_gb[from_key], dict(), output_map, new_path_from, ())

	for to_key_remaining in to_key_set:
		new_path_to = cur_path_to + (to_key_remaining, )
		to_full_name = "".join(new_path_to)
		output_map[to_full_name] = {
			"path_from": (),
			"path_to": new_path_to
		}
		shadow_path_map(dict(), to_dict_like_tx[to_key_remaining], output_map, (), new_path_to)
	return output_map




"""
暂不使用
"""
def joined_area_dict_tx_gb(tx_area_dict: dict, gb_nested_area_dict: dict, joined_area_dict=None):
	"""
	这个函数可以将腾讯的疫情地区字典和国标整合起来
	但这个函数因为数据结构的需求变化，暂不使用
	:param tx_area_dict:
	:param gb_nested_area_dict:
	:param joined_area_dict:
	:return:
	"""
	joined_area_dict = joined_area_dict if joined_area_dict else dict()
	gb_area_name_set = set(gb_nested_area_dict)
	for tx_area_name, tx_area_value in tx_area_dict.items():
		# -----------  疫情专用 ------------------#
		if re.search("外地来|待确认", tx_area_name):
			joined_area_dict[tx_area_name] = tx_area_value
		# -----------  万能场合 ------------------#
		elif re.search("香港|澳门|台湾", tx_area_name):
			joined_area_dict[tx_area_name] = tx_area_value
		# -----------  遍历匹配 ------------------#
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
