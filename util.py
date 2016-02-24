# coding: utf-8
# 함수모음 util.py

import sys
import re
import winsound
import os
import _winreg
import urllib
import wx
from threading import Thread
import time


class Utility():
	def __init__(self):
		self.key = "%x" % os.path.getctime(os.environ["APPDATA"])

	def TreeMenuFromFile(self):
		""" PageInfo.Dat 파일로부터 목록상자에 표시될 트리메뉴를 만듭니다. 반환값 : 사전 객체"""
		d = {
			"top": (u"초기화면".encode("euc-kr", "ignore"), "", "green|guide|mail|bbs|computer|potion|blindnews|magazin|pds"), 
			"green": (u"0. 초록등대".encode("euc-kr", "ignore"), "top", "green1|green2|green3|green4|green5|green6|green7|green8|green9|green99"), 
			"green1": (u"1. 공지사항".encode("euc-kr", "ignore"), "green", "http://web.kbuwel.or.kr/menu/index.php?mo=green&club=green&bcode=green1"), 
			"green2": (u"2. 나눔장터".encode("euc-kr", "ignore"), "green", "http://web.kbuwel.or.kr/menu/index.php?mo=green&club=green&bcode=green2"), 
			"green3": (u"3. 우리들의 이야기".encode("euc-kr", "ignore"), "green", "http://web.kbuwel.or.kr/menu/index.php?mo=green&club=green&bcode=green3"), 
			"green4": (u"4. 자료실".encode("euc-kr", "ignore"), "green", "green41|green42|green43|green44|green45|green46|green47"), 
			"green41": (u"1. 운영체제 / 드라이버".encode("euc-kr", "ignore"), "green4", "http://web.kbuwel.or.kr/menu/index.php?mo=green4&club=green&bcode=green41"), 
			"green42": (u"2. 일반 자료실".encode("euc-kr", "ignore"), "green4", "http://web.kbuwel.or.kr/menu/index.php?mo=green4&club=green&bcode=green42"), 
			"green43": (u"3. 포터블 자료실".encode("euc-kr", "ignore"), "green4", "http://web.kbuwel.or.kr/menu/index.php?mo=green4&club=green&bcode=green43"), 
			"green44": (u"4. 멀티미디어 / 인터넷".encode("euc-kr", "ignore"), "green4", "http://web.kbuwel.or.kr/menu/index.php?mo=green4&club=green&bcode=green44"), 
			"green45": (u"5. 프로그램 자동설치".encode("euc-kr", "ignore"), "green4", "http://web.kbuwel.or.kr/menu/index.php?mo=green4&club=green&bcode=green45"), 
			"green46": (u"6. 강의실".encode("euc-kr", "ignore"), "green4", "http://web.kbuwel.or.kr/menu/index.php?mo=green4&club=green&bcode=green46"), 
			"green47": (u"7. 기타자료실".encode("euc-kr", "ignore"), "green4", "http://web.kbuwel.or.kr/menu/index.php?mo=green4&club=green&bcode=green47"), 
			"green5": (u"5. 시각장애인 대학생 후원 희망통장".encode("euc-kr", "ignore"), "green", "green51|green52|green53"), 
			"green51": (u"1. 공지사항 및 후원내역".encode("euc-kr", "ignore"), "green5", "http://web.kbuwel.or.kr/menu/index.php?mo=green5&club=green&bcode=green51"), 
			"green52": (u"2. 포근한 이야기방".encode("euc-kr", "ignore"), "green5", "http://web.kbuwel.or.kr/menu/index.php?mo=green5&club=green&bcode=green52"),
			"green53": (u"3. 자료실".encode("euc-kr", "ignore"), "green5", "http://web.kbuwel.or.kr/menu/index.php?mo=green5&club=green&bcode=green53"),
			"green6": (u"6. 엔터테인먼트".encode("euc-kr", "ignore"), "green", "green61|green62|green63|green64|green65|green66|green67|green699"),
			"green61": (u"1. 가요".encode("euc-kr", "ignore"), "green6", "http://web.kbuwel.or.kr/menu/index.php?mo=green6&club=green&bcode=green61"),
			"green62": (u"2. 동영상".encode("euc-kr", "ignore"), "green6", "http://web.kbuwel.or.kr/menu/index.php?mo=green6&club=green&bcode=green62"),
			"green63": (u"3. 팝 / 클래식".encode("euc-kr", "ignore"), "green6", "http://web.kbuwel.or.kr/menu/index.php?mo=green6&club=green&bcode=green63"),
			"green64": (u"4. MR노래방".encode("euc-kr", "ignore"), "green6", "http://web.kbuwel.or.kr/menu/index.php?mo=green6&club=green&bcode=green64"),
			"green65": (u"5. 앨범".encode("euc-kr", "ignore"), "green6", "http://web.kbuwel.or.kr/menu/index.php?mo=green6&club=green&bcode=green65"),
			"green66": (u"6. 기타자료실".encode("euc-kr", "ignore"), "green6", "http://web.kbuwel.or.kr/menu/index.php?mo=green6&club=green&bcode=green66"),
			"green67": (u"7. 토렌트 파일".encode("euc-kr", "ignore"), "green6", "http://web.kbuwel.or.kr/menu/index.php?mo=green6&club=green&bcode=green67"),
			"green699": (u"8. 요청게시판".encode("euc-kr", "ignore"), "green6", "http://web.kbuwel.or.kr/menu/index.php?mo=green6&club=green&bcode=green699"),
			"green7": (u"7. 스카이프 친구등록".encode("euc-kr", "ignore"), "green", "http://web.kbuwel.or.kr/menu/index.php?mo=green&club=green&bcode=green7"), 
			"green8": (u"8. 건의함".encode("euc-kr", "ignore"), "green", "http://web.kbuwel.or.kr/menu/index.php?mo=green&club=green&bcode=green8"), 
			"green9": (u"9. 질문게시판".encode("euc-kr", "ignore"), "green", "http://web.kbuwel.or.kr/menu/index.php?mo=green&club=green&bcode=green9"), 
			"green99": (u"10. 회원가입".encode("euc-kr", "ignore"), "green", "http://web.kbuwel.or.kr/menu/index.php?cmd=club_join&mo=green&club=green&bcode=green99")
			}

		f = open("PageInfo.Dat")
		l = f.readlines()
		f.close()

		ptn = re.compile(r"(.+)([\r\n]+)$")
		for s in l:
			if not s or not "\t" in s: continue
			s = ptn.sub(r"\1", s)
			kv = s.split("\t")
			d[kv[0]] = (kv[1], kv[2], kv[3])
		if not ("top" in d): d["top"] = (u"초기화면", "", "green")
		if not d["top"][2].startswith("green"): d["top"] = (u"초기화면", "", "green|" + d["top"][2])
		return d

	def Play(self, wavfile, async=True):
		try:
			if async:
				winsound.PlaySound(os.path.dirname(__file__) + "\\sound\\" + wavfile, winsound.SND_ASYNC)
			else:
				winsound.PlaySound(os.path.dirname(__file__) + "\\sound\\" + wavfile, winsound.SND_NOSTOP)
		except:
			pass

	def WriteReg(self, key, value):
		try:
			root_key = _winreg.HKEY_CLASSES_ROOT
			sub_key = _winreg.CreateKey(root_key, r'SOFTWARE\JangSoft')
			_winreg.SetValueEx(sub_key, key, 0, _winreg.REG_SZ, value)
			return True
		except:
			return False


	def ReadReg(self, key):
		try:
			root_key = _winreg.HKEY_CLASSES_ROOT
			sub_key = _winreg.CreateKey(root_key, r'SOFTWARE\JangSoft')
			r = _winreg.QueryValueEx(sub_key, key)
			return r[0]
		except:
			return ""


	def Encrypt(self, s):
		if len(s) < 3: return ''
		try:
			r = ''
			i = 0
			for c in s:
				i = i % len(self.key)
				n = ord(c) + ord(self.key[i])
				r += chr(n) if n <= 126 else chr(n - 95)
				i += 1
			return r
		except:
			return ''


	def Decrypt(self, s):
		try:
			r = ''
			i = 0
			for c in s:
				i = i % len(self.key)
				n= ord(c) - ord(self.key[i])
				r += chr(n) if n >= 32 else chr(n + 95)
				i += 1
			return r
		except:
			return ''

	def ParamSplit(self, url):
