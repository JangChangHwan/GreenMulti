# coding: utf-8
# 메인 프로그램

import sys
import wx
from util import *
from web import *

class GreenMulti(wx.Frame, WebProcess):
	def __init__(self, title):
		WebProcess.__init__(self)
		wx.Frame.__init__(self, None, -1, title)

		self.Size = wx.Size(1015, 500)

		panel = wx.Panel(self, -1)
		panel.SetAutoLayout(True)

		lbl_listctrl = wx.StaticText(panel, -1, '메뉴 및 게시물 목록', (5, 5), (500, 20))
		self.listctrl = wx.ListCtrl(panel, -1, (5, 30), (500, 565), wx.LC_REPORT | wx.LC_SINGLE_SEL)
		self.listctrl.InsertColumn(0, '', width=400)
		self.listctrl.InsertColumn(1, '작성자', width=100)
		self.listctrl.Bind(wx.EVT_KEY_DOWN, self.listctrl_KeyDown)
#		self.listctrl.Bind(wx.EVT_RIGHT_DOWN, self.on_listctrl1_right_down)

		self.Show()
		self.DisplayItems(0)

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

		elif e.GetModifiers() == wx.MOD_ALT and k == wx.WXK_LEFT:
			parent = self.dTreeMenu[self.bcode][1]
			if not parent: return
			title, temp, href = self.dTreeMenu[parent]
			self.GetInfo((parent, title, "", href))
			self.DisplayItems(0)

		else:
			e.Skip()


if __name__ == "__main__":
	app = wx.App()
	GreenMulti("초록멀티 v1.2")
	app.MainLoop()
