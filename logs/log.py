# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/2 16:34
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

import logging
from datetime import datetime
from settings_base import *

# create logger
LOG_NAME = "log"
logger =  logging.getLogger(LOG_NAME)
logger.setLevel(logging.DEBUG)

# create file handler
FILE_NAME = "{}.log".format(datetime.now().strftime("%y%m%d_%H%M%S"))
LOG_DIR = os.path.join(PROJECT_PATH, "logs/history")
LOG_PATH = os.path.join(LOG_DIR, FILE_NAME)
LOG_HANDLE = logging.FileHandler(filename=LOG_PATH)
LOG_HANDLE.setLevel(logging.INFO)

# create formatter
LOG_FMT = "%(asctime)-15s %(levelname)s (%(name)s) [%(threadName)s - %(funcName)s - %(lineno)s]: %(message)s"
DATE_FMT = "%a %d %b %Y %H:%M:%S"
LOG_FORMATTER = logging.Formatter(LOG_FMT, DATE_FMT)

# add handler and formatter
LOG_HANDLE.setFormatter(LOG_FORMATTER)
logger.addHandler(LOG_HANDLE)


logger.info("Hello ")
logging.info("hjdfbasC")