# url 주소 문자열을 유니코드로 바꾸고 base_url 문자열과 매개변수가 담긴 사전으로 반환한다.
		d = {}
		base_url, params = url.split("?")
		for kvp in params.split("&"):
			if not kvp or not ("=" in kvp): continue
			k, v = kvp.split("=")
			if not k: continue
			d[k] = v
		return (base_url, d)

	def ParamJoin(self, d, enc = True):
# 다시 url로 조립 물론 urlencode를  사용할지를 선택
		if enc: 
			params = urllib.urlencode(d)
		else:
			params = "&".join(["%s=%s" % (k, v) for k, v in d.items()])
		return params


class WriteDialog(wx.Dialog):
	def __init__(self, parent, title, soup):
		wx.Dialog.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(800, 600))
		self.soup = soup
		self.action = ""
		self.attach = ""

		lbl_title = wx.StaticText(self, -1, u'제목', (5, 5), (100, 20))
		self.textctrl1 = wx.TextCtrl(self, -1, '', (110, 5), (685, 20))

		lbl_body = wx.StaticText(self, -1, u'내용', (5, 30), (100, 20))
		self.textctrl2 = wx.TextCtrl(self, -1, '', (110, 30), (685, 540), wx.TE_MULTILINE)

		self.btn_attach = wx.Button(self, -1, u'첨부파일', (5, 475), (310, 20))
		self.btn_attach.Bind(wx.EVT_BUTTON, self.OnAttach)
		self.btn_attach.Hide()

		self.btn_save = wx.Button(self, wx.ID_OK, u'저장', (590, 475), (100, 20))
		self.btn_cancel = wx.Button(self, wx.ID_CANCEL, u'취소', (695, 475), (100, 20))

