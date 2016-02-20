# coding: utf-8
# GreenMulti 

import sys
import wx
from userfunc import *
from webprocess import *
from multiprocessing import Process, Queue, freeze_support
from threading import Thread
import winsound
import os
from bs4 import BeautifulSoup as bs
import re
import requests
import subprocess
from context import *
import time
import httplib
import MultipartPostHandler


class My_Frame(wx.Frame):

	s_app_title = u'새로운 초록멀티 v1.2'
	sound_dir = os.path.dirname(sys.argv[0]) + r'\sound'
	down_dict = {}
	info_dict = {}
	cmd_exit = []

	def __init__(self):
		super(My_Frame, self).__init__(None, -1)
		self.Title = self.s_app_title
		self.Size = wx.Size(1015, 600)
		self.q = Queue()
		self.q2 = Queue()

# 풀다운 메뉴 설정
		menubar = wx.MenuBar()
		file_menu = wx.Menu()
		notice_mi = wx.MenuItem(file_menu, wx.ID_ANY, u'&1. 공지사항')
		file_menu.AppendItem(notice_mi)
		self.Bind(wx.EVT_MENU, self.on_notice_mi, notice_mi)
		mart_mi = wx.MenuItem(file_menu, wx.ID_ANY, u'&2. 나눔장터')
		file_menu.AppendItem(mart_mi)
		self.Bind(wx.EVT_MENU, self.on_mart_mi, mart_mi)
		free_mi = wx.MenuItem(file_menu, wx.ID_ANY, u'&3. 우리들의 이야기')
		file_menu.AppendItem(free_mi)
		self.Bind(wx.EVT_MENU, self.on_free_mi, free_mi)

# 자료실
		data_menu = wx.Menu()
		os_mi = wx.MenuItem(data_menu, -1, u'&1. 운영체제/드라이버')
		data_menu.AppendItem(os_mi)
		self.Bind(wx.EVT_MENU, self.on_os_mi, os_mi)
		gen_mi = wx.MenuItem(data_menu, -1, u'&2. 일반자료실')
		data_menu.AppendItem(gen_mi)
		self.Bind(wx.EVT_MENU, self.on_gen_mi, gen_mi)
		port_mi = wx.MenuItem(data_menu, -1, u'&3. 포터블자료실')
		data_menu.AppendItem(port_mi)
		self.Bind(wx.EVT_MENU, self.on_port_mi, port_mi)
		multi_mi = wx.MenuItem(data_menu, -1, u'&4. 멀티미디어/인터넷')
		data_menu.AppendItem(multi_mi)
		self.Bind(wx.EVT_MENU, self.on_multi_mi, multi_mi)
		auto_mi = wx.MenuItem(data_menu, -1, u'&5. 프로그램 자동설치')
		data_menu.AppendItem(auto_mi)
		self.Bind(wx.EVT_MENU, self.on_auto_mi, auto_mi)
		lect_mi = wx.MenuItem(data_menu, -1, u'&6. 강의실')
		data_menu.AppendItem(lect_mi)
		self.Bind(wx.EVT_MENU, self.on_lect_mi, lect_mi)
		etc_mi = wx.MenuItem(data_menu, -1, u'&7. 기타자료실')
		data_menu.AppendItem(etc_mi)
		self.Bind(wx.EVT_MENU, self.on_etc_mi, etc_mi)
		file_menu.AppendMenu(-1, u'&4. 자료실', data_menu)

# 시각장애인 대학생 후원 희망통장
		gibu_menu = wx.Menu()
		gongji_mi = wx.MenuItem(gibu_menu, -1, u'&1. 공지사항 및 후원내역')
		gibu_menu.AppendItem(gongji_mi)
		self.Bind(wx.EVT_MENU, self.on_gongji_mi, gongji_mi)
		story_mi = wx.MenuItem(gibu_menu, -1, u'&2. 포근한 이야기방')
		gibu_menu.AppendItem(story_mi)
		self.Bind(wx.EVT_MENU, self.on_story_mi, story_mi)
		jaryo_mi = wx.MenuItem(gibu_menu, -1, u'&3. 자료실')
		gibu_menu.AppendItem(jaryo_mi)
		self.Bind(wx.EVT_MENU, self.on_jaryo_mi, jaryo_mi)
		file_menu.AppendMenu(-1, u'&5. 시각장애인 대학생 후원 희망통장', gibu_menu)

