# coding: utf-8
# 메인 프로그램

import sys
from util import *
from web import *
import winsound
import os
import wx
from bs4 import BeautifulSoup as bs
from multiprocessing import Process, Queue, freeze_support
from threading import Thread
import time
import subprocess

reload(sys)
sys.setdefaultencoding('utf-8')


class GreenMulti(wx.Frame, WebProcess):
	def __init__(self, title):
		WebProcess.__init__(self)
		Utility.__init__(self)
		wx.Frame.__init__(self, None, -1, title)

		self.limit = 100
		self.ResQ = Queue()
		self.dProcess = {}
		self.dTransInfo = {}
		self.msg = ""
		self.p_num = 0
# Queue 관리자를 실행
		self.th = Thread(target=QueueManager, args=(self,))
		self.th.start()

		self.Size = wx.Size(1015, 410)

		menubar = wx.MenuBar()
		file_menu = wx.Menu()
		help_mi = wx.MenuItem(file_menu, wx.ID_ANY, u"도움말\tF1")
		file_menu.AppendItem(help_mi)
		self.Bind(wx.EVT_MENU, self.OnHelp, help_mi)
		lib_mi = wx.MenuItem(file_menu, wx.ID_ANY, u"아이프리 전자도서관\tCtrl+L")
		file_menu.AppendItem(lib_mi)
		self.Bind(wx.EVT_MENU, self.OnLibrary, lib_mi)
		home_mi = wx.MenuItem(file_menu, wx.ID_ANY, u"홈으로 이동\tAlt+Home")
		file_menu.AppendItem(home_mi)
		self.Bind(wx.EVT_MENU, self.OnComeBackHome, home_mi)
		find_mi = wx.MenuItem(file_menu, wx.ID_ANY, u"검색\tCtrl+F")
		file_menu.AppendItem(find_mi)
		self.Bind(wx.EVT_MENU, self.OnFind, find_mi)
		direct_mi = wx.MenuItem(file_menu, wx.ID_ANY, u"코드 바로가기\tCtrl+G")
		file_menu.AppendItem(direct_mi)
		self.Bind(wx.EVT_MENU, self.OnDirectMove, direct_mi)
		status_mi = wx.MenuItem(file_menu, wx.ID_ANY, u"파일 전송 정보\tCtrl+J")
		file_menu.AppendItem(status_mi)
		self.Bind(wx.EVT_MENU, self.OnTransferStatus, status_mi)
		opendir_mi = wx.MenuItem(file_menu, wx.ID_ANY, u"다운로드 폴더 열기\tCtrl+O")
		file_menu.AppendItem(opendir_mi)
		self.Bind(wx.EVT_MENU, self.OnOpenDownFolder, opendir_mi)
		chdir_mi = wx.MenuItem(file_menu, wx.ID_ANY, u"다운로드 폴더 변경")
		file_menu.AppendItem(chdir_mi)
		self.Bind(wx.EVT_MENU, self.OnChangeDownFolder, chdir_mi)
		init_mi = wx.MenuItem(file_menu, wx.ID_ANY, u"설정 초기화")
		file_menu.AppendItem(init_mi)
		self.Bind(wx.EVT_MENU, self.OnInitialize, init_mi)
		quit_mi = wx.MenuItem(file_menu, wx.ID_ANY, u'종료(&X)\tAlt+F4)')
		file_menu.AppendItem(quit_mi)
		self.Bind(wx.EVT_MENU, self.OnClose, quit_mi)

		menubar.Append(file_menu, u'파일(&F)')
		self.SetMenuBar(menubar)


		panel = wx.Panel(self, -1)
		panel.SetAutoLayout(True)

		lbl_listctrl = wx.StaticText(panel, -1, u'메뉴, 게시물', (5, 5), (500, 20))
		self.listctrl = wx.ListCtrl(panel, -1, (5, 30), (500, 375), wx.LC_REPORT | wx.LC_SINGLE_SEL)
		self.listctrl.InsertColumn(0, '', width=400)
		self.listctrl.InsertColumn(1, u'작성자', width=100)
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
		self.btn_reple_save.Bind(wx.EVT_BUTTON, self.OnSaveReplies)
		self.btn_reple_save.Bind(wx.EVT_KEY_DOWN, self.OnRepleKeyDown)
		self.Bind(wx.EVT_CLOSE, self.OnClose)

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
				self.Play("start.wav")
			else:
				self.WriteReg('kbuid', '')
				self.WriteReg('kbupw', '')
				return self.MsgBox(u'알림', u'넓은마을 로그인에 실패했습니다.')

			self.Get('http://web.kbuwel.or.kr/menu/index.php?mo=green6&club=green&bcode=green61')
			if u'목록 조회 권한이 없습니다' in self.soup.get_text():
				self.limit = 3
				return
			else:
				foruser = Thread(target=ForUser, args=(self,))
				foruser.start()

		except:
			pass



	def OnClose(self, e):
		try:
			if self.dProcess: 
				if not self.MsgBox(u"경고", u"파일 전송이 완료되지 않았습니다. 그래도 종료하시겠습니까?", question=True): 
					return

			self.Play("end.wav")
			self.msg = "exit"
			time.sleep(1)
			self.th.join()
			self.OnAllKill(e)
			self.Destroy()
		except:
			sys.exit()

	def OnAllKill(self, e):
		try:
			if self.dProcess: 
				for k, v in self.dProcess.items():
					try:
						v.terminate()
					except:
						pass
		except:
			pass


	def DisplayItems(self, mode):
		if mode == "menu" or mode == "list":
			self.listctrl.DeleteAllItems()
			for t in self.lItemList:
				index = self.listctrl.InsertStringItem(sys.maxint, t[1])
				self.listctrl.SetStringItem(index, 1, t[2])
		elif mode == "view":
			text = self.ViewInfo["content"]
			text = text.replace("\r", "")
			text = re.sub(r"(.*)(\n+)(.*)", r"\1\r\n\3", text)
			self.textctrl1.SetValue(text)
			self.textctrl2.SetValue(self.ViewInfo["replies"])
			self.textctrl3.Clear()

	def listctrl_KeyDown(self, e):
		try:
			self.try_listctrl_KeyDown(e)
		except:
			pass

	def try_listctrl_KeyDown(self, e):
		k = e.GetKeyCode()

		if k == wx.WXK_UP:
			e.Skip()
			n = self.listctrl.GetFocusedItem()
			if n <= 0: 
				self.Play("beep.wav")

		elif k == wx.WXK_DOWN:
			e.Skip()
			n = self.listctrl.GetFocusedItem()
			if n == len(self.lItemList) - 1:
				self.Play("beep.wav")

		elif k == wx.WXK_RETURN:
			n = self.listctrl.GetFocusedItem()
			if n == -1: return

