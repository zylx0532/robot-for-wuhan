# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/5 15:06
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

import requests
import json
import re

API_TX_DISEASE_DATA = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"


def fetch_tx_area_dict():
	res = requests.get(API_TX_DISEASE_DATA)
	data = json.loads(res.json()["data"])
	area_list = data["areaTree"][0]["children"]

	def _convert_tx_area_tree(area_list, cur_dict=dict()):
		for area_item in area_list:
			if area_item.get("children"):
				cur_dict[area_item["name"]] = _convert_tx_area_tree(area_item["children"], dict())
			cur_dict[area_item["name"]] = dict()
		return cur_dict

	area_dict = _convert_tx_area_tree(area_list)
	return area_dict

if __name__ == '__main__':
	tx_area_dict = fetch_tx_area_dict()