# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 12:17
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from settings_base import *
import time


"""
疫情查询
"""

TEMPLATE_NOT_FOUND_AREA_RESULT  = "咦？没有找到{}的数据哦，说不定还没被感染呢，哈哈那也太幸运了！"
TEMPLATE_SEVERAL_AREAS_RESULT   = "您要查询的『{}』有多个结果哦，我就给您一并返回啦：\n"
TEMPLATE_MULTI_AREAS_RESULT     = "哎呀，『{}』咋这么热乎，有这么多结果，我都快分不清了，你看:\n"

TEMPLATE_API_SERVICE_CLOSED     = "查询服务已被关闭，请检查后台系统！"

MAX_AREA_RESULTS            = 3
AREA_DICT_TIMEOUT           = 600
server_enable_check_disease = True
global_area_dict            = dict()
global_updated_time         = time.time()

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
