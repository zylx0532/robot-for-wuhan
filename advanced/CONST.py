# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/2 16:16
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

from settings_base import *
import os
import time

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMP_PATH   = os.path.join(PROJECT_PATH, "temp")
DATA_PATH   = os.path.join(PROJECT_PATH, "data")
LOG_PATH    = os.path.join(PROJECT_PATH, "log")
WX_PATH     = os.path.join(PROJECT_PATH, "robot/data")


