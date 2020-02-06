# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/6 17:18
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
import os

AREA_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(AREA_DIR, "data")
if not os.path.exists(DATA_DIR):
	os.mkdir(DATA_DIR)


class STATUS:
	from collections import namedtuple
	status = namedtuple("status", ["code", "msg"])

	NO_VALID_INFO        = status(1, "咦？您输入了啥，一休我没有明白...")
	VALID_WITH_DATA      = status(2, "叮！")
	VALID_WITHOUT_DATA   = status(3, "哈哈，这个地方暂时还没有数据哦~")
	ROLLBACK             = status(-1, "精度过高，正在回退...")
	CN_NOT_FOUND         = status(-2, "没有找到国内地区，请启动国际搜索")

	GLOBAL_COUNTRY_NOT_FOUND     = status(-3, "没有找到这个国家，请启动城市搜索")
	GLOBAL_CITY_FOUND            = status(4, "哎呀，我们国家暂时还没有收录国际城市的数据哦")
	GLOBAL_CITY_NOT_FOUND        = status(5, "哎呀，查无此地区呢，不要再逗我啦，要不你打赏个红包？")
	GLOBAL_COUNTRY_NOT_INFECTED  = status(6, "哈哈，这个国家还没有感染数据哦~")
	GLOBAL_COUNTRY_INFECTED      = status(7, "叮！")


API_TX_DISEASE_DATA = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"

DATA_TIMEOUT = 60 * 10

# 	AREA_SLOGAN = {
# 	'县', '岭', '市', '园', '认', '沪', '门', '子', '师', '会', '州', '区',
# 	'城', '旗', '岛', '盟', '渠', '域', '省', '港', '特', '津', '京', '湾'
# }
AREA_SLOGAN = {
	"县", "区", "市", "州", "省",
}
SPECIAL_CASES = {
	"全国": "中国"
}


GB_NESTED_AREA_DICT_PATH_TO_READ    = os.path.join(DATA_DIR, 'gb_nested_area_dict.json')
CN_GBTX_DATA_MAP_PATH_TO_WRITE      = os.path.join(DATA_DIR, 'cn_gbtx_data_map.json')
GLOBAL_COUNTRIES_DICT_PATH          = os.path.join(DATA_DIR, "global_countries_dict.json")
GLOBAL_CITIES_DICT_PATH             = os.path.join(DATA_DIR, "global_cities_dict.json")
