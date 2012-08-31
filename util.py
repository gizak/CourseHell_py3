#!/usr/local/bin/python3
# _*_ coding: utf-8 _*_

import urllib.request
import urllib.parse
import urllib.response
import re
import webbrowser
import time
import sys

class Capture:
	__url_login='http://jwas3.nju.edu.cn:8080/jiaowu/login.do'
	__url_campus='%E4%BB%99%E6%9E%97%E6%A0%A1%E5%8C%BA'
	__url_catch='http://jwas3.nju.edu.cn:8080/jiaowu/student/elective/courseList.do?method=discussRenewCourseList&campus='
	__store=[]
	__token_login={'userName':'091270012','password':'090062'}
	__data_raw=None
	__data=''

	def __init__(self):
		self.__url_catch+=self.__url_campus
		self.token_assign()
		self.cookie_init()

	def token_assign(self):
		pass

	def cookie_init(self):
		opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
		urllib.request.install_opener(opener)
		urllib.request.urlopen(self.__url_login,urllib.parse.urlencode(self.__token_login).encode('utf-8'))
		self.__get_raw()
		self.__fetch_array()

	def __get_raw(self):
		self.__data_raw=urllib.request.urlopen(self.__url_catch).read()

	def __get_major(self):
		pass

	def __fetch_array(self):
		rs=re.findall(r'(?<=<tr class="TABLE_TR_0[12]">).*?(?=</tr>)',self.__data_raw.decode())
		for item in rs:
			self.__store.append(re.findall(r'(?<=<td valign="middle">)[^<]+(?=</td>)|(?<=<td align="center" valign="middle">)\w+|(?<=<td>).*?(?=</td></tr>)',item))

	def get_store(self,):
		return self.__store

	def refresh(self):
		self.__get_raw()
		self.__fetch_array()

	def dump(self):
		for it in self.__store:
			print(it,'\n')

	def detect(self):
		rs=[]
		flag_t=0
		for it in self.__store:
			if int(it[5]) != 0 : flag_t=-1
			if int(it[6+flag_t]) > int(it[7+flag_t]) :
				rs.append(int(it[0]))
			flag_t=0
		return rs


if __name__ == '__main__':
	ins=Capture()
	cnt=0
	while len(ins.detect())==0:
		time.sleep(1)
		ins.refresh()
		print('Round[',cnt,'] None')
		cnt+=1
	print('Detected leak ! ',ins.detect())
	#ins.dump()
