# -*- coding: utf-8 -*-
# -----------------------------------
# @CreateTime   : 2020/2/2 16:20
# @Author       : Mark Shawn
# @Email        : shawninjuly@gmai.com
# ------------------------------------
from wx_robot.utils import *
from wx_robot.connect_servers import start_servers

from wxpy import *

class MyBot(Bot):

	def __init__(self, *args, **kwargs):
		super().__init__(
			cache_path=WX_COOKIE_PATH,
			qr_path=WX_QR_PATH,
			logout_callback=self.log_out_callback
		)
		# 将log发送给自己的文件助手
		self.my_fh                  = self.file_helper
		self.my_log                 = get_wechat_logger(self, level=logging.DEBUG, name="WXPY")

		# 添加PUID路径，用于追溯用户ID的唯一标识
		self.enable_puid(WX_PUID_PATH)
		self.target_group_keys      = WX_TARGET_GROUP_KEYS
		self.target_groups          = []


		self.verified_msgs_dict     = dict()    # TODO 设置一个固定长的字典队列

		self.start_servers          = start_servers
		self.enable_verify_news     = ENABLE_VERIFY_NEWS        # 辟谣
		self.enable_check_disease   = ENABLE_CHECK_DISEASE      # 疫情数据
		self.enable_check_transport = ENABLE_CHECK_TRANSPORT    # 出行人数据

		self.send_greetings         = SEND_GREETING
		self.born_time              = time.time()


	def run(self):
		self.my_log.info("Welcome to use Robot-For-Wuhan ~")
		# self.born_time = time.time() - 60 * 60
		# self.send_greetings = True
		self.load_groups_to_monitor()
		self.start_servers(self)
		embed()


	def load_groups_to_monitor(self):
		for search_key in self.target_group_keys:
			try:
				searched_group = ensure_one(self.groups().search(search_key))  # type: Group
			except:
				self.my_log.error("Failed to load group with key {}".format(search_key))
			else:
				self.target_groups.append(searched_group)
				self.my_log.info("Loaded group {} ~".format(searched_group.name, search_key))

				if self.send_greetings:
					searched_group.send(TEMPLATE_LOG_IN_GREETING)

	def log_out(self):
		"""
		这个函数是我们手动设置的登出命令，系统默认的登出命令是self.logout()
		:return:
		"""
		self.lifetime = (time.time() - self.born_time) / 60
		if self.send_greetings:
			for target_group in self.target_groups:
				target_group.send("收到！我这就下线，感谢有大家陪伴的{:.2f}分钟，我们下次再见~".format(self.lifetime))
		self.logout()

	def log_out_callback(self):
		"""
		这个函数是在机器人登出后才会运行的
		由于登出后无法再向自己的文件助手发送消息，因此就不做扩展了
		:return:
		"""
		pass


if __name__ == '__main__':
	my_bot = MyBot()
	my_bot.run()



# wxpy.Bot()对象的参数
"""
classwxpy.Bot(cache_path=None, console_qr=False, qr_path=None, qr_callback=None, login_callback=None, logout_callback=None)
cache_path –
设置当前会话的缓存路径，并开启缓存功能；为 None (默认) 则不开启缓存功能。
开启缓存后可在短时间内避免重复扫码，缓存失效时会重新要求登陆。
设为 True 时，使用默认的缓存路径 ‘wxpy.pkl’。
console_qr –
在终端中显示登陆二维码，需要安装 pillow 模块 (pip3 install pillow)。
可为整数(int)，表示二维码单元格的宽度，通常为 2 (当被设为 True 时，也将在内部当作 2)。
也可为负数，表示以反色显示二维码，适用于浅底深字的命令行界面。
例如: 在大部分 Linux 系统中可设为 True 或 2，而在 macOS Terminal 的默认白底配色中，应设为 -2。
qr_path – 保存二维码的路径
qr_callback – 获得二维码后的回调，可以用来定义二维码的处理方式，接收参数: uuid, status, qrcode
login_callback – 登陆成功后的回调，若不指定，将进行清屏操作，并删除二维码文件
logout_callback – 登出时的回调
"""

# 注意如果receiver为空将开启一个新的机器人！
"""
wxpy.get_wechat_logger(receiver=None, name=None, level=30)
receiver –
当为 None, True 或字符串时，将以该值作为 cache_path 参数启动一个新的机器人，并发送到该机器人的”文件传输助手”
当为 机器人 时，将发送到该机器人的”文件传输助手”
当为 聊天对象 时，将发送到该聊天对象
name – Logger 名称
level – Logger 等级，默认为 logging.WARNING
"""

# 消息的主要属性
"""
Message.bot
接收此消息的 机器人对象

Message.id
消息的唯一 ID (通常为大于 0 的 64 位整型)

内容数据
Message.text
消息的文本内容

Message.get_file(save_path=None)[源代码]
下载图片、视频、语音、附件消息中的文件内容。

可与 Message.file_name 配合使用。

参数:	save_path – 文件的保存路径。若为 None，将直接返回字节数据
Message.file_name
消息中文件的文件名

Message.file_size
消息中文件的体积大小

Message.media_id
文件类消息中的文件资源 ID (但图片视频语音等其他消息中为空)

Message.raw
原始数据 (dict 数据)

用户相关
Message.chat
消息所在的聊天会话，即:

对于自己发送的消息，为消息的接收者
对于别人发送的消息，为消息的发送者
返回类型:	wxpy.User, wxpy.Group
Message.sender
消息的发送者

返回类型:	wxpy.User, wxpy.Group
Message.receiver
消息的接收者

返回类型:	wxpy.User, wxpy.Group
Message.member
若消息来自群聊，则此属性为消息的实际发送人(具体的群成员)
若消息来自其他聊天对象(非群聊)，则此属性为 None
返回类型:	NoneType, wxpy.Member
Message.card
好友请求中的请求用户
名片消息中的推荐用户
群聊相关
Message.member
若消息来自群聊，则此属性为消息的实际发送人(具体的群成员)
若消息来自其他聊天对象(非群聊)，则此属性为 None
返回类型:	NoneType, wxpy.Member
Message.is_at
当消息来自群聊，且被 @ 时，为 True

时间相关
Message.create_time
服务端发送时间

Message.receive_time
本地接收时间

Message.latency
消息的延迟秒数 (发送时间和接收时间的差值)

其他属性
Message.url
分享类消息中的网页 URL

Message.articles
公众号推送中的文章列表 (首篇的 标题/地址 与消息中的 text/url 相同)

其中，每篇文章均有以下属性:

title: 标题
summary: 摘要
url: 文章 URL
cover: 封面或缩略图 URL
Message.location
位置消息中的地理位置信息

Message.img_height
图片高度

Message.img_width
图片宽度

Message.play_length
视频长度

Message.voice_length
语音长度
"""