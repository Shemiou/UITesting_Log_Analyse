#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from biplist import *


#/Users/wangpingyang/Library/Developer/Xcode/DerivedData/inke-fazrydnyhteyabchpbqfqcblmmxu/Logs/Test

#遍历工程文件所在文件夹 - 获取UI Testing结果
def getFile_is_plist(rootPath):
	#判断path是否为路径
	if not os.path.isdir(rootPath):
		return

	#遍历
	for root,dirs,files in os.walk(rootPath):
		for filename in files:
			if ".plist" in filename:
				#plist文件
				plistPath = rootPath + filename
				return(openFile_is_plist(rootPath,plistPath))

#解析 plist 文件，获取所有截图名称
def openFile_is_plist(rootPath,plistPath):
	title_array = []
	# n 层解析，得到 array 数据
	plist = readPlist(plistPath)
	# TestableSummaries(数组) -> Item0(字典) -> Tests(数组) -> Item0(字典)
	#最外层 Array 第一层
	TestableSummaries = plist['TestableSummaries']
	#第一层 dictionary
	Item0_0 = TestableSummaries[0]
	#第二层 Array
	Tests = Item0_0['Tests']
	#第二层 dictionary
	Item0_1 = Tests[0]
	Subtests_0 = Item0_1['Subtests']
	Item0_2 = Subtests_0[0]
	Subtests_1 = Item0_2['Subtests']
	Item0_3 = Subtests_1[0]
	Subtests_2 = Item0_3['Subtests']
	Item0_4 = Subtests_2[0]
	ActivitySummaries = Item0_4['ActivitySummaries']
	# dictionary - 点击事件描述 + 截图保存
	for dictionary in ActivitySummaries:
		# 第一层
		title_array = function_dictionary(rootPath,dictionary,title_array)

		if "SubActivities" in dictionary:
			# 子数组
			SubActivities = dictionary['SubActivities']
			for tempDict in SubActivities:
				# 第二层 
				title_array = function_dictionary(rootPath,tempDict,title_array)
				if "SubActivities" in tempDict:
					#又一层数组
					sub_0 = tempDict['SubActivities']
					for lastDict in sub_0:
						title_array = function_dictionary(rootPath,lastDict,title_array)
	
	return title_array_pack(title_array)

def function_dictionary(rootPath,dictionary,title_array):
	title = str(dictionary['Title'])
	imagePath = append_image_path(rootPath,dictionary['UUID'])
	global isWait
	if "Synthesize event" in title:
		return title_array
	elif "Snapshot accessibility hierarchy for com.meelive.ingkee" in title:
		return title_array
	elif "Use cached accessibility hierarchy for com.meelive.ingkee" in title:
		return title_array
	elif "Unable to" in title:
		return title_array
	elif "Set Up" in title:
		return title_array
	elif "Terminate" in title:
		return title_array
	elif "Get" in title:
		return title_array
	elif "Find" in title:
		return title_array
	elif "Launch com.meelive.ingkee" in title:
		return title_array
	elif "Start Test" in title:
		return title_array
	else:
		title_array.append({title:imagePath})
		return title_array

#这里又很多冗余的信息，需要处理
def title_array_pack(title_array):
	isWait = False
	temp_title_array = []

	for x in xrange(0,len(title_array) - 1):
		dictionary = title_array[x]
		title = dictionary.keys()
		if "Wait for app to idle" in title[0]:
			#在这里 处理 所有 多余的 "Wait for app to idle"
			if isWait == False:
				temp_title_array.append(title_array[x])
				isWait = True
		else:
			temp_title_array.append(title_array[x])
			isWait = False

	return create_new_title_array(temp_title_array)

def create_new_title_array(title_array):
	#奇数组
	title_array_odd = []

	#偶数组
	title_array_even = []

	#新建数组
	title_array_new = []

	#根据 整除奇数、偶数 将两个数组融合 - 去掉 ”Wait for app to idle“
	#这里有个前提：总数为偶数 - 目前为止，总是满足这个条件
	for x in xrange(0,len(title_array) - 1):
		if x % 2 == 0:
			title_array_even.append(title_array[x])
		else:
			title_array_odd.append(title_array[x])

	#开始讲两个数组 合并 成一个新的数组
	for x in xrange(0,len(title_array_even) - 1):
		#获取 奇数的 title
		dictionary_odd = title_array_odd[x]
		title_odd = dictionary_odd.keys()

		#获取偶数的 imageSource
		dictionary_even = title_array_even[x]
		title_even = dictionary_even.keys()
		
		#print(title_odd[0])
		title_array_new.append({title_odd[0]:dictionary_even[title_even[0]]})

	return title_array_new

#打开截图所在的文件夹，获取截图名称
def append_image_path(filename,imageName):
	front = 'Attachments/Screenshot_'
	imagePath = filename + front + imageName + '.png'
	return imagePath