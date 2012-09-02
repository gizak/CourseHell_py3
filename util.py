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
	__url_campus_gl='%e9%bc%93%e6%a5%bc%e6%a0%a1%e5%8c%ba'
	__url_campus_xl='%E4%BB%99%E6%9E%97%E6%A0%A1%E5%8C%BA' 
	__url_campus=None
	__url_catch='http://jwas3.nju.edu.cn:8080/jiaowu/student/elective/courseList.do?method=discussRenewCourseList&campus='
	__url_submit='http://jwas3.nju.edu.cn:8080/jiaowu/student/elective/courseList.do?method=submitDiscussRenew&campus='
	__store=[]
	__token_login={'userName':'091279049','password':'000000'} 
	__data_raw=None
	__data=''

	def __init__(self):
		self.token_assign()
		self.cookie_init()
		self.campus_assign()
		self.__get_raw()
		self.__fetch_array()		

	def token_assign(self):
		self.__token_login['userName']=input('User Name:')
		self.__token_login['password']=input('Password:')
		print('\n')

	def campus_assign(self):
		choose=int(input('choose campus: 0:GuLou, 1:XianLin  '))
		if choose == 0 :
			self.__url_campus=self.__url_campus_gl
		else:
			self.__url_campus=self.__url_campus_xl
		self.__url_catch+=self.__url_campus
		self.__url_submit+=self.__url_campus
		
	def cookie_init(self):
		opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor())
		urllib.request.install_opener(opener)
		login=urllib.request.urlopen(self.__url_login,urllib.parse.urlencode(self.__token_login).encode('utf-8'))
		is_valid=re.search(r'<div id="UserInfo">',login.read().decode())
		if not is_valid :
			print('login failed, retry:\n')
			self.token_assign()
			self.cookie_init()
		else:
			print('start:')
		    
	def __get_raw(self):
		self.__data_raw=urllib.request.urlopen(self.__url_catch).read()

	def __get_major(self):
		pass

	def __fetch_array(self):
		rs=re.findall(r'(?<=<tr class="TABLE_TR_0[12]">).*?(?=</tr>)',self.__data_raw.decode())
		for item in rs:
			self.__store.append(re.findall(r'(?<=<td valign="middle">)[^<]+(?=</td>)|(?<=<td align="center" valign="middle">)\w+|(?<=value=").*(?="></td>)',item))

	def get_store(self):
		return self.__store

	def submit(self,cid):
		self.__url_submit+= '&classId='+cid
		urllib.request.urlopen(self.__url_submit)

	def refresh(self):
		self.__get_raw()
		self.__fetch_array()

	def dump(self):
		for it in self.__store:
			print(it,'\n')

	def detect(self):
		rs_cid=[]
		rs_idx=[]
		idx_cnt=0
		flag_t=0 #is non-teacher ? assume have t
		for it in self.__store:
			if int(it[5]) != 0 : flag_t=-1 #no t
			if int(it[6+flag_t]) > int(it[7+flag_t]) :
				rs_cid.append(it[-1])
				rs_idx.append(idx_cnt)
			flag_t=0
			idx_cnt+=1
		return (rs_cid,rs_idx)


if __name__ == '__main__':
	ins=Capture()
	cnt=0
	info_detect=ins.detect()
	while len(info_detect[0])==0:
		time.sleep(1)
		ins.refresh()
		info_detect=ins.detect()
		print('Round[',cnt,'] None')
		cnt+=1
	class_id_set=info_detect[0]
	print('Detected leak !')
	print('classId=',class_id_set[0])
	#print('dump:',ins.get_store()[info_detect[1][0]])
	print('onSubmit...')
	ins.submit(class_id_set[0])
	print('submit complete!')
	#ins.dump()
