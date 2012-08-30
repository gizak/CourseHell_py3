import urllib.request
import urllib.parse
import urllib.response
import re
import webbrowser
import time
import os

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
		conn=urllib.request.urlopen(self.__url_login,urllib.parse.urlencode(self.__token_login).encode('utf-8'))

	def __get_raw(self):
		self.__data_raw=urllib.request.urlopen(self.__url_catch).read()

	def __get_major(self):
		pass

	def __get_tr_batch(self):
		return re.findall(r'(?<=<tr class="TABLE_TR_0[12]">).*?(?=</tr>)',self.__data_raw)

	def __get_row(self,tr):
		return re.findall(r'(?<=<td valign="middle">)[^<]+(?=</td>)|(?<=<td align="center" valign="middle">)\w+|(?<=<td>).*?(?=</td></tr>)',tr)

	def __fetch_array(self):
		rs=self.__get_tr_batch()
		for item in rs:
			self.__store.append(self.__get_row(item))

	def get_store(self,):
		if not self.__store :
			self.get_raw()
			self.__fetch_array()
		return self.__store

	def refresh(self):
		pass

	def dump(self):
		self.__get_raw()
		print(self.__data_raw)


if __name__ == '__main__':
	#ins=Capture()
	#ins.dump()
	b=b'\r\n\r\n\r\n<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\r\n<html xmlns="http://www.w3.org/1999/xhtml">\r\n  <head>\r\n    <title>\xe5\x8d\x97\xe4\xba\xac\xe5\xa4\xa7\xe5\xad\xa6\xe6\x95\x99\xe5\x8a\xa1\xe7\xb3\xbb\xe7\xbb\x9f</title>'
	print(type(b.decode('utf-8')))
	os.system('pause')
	