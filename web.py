# coding: utf-8
# 웹처리부분

from util import *
from bs4  import BeautifulSoup as bs
import MultipartPostHandler
import urllib, urllib2, cookielib
import re
from multiprocessing import Process, Queue
import os
import sys
import winsound
import time


class WebProcess(Utility):
	def __init__(self):
		self.dTreeMenu = self.TreeMenuFromFile()
		self.bcode = "top"
		self.lItemList = [("top", "제목", "", self.dTreeMenu["top"][2])]
		self.GetInfo(self.lItemList[0])

# 웹탐색 관련
		self.ListInfo = {}
		self.ViewInfo = {}
		self.soup = None
		self.html = ""
		self.response = None
		self.opener = self.BuildOpener()


	def GetInfo(self, t):
		if "mail.php" in t[3] and "cmd=list" in t[3]:
			r = self.GetMailList(t)
		elif "mail.php" in t[3] and "cmd=view" in t[3]:
			r = self.GetMailView(t)
		elif "cmd=view" in t[3]:
			r = self.GetView(t)
		elif not ("bcode=" in t[3]):
			r = self.GetMenu(t)
		else:
			r = self.GetList(t)

		return r


	def GetMenu(self, t): # t는 lItemList의 원소 형식
		self.lItemList = []
		for c in t[3].split("|"):
			if not c in self.dTreeMenu: continue
			l = self.dTreeMenu[c]
			self.lItemList.append((c, unicode(l[0], "euc-kr", "ignore"), "", l[2]))
		self.bcode = t[0]
		return "menu" if l[0] else False


	def GetList(self, t):
# 게시물 목록 뽑아내기 / 게시판 코드가 있으면 bcode에 넣고 없으면 패스
		self.lItemList = []
		self.ListInfo.clear()
		self.ListInfo["host"] = re.sub(r"(?ims)^(http.?://[^/]+)(/.+)", r"\1", t[3])
		self.Get(t[3])
		self.ListInfo["url"] = self.response.url 
		links = self.soup("a", href=re.compile(r"(?ims)cmd=view"))
		if links is None: return False
		for l in links:
			href = ""
			title = ""
			author = ""
# 링크 주소를 href에 저장
			try:
						href = self.ListInfo["host"] + l["href"]
			except:
				pass
# 제목을 title에 저장
			try:
				title = l.get_text()
			except:
				pass
# 작성자를 author에 저장
			try:
				author = l.parent.next_sibling.next_sibling.get_text()
			except:
				pass
			if not author and (title == u"이용약관" or title == u"개인정보취급방침"): continue
			self.lItemList.append(("", title, author, href))
		if t[0]: self.bcode = t[0]
# 글쓰기 버튼 추출
		wlink = self.soup.find(name='a', href=re.compile(r'(?i)cmd=write'))
		if wlink is not None: self.ListInfo['write_url'] = self.ListInfo['host'] + wlink['href'] 
# 게시물 검색 action 주소를 ListInfo["find_action"]에 저장
		self.ListInfo["find_action"] = ""
		find = self.soup.find("form", attrs={"name":"form_search"})
		if find is not None: self.ListInfo["find_action"] = self.ListInfo["host"] + find["action"] 

		self.ViewInfo = {}
		return "list" if href else False


	def GetView(self, t):
		self.ViewInfo.clear()
		self.Get(t[3])
		self.ViewInfo["url"] = self.response.url

		tables = self.soup('table')

# 본문
		self.ViewInfo["content"] = ""
		try:
			title = tables[2].get_text()
			self.ViewInfo["content"] = '\r\n' + tables[2].get_text() + '\r\n' + tables[3].get_text()  
		except:
			pass

# 첨부파일
		dFiles = {}
		files = self.soup(name='a', href=re.compile(r'(?i)cmd=download'))
		for f in files:
			try:
				dFiles[f.img['alt']] = self.ListInfo['host'] + f['href']
			except:
				pass
		self.ViewInfo["files"] = dFiles