# 엔터테인먼트
		enter_menu = wx.Menu()
		kpop_mi = wx.MenuItem(enter_menu, -1, u'&1. 가요')
		enter_menu.AppendItem(kpop_mi)
		self.Bind(wx.EVT_MENU, self.on_kpop_mi, kpop_mi)
		mov_mi = wx.MenuItem(enter_menu, -1, u'&2. 동영상')
		enter_menu.AppendItem(mov_mi)
		self.Bind(wx.EVT_MENU, self.on_mov_mi, mov_mi)
		pop_mi = wx.MenuItem(enter_menu, -1, u'&3. 팝/클래식')
		enter_menu.AppendItem(pop_mi)
		self.Bind(wx.EVT_MENU, self.on_pop_mi, pop_mi)
		mr_mi = wx.MenuItem(enter_menu, -1, u'&4. MR노래방')
		enter_menu.AppendItem(mr_mi)
		self.Bind(wx.EVT_MENU, self.on_mr_mi, mr_mi)
		album_mi = wx.MenuItem(enter_menu, -1, u'&5. 앨범')
		enter_menu.AppendItem(album_mi)
		self.Bind(wx.EVT_MENU, self.on_album_mi, album_mi)
		gita_mi = wx.MenuItem(enter_menu, -1, u'&6. 기타자료실')
		enter_menu.AppendItem(gita_mi)
		self.Bind(wx.EVT_MENU, self.on_gita_mi, gita_mi)
		request_mi = wx.MenuItem(enter_menu, -1, u'&7. 요청게시판')
		enter_menu.AppendItem(request_mi)
		self.Bind(wx.EVT_MENU, self.on_request_mi, request_mi)
		file_menu.AppendMenu(-1, u'&6. 엔터테인먼트', enter_menu)

		skype_mi = wx.MenuItem(file_menu, wx.ID_ANY, u'&7. 스카이프 친구등록')
		file_menu.AppendItem(skype_mi)
		self.Bind(wx.EVT_MENU, self.on_skype_mi, skype_mi)
		qna_mi = wx.MenuItem(file_menu, wx.ID_ANY, u'&9. 질문게시판')
		file_menu.AppendItem(qna_mi)
		self.Bind(wx.EVT_MENU, self.on_qna_mi, qna_mi)

		change_mi = wx.MenuItem(file_menu, wx.ID_ANY, u'다운로드 폴더 변경')
		file_menu.AppendItem(change_mi)
		self.Bind(wx.EVT_MENU, self.on_change_mi, change_mi)
		open_mi = wx.MenuItem(file_menu, wx.ID_ANY, u'다운로드 폴더 열기\tCtrl+O')
		file_menu.AppendItem(open_mi)
		self.Bind(wx.EVT_MENU, self.on_open_mi, open_mi)

		downloading_mi = wx.MenuItem(file_menu, wx.ID_ANY, u'다운로드 파일 정보\tCtrl+J')
		file_menu.AppendItem(downloading_mi)
		self.Bind(wx.EVT_MENU, self.on_downloading_mi, downloading_mi)

		logout_mi = wx.MenuItem(file_menu, wx.ID_ANY, u'로그인 정보 삭제\tCtrl+X')
		file_menu.AppendItem(logout_mi)
		self.Bind(wx.EVT_MENU, self.on_logout_mi, logout_mi)

		quit_mi = wx.MenuItem(file_menu, wx.ID_ANY, u'종료(&X)')
		file_menu.AppendItem(quit_mi)
		self.Bind(wx.EVT_MENU, self.on_close, quit_mi)

		menubar.Append(file_menu, u'초록등대(&G)')

		kbu_menu = wx.Menu()
		kbu_notice_menu = wx.Menu()
		kbu_notice_mi = wx.MenuItem(kbu_notice_menu, -1, u'&1. 공지사항')
		kbu_notice_menu.AppendItem(kbu_notice_mi)
		self.Bind(wx.EVT_MENU, self.on_kbu_notice_mi, kbu_notice_mi)
		kbu_last_notice_mi = wx.MenuItem(kbu_notice_menu, -1, u'&2. 지난 공지')
		kbu_notice_menu.AppendItem(kbu_last_notice_mi)
		self.Bind(wx.EVT_MENU, self.on_kbu_last_notice_mi, kbu_last_notice_mi)
		kbu_guide_mi = wx.MenuItem(kbu_notice_menu, -1, u'&3. 마을 이용안내')
		kbu_notice_menu.AppendItem(kbu_guide_mi)
		self.Bind(wx.EVT_MENU, self.on_kbu_guide_mi, kbu_guide_mi)
		kbu_menu.AppendMenu(-1, u'&1. 공지사항 및 이용안내', kbu_notice_menu)

		kbu_bbs_menu = wx.Menu()
		kbu_free_mi = wx.MenuItem(kbu_bbs_menu, -1, u'&1. 자유게시판')
		kbu_bbs_menu.AppendItem(kbu_free_mi)
		self.Bind(wx.EVT_MENU, self.on_kbu_free_mi, kbu_free_mi)
		kbu_freeinfo_mi = wx.MenuItem(kbu_bbs_menu, -1, u'&2. 자유공지 / 광고')
		kbu_bbs_menu.AppendItem(kbu_freeinfo_mi)
		self.Bind(wx.EVT_MENU, self.on_kbu_freeinfo_mi, kbu_freeinfo_mi)
		kbu_mart_mi = wx.MenuItem(kbu_bbs_menu, -1, u'&3. 벼룩시장 / 구인, 구직')
		kbu_bbs_menu.AppendItem(kbu_mart_mi)
		self.Bind(wx.EVT_MENU, self.on_kbu_mart_mi, kbu_mart_mi)
		kbu_comedy_mi = wx.MenuItem(kbu_bbs_menu, -1, u'&7. 유머 / 공포 / 황당')
		kbu_bbs_menu.AppendItem(kbu_comedy_mi)
		self.Bind(wx.EVT_MENU, self.on_kbu_comedy_mi, kbu_comedy_mi)
		kbu_menu.AppendMenu(-1, u'&3. 게시판', kbu_bbs_menu)

		menubar.Append(kbu_menu, u'넓은마을(&K)')
		self.SetMenuBar(menubar)

