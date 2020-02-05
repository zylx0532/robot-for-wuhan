# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/5 15:06
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

import requests
import json
import re

DATA_GB_AREA_DICT = "area_dict.json"
API_TX_DISEASE_DATA = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"


def fetch_tx_area_dict():
	res = requests.get(API_TX_DISEASE_DATA)
	data = json.loads(res.json()["data"])
	area_list = data["areaTree"][0]["children"]

	def _convert_tx_area_tree(area_list, cur_dict=dict()):
		for area_item in area_list:
			if area_item.get("children"):
				cur_dict[area_item["name"]] = _convert_tx_area_tree(area_item["children"], dict())
			else:
				cur_dict[area_item["name"]] = dict()
		return cur_dict

	area_dict = _convert_tx_area_tree(area_list)
	return area_dict

def get_gb_area_dict():
	gb_area_dict = json.load(open(DATA_GB_AREA_DICT, "r", encoding="utf-8"))
	return gb_area_dict

import time
def calculate_time(func):
	def wrapper():
		s_time = time.time()
		func()
		print(func.__name__, time.time() - s_time)
	return wrapper


ROW_NUM = 10000
@calculate_time
def test_insert_open_once():
	with open("test_insert_once.txt", "a", encoding="utf-8") as f:
		for i in range(ROW_NUM):
			f.write("test\n")

@calculate_time
def test_insert_open_multi():
	for i in range(ROW_NUM):
		with open("test_insert_multi.txt", "a", encoding="utf-8") as f:
			f.write("test\n")


if __name__ == '__main__':
	fetch_tx_area_dict()
	get_gb_area_dict()
