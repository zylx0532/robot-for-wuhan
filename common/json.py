# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 13:57
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
import json

def read_json_file(file_path: str) -> [list, dict]:
	return json.load(open(file_path, "r", encoding="utf-8"))


def write_json_file(content: [list, dict], file_path: str) -> None:
	json.dump(content, open(file_path, "w", encoding="utf-8"))