# 댓글
		try:
			self.ViewInfo['replies'] = ''
			if tables[6].td.get_text() == u'☞ 댓글':
				trs = tables[7].find_all('tr')
				for tr in trs:
					try:
						self.ViewInfo["replies"] += '\r\n[' + tr.td.get_text() + ']\r\n' + tr.td.next_sibling.next_sibling.get_text() + '\r\n' 
						if tr.td.next_sibling.next_sibling.next_sibling.next_sibling.a is not None: self.ViewInfo["replies"] += tr.td.next_sibling.next_sibling.next_sibling.next_sibling.a['title'] 
					except:
						pass
		except:
			pass

# 수정버튼 찾기'
		elink = self.soup.find(name='a', href=re.compile(r'(?i)cmd=edit'))
		if elink is not None: self.ViewInfo['edit_url'] = self.ListInfo['host'] + elink['href']
# 삭제버튼
		dellink = self.soup.find(name='a', href=re.compile(r'(?i)cmd=delete'))
		if elink is not None: self.ViewInfo['delete_url'] = self.ListInfo['host'] + dellink['href']

# 댓글 입력 관련 태그들
		self.ViewInfo["data"] = {}
		self.ViewInfo["action"] = ""
		form = self.soup.find(name='form', attrs={"name":"comment"})
		if form is not None:
			self.ViewInfo['action'] = self.ListInfo['host'] + form['action']
			self.ViewInfo["data"]["ccname"] = self.soup.find(name='input', attrs={"name":"ccname"})['value'].encode('euc-kr', 'ignore')
			hiddens = self.soup(name='input', type='hidden')
			for h in hiddens:
				self.ViewInfo["data"][h['name']] = h['value']

		return "view" if self.ViewInfo["content"] else False



	def GetMailList(self, t):
# 게시물 목록 뽑아내기 / 게시판 코드가 있으면 bcode에 넣고 없으면 패스
		self.lItemList = []
		self.ListInfo.clear()
		self.ListInfo["host"] = re.sub(r"(?ims)^(http.?://[^/]+)(/.+)", r"\1", t[3])
		self.Get(t[3])
		self.ListInfo["url"] = self.response.url
		links = self.soup("a", href=re.compile(r"(?ims)cmd=view"))
		if links is None: return False
		for l in links:
			href = ""
			title = ""
			author = ""
# 링크 주소를 href에 저장
			try:
						href = self.ListInfo["host"] + l["href"]
			except:
				pass
# 보낸이를 title에 저장
			try:
				author = l.get_text()
			except:
				pass
# 제목인지를 검사하고 title에 저장
			try:
				l2 = l.parent.next_sibling.next_sibling.a
				if l["href"] != l2["href"]: continue
				title = l2.get_text()
			except:
				continue

			if not author and (title == u"이용약관" or title == u"개인정보취급방침"): continue
			self.lItemList.append(("", title, author, href))
		if t[0]: self.bcode = t[0]
		return "list" if self.lItemList else False



	def GetMailView(self, t):
		self.ViewInfo.clear()
		self.Get(t[3])
		self.ViewInfo["url"] = self.response.url

		tables = self.soup('table')

# 본문
		self.ViewInfo["content"] = ""
		try:
			title = tables[3].get_text()
			self.ViewInfo["content"] = tables[3].get_text() + tables[4].get_text()  
		except:
			pass

# 첨부파일
		dFiles = {}
		files = self.soup(name='a', href=re.compile(r'(?i)cmd=download&'))
		for f in files:
			try:
				dFiles[f.get_text()] = "http://web.kbuwel.or.kr/menu/mail.php" + f['href']
			except:
				pass
		self.ViewInfo["files"] = dFiles

		self.ViewInfo["replies"] = ""

