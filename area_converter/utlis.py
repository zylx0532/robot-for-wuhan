# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/6 16:49
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

import re
import os
import time
import json
import random
import requests
from .CONST import *



def read_json_file(file_path: str) -> [list, dict]:
	return json.load(open(file_path, "r", encoding="utf-8"))


def write_json_file(content: [list, dict], file_path: str):
	json.dump(content, open(file_path, "w", encoding="utf-8"),
	          ensure_ascii=False, indent=4, sort_keys=False)


def write_json_decorator(PATH):
	def saved_path(func):
		def wrapper(*args, **kwargs):
			res = func(*args, **kwargs)
			if isinstance(res, dict):
				write_json_file(res, PATH)
			return res
		return wrapper
	return saved_path


def re_sub_area_name(x):
	return re.sub("|".join(AREA_SLOGAN), "", x)


def simple_match_in(search_key: str, iterator: [set, dict, tuple]):
	key_sets = set(iterator)
	for key in key_sets:
		if search_key == key:
			return True, key
	for key in key_sets:
		if search_key in key:
			return True, key
	return False, search_key


def fuzzy_join_two_dicts(dict_in: dict, dict_out: dict, joined_dict=None):
	"""
	测例通过：{"a": {"a1": {}}, "b": {"b1": {}}}, {"a": {}, "c": {"c1": {}}}
	:param dict_in:
	:param dict_out:
	:param joined_dict:
	:return:
	"""
	joined_dict = dict() if not joined_dict else joined_dict
	dict_out_keys_set = set(dict_out)
	for key_in in dict_in:
		status, key_matched = simple_match_in(key_in, dict_out)
		if status:
			dict_out_keys_set.remove(key_matched)
			joined_dict[key_matched] = fuzzy_join_two_dicts(
				dict_in.get(key_in, dict()), dict_out.get(key_matched, dict()), dict())
		else:
			joined_dict[key_in] = dict_in.get(key_in, dict())
	else:
		for key_out_remaining in dict_out_keys_set:
			joined_dict[key_out_remaining] = dict_out.get(key_out_remaining, dict())
	return joined_dict


def flat_dict_to_map(input_dict :dict, output_map=None, cur_path=()):
	output_map = output_map if output_map else dict()
	for key, value in input_dict.items():
		new_path = cur_path + (key, )
		full_name = "".join(new_path)
		output_map[full_name] = {
			"path": new_path,
			"name": key,
			"full_name": full_name,
			"level": len(new_path)
		}
		flat_dict_to_map(value, output_map, new_path)
	return output_map


