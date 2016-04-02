# coding: utf-8

from util import *
from multiprocessing import Process, Queue
import re
import sys
import os
import urllib2, cookielib
import time
import subprocess

class YoutubeDownloader(Process, Utility):
	def __init__(self, url, mode, p_num, q):
		Process.__init__(self)
		Utility.__init__(self)

		try:
			self.q = q
			self.mode = mode
			self.url = url
			self.down_url = ""
			self.title = ""

			self.downfolder = self.ReadReg("downfolder")
			self.p_num = p_num
			if not self.downfolder: self.downfolder = "c:\\"
			if type(self.downfolder) == unicode: self.downfolder = self.downfolder.encode("euc-kr", "ignore")
			cj = cookielib.CookieJar()
			self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
			urllib2.install_opener(self.opener)

			if self.prepare(): 			self.run()
		except:
			pass
		finally:
			self.Play("error.wav", async=False)
			self.q.put((100.0, u"다운로드 완료", "", 0, 0, self.p_num))
			while True:
				time.sleep(1)

	def prepare(self):
		host, params = self.ParamSplit(self.url)
		if "v" in params:
			url = host + "?v=" + params["v"]
		elif "V" in params:
			url = host + "?v=" + params["V"]
		else:
			url = self.url

		r = self.opener.open(url)
		html = r.read()
		m = re.search('(?ims)"url_encoded_fmt_stream_map"\s*:\s*"([^"]+)",', html)
		if m is None: return False
		maps = m.groups()[0]
		maps = maps.replace("\\u0026", "&")
		urls = re.findall(r'(?ims)url=([^&]+)&', maps)
		if not urls: return False
		self.down_url = urls[0]
		self.down_url = self.down_url.replace("%", r"\u00")
		self.down_url = self.down_url.decode("unicode-escape")

		m = re.search(r'(?i)name="title" content="([^"]+)"', html)
		if m is None: return False
		self.title = m.groups()[0]
		if type(self.title) == str: self.title = unicode(self.title, "utf-8")
		self.title = self.title.encode("euc-kr", "ignore")
		self.title = re.sub(r'[/\?%*:|"<>]', '', self.title)
		return True


	def run(self):
		res = self.opener.open(self.down_url)
		meta = res.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		down_size = 0
		block_size = 1024 * 1024
		start_time = time.time()
		filepath = os.path.join(self.downfolder, self.title + ".mp4")
		if type(filepath) == unicode: filepath = filepath.encode("euc-kr", "ignore")

		self.Play("down_start.wav")
# 로컬디스크에서 파일 크기를 보고 크기가 같으면 다운로드 종료
		if not os.path.exists(filepath) or os.path.getsize(filepath) != file_size:
			fp = open(filepath, "wb")
			file = self.title + ".mp4"
			self.q.put((0, u"다운로드 중", file, 0, 0, self.p_num)) 
			while True:
				buffer = res.read(block_size)
				if not buffer: break
				down_size += len(buffer)
				fp.write(buffer)
				per = down_size * 100.0 / file_size
				if per == 100: break
				t = time.time() - start_time
				if t <= 0: continue
				speed = down_size / t / 1024 / 1024
				remain = t * file_size / down_size
				self.q.put((per, u"다운로드 중", file, speed, remain, self.p_num))
# 다운완료라면
			fp.close()

			# mp3 변환 작업
		if self.mode:
			si = subprocess.STARTUPINFO()
			si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			cmd = '"' + os.path.join(os.path.dirname(sys.argv[0]), "ffmpeg.exe") + '" -y -i "' + filepath + '" -vn -ar 44100 -ac 2 -ab 192 -f mp3 "' + filepath[:-4] + '.mp3"'
			if type(cmd) == unicode: cmd = cmd.encode("euc-kr", "ignore")
			subp = subprocess.Popen(cmd, startupinfo=si)
			subp.wait()
			subp.terminate()
			os.remove(filepath)

		self.Play("down.wav", async=False)
		self.q.put((100.0, u"다운로드 완료", "", 0, 0, self.p_num))
		while True:
			time.sleep(1)