# 패널
		panel = wx.Panel(self, -1)
		panel.SetAutoLayout(True)

# 목록상자
		lbl_listctrl1 = wx.StaticText(panel, -1, u'게시물 목록', (5, 5), (500, 20))
		self.listctrl1 = wx.ListCtrl(panel, -1, (5, 30), (500, 565), wx.LC_REPORT | wx.LC_SINGLE_SEL)
		self.listctrl1.InsertColumn(0, '', width=50)
		self.listctrl1.InsertColumn(1, '', width=350)
		self.listctrl1.InsertColumn(2, u'작성자', width=100)
		self.listctrl1.Bind(wx.EVT_KEY_DOWN, self.on_listctrl1_key_down)
		self.listctrl1.Bind(wx.EVT_RIGHT_DOWN, self.on_listctrl1_right_down)

# 게시물 읽기 편집창
		lbl_textctrl1 = wx.StaticText(panel, -1, u'본문 영역', (510, 5), (500, 20))
		self.textctrl1 = wx.TextCtrl(panel, wx.ID_ANY, '', (510, 30), (500, 325), wx.TE_MULTILINE | wx.TE_READONLY)
		self.textctrl1.Bind(wx.EVT_KEY_DOWN, self.on_textctrl1_key_down)
		self.textctrl1.Bind(wx.EVT_RIGHT_DOWN, self.on_textctrl1_right_down)

		lbl_textctrl2 = wx.StaticText(panel, -1, u'댓글 영역', (510, 360), (500, 20))
		self.textctrl2 = wx.TextCtrl(panel, wx.ID_ANY, '', (510, 385), (500, 160), wx.TE_MULTILINE | wx.TE_READONLY)
		self.textctrl2.Bind(wx.EVT_KEY_DOWN, self.on_textctrl2_key_down)

		lbl_textctrl3 = wx.StaticText(panel, -1, u'댓글입력', (510, 575), (100, 20))
		self.textctrl3 = wx.TextCtrl(panel, wx.ID_ANY, '', (615, 575), (290, 20), wx.TE_MULTILINE)
		self.textctrl3.Bind(wx.EVT_KEY_DOWN, self.on_textctrl3_key_down)

		self.btn_reple_save = wx.Button(panel, -1, u'댓글저장', (910, 575), (100, 20))
		self.btn_reple_save.Bind(wx.EVT_BUTTON, self.on_reple_save)
		self.btn_reple_save.Bind(wx.EVT_KEY_DOWN, self.on_reple_key_down)
		self.Bind(wx.EVT_CLOSE, self.on_close)

		self.Show(True)

		self.bbs = BBS()
		self.kbu_login()
		self.kill = Thread(target=kill_process, args=(self,))
		self.get_q = Thread(target=get_q, args=(self,))
		self.for_use = Thread(target=for_use, args=(self,))
		self.kill.SetDaemon = True
		self.get_q.SetDaemon = True
		self.for_use.SetDaemon = True
		self.kill.start()
		self.get_q.start()
		self.for_use.start()

	def on_close(self, e):
		d = wx.MessageDialog(self, u'정말로 GreenMulti를 종료할까요?', u'알림', wx.OK | wx.CANCEL)
		if d.ShowModal() == wx.ID_OK:
			if self.down_dict: 
				for f, p in self.down_dict.items(): p.terminate()
				self.exit = 1
				time.sleep(1)
			self.cmd_exit.append(1)
			self.kill.join()
			self.get_q.join()
			self.for_use.join()
			winsound.PlaySound(os.path.dirname(sys.argv[0]) + u'\\sound\\종료.wav'.encode('euc-kr', 'ignore'), winsound.SND_NOSTOP)
			self.Destroy()



	def kbu_login(self):
