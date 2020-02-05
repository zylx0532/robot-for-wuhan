# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/5 6:25
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from common.json import write_json_file
from common.fetch import get_json
from wx_servers.CONST import *
import time
import json
import re

AREA_SPLIT_WORDS_LIST = [     # 长的词要在前面
	"特别行政区",
	"自治州", "自治区", "自治县",
	"新区",                          # 这个可以匹配浦东
	"省", "市", "县", "区"
]
SPECIAL_AREA_CASES = {
	"全国": "中国",
}



def _gen_area_dict_from_area_tree(area_tree: list, cur_area_dict: dict=dict(), cur_area_chain: str="") -> dict:
	"""
	该函数用于将腾讯的地区数据列表转为重新结构化的地区数据字典，以实现多种用途
	:param area_tree:
	:param cur_area_dict:
	:param cur_area_chain:
	:return:
	"""
	for area_info in area_tree:
		area_name = area_info["name"]
		area_chain = cur_area_chain + area_name
		cur_area_dict[area_name] = {
			"name": area_name,
			"total": area_info["total"],
			"today": area_info["today"],
			"name_chain": area_chain,
		}
		if area_info.get("children"):
			_gen_area_dict_from_area_tree(area_info["children"], cur_area_dict, area_chain)
	return cur_area_dict


def fetch_disease_data() :
	"""
	这个函数建议每10分钟或者1小时运行一次，生成本地全局字典
	以减轻服务器压力，提高程序运行效率
	:return:
	"""
	global server_enable_check_disease
	global global_area_dict
	if server_enable_check_disease:
		data = get_json(API_TX_DISEASE_DATA)

		# 返回码不为0直接关闭服务
		if data["ret"] != 0:
			server_enable_check_disease = False
			err_log_path = os.path.join(WX_SERVER_DATA_DIR, "{}_error.log".format(int(time.time())))
			write_json_file(data, err_log_path)
			return {
				"code": data["ret"],
				"msg": "ERROR！返回码不为0！已保存log到{}.".format(err_log_path)
		}

		data = json.loads(data["data"])
		area_tree = data["areaTree"]
		global_area_dict = _gen_area_dict_from_area_tree(area_tree)
		return {
			"code": 0,
			"msg": "SUCCESS! 成功生成地区字典 ~"
		}
	return {
		"code": -1,
		"msg": "ERROR! 服务已关闭！详情请查询日志，目录为{}.".format(WX_SERVER_DATA_DIR)
	}


def _area_disease_template(item: dict) -> str:
	def _translate(data_item: dict) -> str:
		translated = "确认{}人，死亡{}人，治愈{}人".format(data_item["confirm"], data_item["dead"], data_item["heal"])
		if data_item["suspect"] > 0:
			translated += "，嫌疑{}人".format(data_item["suspect"])
		return translated

	disease_data_str = item["name"]
	disease_data_str += "今日{}；".format(_translate(item["today"]))
	disease_data_str += "总计{}。".format(_translate(item["total"]))
	disease_data_str += "🙏🙏"
	return disease_data_str


def check_disease_by_area(area_input):
	############## 初始化地区字典 ############
	if server_enable_check_disease and not global_area_dict:
		fetch_result = fetch_disease_data()
		if fetch_result["code"] != 0:
			return fetch_result
	############## 更新地区字典 ###############
	elif global_area_dict and time.time() - global_updated_time > AREA_DICT_TIMEOUT:
		fetch_result = fetch_disease_data()
		if fetch_result["code"] != 0:
			return fetch_result

	############## 分析用户输入 ##################
	# 特例转换
	area_input = SPECIAL_AREA_CASES.get(area_input, area_input)
	"""
	虽然以下对用户输入先切割再合成的处理，原目标是为了与腾讯的地区字典匹配，但显然这种思想是非常好的
	"""
	# 后缀切割
	area_chain = re.split("|".join(AREA_SPLIT_WORDS_LIST), area_input)
	area_chain = list(filter(lambda x: x, area_chain))
	# 空值返回
	if len(area_chain) == 0:
		return {
			"code": 0,
			"msg": "别调戏我啦，{}貌似不是一个有效地名哦~".format(area_input)
		}

	# 保留前三级分割的词语，因为只有国-省-市三个级别；并合成新的句子
	area_chain = area_chain[:3]
	area_concat = "".join(area_chain)

	# 先判断是否在字典的直接索引中
	if global_area_dict.get(area_concat):
		return {
			"code": 0,
			"msg": _area_disease_template(global_area_dict[area_concat])
		}

	multi_areas = [v for v in global_area_dict.values() if area_concat in v["name_chain"]]
	if not multi_areas:
		return {
			"code": 0,
			"msg": "咦？没有找到{}的数据哦，说不定还没被感染呢，哈哈那也太幸运了！".format(area_input)
		}

	if len(multi_areas) > MAX_AREA_RESULTS:
		multi_areas_template = "哎呀，这个地名咋这么热乎，有这么多结果，我都快分不清了，你看:\n"
		for area_seq, area_item in enumerate(multi_areas):
			area_seq = area_seq + 1
			if area_seq <= MAX_AREA_RESULTS:
				multi_areas_template += "{}. {}\n".format(area_seq, area_item["name_chain"])
			else:
				multi_areas_template += "...（以下省略{}条，Orz）".format(len(multi_areas) - MAX_AREA_RESULTS)
				break
		return {
			"code": 0,
			"msg":  multi_areas_template
		}

	# 只有一个的时候，直接返回
	if len(multi_areas) == 1:
		return {
			"code": 0,
			"msg": _area_disease_template(multi_areas[0])
		}

	# 有少数几个的时候也一起返回
	multi_areas_template_2 = "您要查询的{}有多个结果哦，我就给您一并返回啦：\n".format(area_input)
	for area_seq, area_item in enumerate(multi_areas):
		multi_areas_template_2 += "{}. {}\n".format(area_seq + 1, _area_disease_template(area_item))
	return {
		"code": 0,
		"msg": multi_areas_template_2
	}
