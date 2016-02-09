# coding: utf-8
# 웹처리부분
import wx

from util import *

class WebProcess():
	def __init__(self):
		self.dTreeMenu = TreeMenuFromFile()
		self.bcode = "top"
		self.lItemList = [("top", "제목", "", self.dTreeMenu["top"][2])]
		self.GetInfo(self.lItemList[0])

	def GetInfo(self, t):
		if "cmd=view" in t[3]:
			self.GetView(t)
		elif "http" in t[3]:
			self.GetList(t)
		else:
			self.GetMenu(t)


	def GetMenu(self, t):
		self.lItemList = []
		for c in t[3].split("|"):
			if not c in self.dTreeMenu: continue
			l = self.dTreeMenu[c]
			self.lItemList.append((c, unicode(l[0], "euc-kr", "ignore"), "", l[2]))
		self.bcode = t[0]

	def GetView(self, s):
		pass

	def GetList(self, s):
		pass
