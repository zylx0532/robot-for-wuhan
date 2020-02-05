# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/2 16:16
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

from datetime import datetime
import logging
import time
import sys
import os


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

TEMP_DIR   = os.path.join(PROJECT_DIR, "temp")
DATA_DIR   = os.path.join(PROJECT_DIR, "data")
LOG_DIR    = os.path.join(PROJECT_DIR, "logs")
DATASET_DIR = os.path.join(PROJECT_DIR, "dataset")

WX_ROBOT_DIR    = os.path.join(PROJECT_DIR, "wx_robot")
WX_SERVERS_DIR  = os.path.join(PROJECT_DIR, "wx_servers")


"""
微信机器人配置
"""
# 该文件夹内的数据是您自己的用户数据，不会上传到Github，但需要确保文件夹存在
WX_ROBOT_DATA_DIR         = os.path.join(WX_ROBOT_DIR, "data")
if not os.path.exists(WX_ROBOT_DATA_DIR):
	os.mkdir(WX_ROBOT_DATA_DIR)

WX_COOKIE_PATH      = os.path.join(WX_ROBOT_DATA_DIR, "cookie.pkl")
WX_PUID_PATH        = os.path.join(WX_ROBOT_DATA_DIR, "puid.pkl")
WX_QR_PATH          = os.path.join(WX_ROBOT_DATA_DIR, "QR.png")

WX_COOKIE_TIMEOUT   = 30 * 60 * 60    # 微信Cookie文件的过期时间，设置成30小时
WX_MSG_VERIFY_TIMEOUT = 60            # 微信辟谣的时间延迟，超过一分钟就不辟谣了


"""
微信服务配置
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
日志配置
"""
LOG_HISTORY_DIR = os.path.join(LOG_DIR, "history")





