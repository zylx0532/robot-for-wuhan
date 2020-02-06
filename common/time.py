# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/5 18:28
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

import time
def calc_time(func):
	def wrapper():
		s_time = time.time()
		func_result = func()
		print(func.__name__, time.time() - s_time)
		return func_result
	return wrapper
