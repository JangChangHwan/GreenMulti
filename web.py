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
		files = self.soup(name='a', href=re.compile(r'(?i)cmd=download'))
		for f in files:
			try:
				dFiles[f.img['alt']] = self.ListInfo['host'] + f['href']
			except:
				pass
		self.ViewInfo["files"] = dFiles

		self.ViewInfo["replies"] = ""

# 삭제버튼
		dellink = self.soup.find(name='a', href=re.compile(r'(?i)cmd=del2'))
		if dellink is not None: self.ViewInfo['delete_url'] = self.ListInfo['host'] + dellink['href']
		return "view" if self.ViewInfo["content"] else False


	def Get(self, url):
		url2 = url
		try:
			url = url.encode("euc-kr", "ignore")
		except:
			url = url2

		self.response = self.opener.open(url)
		self.html = unicode(self.response.read(), "euc-kr", "ignore")
		self.soup = bs(self.html, "html.parser")


	def Post(self, url, d): 
		url2 = url
		try:
			url = url.encode("euc-kr", "ignore")
		except:
			url = url2

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
	def __init__(self, action, title, body, file, q):
		try:
			Process.__init__(self)
			Utility.__init__(self)
			WebProcess.__init__(self)
			if not action or not title or not body: return
			self.action = action.encode("euc-kr", "ignore")
			self.title = title.encode("euc-kr", "ignore")
			self.body = body.encode("euc-kr", "ignore")
			self.q = q
			if file and os.path.exists(file): 
				self.file = file.encode("euc-kr", "ignore")
			else:
				self.file = False
			if not self.KbuLogin(): return
			self.run()
		except:
			self.Play("error.wav", async=False)

	def KbuLogin(self):
#		try:
			kbuid = self.Decrypt(self.ReadReg('kbuid'))
			kbupw = self.Decrypt(self.ReadReg('kbupw'))
			params = {"ret":"notice_top", "ret2":"", "cmd":"check_login", "log_id":kbuid, "log_passwd":kbupw}
			self.Post('http://web.kbuwel.or.kr/menu/login.php', params)
			if not("login=true" in self.soup.get_text()): return False
			return True
#		except:
#			return False

	def run(self):
		host, data = self.ParamSplit(self.action)
		data[u"제목".encode("euc-kr", "ignore")] = self.title
		data["tbody"] = self.body
		if self.file: data["up_file1"] = open(self.file, "rb")
		self.q.put((0, u"업로드 중", self.file, 0, 0))
		self.Post(host, data)
		self.q.put((100, u"업로드 완료", self.file, 0, 0))
		self.Play("up.wav", async=False)



class Download(Process, WebProcess):
	def __init__(self, f, u, q):
		Process.__init__(self)
		Utility.__init__(self)
		WebProcess.__init__(self)

		self.Play("down_start.wav")
		self.q = q
		self.filename = f
		self.url = u
		self.downfolder = self.ReadReg("downfolder")
		if not self.downfolder: self.downfolder = "C:\\"
		if not self.KbuLogin(): return
		self.run()

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
			self.q.put((0, u"다운로드 중", self.filename, 0, 0)) # (up/down, filename, speed, remain)
			while True:
				buffer = res.read(block_size)
				if not buffer: break
				down_size += len(buffer)
				fp.write(buffer)
				per = down_size * 100.0 / file_size
				t = time.time() - start_time
				speed = down_size / t / 1024 / 1024
				remain = t * file_size / down_size
				self.q.put((per, u"다운로드 중", self.filename, speed, remain))
# 다운완료라면
			fp.close()
			self.q.put((100.0, u"다운로드 완료", self.filename, 0, 0))
		self.Play("down.wav", async=False)


