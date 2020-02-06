# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/6 16:00
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from area import *


AREA_DATA_DIR                   = os.path.join(AREA_DIR, "archive")
DATA_CN_AREA_DICT_PATH          = os.path.join(AREA_DATA_DIR, "gb_area_dict.json")
DATA_CN_NESTED_AREA_DICT_PATH   = os.path.join(AREA_DATA_DIR, "gb_nested_area_dict.json")

DATA_TX_CN_WUHAN_DISEASE_PATH   = os.path.join(AREA_DATA_DIR, "tx_cn_area_dict.json")

AREA_SLOGAN = {
	"县", "区", "市", "州", "省",
}
