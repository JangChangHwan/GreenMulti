# coding: utf-8
# 메인 프로그램

import sys
import wx
from util import *
from web import *
import winsound
import os


class GreenMulti(wx.Frame, WebProcess):
	def __init__(self, title):
		WebProcess.__init__(self)
		Utility.__init__(self)
		wx.Frame.__init__(self, None, -1, title)
		self.Size = wx.Size(1015, 410)
		panel = wx.Panel(self, -1)
		panel.SetAutoLayout(True)

		lbl_listctrl = wx.StaticText(panel, -1, '메뉴 및 게시물 목록', (5, 5), (500, 20))
		self.listctrl = wx.ListCtrl(panel, -1, (5, 30), (500, 375), wx.LC_REPORT | wx.LC_SINGLE_SEL)
		self.listctrl.InsertColumn(0, '', width=400)
		self.listctrl.InsertColumn(1, '작성자', width=100)
		self.listctrl.Bind(wx.EVT_KEY_DOWN, self.listctrl_KeyDown)
#		self.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.on_listctrl1_right_down)

# 게시물 읽기 편집창
		lbl_textctrl1 = wx.StaticText(panel, -1, u'본문 영역', (510, 5), (500, 20))
		self.textctrl1 = wx.TextCtrl(panel, wx.ID_ANY, '', (510, 30), (500, 170), wx.TE_MULTILINE | wx.TE_READONLY)
		self.textctrl1.Bind(wx.EVT_KEY_DOWN, self.OnTextCtrl1KeyDown)
#		self.textctrl1.Bind(wx.EVT_RIGHT_DOWN, self.on_textctrl1_right_down)

		lbl_textctrl2 = wx.StaticText(panel, -1, u'댓글 영역', (510, 205), (500, 20))
		self.textctrl2 = wx.TextCtrl(panel, wx.ID_ANY, '', (510, 230), (500, 150), wx.TE_MULTILINE | wx.TE_READONLY)
		self.textctrl2.Bind(wx.EVT_KEY_DOWN, self.OnTextCtrl2KeyDown)

		lbl_textctrl3 = wx.StaticText(panel, -1, u'댓글입력', (510, 385), (100, 20))
		self.textctrl3 = wx.TextCtrl(panel, wx.ID_ANY, '', (615, 385), (290, 20), wx.TE_MULTILINE)
		self.textctrl3.Bind(wx.EVT_KEY_DOWN, self.OnTextCtrl3KeyDown)

		self.btn_reple_save = wx.Button(panel, -1, u'댓글저장', (910, 385), (100, 20))
#		self.btn_reple_save.Bind(wx.EVT_BUTTON, self.on_reple_save)
		self.btn_reple_save.Bind(wx.EVT_KEY_DOWN, self.OnRepleKeyDown)
