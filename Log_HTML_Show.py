#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from Plist_File_Analyse import getFile_is_plist
from pyh import *
from send_email import send_mail_to_test
from email.mime.text import MIMEText
reload(sys)
sys.setdefaultencoding('utf8')

def getData_from_plist():
	#获取plist文件 - 数据获取
	rootPath = "/Users/wangpingyang/Library/Developer/Xcode/DerivedData/" + sys.argv[1] + "/Logs/Test/"
	info_array = getFile_is_plist(rootPath)
	create_html_page(info_array)

def create_html_page(info_array):
	# tr - 行
	# td - 行内内容
	ncols = len(info_array)

	#创建表单
	page = PyH('My wonderful PyH page')
	mytab = page << table(border="1", bordercolor="black", cellspacing="1")

	rowsName = ["NO.","Title","Screen"]
	# n 行 ，遍历数组
	for i in xrange(1,ncols):
		#获取 信息 每一行信息
		dictionary = info_array[i]
		tempKey = dictionary.keys()
		title = tempKey[0]
		imageSource = dictionary[title]
		tempTrArray = [str(i),title,imageSource]
		#列
		mytr = mytab << tr()
		for j in xrange(1,4):
			if j == 3:
				mytr << td(img(src=tempTrArray[j-1],width="200",height="280",align="center"))
			else:
				mytr << td(tempTrArray[j-1] + '      ',style='color:#00AEAE;')
		
	page.printOut()
	#context = MIMEText(page,_subtype='html',_charset='utf-8')
	#send_mail_to_test(context)

if __name__ == "__main__":
	getData_from_plist()