#		try:
			kbuid = decrypt(read_reg('kbuid'))
			if not kbuid: kbuid = self.inputbox(u'넓은마을 로그인', u'아이디')
			kbupw = decrypt(read_reg('kbupw'))
			if not kbupw: kbupw = self.inputbox(u'넓은마을 로그인', u'비밀번호', pwd=1) 
			if not kbuid or not kbupw: return self.msgbox(u'알림', u'사용자 아이디와 비밀번호는 필수 입력사항입니다.')
			if self.bbs.login('http://web.kbuwel.or.kr/menu/login.php', kbuid, kbupw):
				write_reg('kbuid', encrypt(kbuid))
				write_reg('kbupw', encrypt(kbupw))
				self.play(u'로그인.wav'.encode('euc-kr', 'ignore'))

			else:
				write_reg('kbuid', '')
				write_reg('kbupw', '')
				return self.msgbox(u'알림', u'초록등대 회원인증에 실패했습니다.')
#		except:
#			pass

	def on_logout_mi(self, e):
		try:
			write_reg('kbuid', '')
			write_reg('kbupw', '')
			self.msgbox(u'알림', u'로그인 정보를 삭제했습니다. 프로그램을 다시 실행하실 때 아이디와 비밀번호를 입력하셔야 합니다.')
		except:
			self.msgbox(u'오류', u'로그인 정보 삭제에 실패했습니다.')


	def inputbox(self, title, text, pwd=0):
		style = wx.OK | wx.CANCEL | wx.TE_PASSWORD if pwd else wx.OK | wx.CANCEL
		entry = wx.TextEntryDialog(self, text, title, '', style)
		if entry.ShowModal() == wx.ID_OK: return entry.GetValue()
		entry.Destroy()


	def msgbox(self, title, text):
		d = wx.MessageDialog(self, text, title, wx.OK)
		d.ShowModal()
		d.Destroy()

	def play(self, file):
		try:
			winsound.PlaySound(self.sound_dir + '\\' + file, winsound.SND_ASYNC)
		except:
			pass


	def on_free_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green3&mo=green&&gonum=&s_que=')

	def on_notice_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green1&mo=green&&gonum=&s_que=')

	def on_mart_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green2&mo=green&&gonum=&s_que=')

	def on_skype_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green7&mo=green&&gonum=&s_que=')

	def on_qna_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green9&mo=green&&gonum=&s_que=')

	def on_os_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green41&mo=green&&gonum=&s_que=')

	def on_gen_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green42&mo=green&&gonum=&s_que=')

	def on_port_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green43&mo=green&&gonum=&s_que=')

	def on_multi_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green44&mo=green&&gonum=&s_que=')

	def on_auto_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green45&mo=green&&gonum=&s_que=')

	def on_lect_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green46&mo=green&&gonum=&s_que=')

	def on_etc_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green47&mo=green&&gonum=&s_que=')

	def on_kpop_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green61&mo=green6&&gonum=&s_que=')

	def on_mov_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green62&mo=green&&gonum=&s_que=')

	def on_pop_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green63&mo=green&&gonum=&s_que=')

	def on_mr_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green64&mo=green&&gonum=&s_que=')

	def on_album_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green65&mo=green&&gonum=&s_que=')

	def on_gita_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green66&mo=green&&gonum=&s_que=')

	def on_request_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green699&mo=green6&1&gonum=&s_que=')

	def on_gongji_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green51&mo=green&&gonum=&s_que=')

	def on_story_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green52&mo=green&&gonum=&s_que=')

	def on_jaryo_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/index.php?page=1&club=green&bcode=green53&mo=green&&gonum=&s_que=')

	def on_change_mi(self, e):
		try:
			down = read_reg('down_dir')
			if not down: down = 'c:\\'
			fd = wx.DirDialog(self, u'다운로드 폴더 변경', down)
			if fd.ShowModal() == wx.ID_OK:
				write_reg('down_dir', fd.GetPath())
				fd.Destroy()
		except:
			pass

	def on_open_mi(self, e):
		down_dir = read_reg('down_dir') if read_reg('down_dir') else 'c:\\'
		subprocess.call(['explorer.exe', down_dir])

	def on_downloading_mi(self, e):
		dd = downloading(self)

	def on_kbu_notice_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/?page=1&club=main&bcode=notice&mo=guide&&gonum=&s_que=')

	def on_kbu_last_notice_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/?page=1&club=main&bcode=oldinfo&mo=guide&&gonum=&s_que=')

	def on_kbu_guide_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/?page=1&club=main&bcode=rtguide&mo=guide&&gonum=&s_que=')

	def on_kbu_free_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/?page=1&club=main&bcode=free&mo=bbs&&gonum=&s_que=')

	def on_kbu_freeinfo_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/?page=1&club=main&bcode=freeinfo&mo=bbs&&gonum=&s_que=')

	def on_kbu_mart_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/?page=1&club=main&bcode=mark&mo=bbs&&gonum=&s_que=')

	def on_kbu_comedy_mi(self, e):
		self.open_bbs('http://web.kbuwel.or.kr/menu/?page=1&club=main&bcode=humor&mo=bbs&&gonum=&s_que=')



	def clear(self, b=True):
		if b: self.listctrl1.DeleteAllItems()
		self.textctrl1.Clear()
		self.textctrl2.Clear()
		self.textctrl3.Clear()

	def open_bbs(self, url):
		self.bbs.open(url)
		self.clear()
		self.display_link()
		self.listctrl1.SetFocus()
		self.play(u'목록열림.wav'.encode('euc-kr', 'ignore'))


	def display_view(self):
		try:
			self.textctrl1.SetValue(self.bbs.view.text)
			self.textctrl2.SetValue(self.bbs.view.replies)
			self.textctrl3.Clear()
			self.play(u'페이지열림.wav'.encode('euc-kr', 'ignore'))
		except:
			pass

	def display_link(self):
		try:
			if not self.bbs.link: return
			l = self.bbs.link.items()
			l.sort()
			l.reverse()
			for num, info in l:
				index = self.listctrl1.InsertStringItem(sys.maxint, str(num))
				self.listctrl1.SetStringItem(index, 1, info[0])
				self.listctrl1.SetStringItem(index, 2, info[1])
		except:
			pass

	def on_listctrl1_key_down(self, e):
		k = e.GetKeyCode()

