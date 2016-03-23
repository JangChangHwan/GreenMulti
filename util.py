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
import telnetlib
import zipfile
from bs4 import BeautifulSoup as bs


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
				winsound.PlaySound(os.path.dirname(sys.argv[0]) + "\\sound\\" + wavfile, winsound.SND_ASYNC)
			else:
				winsound.PlaySound(os.path.dirname(sys.argv[0]) + "\\sound\\" + wavfile, winsound.SND_NOSTOP)
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
		try:
			file = self.soup.find("input", type="file")
			if file is not None: self.btn_attach.Show()
			title = self.soup.find("input", type="text")
			if title is not None and title["value"]: self.textctrl1.SetValue(title["value"])
			body = self.soup.find("textarea")
			if body is not None and body.get_text(): self.textctrl2.SetValue(body.get_text())
			form = self.soup.find("form")
			if form is not None: self.action = form["action"]
		except:
			pass


	def OnAttach(self, e):
		try:
			if self.attach:
				self.attach = ""
				self.btn_attach.SetLabel(u"첨부 파일")
				return self.MsgBox(u"첨부파일 제거", u"첨부파일 등록을 제거했습니다.")

			fd = wx.FileDialog(self, u"파일 선택", "", "*.*", u"모든 파일 (*.*)", wx.FD_OPEN)
			if fd.ShowModal() == wx.ID_OK:
				filepath = fd.GetPath()
				euc = filepath if type(filepath) == str else filepath.encode("euc-kr", "ignore")
				if os.path.exists(euc) and os.path.getsize(euc) < (1024 * 1024 * 1025): 
					self.attach = filepath
					self.btn_attach.SetLabel(self.attach)
				else:
					self.MsgBox(u"오류", u"파일이 없거나 크기가 1GB를 넘습니다. 1GB가 넘는 파일은 올릴 수 없습니다.")
		except:
			pass

	def MsgBox(self, title, text):
		try:
			d = wx.MessageDialog(self, text, title, wx.OK)
			d.ShowModal()
			d.Destroy()
		except:
			pass