# 단축키 지정
		accel = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, wx.ID_CANCEL)])
		self.SetAcceleratorTable(accel)

		self.Setting()

	def Setting(self):
		file = self.soup.find("input", type="file")
		if file is not None: self.btn_attach.Show()
		title = self.soup.find("input", type="text")
		if title is not None and title["value"]: self.textctrl1.SetValue(title["value"])
		body = self.soup.find("textarea")
		if body is not None and body.get_text(): self.textctrl2.SetValue(body.get_text())
		form = self.soup.find("form")
		if form is not None: self.action = form["action"]

	def OnAttach(self, e):
		if self.attach:
			self.attach = ""
			self.btn_attach.SetLabel(u"첨부 파일")
			return self.MsgBox(u"첨부파일 제거", u"첨부파일 등록을 제거했습니다.")

		fd = wx.FileDialog(self, u"파일 선택", "", "*.*", u"모든 파일 (*.*)", wx.FD_OPEN)
		if fd.ShowModal() == wx.ID_OK:
			self.attach = fd.GetPath()
			self.btn_attach.SetLabel(self.attach)


	def MsgBox(self, title, text):
		d = wx.MessageDialog(self, text, title, wx.OK)
		d.ShowModal()
		d.Destroy()


class TransferStatus(wx.Dialog):
	def __init__(self, parent):
		super(TransferStatus, self).__init__(parent, -1, u'파일 전송 정보', wx.DefaultPosition, wx.Size(500, 500))

		self.parent = parent

		self.listctrl = wx.ListCtrl(self, -1, (5, 5), (490, 490), wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING)
		self.listctrl.InsertColumn(0, '', width=50) # 퍼센트
		self.listctrl.InsertColumn(1, '', width=50) # 전송모드 / 업, 다운
		self.listctrl.InsertColumn(2, '', width=240) # 파일 이름
		self.listctrl.InsertColumn(3, u'속도', width=50)
		self.listctrl.InsertColumn(4, u'남은 시간')
		self.listctrl.Bind(wx.EVT_KEY_DOWN, self.on_listctrl)

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.get_info()

	def OnClose(self, e):
		self.Destroy()

	def on_listctrl(self, e):
		k = e.GetKeyCode()

		if k == ord(' ') or k == wx.WXK_RETURN:
			self.get_info()
			e.Skip()

		elif k == wx.WXK_ESCAPE:
			self.Destroy()

		elif k == wx.WXK_DELETE:
			self.cancel()

		else:
			e.Skip()


	def cancel(self):
		try:
			n = self.listctrl.GetFocusedItem()
			if n == -1: return
			d = wx.MessageDialog(self, '다운로드를 중단할까요?', '알림', wx.OK | wx.CANCEL)
			if d.ShowModal() == wx.ID_OK:
				f = self.listctrl.GetItemText(n, 2)

				if not f in self.parent.dProcess and f in self.parent.dTransInfo: 
					self.parent.dTransInfo.pop(f)
					self.get_info()
					return

				pid = self.parent.dProcess.pop(f)
				pid.terminate()
				self.parent.dTransInfo.pop(f)
				self.get_info()
		except:
			pass


	def get_info(self):
		self.listctrl.DeleteAllItems()
		if not self.parent.dTransInfo: return
		for k, v in self.parent.dTransInfo.items():
			k2 = k
# 한글 포함 여부에 따라 파일 이름 정리
			try:
				k = unicode(k, "euc-kr", "ignore")
			except:
				k = k2
			index = self.listctrl.InsertItem(sys.maxint, "%8.2f%%" % v[0])
			self.listctrl.SetItem(index, 1, v[1])
			self.listctrl.SetItem(index, 2, k)
			self.listctrl.SetItem(index, 3, "%8.2fMB" % v[2])
			self.listctrl.SetItem(index, 4, self.remaining(v[3]))


	def remaining(self, t):
		min = int(t // 60)
		sec = int(t % 60)
		return u"%d분 %d초" % (min, sec)


class QueueManager(Thread):
	def __init__(self, parent):
		Thread.__init__(self)
		self.parent = parent
		self.run()

	def run(self):
		while True:
			try:
				if self.parent.msg == "exit": break
				per, mode, filename, speed, remain = self.parent.ResQ.get_nowait()
				if per < 100.0:
					self.parent.dTransInfo[filename] = (per, mode, speed, remain)
				else:
					self.parent.dProcess.pop(filename)
					self.parent.dTransInfo.pop(filename)
			except:
				time.sleep(0.1)