# 삭제버튼
		dellink = self.soup.find(name='a', href=re.compile(r'(?i)cmd=del2'))
		if dellink is not None: self.ViewInfo['delete_url'] = self.ListInfo['host'] + dellink['href']
		return "view" if self.ViewInfo["content"] else False


	def Get(self, url):
		if type(url) == unicode: url = url.encode("euc-kr", "ignore")
		self.response = self.opener.open(url)
		self.html = unicode(self.response.read(), "euc-kr", "ignore")
		self.soup = bs(self.html, "html.parser")


	def Post(self, url, d): 
		if type(url) == unicode: url = url.encode("euc-kr", "ignore")
		self.response = self.opener.open(url, d)
		self.html = unicode(self.response.read(), "euc-kr", "ignore")
		self.soup = bs(self.html, "html.parser")

	def BuildOpener(self):
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), MultipartPostHandler.MultipartPostHandler)
		urllib2.install_opener(opener)
		return opener

	def PageMove(self, down=True):
		base_url, d = self.ParamSplit(self.ListInfo["url"])
		# page 키가 없거나 값 없다면 page를 1로 설정
		if not ("page" in d) or not d["page"]: d["page"] = "1"
		if down == False and d["page"] <= "1": return False
		n = int(d["page"]) + 1 if down else int(d["page"]) - 1
		d["page"] = str(n)
		n_url = base_url + "?" + self.ParamJoin(d, False)
		title, p, href = self.dTreeMenu[self.bcode]
		self.GetInfo((self.bcode, title, "", n_url))
		return "list"


	def SaveReplies(self, memo):
		if not memo: return False
		self.ViewInfo["data"]["ccmemo"] = memo.encode('euc-kr', 'ignore')
		self.Post(self.ViewInfo["action"], self.ViewInfo["data"])
		self.GetInfo(("", "", "", self.ViewInfo["url"]))
		return True


class Upload(Process, WebProcess):
	def __init__(self, action, title, body, file, p_num, q):
		try:
			Process.__init__(self)
			Utility.__init__(self)
			WebProcess.__init__(self)
			if not action or not title or not body: return
			if type(action) == unicode: action = action.encode("euc-kr", "ignore")
			self.action = action 
			self.title = title.encode("euc-kr", "ignore")
			self.body = body.encode("euc-kr", "ignore")
			self.q = q
			self.p_num = p_num
			if file and os.path.exists(file): 
				self.file = file.encode("euc-kr", "ignore")
			else:
				self.file = ""
			if not self.KbuLogin(): return
			self.run()
		except:
			self.Play("error.wav", async=False)

	def KbuLogin(self):
		try:
			kbuid = self.Decrypt(self.ReadReg('kbuid'))
			kbupw = self.Decrypt(self.ReadReg('kbupw'))
			params = {"ret":"notice_top", "ret2":"", "cmd":"check_login", "log_id":kbuid, "log_passwd":kbupw}
			self.Post('http://web.kbuwel.or.kr/menu/login.php', params)
			if not("login=true" in self.soup.get_text()): return False
			return True
		except:
			return False

	def run(self):
		host, data = self.ParamSplit(self.action)
		data[u"제목".encode("euc-kr", "ignore")] = self.title
		data["tbody"] = self.body
		file = ""
		if self.file: 
			data["up_file1"] = open(self.file, "rb")
			file = self.file if type(self.file) == unicode else unicode(self.file, "euc-kr", "ignore")

		if file: self.q.put((0, u"업로드 중", file, 0, 0, self.p_num))
		self.Post(host, data)
		self.Play("up.wav", async=False)
		if file: self.q.put((100, u"업로드 완료", file, 0, 0, self.p_num))

		while True:
			time.sleep(1)


class Download(Process, WebProcess):
	def __init__(self, f, u, p_num, q):
		Process.__init__(self)
		Utility.__init__(self)
		WebProcess.__init__(self)

		self.Play("down_start.wav", async=False)
		self.q = q
		self.filename = f
		self.url = u if type(u) == str else u.encode("euc-kr", "ignore")
		self.downfolder = self.ReadReg("downfolder")
		if not self.downfolder: self.downfolder = "c:\\"
		self.p_num = p_num
		if not self.KbuLogin(): return
		self.run()
		while True:
			time.sleep(1)

	def KbuLogin(self):
		try:
			kbuid = self.Decrypt(self.ReadReg('kbuid'))
			kbupw = self.Decrypt(self.ReadReg('kbupw'))
			params = {"ret":"notice_top", "ret2":"", "cmd":"check_login", "log_id":kbuid, "log_passwd":kbupw}
			self.Post('http://web.kbuwel.or.kr/menu/login.php', params)
			if not("login=true" in self.soup.get_text()): return False
			return True
		except:
			self.Play("error.wav", async=False)
			return False


	def run(self):
		res = self.opener.open(self.url)
		meta = res.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		down_size = 0
		block_size = 1024 * 1024
		start_time = time.time()
		filepath = self.downfolder + "\\" + self.filename
		filepath = filepath.replace("\\\\", "\\")
