# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 19:53
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------

def match_full_area(area: str) -> dict:
	def match_full_area(s):
		return re.match(r'(.+?(?:自治区|行政区|省))?(.+?市)?(.+?(?:区|县))?', s).groups()

	province, city, county = match_full_area(area)
	if province is None and city is None and county is None:
		return {
			"matched": False
		}
	elif city in ["北京市", "上海市", "天津市", "重庆市"]:
		return {
			"matched":  True,
			1:          city,
			2:          "直辖市",
			3:          county
		}
	else:
		return {
			"matched":  True,
			1:          province,
			2:          city,
			3:          county
		}

def verify_full_area(province_str, city_str, county_str):
	results = []
	if province_str:
		for province_key, cities_list in area_dict.items():
			if province_str in province_key:
				if city_str:
					# 注意，国标里没有港澳台！
					for city_key, counties_dict in cities_dict.items():
						if city_str in city_key:
							if county_str:
								# 由于国标对直辖市设置了中间的”市辖区“虚二级单位，因此三级单位全部存在
								pass
								# for county_key
							else:
								return {
									"code": 0,
									"msg": {
										1: province_key,
										2: city_key,
									}
								}
					else:
						return {
							"code": -2,
							"msg": "No matched city key for {} in {}".format(city_str, province_key)
						}
				else:
					return {
						"code": 0,
						"msg": {
							1: province_key
						}
					}
		else:
			return {
				"code": -1,
				"msg": "No matched province key to {}".format(province_str)
			}

def init_area_set():
	"""
	该函数将地区的层次数据nest成一张map，目前没有用途
	:return:
	"""
	def _recursive_area(area_dict_to_go: dict, str_now: str):
		for k, v in area_dict_to_go.items():
			str_new =  "{}/{}".format(str_now, k) if str_now else k
			if v:
				for i in v:
					yield from _recursive_area(i,str_new)
			else:
				yield str_new

	area_dict = read_json_file(DATA_AREA_DICT_PATH)
	area_set = set(i for i in _recursive_area(area_dict, ""))
	return area_set

