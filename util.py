# coding: utf-8
# 함수모음 util.py

import re

def TreeMenuFromFile():
	""" PageInfo.Dat 파일로부터 목록상자에 표시될 트리메뉴를 만듭니다. 반환값 : 사전 객체"""
	d = {} # 반환될 내요을 담을 사전

	f = open("PageInfo.Dat")
	l = f.readlines()
	f.close()

	ptn = re.compile(r"(.+)([\r\n]+)$")
	for s in l:
		s = ptn.sub(r"\1", s)
		kv = s.split("\t")
		d[kv[0]] = (kv[1], kv[2], kv[3])
	return d

if __name__ == "__main__":
	d = TreeMenuFromFile()
	print(d)