# 메일쓰기
			if "mail.php" in self.lItemList[n][3] and "cmd=write" in self.lItemList[n][3]:
				self.WriteMail(u"메일 쓰기", receiver="", retitle="", rebody="")
				return
# 동호회 회원가입
			elif "club_join&mo=green" in self.lItemList[n][3]:
				self.MemberJoin()
				return

# 일반적인 처리 시작
			r = self.GetInfo(self.lItemList[n])
			if r: 
				self.DisplayItems(r)
				self.Play("page_next.wav")
				if r == "view": self.textctrl1.SetFocus()

		elif (e.GetModifiers() == wx.MOD_ALT and k == wx.WXK_LEFT) or k == wx.WXK_ESCAPE or k == 8:
			parent = self.dTreeMenu[self.bcode][1]
			if not parent: 
				self.Play("home.wav")
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

		elif k == ord("W") or k == ord("w"):
			self.WriteArticle()

		elif k == wx.WXK_DELETE:
			n = self.listctrl.GetFocusedItem()
			if n == -1 or not ("cmd=view" in self.lItemList[n][3]): return 
			url = self.lItemList[n][3] if type(self.lItemList[n][3]) == str else self.lItemList[n][3].encode("euc-kr", "ignore")
			res = self.opener.open(url)
			html = unicode(res.read(), "euc-kr", "ignore")
			soup = bs(html, "html.parser")
			if "mail.php" in self.lItemList[n][3]:
				deltag = soup.find("a", href=re.compile(r"(?ims)cmd=del2"))
			else:
				deltag = soup.find("a", href=re.compile(r"(?ims)cmd=delete"))
			if deltag is None: return
			self.DeleteArticle(self.ListInfo["host"] + deltag["href"])

		elif k == ord("E") or k == ord("e"):
			n = self.listctrl.GetFocusedItem()
			if n == -1 or not ("cmd=view" in self.lItemList[n][3]): return 
			url = self.lItemList[n][3]
			if type(url) == unicode: url = url.encode("euc-kr", "ignore")
			res = self.opener.open(url)
			html = unicode(res.read(), "euc-kr", "ignore")
			soup = bs(html, "html.parser")
			edittag = soup.find("a", href=re.compile(r"(?ims)cmd=edit"))
			if edittag is None: return
			self.EditArticle(self.ListInfo["host"] + edittag["href"])

		elif k == ord("D") or k == ord("d"):
			n = self.listctrl.GetFocusedItem()
			if n == -1 or not ("cmd=view" in self.lItemList[n][3]): return 
			url = self.lItemList[n][3] if type(self.lItemList[n][3]) == str else self.lItemList[n][3].encode("euc-kr", "ignore")
			res = self.opener.open(url)
			html = unicode(res.read(), "euc-kr", "ignore")
			soup = bs(html, "html.parser")
			files = soup("a", href=re.compile(r"(?ims)cmd=download&"))
			if files is None: return
			dFiles = {}
			for f in files:
				if "mail.php" in self.ListInfo["url"]:
					dFiles[f.get_text()] = "http://web.kbuwel.or.kr/menu/mail.php" + f['href']
				else:
					dFiles[f.img['alt']] = self.ListInfo['host'] + f['href']
			self.Download(dFiles)

		elif k == wx.WXK_F5:
			self.GetInfo(("", "", "", self.ListInfo["url"]))
			self.DisplayItems("list")
			self.Play("refresh.wav")

		elif k == wx.WXK_F2:
			n = self.listctrl.GetFocusedItem()
			if n == -1: return
			self.MsgBox("", self.lItemList[n][3])

		else:
			e.Skip()


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

	def OnTextCtrl1KeyDown(self, e):
		try:
			self.try_OnTextCtrl1KeyDown(e)
		except:
			pass

	def try_OnTextCtrl1KeyDown(self, e):
		k = e.GetKeyCode()

		if k == wx.WXK_ESCAPE or (e.GetModifiers() == wx.MOD_ALT and k == wx.WXK_LEFT) or k == 8:
			self.listctrl.SetFocus()
			self.Play("back.wav")

		elif k == wx.WXK_F5:
			self.GetInfo(("", "", "", self.ViewInfo["url"]))
			self.DisplayItems("view")
			self.textctrl1.SetFocus()
			self.Play("refresh.wav")

		elif k == ord("W") or k == ord("w"):
			self.WriteArticle()

		elif k == wx.WXK_DELETE:
			if not ("delete_url" in self.ViewInfo) or not self.ViewInfo["delete_url"]: return
			self.DeleteArticle(self.ViewInfo["delete_url"])

		elif k == ord("E") or k == ord("e"):
			if not ("edit_url" in self.ViewInfo) or not self.ViewInfo["edit_url"]: return
			self.EditArticle(self.ViewInfo["edit_url"])

		elif k == ord("D") or k == ord("d"):
			if not ("files" in self.ViewInfo) or not self.ViewInfo["files"]: return
			self.Download(self.ViewInfo["files"])

		else:
			e.Skip()
	def OnTextCtrl2KeyDown(self, e):
		try:
			self.try_OnTextCtrl2KeyDown(e)
		except:
			pass

	def try_OnTextCtrl2KeyDown(self, e):
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

		elif k == wx.WXK_RETURN:
