# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/5 2:19
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from settings_base import *

try:
	import pymongo
except:
	USE_MONGODB = False

class MyMongoDB():

	def __init__(self):
		self.uri    = pymongo.MongoClient("localhost:27017")
		self.db     = self.uri[DB_NAME]
		self.coll   = self.db[COLL_NAME]

	def insert_one(self, item: dict):
		self.coll.insert_one(item)

	def __del__(self):
		self.uri.close()

class MyFileWriter():

	def __init__(self):
		self.file_writer = open(MSG_HISTORY_PATH, "a", encoding="utf-8")
		self.file_writer.write("[")

	def insert_one(self, item: dict):
		item.pop("msg_raw")             # 减少本地存储信息量
		self.file_writer.write("{}\n".format(item))

	def __del__(self):
		self.file_writer.write("]")
		self.file_writer.close()


if USE_MONGODB:
	my_db = MyMongoDB()
else:
	my_db = MyFileWriter()