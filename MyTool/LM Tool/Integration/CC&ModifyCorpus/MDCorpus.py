# -*- coding: utf-8 -*-
"""
ModifyCorpus Tool
Latest Date : 2019-2-25
Version : V1.1
Developer by Park June woo

기존에 사용하던 ModifyCorpus.exe --> python ModifyCorpus.py 로 사용

기능 순서
1) Original init(txt)를 로드 -> SLOT의 "<, >" 제거
2) ENU의 경우 관사(the, a) 제거
3) ENU, ENG의 경우 the를 a로 치환
  * 나머지 언어는 1)의 결과와 같음

4) 1~3)의 과정을 걸처 만들어진 txt에 존재하는 SLOT들을 REPLACE에 존재하는
   형식으로 치환
   Ex) SLOT_CONTACTNAME => xxx
       SLOT_VAD_NUM_SLOT => xyx
"""
from subprocess import call
import sys
import re

class ModifyCorpus:

	def __init__(self):
		#File(or Directory) init
		self.config = ".\CONFIG.txt"
		self.slotlist = ".\SLOTLIST.txt"
		self.replace =".\corpus\\REPLACE.txt"
		self.init = ".\corpus\INIT\\"

		#ETC init
		self.replace_dict ={} # REPLACE 목록이 담기게 될 Dictionary
		self.original = ["ORIGINAl", "REMOVE", "REPLACE"]
		self.original_slot = ["ORIGINAl_SLOT", "REMOVE_SLOT", "REPLACE_SLOT"]

		self.result_original = ["0_SLM_MULTI_ORIGIN", "0_SLM_MULTI_ORIGIN_DELETE_A_THE",\
							"0_SLM_MULTI_ORIGIN_REPLACE_THE_TO_A"]
		self.result_original_slot = ["1_SLM_MULTI_ORIGIN_CHANGE_SLOT_XYZ",\
						"1_SLM_MULTI_ORIGIN_DELETE_A_THE_CHANGE_SLOT_XYZ",\
						"1_SLM_MULTI_ORIGIN_REPLACE_THE_TO_A_CHANGE_SLOT_XYZ"]


		self.slot_list = {} # SLOT목록이 담기게 될 DICT
		self.not_in_slot = {} # REPLACE에 없는 SLOT
		self.corpus_file = []

		#Regular Expression compile
		"""
		Ex 1) SLOT_NAME
		Ex 2) SLOT_NAME_NAME
		Ex 3) SLOT_NAME_NAME_NAME
		"""
		self.none_space_slot = re.compile("([a-zA-Z]+_[a-zA-Z]+_[a-zA-Z]+_[a-zA-Z]+|[a-zA-Z]+_[a-zA-Z]+_[a-zA-Z]+|[a-zA-Z]+_[a-zA-Z]+)")

	def deleteString(self, word):
		"""
		'a', 'the'를 제거해주는 메서드
		"""
		ls = word.split(' ')
		if 'a' in ls:
			while True:
				try:
					ls.remove('a')
				except:
					break
		if 'the' in ls:
			while True:
				try:
					ls.remove('the')
				except:
					break
		return ' '.join(ls)

	def replaceString(self, word):
		"""
		'the'를 'a'로 치환해주는 메서드
		"""
		ls = word.split(' ')
		tempList = list()
		for i in ls:
			if i == "the":
				i = "a"
			tempList.append(i)

		return ' '.join(tempList)

	def loadReplace(self):
		"""
		REPLACE.txt 로드 -> SLOT이 대체 될 문자가 들어 있는 텍스트
		"""
		with open(self.replace, "r") as lr:
			lines = lr.readlines()
			for i in lines:
				self.replace_dict[i.split('\t')[0]]=i.split('\t')[1].replace("\n", "")


	def loadConfig(self):
		"""
		CONFIG.txt 로드 -> Modify할 Domain Text와 LANG가 적재 되어 있음
		기존에 사용하던 방식과 비슷 방식으로 사용 할 수 있도록 구현
		"""
		check = False
		with open(self.config, "r") as lc:
			lines = lc.readlines()
			for i in lines:
				i = i.replace(" ", "")
				if i.split("=")[0] =="VOCON":
					self.vocon = i.replace("\n", "").split("=")[1]
				if i.split("=")[0] =="PLATFORM":
					self.platform = i.replace("\n", "").split("=")[1]
				if i.split("=")[0] =="LANG":
					self.lang = i.replace("\n", "").split("=")[1]
				if "CORPUS_FILE" in i:
					check=True
					continue
				if check:
					self.corpus_file.append(i.replace("\n", ""))
					print(self.corpus_file)

	# ORGINAL 파일 생성
	# "<", ">" 제거
	def originalGen(self, corpus_file): # original remove "<". ">"
		filename = self.init+self.lang+"\\"+corpus_file
		filename_full = ".\corpus\\"+self.original[0]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		result_full = "..\SRILM\\data\\corpus\\"+self.result_original[0]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		try:
			with open(filename, "r", encoding='utf-8') as sf:
				lines = sf.readlines()
			with open(filename_full, "w+", encoding='utf-8') as ff:
				for i in lines:
					i = i.replace("<", '')
					i = i.replace(">", '')
					i = i.lower()
					i = i.rstrip()
					tempList = self.none_space_slot.findall(i)
					for j in tempList:
						i = i.replace(j, j.upper())
					ff.write(i+"\n")
		except Exception as e:
			print("파일이 존재하지 않습니다.")
			return None

		call(["copy", filename_full, result_full], shell=True)

	# SLOT을 Replace에 존재하는 문자로 변경
	def originalGenSlot(self, corpus_file):
		self.slot_list[corpus_file] = []
		self.not_in_slot[corpus_file] = []
		check_space = False
		filename = ".\corpus\\"+self.original[0]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		filename_full = ".\corpus\\"+self.original_slot[0]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		result_full = "..\SRILM\\data\\corpus\\"+self.result_original_slot[0]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		try:
			with open(filename, "r", encoding='utf-8') as sf:
				lines = sf.readlines()
			with open(filename_full, "w+", encoding='utf-8') as ff:
				for i in lines:
					if self.none_space_slot.findall(i):
						tempList = self.none_space_slot.findall(i)
						for j in tempList:
							try:
								# 띄어쓰기가 안된 부분 처리
								# Ex) t'SLOT_NAME

								try:
									i = i.replace(j, " "+self.replace_dict[j])
								except:
									if not j in self.not_in_slot[corpus_file]:
										self.not_in_slot[corpus_file].append(j)
								i = i.replace("  ", " ").lstrip()
								if not j in self.slot_list[corpus_file]:
									self.slot_list[corpus_file].append(j)
							except:
								pass
					ff.write(i)
		except Exception as e:
			print("파일이 존재하지 않습니다.")
			print(e)
			return None

		call(["copy", filename_full, result_full], shell=True)

	# "a", "the"(관사) 제거
	# remove "a, the"
	def removeGen(self, corpus_file):
		filename = ".\corpus\\"+self.original[0]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		filename_full = ".\corpus\\"+self.original[1]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		result_full = "..\SRILM\\data\\corpus\\"+self.result_original[1]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		try:
			with open(filename, "r", encoding='utf-8') as sf:
				lines = sf.readlines()
			with open(filename_full, "w+", encoding='utf-8') as ff:
				for i in lines:
					if self.lang in("ENU", "ENG"): # 언어가 ENU, ENG일때만
						i = self.deleteString(i)
					ff.write(i)
		except Exception as e:
			print(e)
			print("파일이 존재하지 않습니다.")
			return None

		call(["copy", filename_full, result_full], shell=True)

	# 관사가 제거되고 SLOT이 대체되는 부분
	def removeGenSlot(self, corpus_file):
		check_space = False
		filename = ".\corpus\\"+self.original[1]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		filename_full = ".\corpus\\"+self.original_slot[1]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		result_full = "..\SRILM\\data\\corpus\\"+self.result_original_slot[1]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		try:
			with open(filename, "r", encoding='utf-8') as sf:
				lines = sf.readlines()
			with open(filename_full, "w+", encoding='utf-8') as ff:
				for i in lines:
					if self.none_space_slot.findall(i):
						tempList = self.none_space_slot.findall(i)
						for j in tempList:
							try:
								# 띄어쓰기가 안된 부분 처리
								# Ex) t'SLOT_NAME
								i = i.replace(j, " "+self.replace_dict[j])
								i = i.replace("  ", " ").lstrip()
							except:
								pass
					ff.write(i)
		except Exception as e:
			print(e)
			print("파일이 존재하지 않습니다")
			return None

		call(["copy", filename_full, result_full], shell=True)

	# "The"가 "A"로 대체되는 부분
	# replace "the to a"
	def replaceGen(self, corpus_file):
		filename = ".\corpus\\"+self.original[0]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		filename_full = ".\corpus\\"+self.original[2]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		result_full = "..\SRILM\\data\\corpus\\"+self.result_original[2]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		try:
			with open(filename, "r", encoding='utf-8') as sf:
				lines = sf.readlines()
			with open(filename_full, "w+", encoding='utf-8') as ff:
				for i in lines:
					if self.lang in ("ENU", "ENG"):# 언어가 ENU, ENG일때만
						i = self.replaceString(i)
					ff.write(i)
		except:
			print("파일이 존재하지 않습니다")
			return None

		call(["copy", filename_full, result_full], shell=True)

	# "The"가 "A"로 대체된 부분의 SLOT을 대체
	def replaceGenSlot(self, corpus_file):
		check_space = False
		filename = ".\corpus\\"+self.original[2]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		filename_full = ".\corpus\\"+self.original_slot[2]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		result_full = "..\SRILM\\data\\corpus\\"+self.result_original_slot[2]+"\\"+self.platform+"\\"+self.lang+"\\"+corpus_file
		try:
			with open(filename, "r", encoding='utf-8') as sf:
				lines = sf.readlines()
			with open(filename_full, "w+", encoding='utf-8') as ff:
				for i in lines:
					if self.none_space_slot.findall(i):
						tempList = self.none_space_slot.findall(i)
						for j in tempList:
							try:
								# 띄어쓰기가 안된 부분 처리
								# Ex) t'SLOT_NAME
								i = i.replace(j, " "+self.replace_dict[j])
								i = i.replace("  ", " ").lstrip()
							except:
								pass
					ff.write(i)
		except:
			print("파일이 존재하지 않습니다")
			return None

		call(["copy", filename_full, result_full], shell=True)

	# SLOTLIST.txt에 SLOT목록 기입
	def assignSlot(self):
		with open(self.slotlist, "w") as sf:
			for i in self.slot_list:
				sf.write("------"+i+"------\n")
				for j in self.slot_list[i]:
					sf.write(j+"\n")
				sf.write("*****NOT IN*****\n")
				for j in self.not_in_slot[i]:
					sf.write(j+"\n")
				sf.write("****************\n")


	def mkdir(self):
		from subprocess import call
		for i in self.original:
			call(['md', '.\\corpus\\{i}\\{platform}\\{lang}'.format(i=i.replace(".txt", ""), platform=self.platform, lang=self.lang)],\
				shell=True)
		for i in self.original_slot:
			call(['md', '.\\corpus\\{i}\\{platform}\\{lang}'.format(i=i.replace(".txt", ""), platform=self.platform, lang=self.lang)],\
				shell=True)
		for i in self.result_original:
			call(['md', '..\\SRILM\\data\\corpus\\{i}\\{platform}\\{lang}'.format(i=i.replace(".txt", ""), platform=self.platform, lang=self.lang)],\
				shell=True)
		for i in self.result_original_slot:
			call(['md', '..\\SRILM\\data\\corpus\\{i}\\{platform}\\{lang}'.format(i=i.replace(".txt", ""), platform=self.platform, lang=self.lang)],\
				shell=True)

		# output make dir
		for i in self.corpus_file:
			call(['md', '..\\__Batch\\out\\{platform}\\{lang}\\{res}'.format(platform=self.platform, lang=self.lang, res=i.replace(".txt", ""))],\
				shell=True)

	def compileTo(self):
		from subprocess import call

		#SRILM_Batch
		for i in self.corpus_file:
			call(['..\\SRILM\\SRILM_Batch.exe', '{res}'.format(res=i.replace(".txt", "")),\
			 		'..\\SRILM\\data\\{platform}\\{lang}\\{res}.fsr'.format(platform=self.platform, lang=self.lang, res=i.replace(".txt", "")),\
					'..\\SRILM\\result', '..\\SRILM'], shell=True)

		#Move to .arpa, .vocab, .count
		for i in self.corpus_file:
			call(['MOVE', '..\\SRILM\\result\\{res}.arpa'.format(res=i.replace(".txt", "")),\
			 		'..\\__Batch\\out\\{platform}\\{lang}\\{res}\\{res}.arpa'.format(platform=self.platform, lang=self.lang, res=i.replace(".txt", ""))],\
					shell=True)
			call(['MOVE', '..\\SRILM\\result\\{res}.vocab'.format(res=i.replace(".txt", "")),\
			 		'..\\__Batch\\out\\{platform}\\{lang}\\{res}\\{res}.vocab'.format(platform=self.platform, lang=self.lang, res=i.replace(".txt", ""))],\
					shell=True)
			call(['MOVE', '..\\SRILM\\result\\{res}.count'.format(res=i.replace(".txt", "")),\
			 		'..\\__Batch\\out\\{platform}\\{lang}\\{res}\\{res}.count'.format(platform=self.platform, lang=self.lang, res=i.replace(".txt", ""))],\
					shell=True)

		#Nuance
		if self.vocon in ["4.11", "4.12"]:
			for i in self.corpus_file:
				call(['..\\tools_{version}\\slmcpl.exe'.format(version=self.version), '-p',\
				 	'..\\SRILM\\data\\{platform}\\{lang}\\{res}.param'.format(platform=self.platform, lang=self.lang, res=i.replace(".txt.", "")),\
					'--lmFilepath=..\\__Batch\\out\\{platform}\\{lang}\\{res}\\{res}.arpa'.format(platform=self.platform, lang=self.lang, res=i.replace(".txt", "")),\
					'--contextBufferFilepath=..\\__Batch\\out\\{platform}\\{lang}\\{res}\\{res}.LCF'.format(platform=self.platform, lang=self.lang, res=i.replace(".txt", ""))],\
					shell=True)
		elif self.vocon in ["4.7", "4.8"]:
			for i in self.corpus_file:
				call(['..\\tools_{version}\\arpaslmcontextcpl.exe'.format(version=self.version), '-p',\
					'..\\SRILM\\data\\{platform}\\{lang}\\{res}.param'.format(platform=self.platform, lang=self.lang, res=i.replace(".txt.", "")),\
					'--lmFilepath=..\\__Batch\\out\\{platform}\\{lang}\\{res}\\{res}.arpa'.format(platform=self.platform, lang=self.lang, res=i.replace(".txt", "")),\
					'--contextBufferFilepath=..\\__Batch\\out\\{platform}\\{lang}\\{res}\\{res}.LCF'.format(platform=self.platform, lang=self.lang, res=i.replace(".txt", ""))],\
					shell=True)

		else:
			print("bad vocon version")

	def generate(self):
		"""
		1) config file Load 후 Slot의 "<, >"제거 명령어 실행
		2) ENU의 경우 관사 제거 및 관사 대체 실행
		3) 다른 언어의 경우는 originalGen의 결과와 같음
		"""
		self.loadConfig()
		self.mkdir()


	# 각종 slot_replace 함수 실행
	def slotGenerate(self):
		"""
		ENU외의 다른 언어는 모든 결과 값이 original과 동일
		"""
		for i in self.corpus_file:
			self.originalGen(i)
			self.removeGen(i)
			self.replaceGen(i)
			self.originalGenSlot(i)
			self.removeGenSlot(i)
			self.replaceGenSlot(i)

	def start(self):
		self.loadReplace()
		self.generate()
		self.slotGenerate()
		self.assignSlot()
		self.compileTo()

if __name__=='__main__':

	md = ModifyCorpus()
	md.start()
