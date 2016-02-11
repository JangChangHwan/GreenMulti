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

		self.Show()
		self.KbuLogin()
		self.DisplayItems(0)


	def KbuLogin(self):
#		try:
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
#		except:
#			pass


	def DisplayItems(self, n):
		if n < 0: return
		self.listctrl.DeleteAllItems()
		for t in self.lItemList:
			index = self.listctrl.InsertItem(sys.maxint, t[1])
			self.listctrl.SetItem(index, 1, t[2])


	def listctrl_KeyDown(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_RETURN:
			n = self.listctrl.GetFocusedItem()
			self.GetInfo(self.lItemList[n])
			self.DisplayItems(n)
			self.Play("page_next.wav")

		elif (e.GetModifiers() == wx.MOD_ALT and k == wx.WXK_LEFT) or k == wx.WXK_ESCAPE:
			parent = self.dTreeMenu[self.bcode][1]
			if not parent: 
				self.Play("beep.wav")
				return

			title, temp, href = self.dTreeMenu[parent]
			self.GetInfo((parent, title, "", href))
			self.DisplayItems(0)
			self.Play("back.wav")

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


if __name__ == "__main__":
	app = wx.App()
	GreenMulti("초록멀티 v1.2")
	app.MainLoop()