class TransferStatus(wx.Dialog):
	def __init__(self, parent):
		super(TransferStatus, self).__init__(parent, -1, u'파일 전송 정보', wx.DefaultPosition, wx.Size(500, 500))

		self.parent = parent

		self.listctrl = wx.ListCtrl(self, -1, (5, 5), (490, 490), wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING)
		self.listctrl.InsertColumn(0, '', width=50) # 퍼센트
		self.listctrl.InsertColumn(1, '', width=50) # 전송모드 / 업, 다운
		self.listctrl.InsertColumn(2, '', width=200) # 파일 이름
		self.listctrl.InsertColumn(3, u'속도', width=50)
		self.listctrl.InsertColumn(4, u'남은 시간', width=50)
		self.listctrl.InsertColumn(5, 'p_num', width=40)
		self.listctrl.Bind(wx.EVT_KEY_DOWN, self.on_listctrl)

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.get_info()

	def OnClose(self, e):
		self.Destroy()

	def on_listctrl(self, e):
		try:
			self.try_on_listctrl(e)
		except:
			pass

	def try_on_listctrl(self, e):
		k = e.GetKeyCode()

		if k == ord(' '):
			self.get_info()
			e.Skip()

		elif k == wx.WXK_RETURN:
			d = wx.MessageDialog(self, u'현재 %s 개의 프로세스가 작업 중입니다.' % len(self.parent.dProcess), u'프로세스 현황', wx.OK)
			d.ShowModal()
			d.Destroy()

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
			d = wx.MessageDialog(self, u'다운로드를 중단할까요?', u'알림', wx.OK | wx.CANCEL)
			if d.ShowModal() == wx.ID_OK:
				p_num = int(self.listctrl.GetItemText(n, 5))
				try:
					self.parent.dTransInfo.pop(p_num)
				except:
					pass
				try:
					pid = self.parent.dProcess.pop(p_num)
					pid.terminate()
				except:
					pass
				self.get_info()
		except:
			pass


	def get_info(self):
		try:
			self.listctrl.DeleteAllItems()
			if not self.parent.dTransInfo: return
			for k, v in self.parent.dTransInfo.items():
				index = self.listctrl.InsertStringItem(sys.maxint, "%8.2f%%" % v[0])
				self.listctrl.SetStringItem(index, 1, v[1])
				filename = v[2] if type(v[2]) == unicode else unicode(v[2], "euc-kr", "ignore")
				self.listctrl.SetStringItem(index, 2, filename)
				self.listctrl.SetStringItem(index, 3, "%8.2fMB" % v[3])
				self.listctrl.SetStringItem(index, 4, self.remaining(v[4]))
				self.listctrl.SetStringItem(index, 5, str(k))
		except:
			pass

	def remaining(self, t):
		min = int(t // 60)
		sec = int(t % 60)
		return u"%d분 %d초" % (min, sec)


class QueueManager(Thread):
	def __init__(self, parent):
		Thread.__init__(self)
		self.parent = parent
		try:
			self.run()
		except:
			pass

	def run(self):
		while True:
			try:
				if self.parent.msg == "exit": break
				per, mode, filename, speed, remain, p_num = self.parent.ResQ.get_nowait()
				if per < 100: 
					self.parent.dTransInfo[p_num] = (per, mode, filename, speed, remain)
				else:
					pid = self.parent.dProcess.pop(p_num, 0)
					if pid: pid.terminate()
					if p_num in self.parent.dTransInfo: self.parent.dTransInfo.pop(p_num)
			except:
				time.sleep(0.1)


class DirectMove(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, u"코드 바로가기", wx.DefaultPosition, wx.Size(340, 100))
		self.parent = parent
		lbl1 = wx.StaticText(self, -1, u"메뉴 코드나 게시판 코드를 입력하거나 선택하세요.", (10, 10), (320, 20))
		lbl2 = wx.StaticText(self, -1, u"Code", (10, 40), (100, 20))
		self.combo = wx.ComboBox(self, -1, "", (120, 40), (210, 20), self.parent.dTreeMenu.keys(), wx.CB_DROPDOWN | wx.CB_SORT | wx.CB_READONLY)
		btn_ok = wx.Button(self, wx.ID_OK, u"확인", (120, 70), (100, 20))
		btn_cancel = wx.Button(self, wx.ID_CANCEL, u"취소", (230, 70), (100, 20))

		accel = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, wx.ID_CANCEL), (wx.ACCEL_NORMAL, wx.WXK_RETURN, wx.ID_OK)])
		self.SetAcceleratorTable(accel)



class WriteMailDialog(wx.Dialog):
	def __init__(self, parent, title, receiver="", retitle="", rebody=""):
		wx.Dialog.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(670, 570))
		self.receiver = receiver
		self.retitle = retitle
		self.rebody = rebody
		self.attach1 = ""
		self.attach2 = ""
		self.attach3 = ""

		lbl_recv = wx.StaticText(self, -1, u'받는사람', (10, 10), (100, 20))
		self.textctrl1 = wx.TextCtrl(self, -1, self.receiver, (120, 10), (540, 20))
		lbl_corecv = wx.StaticText(self, -1, u'함께받는사람', (10, 40), (100, 20))
		self.textctrl2 = wx.TextCtrl(self, -1, "", (120, 40), (540, 20))
		lbl_title = wx.StaticText(self, -1, u'제목', (10, 70), (100, 20))
		self.textctrl3 = wx.TextCtrl(self, -1, self.retitle, (120, 70), (540, 20))

		lbl_body = wx.StaticText(self, -1, u'내용', (10, 100), (100, 20))
		self.textctrl4 = wx.TextCtrl(self, -1, self.rebody, (120, 100), (540, 400), wx.TE_MULTILINE)

		self.btn_attach1 = wx.Button(self, -1, u'첨부파일 #1', (10, 510), (210, 20))
		self.btn_attach1.Bind(wx.EVT_BUTTON, self.OnAttach1)
		self.btn_attach2 = wx.Button(self, -1, u'첨부파일 #2', (230, 510), (210, 20))
		self.btn_attach2.Bind(wx.EVT_BUTTON, self.OnAttach2)
		self.btn_attach3 = wx.Button(self, -1, u'첨부파일 #3', (450, 510), (210, 20))
		self.btn_attach3.Bind(wx.EVT_BUTTON, self.OnAttach3)

		self.btn_save = wx.Button(self, wx.ID_OK, u'전송', (230, 540), (100, 20))
		self.btn_cancel = wx.Button(self, wx.ID_CANCEL, u'취소', (340, 540), (100, 20))

