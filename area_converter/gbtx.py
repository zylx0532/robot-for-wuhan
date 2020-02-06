# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/5 15:06
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# --------------------------------
from area_converter.utlis import *


class GBTX(object):

	def __init__(self):

		self._global_countries       = read_json_file(GLOBAL_COUNTRIES_DICT_PATH)
		self._global_cities          = read_json_file(GLOBAL_CITIES_DICT_PATH)
		self._gb_dict                = read_json_file(GB_NESTED_AREA_DICT_PATH_TO_READ)

		self._update_tx_disease_data()
		self._initialize_cn_path_map()

	def _update_tx_disease_data(self):
		res_json = requests.get(API_TX_DISEASE_DATA)
		assert res_json.status_code == 200
		data = json.loads(res_json.json()["data"])
		area_list = data["areaTree"]
		self.china_area_disease     = area_list[0].pop("children")
		self.global_area_disease    = area_list
		self.time_tx_disease_data_updated = time.time()

	def _initialize_cn_path_map(self):
		self.tx_dict                = self._tx_cn_list2dict(self.china_area_disease)
		self.sorted_cn_path_map     = self._shadow_cn_path_map(self._gb_dict, self.tx_dict)

	@classmethod
	def _match_contains(cls, search_key: str, iterator: [set, dict, tuple], nest: bool) -> [bool, str]:
		"""
		必须要两遍搜索，主要是解决集合过滤的问题
		:param search_key:
		:param iterator:
		:param nest:
		:return:
		"""
		if not nest:
			for key in iterator:
				if search_key == key:
					return True, key
			for key in iterator:
				if key in search_key:
					return True, key
			return False, search_key
		if nest:
			search_key_nested = re_sub_area_name(search_key)
			for key in iterator:
				key_nested = re_sub_area_name(key)
				if key_nested == search_key_nested:
					return True, key
			for key in iterator:
				key_nested = re_sub_area_name(key)
				if key_nested in search_key_nested:
					return True, key
			return False, search_key

	@staticmethod
	def _tx_cn_list2dict(tx_area_list: list):
		def _convert(tx_area_data_list: list, converted_dict=None):
			converted_dict = dict() if not converted_dict else converted_dict
			for tx_area_item in tx_area_data_list:
				converted_dict[tx_area_item["name"]] = _convert(tx_area_item.get("children", []), dict())
			return converted_dict
		return _convert(tx_area_list)

	def is_a_country(self, keyword: str) -> [bool, str]:
		return simple_match_in(keyword, self._global_countries.values())

	def is_a_city(self, keyword: str) -> [bool, str]:
		return simple_match_in(keyword, self._global_cities.values())

	def _shadow_cn_path_map(self, from_dict_like_gb: dict, to_dict_like_tx: dict,
	                        output_map=None, cur_path_from=(), cur_path_to=(), sort=True):
		"""
		该函数用来生成一个国标与对应字典结合的映射表，非常重要
		并且记得，最后再排个序
		:param from_dict_like_gb:
		:param to_dict_like_tx:
		:param output_map:
		:param cur_path_from:
		:param cur_path_to:
		:return:
		"""

		def search_key_try(from_key, to_key_set, choose_nest):
			status, to_key_matched = self._match_contains(from_key, to_key_set, choose_nest)
			if status:
				to_key_set.remove(to_key_matched)
				new_path_to = cur_path_to + (to_key_matched,)
				output_map[from_full_name] = {
					"path_from": new_path_from,
					"path_to": new_path_to,
				}
				self._shadow_cn_path_map(from_dict_like_gb[from_key], to_dict_like_tx[to_key_matched], output_map,
				                         new_path_from, new_path_to)
				return True

		def sort_cn_path_map(cn_path_map):
			return dict(sorted(cn_path_map.items(), key=lambda x: max(len(x[1]["path_from"]), len(x[1]["path_to"]))))

		output_map = output_map if output_map else dict()
		to_key_set = set(to_dict_like_tx)

		for from_key in list(from_dict_like_gb):
			# assert from_key != "湖北省恩施土家族苗族自治州"
			new_path_from = cur_path_from + (from_key,)
			from_full_name = "".join(new_path_from)

			if not search_key_try(from_key, to_key_set, False):
				if not search_key_try(from_key, to_key_set, True):
					output_map[from_full_name] = {"path_from": new_path_from, "path_to": ()}
					self._shadow_cn_path_map(from_dict_like_gb[from_key], dict(), output_map, new_path_from, ())

		for to_key_remaining in to_key_set:
			new_path_to = cur_path_to + (to_key_remaining, )
			to_full_name = "".join(new_path_to)
			output_map[to_full_name] = {
				"path_from": (),
				"path_to": new_path_to
			}
			self._shadow_cn_path_map(dict(), to_dict_like_tx[to_key_remaining], output_map, (), new_path_to)
		cn_path_map = sort_cn_path_map(output_map) if sort else output_map
		return sort_cn_path_map(cn_path_map)

	def _get_cn_disease_data(self, area_path: tuple) -> dict:
		data = {"children": self.china_area_disease}
		for key in area_path:
			for item in data["children"]:
				if item["name"] == key:
					data = item
					break
		return data

	def _get_accurate_disease_data_all(self, input_list: list):
		if input_list:
			return list(map(self._get_cn_disease_data, input_list))


	def _search_key_in_path_map(self, search_key: str, path_map: dict, nest=False, result=None, LEVEL_LIMIT=5)\
			-> [STATUS.status, [None, list]]:
		result = result if result else []
		search_key = search_key if not nest else re_sub_area_name(search_key)

		# 寻找直接匹配的地区全名
		for area_full_name, area_info in path_map.items():
			path_to = area_info["path_to"]
			if max(len(path_to), len(area_info["path_from"])) > LEVEL_LIMIT:
				break
			area_full_name_to_search = area_full_name if not nest else re_sub_area_name(area_full_name)
			if search_key in area_full_name_to_search:
				result.append(path_to)
				LEVEL_LIMIT = len(path_to)

		if not result:
			return STATUS.CN_NOT_FOUND, None

		filtered_searched_result = list(filter(lambda x: x, result))
		if not filtered_searched_result:
			return STATUS.VALID_WITHOUT_DATA, None
		return STATUS.VALID_WITH_DATA, filtered_searched_result

	def search_china_area(self, search_key: str) -> [STATUS.status, [None, list]]:
		if not search_key:
			return STATUS.NO_VALID_INFO, None

		for nest in [False, True]:
			s, v = self._search_key_in_path_map(search_key, self.sorted_cn_path_map , nest)
			if s.code > 0:
				return s, v

		return STATUS.CN_NOT_FOUND, None

	def search_global_area(self, search_key: str) -> [STATUS.status, [None, list]]:

		# 否则看看是不是国家
		is_country, area_name = self.is_a_country(search_key)
		if is_country:
			return STATUS.GLOBAL_COUNTRY_NOT_INFECTED, None

		# 再看是不是城市
		is_city, city_name = self.is_a_city(search_key)
		if is_city:
			return STATUS.GLOBAL_CITY_FOUND, None
		return STATUS.GLOBAL_CITY_NOT_FOUND, None

	def search_disease_by_area(self, search_key: str) -> [STATUS.status, [None, dict]]:
		##################### 更新表 ########################
		if time.time() - self.time_tx_disease_data_updated > DATA_TIMEOUT:
			self._update_tx_disease_data()

		###################    预 处 理   ####################
		search_key = re.sub("[^\u4e00-\u9fa5]*", "", search_key)            # 去除非中文
		search_key = SPECIAL_CASES.get(search_key, search_key)   # 替换特例

		##################### 先遍历感染疫情的目标国家字典 ##### 解决“中国”bug
		country_items = [country_item for country_item in self.global_area_disease if search_key in country_item["name"]]
		if country_items:
			return STATUS.GLOBAL_COUNTRY_INFECTED, country_items

		##################### 搜国内 #########################
		k, v = self.search_china_area(search_key)
		if k.code > 0:
			return k, self._get_accurate_disease_data_all(v)

		##################### 搜全球 #########################
		return self.search_global_area(search_key)


if __name__ == '__main__':
	gbtx = GBTX()