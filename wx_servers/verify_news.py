# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/3 19:17
# @Author	   : Mark Shawn
# @Email		: shawninjuly@gmai.com
# ------------------------------------
from logs.log import logger
from wx_servers.CONST import *

import requests
import json



def _search_fact(title: str):
	# api调用状态码肯定200，直接看code码即可
	res_json = requests.get(url=VERIFY_NEWS_URL, params={"title": title, "num": 0}, headers=VERIFY_NEWS_HEADERS).json()

	if res_json["code"] != 0:
		return {
			"code": -2,
			"title": title,
			"reason": "返回码出错: {}".format(res_json)
		}
	if res_json["total"] == 0:
		return {
			"code": -3,
			"title": title,
			"reason": "搜索显示没有结果，请考虑使用更简单的关键词"
		}
	if res_json["total"] > THRESHOLD_CONTENT_CNT:
		return {
			"code": -4,
			"title": title,
			"reason": "搜索显示结果过多，共有{}条".format(res_json["total"])
		}

	# 返回第一条（最相关）消息
	return {
		"code": 0,
		"title": title,
		"reason": res_json["content"][0]
	}


def verify_news(title):

	def _cut_abstract(abstract: str):
		if len(abstract) > CUT_ABSTRACT_LEN:
			return abstract[: CUT_ABSTRACT_LEN] + "..."
		return abstract

	# SAMPLE RESPONSE FROM JIAOZHEN
	"""
	{'code': 0,
	 'content': [{'_id': '27c8b50125ad0f313b17199b6e061cdd',
	              '_index': 'jiaozhen',
	              '_score': 1.8531526,
	              '_source': {'abstract': '耳朵发热是大脑发出的暗号，告诉你发烧这一侧的大脑正在忙。连接着身体和大脑的颈动脉负责向大脑输送血液，而当血液流经颈动脉的时候，会有一部分血液分流到耳朵，在耳朵上完成循环。如果恰巧这时候你在用脑思考，那么大脑的需氧量会上升，血流自然也就会比较多，这一侧耳朵的血流增加，就会使耳朵出现发热的情况。\n'
	                                      '当然还有一些其他情况，也容易让人出现耳朵热的情况，比如剧烈运动后大脑皮质高度兴奋，用手机打电话过久等等。',
	                          'author': '科普中国',
	                          'authordesc': '中国科协为深入推进科普信息化建设而塑造的全新品牌',
	                          'cover': 'http://p.qpic.cn/jiaozhen/0/fae803cf8e9745af824bfa38f67178ea/0',
	                          'date': '2019-10-23',
	                          'id': '27c8b50125ad0f313b17199b6e061cdd',
	                          'oriurl': 'http://mp.weixin.qq.com/s?__biz=MjA1ODMxMDQwMQ==&mid=2657266485&idx=3&sn=43cc3fceff1ad0c086107ccfc7a7bed0&chksm=4906af5b7e71264dcf97ae74a3f2549df81527af6820d0142ba6daf0b7912c1a1d985bff8420&3rd=MjM5NzM2NjUzNg==&scene=8#rd',
	                          'result': '假-伪科学',
	                          'source': '科普中国',
	                          'title': '耳朵发热是有人想你',
	                          'updatedAt': '2019-11-03 07:44:40'},
	              '_type': 'article',
	              'sort': [1.8531526, 77593]}],
	 'total': 1}
	"""

	res_verify_news = _search_fact(title)
	if res_verify_news["code"] == 0:
		data_dict = json.loads(res_verify_news["reason"])["_source"]
		reply_text = '注意：这个『{}』可能是『{}』，这里有详细的报道：{}\n更多可以了解：{}\n--来自腾讯较真平台'.format(
			title, data_dict["result"], _cut_abstract(data_dict["abstract"]), data_dict['oriurl'])
		logger.info("Replied: {}".format(reply_text))
		return True, reply_text
	else:
		logger.debug("Muted: {}".format(res_verify_news))
		return False, res_verify_news["reason"]



if __name__ == '__main__':
	verify_news("武汉肺炎")