# 단축키 지정
		accel = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, wx.ID_CANCEL)])
		self.SetAcceleratorTable(accel)

	def OnAttach1(self, e):
		try:
			if self.attach1:
				self.attach1 = ""
				self.btn_attach1.SetLabel(u"첨부 파일 #1")
				return self.MsgBox(u"첨부파일 취소", u"첨부파일 등록을 취소했습니다.")

			fd = wx.FileDialog(self, u"파일 선택", "", "*.*", u"모든 파일 (*.*)", wx.FD_OPEN)
			if fd.ShowModal() == wx.ID_OK:
				path = fd.GetPath()
				if path == self.attach2 or path == self.attach3: return self.MsgBox("경고", "이미 첨부 파일로 지정되어 있습니다. 파일 첨부를 취소합니다.")
				euc = path if type(path) == str else path.encode("euc-kr", "ignore")
				if os.path.exists(euc) and os.path.getsize(euc) < (1024 * 1024 * 1025):
					self.attach1 = path
					self.btn_attach1.SetLabel(self.attach1)
				else:
					self.MsgBox(u"오류", u"파일이 없거나 크기가 1GB를 넘습니다. 1GB가 넘는 파일은 올릴 수 없습니다.")
		except:
			pass


	def OnAttach2(self, e):
		try:
			if self.attach2:
				self.attach2 = ""
				self.btn_attach2.SetLabel(u"첨부 파일 #2")
				return self.MsgBox(u"첨부파일 취소", u"첨부파일 등록을 취소했습니다.")

			fd = wx.FileDialog(self, u"파일 선택", "", "*.*", u"모든 파일 (*.*)", wx.FD_OPEN)
			if fd.ShowModal() == wx.ID_OK:
				path = fd.GetPath()
				if path == self.attach1 or path == self.attach3: return self.MsgBox("경고", "이미 첨부 파일로 지정되어 있습니다. 파일 첨부를 취소합니다.")
				euc = path if type(path) == str else path.encode("euc-kr", "ignore")
				if os.path.exists(euc) and os.path.getsize(euc) < (1024 * 1024 * 1025):
					self.attach2 = path
					self.btn_attach2.SetLabel(self.attach2)
				else:
					self.MsgBox(u"오류", u"파일이 없거나 크기가 1GB를 넘습니다. 1GB가 넘는 파일은 올릴 수 없습니다.")
		except:
			pass

	def OnAttach3(self, e):
		try:
			if self.attach3:
				self.attach3 = ""
				self.btn_attach3.SetLabel(u"첨부 파일 #3")
				return self.MsgBox(u"첨부파일 취소", u"첨부파일 등록을 취소했습니다.")

			fd = wx.FileDialog(self, u"파일 선택", "", "*.*", u"모든 파일 (*.*)", wx.FD_OPEN)
			if fd.ShowModal() == wx.ID_OK:
				path = fd.GetPath()
				if path == self.attach1 or path == self.attach2: return self.MsgBox("경고", "이미 첨부 파일로 지정되어 있습니다. 파일 첨부를 취소합니다.")
				euc = path if type(path) == str else path.encode("euc-kr", "ignore")
				if os.path.exists(euc) and os.path.getsize(euc) < (1024 * 1024 * 1025):
					self.attach3 = path
					self.btn_attach3.SetLabel(self.attach3)
				else:
					self.MsgBox(u"오류", u"파일이 없거나 크기가 1GB를 넘습니다. 1GB가 넘는 파일은 올릴 수 없습니다.")
		except:
			pass

	def MsgBox(self, title, text):
		try:
			d = wx.MessageDialog(self, text, title, wx.OK)
			d.ShowModal()
			d.Destroy()
		except:
			pass