# 로컬디스크에서 파일 크기를 보고 크기가 같으면 다운로드 종료
		if not os.path.exists(filepath) or os.path.getsize(filepath) != file_size:
			fp = open(filepath, "wb")
			file = self.filename if type(self.filename) == unicode else unicode(self.filename, "euc-kr", "ignore")
			self.q.put((0, u"다운로드 중", file, 0, 0, self.p_num)) 
			while True:
				buffer = res.read(block_size)
				if not buffer: break
				down_size += len(buffer)
				fp.write(buffer)
				per = down_size * 100.0 / file_size
				if per == 100: break
				t = time.time() - start_time
				if t <= 0: continue
				speed = down_size / t / 1024 / 1024
				remain = t * file_size / down_size
				self.q.put((per, u"다운로드 중", file, speed, remain, self.p_num))
# 다운완료라면
			fp.close()
			self.Play("down.wav", async=False)
			self.q.put((100.0, u"다운로드 완료", file, 0, 0, self.p_num))
		else:
			self.Play("down.wav", async=False)
			self.q.put((100.0, u"다운로드 완료", u"파일이름", 0, 0, self.p_num))



class SendMail(Process, WebProcess):
	def __init__(self, receiver, coreceiver, title, body, file1, file2, file3, p_num, q):
#		try:
			Process.__init__(self)
			Utility.__init__(self)
			WebProcess.__init__(self)
			self.p_num = p_num
			self.action = u"http://web.kbuwel.or.kr/menu/mail.php?cmd=send&".encode("euc-kr", "ignore")
			self.receiver = receiver.encode("euc-kr", "ignore")
			self.coreceiver = coreceiver.encode("euc-kr", "ignore") if coreceiver else ""
			self.title = title.encode("euc-kr", "ignore")
			self.body = body.encode("euc-kr", "ignore")
			self.q = q
			if file1 and os.path.exists(file1): 
				self.file1 = file1.encode("euc-kr", "ignore")
			else:
				self.file1 = ""
			if file2 and os.path.exists(file2): 
				self.file2 = file2.encode("euc-kr", "ignore")
			else:
				self.file2 = ""
			if file3 and os.path.exists(file3): 
				self.file3 = file3.encode("euc-kr", "ignore")
			else:
				self.file3 = ""

			if not self.KbuLogin(): return
			self.run()
#		except:
#			self.Play("error.wav", async=False)

	def KbuLogin(self):
		try:
			kbuid = self.Decrypt(self.ReadReg('kbuid'))
			kbupw = self.Decrypt(self.ReadReg('kbupw'))
			params = {"ret":"notice_top", "ret2":"", "cmd":"check_login", "log_id":kbuid, "log_passwd":kbupw}
			self.Post('http://web.kbuwel.or.kr/menu/login.php', params)
			if not("login=true" in self.soup.get_text()): return False
			return True
		except:
			return False

	def run(self):
		host, data = self.ParamSplit(self.action)
		data[u"받는사람".encode("euc-kr", "ignore")] = self.receiver
		if self.coreceiver: data[u"함께받는이".encode("euc-kr", "ignore")] = self.coreceiver
		data[u"제목".encode("euc-kr", "ignore")] = self.title
		data[u"태그".encode("euc-kr", "ignore")] = u"2".encode("euc-kr", "ignore")

		data["tbody"] = self.body
		if self.file1: data["up_file1"] = open(self.file1, "rb")
		if self.file2: data["up_file2"] = open(self.file2, "rb")
		if self.file3: data["up_file3"] = open(self.file3, "rb")
		file = ""
		if self.file1 or self.file2 or self.file3:
			file = self.file1 + "|" + self.file2 + "|" + self.file3
		if type(file) == str: file = unicode(file, "euc-kr", "ignore")

		if file: self.q.put((0, u"업로드 중", file, 0, 0, self.p_num))
		self.Post(host, data)
		self.Play("up.wav", async=False)
		if file: self.q.put((100, u"업로드 완료", file, 0, 0, self.p_num))
		while True:
			time.sleep(1)
