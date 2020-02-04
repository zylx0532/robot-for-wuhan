# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/3 22:10
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from robot.utils import *
from wxpy import *

class MyBot(Bot):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.enable_puid(WX_PUID_PATH)
		# self.my_log = get_wechat_logger(level=logging.WARNING, name="WXPY")
		# print("Initialized ~")

if __name__ == '__main__':
	MyBot()
	embed()