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
	import atexit
	def __init__(self, file_path=None):
		self.file_path = file_path if file_path else MSG_HISTORY_PATH
		self.file_writer = open(self.file_path, "a", encoding="utf-8")

	def insert_one(self, item: dict):
		self.file_writer.write("{}\n".format(item))

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.file_writer.close()
		return True


if USE_MONGODB:
	my_db = MyMongoDB()
else:
	my_db = MyFileWriter()