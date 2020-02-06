# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/6 15:56
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

import os
import re
import json

AREA_DIR = os.path.dirname(os.path.abspath(__file__))

def read_json_file(file_path: str) -> [list, dict]:
	return json.load(open(file_path, "r", encoding="utf-8"))


def write_json_file(content: [list, dict], file_path: str) -> None:
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