# 엔터키로 동작
		if k == wx.WXK_RETURN:
			self.open_article()

		elif k == wx.WXK_PAGEDOWN:
			self.next_page()

		elif k == wx.WXK_PAGEUP:
			self.previous_page()

# 글쓰기
		elif k== ord('W'):
			href = self.get_list_item()
			self.bbs.view.read(href)
			self.write_article('write')

		elif k== ord('E'):
			href = self.get_list_item()
			self.bbs.view.read(href)
			self.write_article('edit')

# 게시물 삭제
		elif k == wx.WXK_DELETE: 
			href = self.get_list_item()
			self.bbs.view.read(href)
			self.delete_article()


		elif k == ord('D'):
			href = self.get_list_item()
			self.bbs.view.read(href)
			self.start_download()

# 검색
		elif k == ord('F'):
			self.search_bbs()

		else:
			e.Skip()

	def search_bbs(self):
		try:
			if not self.bbs.info['init_url']: return
			kwd = self.inputbox(u'검색', u'검색할 단어를 입력하세요.')
			if kwd: 
				self.bbs.params = {'s_que': kwd.encode('euc-kr', 'ignore'), 's_ord_r': u'번호2'.encode('euc-kr', 'ignore'), 'field_r': 'all'}
			else:
				return
			self.bbs.get(self.bbs.info['init_url'])
			self.bbs.get_info()
			self.bbs.info['page'] = 1
			self.clear()
			self.display_link()
			self.play(u'목록열림.wav'.encode('euc-kr', 'ignore'))
		except:
			pass


	def on_listctrl1_right_down(self, e):
		self.PopupMenu(ListCtrl_PopupMenu(self), e.GetPosition())


	def on_textctrl1_right_down(self, e):
		self.PopupMenu(TextCtrl_PopupMenu(self), e.GetPosition())


	def get_list_item(self):
		try:
			n = self.listctrl1.GetFocusedItem()
			if n == -1: return ''
			num = int(self.listctrl1.GetItemText(n, 0))
			href = self.bbs.link[num][2]
			return href
		except:
			return ''


	def open_article(self):
		try:
			href = self.get_list_item()
			if not href: return
			self.bbs.view.read(href)
			self.display_view()
			self.textctrl1.SetFocus()
		except:
			pass


	def write_article(self, mode):
		try:
			url = self.bbs.view.info['write_url' if mode == 'write' else 'edit_url']
			self.bbs.view.get_fields(url)
			wd = write_dialog(self, u'게시물 쓰기' if mode == 'write' else u'게시물 수정하기')
			if not self.bbs.view.write(): return
			self.clear()
			self.bbs.open(self.bbs.info['init_url'])
			self.display_link()
			self.listctrl1.SetFocus()
			self.play(u'목록열림.wav'.encode('euc-kr', 'ignore'))
		except:
			pass


	def delete_article(self):
		try:
			if not 'delete_url' in self.bbs.view.info: return
			title = self.bbs.view.title
			d = wx.MessageDialog(self, u'게시물을 정말로 삭제할까요?\r\n제목 : ' + title, u'게시물 삭제 경고', wx.OK | wx.CANCEL)
			if d.ShowModal() == wx.ID_OK:
				self.bbs.view.delete()
				self.bbs.open(self.bbs.info['url'])
				self.clear()
				self.display_link()
				self.play(u'삭제.wav'.encode('euc-kr', 'ignore'))
				d.Destroy()
				self.listctrl1.SetFocus()
		except:
			pass


	def next_page(self):
		try:
			if not self.bbs.info['init_url']: return
			self.bbs.move(True)
			self.clear()
			self.display_link()
			self.play(u'목록열림.wav'.encode('euc-kr', 'ignore'))
		except:
			pass

	def previous_page(self):
		try:
			if not self.bbs.info['init_url']: return
			if self.bbs.info['page'] == 1: return
			self.bbs.move(False)
			self.clear()
			self.display_link()
			self.play(u'목록열림.wav'.encode('euc-kr', 'ignore'))
		except:
			pass


	def start_download(self):
		try:
			if not self.bbs.view.files: return
			for f, u in self.bbs.view.files.items():
				if f in self.down_dict: return
				p = Process(target=download, args=(f, u, self.q, self.q2))
				p.SetDaimon = True
				p.start()
				self.down_dict[f] = p
				self.play(u'다운로드시작.wav'.encode('euc-kr', 'ignore'))
		except:
			pass


	def on_textctrl1_key_down(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_ESCAPE:
			self.listctrl1.SetFocus()

		elif k == ord('W'):
			self.write_article('write')

		elif k == ord('E'):
			self.write_article('edit')

		elif k == wx.WXK_DELETE:
			self.delete_article()

		elif k == ord('D'):
			self.start_download()

		else:
			e.Skip()


	def on_textctrl2_key_down(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_ESCAPE:
			self.listctrl1.SetFocus()

		elif k == wx.WXK_RETURN:
			try:
				n = self.textctrl2.GetInsertionPoint()
				x, y = self.textctrl2.PositionToXY(n)
				l = self.textctrl2.GetLineText(y)
				m = re.match(u'^\\d+ 번 리플삭제', l)
				if not l or m is None: return
				d = wx.MessageDialog(self, l[:-4] + u'댓글을 정말로 삭제할까요?', u'댓글 삭제', wx.OK | wx.CANCEL)
				if d.ShowModal() == wx.ID_OK:
					href = self.bbs.info['base'] + '/menu/index.php' + self.bbs.view.soup.find(name='a', title=m.group())['href']
					self.bbs.open(self.bbs.info['url'])
					self.bbs.view.read(href)
					self.clear(True)
					self.display_link()
					self.display_view()
					self.play(u'댓글삭제.wav'.encode('euc-kr', 'ignore'))
			except:
				pass

		elif k == wx.WXK_PAGEDOWN:
			try:
				text = self.textctrl2.GetValue().replace('\n', '\n\n')
				if not text: return
				n = self.textctrl2.GetInsertionPoint()
				p = text.find('[', n+1)
				if p == -1: return winsound.Beep(1000, 100)
				self.textctrl2.SetInsertionPoint(p)
			except:
				pass

		elif k == wx.WXK_PAGEUP:
			try:
				text = self.textctrl2.GetValue().replace('\n', '\n\n')
				if not text: return
				n = self.textctrl2.GetInsertionPoint()
				p = text.rfind('[', 0, n-1)
				if p == -1: return winsound.Beep(1000, 100)
				self.textctrl2.SetInsertionPoint(p)
			except:
				pass

		else:
			e.Skip()


	def on_textctrl3_key_down(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_ESCAPE:
			self.listctrl1.SetFocus()

		else:
			e.Skip()


	def on_reple_save(self, e):
		try:
			ccmemo = self.textctrl3.GetValue()
			if not ccmemo: return
			ccmemo = ccmemo.replace('"', r'\"')
			ccmemo = ccmemo.replace("'", r"\'")
			self.bbs.view.data.clear()
			hiddens = self.bbs.view.soup(name='input', type='hidden')
			for h in hiddens:
				self.bbs.view.data[h['name']] = h['value']

			form = self.bbs.view.soup.find(name='form', action=re.compile(r'(?i)/menu/'))
			action = self.bbs.info['base'] + form['action']

			self.bbs.view.data['ccmemo'] = ccmemo.encode('euc-kr', 'ignore')
			self.bbs.view.data['ccname'] = self.bbs.view.soup.find(name='input', type='text')['value'].encode('euc-kr', 'ignore')
			view_url = self.bbs.view.info['url']
			self.bbs.view.post(action)

			self.bbs.view.data.clear()
			self.bbs.open(self.bbs.info['url'])
			self.bbs.view.read(view_url)

			self.clear(True)
			self.display_link()
			self.display_view()
			self.textctrl3.Clear()
			self.textctrl2.SetFocus()
			self.play(u'댓글달기.wav'.encode('euc-kr', 'ignore'))
		except:
			pass


	def on_reple_key_down(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_ESCAPE:
			self.listctrl1.SetFocus()
		else:
			e.Skip()


	def display_reples(self):
		try:
			reples = ''
			tables = self.soup('table')
			trs = tables[7].find_all('tr')
			for tr in trs:
				try:
					reples += '\r\n[' + tr.td.get_text() + ']\r\n' + tr.td.next_sibling.next_sibling.get_text() + '\r\n' 
					if tr.td.next_sibling.next_sibling.next_sibling.next_sibling.a is not None: reples += tr.td.next_sibling.next_sibling.next_sibling.next_sibling.a['title'] 

				except:
					pass
			self.textctrl2.SetValue(reples)
			return True
		except:
			return False



class write_dialog(wx.Dialog):
	def __init__(self, parent, title):
		super(write_dialog, self).__init__(parent, -1, title, wx.DefaultPosition, wx.Size(800, 600))

		lbl_title = wx.StaticText(self, -1, u'제목', (5, 5), (100, 20))
		self.textctrl1 = wx.TextCtrl(self, -1, '', (110, 5), (685, 20))
		self.textctrl1.SetValue(my_frame.bbs.view.fields['title'])

		lbl_body = wx.StaticText(self, -1, u'내용', (5, 30), (100, 20))
		self.textctrl2 = wx.TextCtrl(self, -1, '', (110, 30), (685, 540), wx.TE_MULTILINE)
		self.textctrl2.SetValue(my_frame.bbs.view.fields['body'])

		self.btn_save = wx.Button(self, -1, u'저장', (590, 475), (100, 20))
		self.btn_save.Bind(wx.EVT_BUTTON, self.on_save)
		self.btn_cancel = wx.Button(self, wx.ID_EXIT, u'취소', (695, 475), (100, 20))
		self.btn_cancel.Bind(wx.EVT_BUTTON, self.on_close)

		self.Bind(wx.EVT_CLOSE, self.on_close)

# 단축키 지정
		accel = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_ESCAPE, wx.ID_EXIT)])
		self.SetAcceleratorTable(accel)
		self.ShowModal()


	def on_close(self, e):
		my_frame.bbs.view.fields['action'] = ''
		my_frame.bbs.view.fields['title'] = ''
		my_frame.bbs.view.fields['body'] = ''
		self.Destroy()

	def on_save(self, e):
		title = self.textctrl1.GetValue()
		body = self.textctrl2.GetValue()
		if not title or not body: return self.msgbox(u'알림', u'제목과 내용은 필수 입력사항입니다.')
		my_frame.bbs.view.fields['title'] = title
		my_frame.bbs.view.fields['body'] = body + '\r\n'
		self.Destroy()

	def msgbox(self, title, text):
		d = wx.MessageDialog(self, text, title, wx.OK)
		d.ShowModal()
		d.Destroy()


class downloading(wx.Dialog):
	def __init__(self, parent):
		super(downloading, self).__init__(parent, -1, u'다운로드 파일 정보', wx.DefaultPosition, wx.Size(500, 500))

		self.parent = parent

		self.Bind(wx.EVT_CLOSE, self.on_close)

		self.listctrl = wx.ListCtrl(self, -1, (5, 5), (490, 490), wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_SORT_ASCENDING)
		self.listctrl.InsertColumn(0, '', width=50)
		self.listctrl.InsertColumn(1, '', width=240)
		self.listctrl.InsertColumn(2, u'속도', width=50)
		self.listctrl.InsertColumn(3, '')
		self.listctrl.Bind(wx.EVT_KEY_DOWN, self.on_listctrl)

		self.get_info()
		self.ShowModal()


	def on_close(self, e):
		self.Destroy()

	def on_listctrl(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_ESCAPE:
			self.Destroy()

		elif k == ord(' ') or k == wx.WXK_RETURN:
			self.get_info()

		elif k == wx.WXK_DELETE:
			self.cancel()

		else:
			e.Skip()


	def cancel(self):
		try:
			d = wx.MessageDialog(self, '다운로드를 중단할까요?', '알림', wx.OK | wx.CANCEL)
			if d.ShowModal() == wx.ID_OK:
				n = self.listctrl.GetFocusedItem()
				if n == -1: return ''
				f = self.listctrl.GetItemText(n, 1)
				if not f in self.parent.down_dict: return
				pid = self.parent.down_dict.pop(f)
				pid.terminate()
				self.parent.info_dict.pop(f)
				self.get_info()
		except:
			pass


	def get_info(self):
		self.listctrl.DeleteAllItems()
		if not self.parent.info_dict: return

		for f, info in self.parent.info_dict.items():
			if info[0] == info[1]: continue
			if not f in self.parent.down_dict: continue
			index = self.listctrl.InsertStringItem(sys.maxint, '%5.1f%%' % (info[1] * 100 / info[0],))
			self.listctrl.SetStringItem(index, 1, f)
			self.listctrl.SetStringItem(index, 2, '%5.2fMB/s' % (info[1] / (info[3] - info[2]) / 1024 / 1024,))
			self.listctrl.SetStringItem(index, 3, u'남은 시간 : %s 현재 : %5.2f MB 전체 : %5.2f MB' % (self.remain(info), info[1] / 1024 / 1024, info[0] / 1024 / 1024))

	def remain(self, info):
		try:
			t1 = info[3] - info[2]
			t2 = int((info[0] - info[1]) * t1 / info[1])
			if t2 <= 60: 
				return u'%s초' % t2
			else:
				min = t2 // 60
				sec = t2%60
				return u'%s분 %s초' % (min, sec)
			

		except:
			return ''


if __name__ == '__main__':
	freeze_support()
	app = wx.App()
	my_frame = My_Frame()
	app.MainLoop()
