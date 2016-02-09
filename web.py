﻿# coding: utf-8
# 웹처리부분

from util import *
from bs4  import BeautifulSoup as bs
import MultipartPostHandler
import urllib, urllib2, cookielib


class WebProcess():
	def __init__(self):
		self.dTreeMenu = TreeMenuFromFile()
		self.bcode = "top"
		self.lItemList = [("top", "제목", "", self.dTreeMenu["top"][2])]
		self.GetInfo(self.lItemList[0])

		self.opener = self.BuildOpener()

	def GetInfo(self, t):
		if "cmd=view" in t[3]:
			self.GetView(t)
		elif "http" in t[3]:
			self.GetList(t)
		else:
			self.GetMenu(t)


	def GetMenu(self, t): # t는 lItemList의 원소 형식
		print(t[0])
		self.lItemList = []
		for c in t[3].split("|"):
			if not c in self.dTreeMenu: continue
			l = self.dTreeMenu[c]
			self.lItemList.append((c, unicode(l[0], "euc-kr", "ignore"), "", l[2]))
		self.bcode = t[0]


	def GetView(self, s):
		pass

	def Get(self, url):
		pass

	def Post(self, url, d): 
		pass

	def BuildOpener(self):
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj), MultipartPostHandler.MultipartPostHandler)
		urllib2.install_opener(opener)
		return opener
