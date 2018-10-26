# -*- coding: utf-8 -*-
import csv
import unicodecsv as unicodecsv
from sets import Set

##########################################################################################
# dir
# .
# ./csv -> before parse
# ./parseCsv -> after parse
# 
# level mapping: 
# 无级别 : 0
# 小于副处 : 1
# 副处 : 2
# 正处 : 3
# 副厅 : 4
# 正厅 : 5
# 副部 : 6
# 正部 : 7
# 副国 : 8
# 正国 : 9
#
# gender mapping:
# 男 : 0
# 女 : 1
#
# ethnic:
# 其他族 : 0
# 汉族 : 1
#
# hometown province:
# 无 : -1
# 山东省 : 0
# 江苏省 : 1
# 山西省 : 2
# 云南省 : 3
# 西藏自治区 : 4
# 上海市 : 5
# 四川省 : 6
# 重庆市 : 7
# 安徽省 : 8
# 江西省 : 9
# 黑龙江省 : 10
# 浙江省 : 11
# 天津市 : 12
# 陕西省 : 13
# 宁夏回族自治区 : 14
# 湖北省 : 15
# 甘肃省 : 16
# 青海省 : 17
# 广西壮族自治区 : 18
# 辽宁省 : 19
# 台湾省 : 20
# 湖南省 : 21
# 吉林省 : 22
# 贵州省 : 23
# 广东省 : 24
# 新疆维吾尔自治区 : 25
# 福建省 : 26
# 河南省 : 27
# 海南省 : 28
# 河北省 : 29
# 北京市 : 30
# 内蒙古自治区 : 31
#
# hometown city
# under ./parseCsv dir
#
# Education Degree
# 无 : -1
# 不详 : 0
# 中专 : 1
# 初中 : 2
# 高中 : 3
# 专科 : 4
# 本科 : 5
# 硕士 : 6
# 博士 : 7
# 博士后 : 8
#
# Status
# 无 : -1
# 死亡 : 0
# 降/辞/撤职 : 1
# 立案查处 : 2
# 在职 : 3
# 退休 : 4
# 不详 : 5
##########################################################################################

# Global Variables
bio_col_name = ['id', 'gender', 'ethnic', 'dob', 'province_h', 'city_h', 'edu', 'curr_status']
work_col_name = ['id', 'start_t', 'end_t', 'country_wide_pos', 'ccp_pos', 'province_code', 'level']


def produce_id_name_mapping(fileIn="./csv/data_work.csv", fileOut="./parseCsv/id_name.csv"):

	# Variables
	id_name_map = {}
	col_name = ['id', 'name_chinese']

	# Main Function
	with open(fileIn, 'rU') as csvfile:
		reader = csv.reader(csvfile)
		header = True
		for row in reader:
			if header:
				header = False
				continue
			id_name_map[int(row[0])] = row[1]

	# Output
	rows2write = [col_name]
	for id in id_name_map.keys():
		rows2write.append([id, id_name_map[id]])
	outFile = open(fileOut, 'w')
	with outFile:
		writer = csv.writer(outFile, delimiter='\t')
		writer.writerows(rows2write)

	print "Finished Produce ID_NAME mapping, write into: " + fileOut
	return None
# produce_id_name_mapping()

def produce_id_work_mapping(fileIn="./csv/data_work.csv", fileOut="./parseCsv/id_work.csv"):

	# Variables
	id_work_mapping = {}
	work_orig_col_ind = [0, 3, 4, 5, 6, 7, 9, 21]

	with open(fileIn, 'rU') as csvfile:
		reader = csv.reader(csvfile)
		header = True
		rows2write=[work_col_name]
		for row in reader:
			if header:
				header = False
				continue
			# skip whole row if empty
			# TODO: might not need to skip
			if row[3] == '' or row[4] == '' :
				continue
			temp_row = []
			temp_row.append(int(row[0]))
			temp_row.append(row[3])
			temp_row.append(row[4])
			if row[5] == u'是'.encode('utf-8'):
				temp_row.append(True)
			elif row[5] == u'否'.encode('utf-8'):
				temp_row.append(False)
			if row[6] == u'是'.encode('utf-8'):
				temp_row.append(True)
			elif row[6] == u'否'.encode('utf-8'):
				temp_row.append(False)
			temp_row.append(row[7])
			if row[21] == u'无级别'.encode('utf-8'):
				temp_row.append(0)
			elif row[21] == u'小于副处'.encode('utf-8'):
				temp_row.append(1)
			elif row[21] == u'副处'.encode('utf-8'):
				temp_row.append(2)
			elif row[21] == u'正处'.encode('utf-8'):
				temp_row.append(3)
			elif row[21] == u'副厅'.encode('utf-8'):
				temp_row.append(4)
			elif row[21] == u'正厅'.encode('utf-8'):
				temp_row.append(5)
			elif row[21] == u'副部'.encode('utf-8'):
				temp_row.append(6)
			elif row[21] == u'正部'.encode('utf-8'):
				temp_row.append(7)
			elif row[21] == u'副国'.encode('utf-8'):
				temp_row.append(8)
			elif row[21] == u'正国'.encode('utf-8'):
				temp_row.append(9)
			else:
				print "Error in parsing!"
			# for ind in work_orig_col_ind:
			# 	print row[ind]
			rows2write.append(temp_row)

	# Output
	outFile = open(fileOut, 'w')
	with outFile:
		writer = csv.writer(outFile, delimiter='\t')
		writer.writerows(rows2write)

	print "Finished Produce ID_WORK mapping, write into: " + fileOut
	return None