#		self.Bind(wx.EVT_CLOSE, self.on_close)

		self.Show()
		self.KbuLogin()
		self.DisplayItems("menu")


	def KbuLogin(self):
		try:
			kbuid = self.Decrypt(self.ReadReg('kbuid'))
			if not kbuid: kbuid = self.InputBox(u'넓은마을 로그인', u'아이디')
			kbupw = self.Decrypt(self.ReadReg('kbupw'))
			if not kbupw: kbupw = self.InputBox(u'넓은마을 로그인', u'비밀번호', pwd=1) 
			if not kbuid or not kbupw: return self.msgbox(u'알림', u'사용자 아이디와 비밀번호는 필수 입력사항입니다.')

			params = {"ret":"notice_top", "ret2":"", "cmd":"check_login", "log_id":kbuid, "log_passwd":kbupw}
			self.Post('http://web.kbuwel.or.kr/menu/login.php', params)
			if "login=true" in self.soup.get_text():
				self.WriteReg('kbuid', self.Encrypt(kbuid))
				self.WriteReg('kbupw', self.Encrypt(kbupw))
				self.Play("program_start.wav")
			else:
				self.WriteReg('kbuid', '')
				self.WriteReg('kbupw', '')
				return self.MsgBox(u'알림', u'초록등대 회원인증에 실패했습니다.')
		except:
			pass


	def DisplayItems(self, mode):
		if mode == "menu" or mode == "list":
			self.listctrl.DeleteAllItems()
			for t in self.lItemList:
				index = self.listctrl.InsertItem(sys.maxint, t[1])
				self.listctrl.SetItem(index, 1, t[2])
		elif mode == "view":
			self.textctrl1.SetValue(self.ViewInfo["content"])
			self.textctrl2.SetValue(self.ViewInfo["replies"])
			self.textctrl3.Clear()

	def listctrl_KeyDown(self, e):
		k = e.GetKeyCode()

		if k == wx.WXK_RETURN:
			n = self.listctrl.GetFocusedItem()
			r = self.GetInfo(self.lItemList[n])
			if r: 
				self.DisplayItems(r)
				self.Play("page_next.wav")
				if r == "view": self.textctrl1.SetFocus()

		elif (e.GetModifiers() == wx.MOD_ALT and k == wx.WXK_LEFT) or k == wx.WXK_ESCAPE:
			parent = self.dTreeMenu[self.bcode][1]
			if not parent: 
				self.Play("beep.wav")
				return

			self.ListInfo.clear()
			self.ViewInfo.clear()
			self.textctrl1.Clear()
			self.textctrl2.Clear()
			self.textctrl3.Clear()

			title, temp, href = self.dTreeMenu[parent]
			r = self.GetInfo((parent, title, "", href))
			if r:
				self.DisplayItems("menu")
				self.Play("back.wav")

		elif k == wx.WXK_PAGEDOWN:
			r = self.PageMove(True)
			if r and len(self.lItemList) > 0:
				self.DisplayItems("list")
				self.Play("page_next.wav")
			else:
				r = self.PageMove(False)
				self.Play("beep.wav")

		elif k == wx.WXK_PAGEUP:
			r = self.PageMove(False)
			if r:
				self.DisplayItems("list")
				self.Play("page_prev.wav")
			else:
				self.Play("beep.wav")

		else:
			e.Skip()


	def InputBox(self, title, text, pwd=False):
		style = wx.OK | wx.CANCEL | wx.TE_PASSWORD if pwd else wx.OK | wx.CANCEL
		entry = wx.TextEntryDialog(self, text, title, '', style)
		if entry.ShowModal() == wx.ID_OK: return entry.GetValue()
		entry.Destroy()


	def MsgBox(self, title, text):
		d = wx.MessageDialog(self, text, title, wx.OK)
		d.ShowModal()
		d.Destroy()


	def OnTextCtrl1KeyDown(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_ESCAPE or (e.GetModifiers() == wx.MOD_ALT and k == wx.WXK_LEFT):
			self.listctrl.SetFocus()
			self.Play("back.wav")
		else:
			e.Skip()

	def OnTextCtrl2KeyDown(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_ESCAPE or (e.GetModifiers() == wx.MOD_ALT and k == wx.WXK_LEFT):
			self.listctrl.SetFocus()
			self.Play("back.wav")

		elif k == wx.WXK_PAGEDOWN:
			text = self.textctrl2.GetValue().replace('\n', '\n\n')
			if not text: return
			n = self.textctrl2.GetInsertionPoint()
			p = text.find('[', n+1)
			if p == -1: return winsound.Beep(1000, 100)
			self.textctrl2.SetInsertionPoint(p)

		elif k == wx.WXK_PAGEUP:
			text = self.textctrl2.GetValue().replace('\n', '\n\n')
			if not text: return
			n = self.textctrl2.GetInsertionPoint()
			p = text.rfind('[', 0, n-1)
			if p == -1: return winsound.Beep(1000, 100)
			self.textctrl2.SetInsertionPoint(p)

		else:
			e.Skip()

	def OnTextCtrl3KeyDown(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_ESCAPE or (e.GetModifiers() == wx.MOD_ALT and k == wx.WXK_LEFT):
			self.listctrl.SetFocus()
			self.Play("back.wav")
		else:
			e.Skip()

	def OnRepleKeyDown(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_ESCAPE or (e.GetModifiers() == wx.MOD_ALT and k == wx.WXK_LEFT):
			self.listctrl.SetFocus()
			self.Play("back.wav")
		else:
			e.Skip()


if __name__ == "__main__":
	app = wx.App()
	GreenMulti("초록멀티 v1.2")
	app.MainLoop()

