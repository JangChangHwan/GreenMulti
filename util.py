# coding: utf-8
# 함수모음 util.py

import sys
import re
import winsound
import os
import _winreg
import urllib
import wx




class Utility():
	def __init__(self):
		self.key = "%x" % os.path.getctime(os.environ["APPDATA"])

	def TreeMenuFromFile(self):
		""" PageInfo.Dat 파일로부터 목록상자에 표시될 트리메뉴를 만듭니다. 반환값 : 사전 객체"""
		d = {} # 반환될 내요을 담을 사전

		f = open("PageInfo.Dat")
		l = f.readlines()
		f.close()

		ptn = re.compile(r"(.+)([\r\n]+)$")
		for s in l:
			if not s or not "\t" in s: continue
			s = ptn.sub(r"\1", s)
			kv = s.split("\t")
			d[kv[0]] = (kv[1], kv[2], kv[3])
		return d

	def Play(self, wavfile, async=True):
		try:
			if async:
				winsound.PlaySound(os.path.dirname(__file__) + "\\sound\\" + wavfile, winsound.SND_ASYNC)
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
		file = self.soup.find("input", type="file")
		if file is not None: self.btn_attach.Show()
		title = self.soup.find("input", attr={"name":u"제목", "type":"text"})
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
