# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/5 2:31
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

import requests
from pprint import pprint


def get_json(url, *args, **kwargs):
	res_json = requests.get(url, *args, **kwargs).json()
	return res_json