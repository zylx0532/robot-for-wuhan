# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 12:17
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from settings_base import *
import time


"""
路径配置
"""
DATA_AREA_DICT_NAME = "area_dict.json"
DATA_COUNTRY_DICT_NAME = "country_dict.json"

DATA_PROVINCE_LIST_NAME = "province.json"
DATA_CITY_DICT_NAME = "city.json"
DATA_COUNTY_DICT_NAME = "county.json"


DATASET_AREA_DIR = os.path.join(DATASET_DIR, "area")
DATASET_PROVINCE_LIST_PATH  = os.path.join(DATASET_AREA_DIR, DATA_PROVINCE_LIST_NAME)
DATASET_CITY_LIST_PATH      = os.path.join(DATASET_AREA_DIR, DATA_CITY_DICT_NAME)
DATASET_COUNTY_LIST_PATH    = os.path.join(DATASET_AREA_DIR, DATA_COUNTY_DICT_NAME)

WX_SERVER_DATA_DIR      = os.path.join(WX_SERVERS_DIR, "data")
DATA_AREA_DICT_PATH  = os.path.join(WX_SERVER_DATA_DIR, DATA_AREA_DICT_NAME)
DATA_COUNTRY_DICT_PATH = os.path.join(WX_SERVER_DATA_DIR, DATA_COUNTRY_DICT_NAME)




"""
疫情查询
"""
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