class ForUser(Thread):
	def __init__(self, parent):
		super(ForUser, self).__init__()
		try:
			self.parent = parent
			self.run()
		except:
			return

	def run(self):
# 아디 비번 불러오기
			kbuid = self.parent.Decrypt(self.parent.ReadReg("kbuid"))
			kbupw = self.parent.Decrypt(self.parent.ReadReg("kbupw"))
			if not kbuid or not kbupw: return

# 호스트접속
			tn = telnetlib.Telnet('bbs.kbuwel.or.kr', timeout=15)
			if self.parent.msg == "exit": return
			tn.read_until(u'아 이 디 :'.encode('euc-kr', 'ignore'), timeout=10)
			if self.parent.msg == "exit": return
			tn.write(kbuid + '\n')
			tn.read_until(u'비밀번호 :'.encode('euc-kr', 'ignore'), timeout=5)
			if self.parent.msg == "exit": return
			tn.write(kbupw + '\n')
			tn.read_until(u'전번'.encode('euc-kr', 'ignore'), timeout=5)
			if self.parent.msg == "exit": return
			tn.write('\n')
			tn.write('\n')
			tn.write('\n')
			tn.write('\n')
			tn.read_until(u'명령>>'.encode('euc-kr', 'ignore'), timeout=5)
			tn.write('green3\n')

			t = 0
			while True:
				if self.parent.msg == "exit": return
				time.sleep(1)
				t += 1
				if t < 60: continue
				text = tn.read_very_eager()
				tn.write('green3\n')
				t = 0


