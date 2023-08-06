import requests
import json
class getinfo:
	json=''
	workjs=''
	def __init__(self,av,bv,uid):
		self.av=av
		self.bv=bv
		self.uid=uid


	def translate(self,x):#将bv号转为av
		table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
		tr={}
		for i in range(58):
			tr[table[i]]=i
		s=[11,10,3,8,4,6]
		xor=177451812
		add=8728348608
		r=0
		for i in range(6):
			r+=tr[x[s[i]]]*58**i
		self.bv=(r-add)^xor
		

	def workinfos(self):
		if(self.bv==""):
			print("bv不存在,请输入bv")
			return None
		else:
			url="http://api.bilibili.com/archive_stat/stat?aid="+str(self.bv)
			p=requests.get(url)
			self.workjs=p.json()
			return self.workjs

	def list_all_member(self):
		for name,value in vars(self).items():
			print('%s=%s'%(name,value))

	def workdraw():
		print("{'code': 0, 'message': '0', 'ttl': 1, 'data': {'aid': 97141821, 'view': 128, 'danmaku': 0, 'reply': 7, 'favorite': 3, 'coin': 13, 'share': 0, 'now_rank': 0, 'his_rank': 0, 'like': 13, 'dislike': 0, 'no_reprint': 1, 'copyright': 1}}")

	
	def authorinfos(self,types):
		if(self.uid==""):
			print("uid不存在,请输入uid")
		else:
			url="http://space.bilibili.com/ajax/member/getSubmitVideos?mid="+str(self.uid)
			p=requests.get(url)
			self.authorjs=p.json()
			if(types!=""):
				self.lists=[]
				for i in range(0,len(self.authorjs["data"]['vlist'])):
					self.lists.append(self.authorjs["data"]['vlist'][i][types])
				return self.lists
			return self.authorjs

	def authordraw(self):
		print(" 'vlist': [{'comment': 7, 'typeid': 173, 'play': 128, 'pic': '//i1.hdslb.com/bfs/archive/f1d364ed703f0f2a951db10bfa5559dd0bd93cf1.jpg', 'subtitle': '', 'description': '炉石传说\nqq: 2534829508 欢迎一起快乐炉石', 'copyright': '', 'title': '来自剽窃贼最后的倔强！！', 'review': 0, 'author': 'panda_face', 'mid': 349550991, 'is_union_video': 0, 'created': 1584561866, 'length': '08:23', 'video_review': 0, 'is_pay': 0, 'favorites': 3, 'aid': 97141821, 'is_steins_gate': 0, 'hide_click': False}], 'count': 1, 'pages': 1}")

	def videoinfos(self,oid,types):#oid可以通过workid中的aid获取
		if(oid==""):
			print("oid不存在,请输入oid")
			return None
		else:
			url="https://api.bilibili.com/x/v2/reply?&type=1&pn=1&oid=498082939"
			p=requests.get(url)
			self.videojs=p.json()
			if(types=='message'):
				self.lists=[]
				for i in range(len(self.videojs['data']['replies'])):
					self.lists.append(self.videojs['data']['replies'][i]['content']['message'])
				return self.lists
			else:
				return self.videojs
	def getgoodjson(self,js):
		jsgood=json.dumps(js,indent=1,ensure_ascii=False)
		print(jsgood)



