# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 12:17
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from settings_base import *
import time


API_TX_DISEASE_DATA = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
API_TX_DISEASE_NEWS = "https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_time_line" # TODO 疫情新闻的推送



"""
辟谣系统
"""
THRESHOLD_CONTENT_CNT = 10      # 如果返回过多，就说明关键词太模糊，这种情况下不辟谣
CUT_ABSTRACT_LEN = 50           # 摘要只返回前50个字，不然太多了


VERIFY_NEWS_HEADERS = {
		'host': 'vp.fact.qq.com',
		'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
		'sec-fetch-mode': 'no-cors',
		'sec-fetch-site': 'same-origin',
		'referer': 'https://vp.fact.qq.com/home?state=2'
	}
VERIFY_NEWS_URL = 'https://vp.fact.qq.com/searchresult'