#			try:
				n = self.textctrl2.GetInsertionPoint()
				x, y = self.textctrl2.PositionToXY(n)
				l = self.textctrl2.GetLineText(y)
				m = re.match(u'^\\d+ 번 리플삭제', l)
				if not l or m is None: return
				d = wx.MessageDialog(self, l[:-4] + u'댓글을 정말로 삭제할까요?', u'댓글 삭제', wx.OK | wx.CANCEL)
				if d.ShowModal() == wx.ID_OK:
					url = self.ViewInfo["url"]
					href = self.ListInfo['host'] + '/menu/index.php' + self.soup.find(name='a', title=m.group())['href']
					self.GetInfo(("", "", "", href))
					self.ViewInfo["url"] = url
					self.textctrl2.Clear()
					self.DisplayItems("view")
					self.textctrl2.SetFocus()
					self.Play("delete.wav")
#			except:
#				pass

		else:
			e.Skip()

	def OnTextCtrl3KeyDown(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_ESCAPE or (e.GetModifiers() == wx.MOD_ALT and k == wx.WXK_LEFT):
			try:
				self.listctrl.SetFocus()
				self.Play("back.wav")
			except:
				pass

		else:
			e.Skip()


	def OnRepleKeyDown(self, e):
		k = e.GetKeyCode()
		if k == wx.WXK_ESCAPE or (e.GetModifiers() == wx.MOD_ALT and k == wx.WXK_LEFT):
			try:
				self.listctrl.SetFocus()
				self.Play("back.wav")
			except:
				pass

		else:
			e.Skip()


	def OnSaveReplies(self, e):
		try:
			ccmemo = self.textctrl3.GetValue()
			if not ccmemo: return
			ccmemo = ccmemo.replace('"', r'\"')
			ccmemo = ccmemo.replace("'", r"\'")
			if not self.SaveReplies(ccmemo): return
			self.DisplayItems("view")
			self.textctrl2.SetFocus()
			self.Play("replies.wav")
		except:
			self.Play("error.wav")

	def WriteArticle(self):
		if not ("write_url" in self.ListInfo) or not self.ListInfo["write_url"]: return
		url = self.ListInfo["write_url"]
		if type(url) == unicode: url = url.encode("euc-kr", "ignore")
		res = self.opener.open(url)
		html = res.read()
		soup = bs(unicode(html, "euc-kr", "ignore"), "html.parser")
		wd = WriteDialog(self, u"게시물 쓰기", soup)
		if wd.ShowModal() == wx.ID_OK:
			self.p_num += 1
			action = wd.action
			title = wd.textctrl1.GetValue()
			body = wd.textctrl2.GetValue()
			file = wd.attach
			wd.Destroy()
			if not title or not body: return self.MsgBox(u"오류", u"게시물 제목과 본문 내용은 필수 입력사항입니다. 게시물을 올릴 수 없습니다.")
			p = Process(target=Upload, args=(self.ListInfo["host"] + action, title, body, file, self.p_num, self.ResQ))
			p.start()
			if file: 
				self.dProcess[self.p_num] = p

		else:
			wd.Destroy()

	def EditArticle(self, url):
		if type(url) == unicode: url = url.encode("euc-kr", "ignore")
		res = self.opener.open(url)
		html = res.read()
		soup = bs(unicode(html, "euc-kr", "ignore"), "html.parser")
		wd = WriteDialog(self, u"게시물 수정하기", soup)
		if wd.ShowModal() == wx.ID_OK:
			action = wd.action
			title = wd.textctrl1.GetValue()
			body = wd.textctrl2.GetValue()
			file = wd.attach
			wd.Destroy()
			if not title or not body: return self.MsgBox(u"오류", u"게시물 제목과 본문 내용은 필수 입력사항입니다. 게시물을 올릴 수 없습니다.")
			p = Process(target=Upload, args=(self.ListInfo["host"] + action, title, body, file, self.p_num, self.ResQ))
			p.start()
		else:
			wd.Destroy()

	def DeleteArticle(self, url):
		url = url if type(url) == str else url.encode("euc-kr", "ignore")
		list_url = self.ListInfo["url"]
		if not self.MsgBox(u"삭제 경고", u"정말로 게시물을 삭제할까요?", True): return
		self.Get(url)
		self.GetInfo((self.bcode, "", "", list_url))
		self.DisplayItems("list")
		self.textctrl1.Clear()
		self.textctrl2.Clear()
		self.textctrl3.Clear()
		self.listctrl.SetFocus()
		self.Play("delete.wav")


	def Download(self, d):
		if not d: return 
		if self.CheckLimit(): 
			return self.MsgBox(u"동시 다운로드 제한", u"동시 다운로드 제한을 넘어서 다운로드 할 수 없습니다. 잠시 후 다시 다운로드해 주세요.")

		for f, u in d.items():
			self.p_num += 1
			p = Process(target=Download, args=(f, u, self.p_num, self.ResQ))
			p.start()
			self.dProcess[self.p_num] = p
			

	def OnTransferStatus(self, e):
		try:
			ts = TransferStatus(self)
			ts.ShowModal()
			ts.Destroy()
		except:
			pass

	def OnChangeDownFolder(self, e):
		try:
			fd = wx.DirDialog(self, u'다운로드 폴더 변경', u"")
			if fd.ShowModal() == wx.ID_OK:
				fdr = fd.GetPath()
				if type(fdr) == unicode: fdr = fdr.encode("euc-kr", "ignore")
				self.WriteReg('downfolder', fdr)
				self.MsgBox(u"결과", u"다운로드 폴더를 변경했습니다.\n" + self.ReadReg("downfolder"))
				fd.Destroy()
		except:
			pass

	def OnOpenDownFolder(self, e):
		try:
			folder = self.ReadReg("downfolder") if self.ReadReg("downfolder") else "c:\\"
			if type(folder) == unicode: folder = folder.encode("euc-kr", "ignore")
			subprocess.Popen('explorer.exe "' + folder + '"')
		except:
			pass

	def OnComeBackHome(self, e):
		try:
			self.GetInfo(("top", "", "", self.dTreeMenu["top"][2]))
			self.DisplayItems("menu")
			self.listctrl.SetFocus()
			self.Play("back.wav")
		except:
			pass

	def OnHelp(self, e):
		try:
			msg = u"""초록멀티 1.5
제작자 : 장창환
이메일 : 462356@gmail.com
*** 단축키 안내 ***
게시판 진입 : Enter 
되돌아 나오기 : Escape도 되고, BackSpace도 되고, Alt + LeftArrow 중 편할 걸로 사용하세요.
컨트롤 간의 이동: Tab 
홈으로 이동 : Alt + Home
다음 페이지 : Page Down / 이전 페이지 Page Up
게시물 쓰기 : 영문 W / 게시물 수정하기 : 영문 E
게시물 삭제하기 : Delete / 다운로드하기 : 영문 D
목록 새로 고침 : F5
게시물 검색하기 : 컨트롤 영문 F / 코드 바로가기 : 컨트롤 영문 G
다운로드 폴더 열기: Control + 영문 O
파일 전송 정보 보기 : Control + 영문 J
파일 정보 보기 대화상자에서의 단축키
정보 새로고침 : Space  
전송 프로세스 갯수 보기 : Enter
전송 취소 : Delete """

			self.MsgBox(u"도움말", msg)
		except:
			pass

	def OnDirectMove(self, e):
		try:
			code = ""
			dm = DirectMove(self)
			if dm.ShowModal() == wx.ID_OK:
				code = dm.combo.GetValue()
				dm.Destroy()
			else:
				dm.Destroy()
				return
			if not code or not code in self.dTreeMenu: return
			r = self.GetInfo((code, "", "", self.dTreeMenu[code][2]))
			self. DisplayItems(r)
			self.textctrl1.Clear()
			self.textctrl2.Clear()
			self.textctrl3.Clear()
			self.listctrl.SetFocus()
			self.Play("code_move.wav")
		except:
			pass


	def OnFind(self, e):
		try:
			if not "find_action" in self.ListInfo or not self.ListInfo["find_action"]: return
			kwd = self.InputBox(u"게시물 검색", u"키워드")
			if not kwd: return
			base_url, d = self.ParamSplit(self.ListInfo["find_action"])
			d["s_ord_r"] = u"번호2".encode("euc-kr", "ignore")
			d["field_r"] = "all"
			d["s_que"] = kwd.encode("euc-kr", "ignore")
			d["page"] = "1"
			url = base_url + "?" + self.ParamJoin(d, True)
			r = self.GetInfo(("", "", "", url))
			self.DisplayItems(r)
			self.listctrl.SetFocus()
			self.textctrl1.Clear()
			self.textctrl2.Clear()
			self.textctrl3.Clear()
			self.Play("page_next.wav")
		except:
			pass


	def WriteMail(self, title, receiver="", retitle="", rebody=""):
		wd = WriteMailDialog(self, title, receiver, retitle, rebody)
		if wd.ShowModal() == wx.ID_OK:
			receiver = wd.textctrl1.GetValue()
			coreceiver = wd.textctrl2.GetValue()
			title = wd.textctrl3.GetValue()
			body = wd.textctrl4.GetValue() + "\n"
			file1 = wd.attach1
			file2 = wd.attach2
			file3 = wd.attach3
			wd.Destroy()
			if not receiver or not title or not body: return self.MsgBox(u"오류", u"받는 사람, 제목, 본문 내용은 필수 입력사항입니다. 메일을 전송할 수 없습니다.")
			self.p_num += 1
			p = Process(target=SendMail, args=(receiver, coreceiver, title, body, file1, file2, file3, self.p_num, self.ResQ))
			p.start()
			if file1 or file2 or file3: 
				self.dProcess[self.p_num] = p

		else:
			wd.Destroy()


	def OnInitialize(self, e):
		try:
			self.WriteReg("kbuid", "")
			self.WriteReg("kbupw", "")
			self.WriteReg("downfolder", "c:\\")
			self.MsgBox(u"초기화 성공", u"초록멀티의 설정값을 초기화했습니다. 아이디와 비밀번호는 삭제되었고, 다운로드 폴더는 C:\\로 설정되었습니다.")
		except:
			pass

	def CheckLimit(self):
		try:
			if not self.dProcess or  len(self.dProcess) < self.limit: 
				return False
			else:
				return True
		except:
				return True

	def MemberJoin(self):
		self.Get("http://web.kbuwel.or.kr/menu/index.php?cmd=club_join&mo=green&club=green&bcode=green99")
		if self.html.find("history.go(-1)") >= 0:
			return self.MsgBox(u"결과", u"이미 초록등대에 가입되어 있거나 가입 신청되어 있습니다.")

		data = {}
		url = "http://web.kbuwel.or.kr/menu/index.php?mo=green&club=green&bcode=green99&cmd=club_join_insert"

		nickname = self.InputBox(u"별명 입력", u"동호회에서 사용할 별명이나 이름을 입력하세요.")
		if not nickname: return self.MsgBox(u"오류", u"별명은 필수입니다. 회원 가입을 다시 해 주세요.")
		data[u"닉네임".encode("euc-kr", "ignore")] = nickname.encode("euc-kr", "ignore")

		name = self.InputBox(u"실명과 성별 입력", u"실명과 성별을 입력하세요.")
		if not name: return self.MsgBox(u"오류", u"실명과 성별은 필수입니다. 회원 가입을 다시 해 주세요.")
		data[u"답변1".encode("euc-kr", "ignore")] = name.encode("euc-kr", "ignore")

		age = self.InputBox(u"나이와 지역 입력", u"나이와 지역을 입력하세요.")
		if not age: return self.MsgBox(u"오류", u"나이와 지역은 필수입니다. 회원 가입을 다시 해 주세요.")
		data[u"답변2".encode("euc-kr", "ignore")] = age.encode("euc-kr", "ignore")

		motive = self.InputBox(u"가입 동기 입력", u"동호회에 가입하게 된 동기를 입력하세요.")
		if not motive: return self.MsgBox(u"오류", u"가입 동기는 필수입니다. 회원 가입을 다시 해 주세요.")
		data[u"답변3".encode("euc-kr", "ignore")] = motive.encode("euc-kr", "ignore")

		if self.MsgBox(u"질문", u"2개월 이상 아무런 활동이 없다면 자동으로 회원 탈퇴됩니다. 동의합니까? 취소를 선택하면 회원 가입이 취소됩니다.", True) == False: return 
		data[u"답변4".encode("euc-kr", "ignore")] = u"예, 동의합니다.".encode("euc-kr", "ignore")

		if self.MsgBox(u"질문", u"동호회 자료는 반드시 동호회 내부에서만 공유되어야합니다. 외부로 유츌시 탈퇴처리됩니다. 동의합니까? 동의하지 않으면 가입이 취소됩니다.", True) == False: return 
		data[u"답변5".encode("euc-kr", "ignore")] = u"예, 동의합니다.".encode("euc-kr", "ignore")

		if self.MsgBox(u"가입 신청", u"정보 입력을 마쳤습니다. 초록등대에 가입 신청을 할까요?", True) == True:
			self.Post(url, data)

	def OnLibrary(self, e):
		lib = Library(self)
		lib.ShowModal()
		lib.Destroy()


if __name__ == "__main__":
	freeze_support()
	app = wx.App()
	f = GreenMulti(u"초록멀티 v1.6")
	app.MainLoop()