# produce_id_work_mapping()


def produce_id_bio_mapping(fileIn="./csv/data_bio.csv", fileOut="./parseCsv/id_bio.csv"):
	id_bio_mapping = {}
	bio_orig_col_ind = [0, 2, 3, 4, 5, 6, 8, 10]
	memo = False

	# construct a map for province hometown
	province = Set([])
	id_province_map = {}
	ind = 0
	with open(fileIn, 'rU') as csvfile:
		reader = csv.reader(csvfile)
		header = True
		rows2write=[work_col_name]
		for row in reader:
			if header:
				header = False
				continue
			if row[5] == '':
				continue
			province.add(row[5])
	for p in province:
		id_province_map[ind] = p
		ind = ind + 1

	############################################################
	if memo:
		id_province_col = ['id', 'province']
		temp_row = [id_province_col]
		for k in id_province_map.keys():
			temp_row.append([k, id_province_map[k]])
		tempOutFile = open('./parseCsv/id_province_map.csv', 'w')
		with tempOutFile:
			writer = csv.writer(tempOutFile, delimiter='\t')
			writer.writerows(temp_row)
	############################################################

	# construct a map for city hometown
	city = Set([])
	id_city_map = {}
	ind = 0
	with open(fileIn, 'rU') as csvfile:
		reader = csv.reader(csvfile)
		header = True
		rows2write=[work_col_name]
		for row in reader:
			if header:
				header = False
				continue
			if row[6] == '':
				continue
			city.add(row[6])
	for c in city:
		id_city_map[ind] = c
		ind = ind + 1
	
	############################################################
	if memo:
		id_city_col = ['id', 'city']
		temp_row = [id_city_col]
		for k in id_city_map.keys():
			temp_row.append([k, id_city_map[k]])
		tempOutFile = open('./parseCsv/id_city_map.csv', 'w')
		with tempOutFile:
			writer = csv.writer(tempOutFile, delimiter='\t')
			writer.writerows(temp_row)
	############################################################
	rows2write=[bio_col_name]
	with open(fileIn, 'rU') as csvfile:
		reader = csv.reader(csvfile)
		header = True
		for row in reader:
			if header:
				header = False
				continue
			temp_row = []
			######
			temp_row.append(int(row[0]))
			######
			if row[2] == u'男'.encode('utf-8'):
				temp_row.append(0)
			elif row[2] == u'女'.encode('utf-8'):
				temp_row.append(1)
			else:
				print "Error in parsing!"
			######
			if row[3] == u'汉族'.encode('utf-8'):
				temp_row.append(1)
			else:
				temp_row.append(0)
			######
			temp_row.append(row[4])
			######
			if row[5] == '':
				temp_row.append(-1)
			else:
				for k in id_province_map.keys():
					if id_province_map[k] == row[5]:
						temp_row.append(k)
			######
			if row[6] == '':
				temp_row.append(-1)
			else:
				for k in id_city_map.keys():
					if id_city_map[k] == row[6]:
						temp_row.append(k)
			######
			if row[8] == '':
				temp_row.append(-1)
			elif row[8] == u'不详'.encode('utf-8'):
				temp_row.append(0)
			elif row[8] == u'中专'.encode('utf-8'):
				temp_row.append(1)
			elif row[8] == u'初中'.encode('utf-8'):
				temp_row.append(2)
			elif row[8] == u'高中'.encode('utf-8'):
				temp_row.append(3)
			elif row[8] == u'专科'.encode('utf-8'):
				temp_row.append(4)
			elif row[8] == u'本科'.encode('utf-8'):
				temp_row.append(5)
			elif row[8] == u'硕士'.encode('utf-8'):
				temp_row.append(6)
			elif row[8] == u'博士'.encode('utf-8'):
				temp_row.append(7)
			elif row[8] == u'博士后'.encode('utf-8'):
				temp_row.append(8)
			else:
				print "Error in parsing!"
			######
			if row[10] == '':
				temp_row.append(-1)
			elif row[10] == u'死亡'.encode('utf-8'):
				temp_row.append(0)
			elif row[10] == u'降/辞/撤职'.encode('utf-8'):
				temp_row.append(1)
			elif row[10] == u'立案查处'.encode('utf-8'):
				temp_row.append(2)
			elif row[10] == u'在职'.encode('utf-8'):
				temp_row.append(3)
			elif row[10] == u'退休'.encode('utf-8'):
				temp_row.append(4)
			elif row[10] == u'不详'.encode('utf-8'):
				temp_row.append(5)
			rows2write.append(temp_row)

		# Output
		outFile = open(fileOut, 'w')
		with outFile:
			writer = csv.writer(outFile, delimiter='\t')
			writer.writerows(rows2write)
	print "Finished Produce ID_BIO mapping, write into: " + fileOut
	return None
# produce_id_bio_mapping()