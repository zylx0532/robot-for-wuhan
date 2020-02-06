from wx_servers.CONST import *
from common.json import read_json_file, write_json_file
import re
import json
import requests


def init_area_dict() -> dict:
	"""
	从china_region拷贝下来的1-4级中国地区数据中，生成我们想要的地区字典
	目前的设计是设计了三层，即 省 - 市 - 县， 再往下就没有必要了
	在启动微信服务的时候，会先加载该地区字典
	:return:
	"""
	if not os.path.exists(DATA_AREA_DICT_PATH):
		print(f"Initializing {DATA_AREA_DICT_NAME} ...")
		from collections import defaultdict
		area_dict = defaultdict(dict)

		province_list   = read_json_file(DATASET_PROVINCE_LIST_PATH)
		city_dict       = read_json_file(DATASET_CITY_LIST_PATH)
		county_dict     = read_json_file(DATASET_COUNTY_LIST_PATH)

		for province_item in province_list:
			sub_province_dict = defaultdict(dict)
			area_dict[province_item["name"]] = sub_province_dict
			for city_item in city_dict[province_item["id"]]:
				sub_cities_dict = defaultdict(dict)
				sub_province_dict[city_item["name"]] = sub_cities_dict
				for county_item in county_dict.get(city_item["id"], []):
					sub_cities_dict[county_item["name"]] = dict()
		write_json_file(area_dict, DATA_AREA_DICT_PATH)
		print(f"Initialized {DATA_AREA_DICT_NAME} ~")

	target_areas_dict =  read_json_file(DATA_AREA_DICT_PATH)
	print(f"Loaded {DATA_AREA_DICT_NAME} ~")
	return target_areas_dict


area_dict = read_json_file(DATA_AREA_DICT_PATH)         # type: dict
country_dict = read_json_file(DATA_COUNTRY_DICT_PATH)   # type: dict


def check_area_info(area_str: str) -> dict:
	# 先判断是否是国家
	if area_str in country_dict.values():
		return fetch_area_disease(area_str, None, None, None)
	# 然后判断国内数据
	area_info = get_local_area(area_str)
	if area_info["code"] != 0:
		return area_info
	return fetch_area_disease(*area_info["msg"])


def search_area_partial(area_to_search):
	"""
	从国标数据库中得到可能多个值的返回结果，形式 [[None, Province, City, County], ...]
	:param area_to_search:
	:return:
	"""
	def _search_area(area_to_search: str, area_dict: dict, area_info=[None, None, None, None], depth=1):
		for k, v in area_dict.items():
			sub_area_info = area_info.copy()
			sub_area_info[depth] = k
			if area_to_search in k: # 如果键中已经有搜索关键字，直接返回
				yield sub_area_info
				continue
			yield from _search_area(area_to_search, v, sub_area_info, depth+1)

	return [i for i in _search_area(area_to_search, area_dict)]


def get_local_area(area_to_search):
	area_info = search_area_partial(area_to_search)
	if not area_info:
		return {
			"code": -1,
			"msg": "该关键字未有对应省、市、区信息\n请核实！"
		}
	if len(area_info) > 1:
		# TODO 明天还得想想这里的接口优化，实在是难啊，这里
		# TODO 当回复多条后，用户会有回复选项的应激反应，这个很好，明日的重点需求
		return {
			"code": -2,
			"msg": "该关键字对应多个地区，如下：\n{}".format(
				"\n".join(["{}.{};".format(i+1, "-".join(list(filter(lambda x: x, j)))) for i, j in enumerate(area_info)])
			)
		}
	return {
		"code": 0,
		"msg": area_info[0],
	}


def fetch_area_disease(country, province, city, county):
	"""
	输入的是国标转化过来的位置，所以对接腾讯的还需要做进一步匹配
	:param country:
	:param province:
	:param city:
	:param county:
	:return:
	"""
	def disease_data_dict2str(item: dict) -> dict:
		def _translate(data_item: dict) -> str:
			translated = "确认{}人，死亡{}人，治愈{}人".format(data_item["confirm"], data_item["dead"], data_item["heal"])
			if data_item["suspect"] > 0:
				translated += "，嫌疑{}人".format(data_item["suspect"])
			return translated
		disease_data_str = item["name"]
		disease_data_str += "今日{}；".format(_translate(item["today"]))
		disease_data_str += "总计{}。".format(_translate(item["total"]))
		disease_data_str += "🙏🙏"
		return {
			"code": 0,
			"msg": disease_data_str
		}

	res_json = requests.get(API_TX_DISEASE_DATA).json()
	if res_json["ret"] != 0:
		return {
			"code": -1,
			"msg": "GG，腾讯接口不能用了！本接口将暂时关闭，等待主人debug！"
		}

	data = json.loads(res_json["archive"])
	area_list = data["areaTree"]
	# 先判断是否是国家
	if country:
		for country_item in area_list:
			if country_item["name"] in country:
				return disease_data_dict2str(country_item)
		else:
			return {
				"code": 0,
				"msg": "hh，{}暂时还没有疫情数据哦~".format(country)
			}
	# 接下来省份是肯定有的
	assert isinstance(province, str), "这个地方怎么可能没有省份数据呢？"
	province_list = area_list[0]["children"]
	for province_item in province_list:
		if province_item["name"] in province:
			if not city:
				return disease_data_dict2str(province_item)

			elif city == "市辖区": # 国标里有市辖区做虚拟二级市，此时county不为空
				assert county, "这个地方怎么可能没有区级数据呢？"
				for city_item in province_item["children"]:
					if city_item["name"] in county:
						return  disease_data_dict2str(city_item)
				else:
					return {
						"code": -3,
						"msg": "hh，{}{}暂时还没有疫情哦".format(province, county)
					}
			else:
				for city_item in province_item["children"]:
					if city_item["name"] in city: # 即使有county，目前也是没有相关信息的，所以直接返回！
						return disease_data_dict2str(city_item)
				else:
					return {
						"code": 0,
						"msg": "hh，{}{}暂时还没有疫情哦~".format(province, city)
					}

	else:
		return {
			"code": -2,
			"msg": "抱歉啊，你输入的省份[{}]没有找到哦！".format(province)
		}
