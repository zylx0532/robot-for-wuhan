# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/4 13:48
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from settings_base import *
import random

"""
消息尾巴
"""
TEMPLATE_RANDOM_MSG_TAIL_LIST   =  [
	"-------------------\n",
]

"""
一些控制命令模板，业务模板请去 wx_servers.CONST 修改
"""

TEMPLATE_LOG_IN_GREETING        = "大家好，我是武汉疫情机器人，特为您提供[查XX]命令查询地区疫情，如需帮助请回复帮助，新年快乐~"
TEMPLATE_LOG_OUT_GREETING       = "收到退出命令，正在下线，bye bye ~"

TEMPLATE_API_FAILED             = "哎呀，服务器好像出错了，IT小哥正在赶在路上啦，我去催催他/她/它快来救我！"
TEMPLATE_NO_KEYWORD             = "您要查啥呢？不如试试查一些城市的疫情数据？比如 『查武汉』=.="

def random_tail(is_sucess=True):
	SUCCESS = [
		"这是你想要的答案吗~",
		"使命必达先生保证完成任务！",
		"如果对本次服务还满意的话，不如给我点个赞吧~",
		"( •̀ ω •́ )，我就知道你会问这个问题~",

		# TODO 多一些模板
		"我猜你是在为难我胖虎，哼哼~",
		"如果我是哆啦A梦就好了，就能知道你到底想要知道什么了！",
		"欸，这是我第九千九百九十一次没有帮别人查到什么了...我是不是很失败...",
		"再来一次，你一定能成功的，我相信你！",
	]
	if is_sucess:
		return random.choice(SUCCESS)
	else:
		return random.choice(FAILURE)