class Library(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, u"아이프리 전자도서관", wx.DefaultPosition, wx.Size(450, 300))
		self.parent = parent
		self.href = []
		self.list_url = ""

		lbl1 = wx.StaticText(self, -1, u"분류", (10, 10), (100, 20))
		choiceList = [u"1. 총류", u"2. 철학", u"3. 종교", u"4. 사회과학", u"5. 순수과학", u"6. 기술과학", u"7. 예술", u"8. 어학", u"9. 문학 - 1. 환타지, SF소설", u"9. 문학 - 2. 무협", u"9. 문학 - 3. 추리, 공포, 꽁트", u"9. 문학 - 4. 일반소설", u"9. 문학 - 5. 소설 외 문학", u"9. 문학 - 6. 아동문학", u"10. 역사", u"20. 전체자료실"]
		self.booklist = ("http://eyefree.org/board/board.php?bdname=bd_main_book1&backurl=/book.php&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book3&backurl=/book.php&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book2&backurl=/book.php&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book4&backurl=/book.php&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book5&backurl=/book.php&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book6&backurl=/book.php&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book7&backurl=/book.php&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book8&backurl=/book.php&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book91&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book92&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book93&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book94&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book95&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book96&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_book10&backurl=/book.php&page=1", "http://eyefree.org/board/board.php?bdname=bd_main_ball&backurl=/book.php&page=1")
		self.choice = wx.ListBox(self, -1, (120, 10), (320, 20), choiceList, wx.LB_SINGLE)
		self.choice.Bind(wx.EVT_LISTBOX, self.OnChoice)
		self.choice.Bind(wx.EVT_KEY_DOWN, self.OnChoiceKeyDown)

		self.listbox = wx.ListBox(self, -1, (10, 40), (430, 250), [], wx.LB_SINGLE)
		self.listbox.Bind(wx.EVT_KEY_DOWN, self.OnListBox)

		# 아이프리 로그인
		self.parent.Get("http://eyefree.org/book.php")
		m = self.parent.soup.find('a', href=re.compile(r"(?i)/login.php"))
		if m is not None: self.SilLogin()


	def SilLogin(self):
		try:
			silid = self.parent.Decrypt(self.parent.ReadReg('silid'))
			if not silid: silid = self.InputBox(u'아이프리 로그인', u'아이디')

			silpw = self.parent.Decrypt(self.parent.ReadReg('silpw'))
			if not silpw: silpw = self.InputBox(u'아이프리 로그인', u'비밀번호', pwd=1) 
			if not silid or not silpw: return self.msgbox(u'알림', u'사용자 아이디와 비밀번호는 필수 입력사항입니다.')

			params = {"uid":silid, "upw":silpw}
			self.parent.Post("http://eyefree.org/member/loginchk.php", params)

			if "../index.php" in self.parent.soup.get_text():
				self.parent.WriteReg('silid', self.parent.Encrypt(silid))
				self.parent.WriteReg('silpw', self.parent.Encrypt(silpw))
			else:
				self.parent.WriteReg('silid', '')
				self.parent.WriteReg('silpw', '')
				return self.MsgBox(u'알림', u'아이프리 로그인에 실패했습니다.')

		except:
			pass



	def InputBox(self, title, text, pwd=False):
		try:
			style = wx.OK | wx.CANCEL | wx.TE_PASSWORD if pwd else wx.OK | wx.CANCEL
			entry = wx.TextEntryDialog(self, text, title, '', style)
			if entry.ShowModal() == wx.ID_OK: return entry.GetValue()
			entry.Destroy()
		except:
			pass

	def MsgBox(self, title, text, question=False):
		try:
			if question:
				d = wx.MessageDialog(self, text, title, wx.OK | wx.CANCEL)
				if d.ShowModal() == wx.ID_OK:
					return True
				else:
					return False
				d.Destroy()
			else:
				d = wx.MessageDialog(self, text, title, wx.OK)
				d.ShowModal()
				d.Destroy()
		except:
			pass


	def DaisyToText(self, path):
		try:
			zfile = zipfile.ZipFile(path, "r")
			for filename in zfile.namelist():
				if not filename.endswith(".xml"): continue
				xml = zfile.read(filename)
				zfile.close()
				break

			xml = re.sub(r"(?ims)<pagenum [^<>]+>\d+</pagenum>", "",  xml)
			soup = bs(xml, "html.parser")
			text = soup.book.get_text()
			text = text.replace(u"\n", u"\r\n")
			text = text.encode("utf-16", "ignore")
			textfile = path[:-4] + ".txt"
			f = open(textfile, "wb")
			f.write(text)
			f.close()
			os.remove(path)
		except:
			self.parent.Play("error.wav")


	def OnChoiceKeyDown(self, e):
		k = e.GetKeyCode()
		if e.GetModifiers() == wx.MOD_CONTROL and k == ord("O"):
			self.parent.OnOpenDownFolder(e)

		elif k == wx.WXK_ESCAPE:
			self.Destroy()

		elif e.GetModifiers() == wx.MOD_CONTROL and k == ord("F"):
			self.Search()


		else:
			e.Skip()


	def OnChoice(self, e):
		try:
			n = self.choice.GetSelection()
			if n == -1: return
			self.list_url = self.booklist[n]
			self.parent.Get(self.list_url)
			self.GetList()
			self.parent.Play("page_next.wav")
		except:
			pass

	def GetList(self):
		self.href = []
		self.listbox.Clear()
		links = self.parent.soup('a', href=re.compile(r"(?i)board_view.php"))
		if links is None: return
		for l in links:
			self.listbox.Append(l.get_text())
			self.href.append("http://eyefree.org/board/" + l["href"])

	def OnListBox(self, e):
		try:
			self.try_OnListBox(e)
		except:
			pass

	def try_OnListBox(self, e):
		k = e.GetKeyCode()
		if k == ord(" "): # 스페이스바 누를 때
			n = self.listbox.GetSelection()
			if n == -1: return
			self.parent.Get(self.href[n])
			bookinfo = self.parent.soup.find("article", attrs={"class":"bbs_view"})
			if bookinfo is None: return
			self.MsgBox(u"도서 정보", bookinfo.get_text())

		elif k == ord("D"):
			n = self.listbox.GetSelection()
			if n == -1: return
			self.parent.Get(self.href[n])
			filelink = self.parent.soup.find("a", href=re.compile(r"(?i)download.php"))
			if filelink is None: return
			filename = filelink.get_text()[7:]
			res = self.parent.opener.open("http://eyefree.org/board/" + filelink["href"])
			file = res.read()

			downfolder = self.parent.ReadReg("downfolder")
			if not downfolder: downfolder = "c:\\"
			path = downfolder + "\\" + filename
			path = path.replace("\\\\", "\\")

			if type(path) == unicode: path = path.encode("euc-kr", "ignore")
			f = open(path, "wb")
			f.write(file)
			f.close()

			if self.parent.limit == 100: self.DaisyToText(path)
			self.parent.Play("down.wav")

		elif e.GetModifiers() == wx.MOD_CONTROL and k == ord("O"):
			self.parent.OnOpenDownFolder(e)

		elif k == wx.WXK_PAGEDOWN:
			url, data = self.parent.ParamSplit(self.list_url)
			n = int(data["page"])
			data["page"] = str(n+1)
			self.list_url = url + "?" + self.parent.ParamJoin(data, enc=False)
			self.parent.Get(self.list_url)
			self.GetList()
			if len(self.href) > 0: 
				self.parent.Play("page_next.wav")
			else:
				data["page"] = str(n)
				self.list_url = url + "?" + self.parent.ParamJoin(data, enc=False)
				self.parent.Get(self.list_url)
				self.GetList()
				self.parent.Play("beep.wav")



		elif k == wx.WXK_PAGEUP:
			url, data = self.parent.ParamSplit(self.list_url)
			n = int(data["page"])
			if n <= 1: return self.parent.Play("beep.wav")
			data["page"] = str(n - 1)
			self.list_url = url + "?" + self.parent.ParamJoin(data, enc=False)
			self.parent.Get(self.list_url)
			self.GetList()
			self.parent.Play("page_prev.wav")

			self.list_


		elif k == wx.WXK_UP:
			if self.listbox.GetSelection() <= 0: 				self.parent.Play("beep.wav")
			e.Skip()

		elif k == wx.WXK_DOWN:
			if self.listbox.GetSelection() == len(self.href) - 1: 				self.parent.Play("beep.wav")
			e.Skip()

		elif k == wx.WXK_ESCAPE:
			self.Destroy()

		elif e.GetModifiers() == wx.MOD_CONTROL and k == ord("F"):
			self.Search()

		else:
			e.Skip()


	def Search(self):
		try:
			# 검색 폼이 있는가?
			form = self.parent.soup.find("form", attrs={"name":"frm_srch"})
			if form is None: return
			# 여러 값을 가져옵니다.
			action = "http://eyefree.org/board/" + form["action"]
			url, data = self.parent.ParamSplit(action)
			hiddens = self.parent.soup("input", type="hidden")
			if hiddens is None: return
			for h in hiddens:
				data[h["name"]] = h["value"]

			kwd = self.InputBox(u"도서 검색", u"키워드")
			if not kwd: return
			if type(kwd) == unicode: kwd = kwd.encode("euc-kr", "ignore")
			data["term1"] = kwd
			data["page"] = 1
			self.list_url = url + "?" + self.parent.ParamJoin(data)
			self.parent.Get(self.list_url)
			self.GetList()
			self.listbox.SetFocus()
			self.parent.Play("page_next.wav")
		except:
			pass

