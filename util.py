# coding: utf-8
# 함수모음 util.py

import sys
import re
import winsound
import os
import _winreg


class Utility():
	def __init__(self):
		self.key = "%x" % os.path.getctime(os.environ["APPDATA"])
		print self.key
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
				winsound.PlaySound(
os.path.dirname(sys.argv[0]) + "\\sound\\" + wavfile, winsound.SND_ASYNC)
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
