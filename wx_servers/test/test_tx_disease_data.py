# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 17:29
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

import requests
from wx_servers.check_disease import *
import re

DATA_TX_AREAS_PATH = "area_tree.json"


def get_tx_area_tree():
	res_json = requests.get(API_TX_DISEASE_DATA).json()
	assert res_json["ret"] == 0

	data = json.loads(res_json["archive"])
	area_tree = data["areaTree"]
	write_json_file(area_tree, DATA_TX_AREAS_PATH)


def test_area_tree(area: str):

	area_info = search_area_partial(area)[0] # type: dict

	tx_tree = read_json_file(DATA_TX_AREAS_PATH)
	tx_tree_cn = tx_tree[0]["children"]

	if area_info.get(1):
		for province_item in tx_tree_cn:
			if province_item["name"] in area_info.get(1):
				if area_info.get(2):
					for city_item in province_item["children"]:
						# 由于国标的地区里，直辖市的二级是“市辖区”，所以与主流互联网平台的层次结构不一样，需要单独处理
						if city_item["name"] in area_info.get(2) if area_info.get(2) != "市辖区" else area_info.get(3):
							return True, city_item
					else:
						return False, "不存在城市与输入匹配，但省份匹配为{}".format(province_item["name"])
				return True, province_item
		else:
			return False, "不存在省份与输入匹配"


def handle_input(area_str) -> dict:
	pass



if __name__ == '__main__':
	s, v = test_area_tree("朝阳")
	s, v = test_area_tree("北京")