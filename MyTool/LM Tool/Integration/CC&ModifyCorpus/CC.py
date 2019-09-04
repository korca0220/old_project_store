# -*- coding: utf-8 -*-
"""
Create Corpus Context
Latest Date : 2018-08-02
Version : V1.2
Develop by Park June Woo

V1.0
1) ModfiyCorpus를 수행하기 위해 파일을 배치시킨 후
2) Replace 파일을 통해 SLOT을 치환
3) fsr 파일과 param 파일 생성
4) SRILM 실행 후 결과 산출

V1.1
1) GUI 프로그램으로 통합 사용
  (현재 소스만 단독 사용 불가(MDCorpus path문제))
2) independent 메서드 추가(Domain 하나만 단독으로 실행할 경우)
3) fsr, param을 생성하지 않을 수 있도록 진행

V1.2
1) CCUI에 Import하여 사용
2) Init File 존재여부 체크하는 메서드 추가(inputCheck)
3) searchFile + inputCheck = frontCheck
"""
import sys
import os
from . import MDCorpus
from subprocess import call

class CorpusCC():

	# ModifyCorpus.exe를 실행하면 각각 저장 될 디렉토리 이름
	FILE_LIST = ["ORIGINAl", "REMOVE", "REPLACE", \
						"ORIGINAl_SLOT", "REMOVE_SLOT", "REPLACE_SLOT"]

	# FILE_LIST의 디렉토리에 저장된 파일들을 복사 할 디렉토리 이름
	RESULT_FILE_LIST = ["0_SLM_MULTI_ORIGIN", "0_SLM_MULTI_ORIGIN_DELETE_A_THE",\
					"0_SLM_MULTI_ORIGIN_REPLACE_THE_TO_A",\
					"1_SLM_MULTI_ORIGIN_CHANGE_SLOT_XYZ",\
					"1_SLM_MULTI_ORIGIN_DELETE_A_THE_CHANGE_SLOT_XYZ",\
					"1_SLM_MULTI_ORIGIN_REPLACE_THE_TO_A_CHANGE_SLOT_XYZ"]

	# 생성자
	def __init__(self, lang, PLATFORM, acmod, useclc, slot_weight, tool, clc, domain):

		self.save_list = list() # SLM_PLATFORM_DOMAIN --> EX)SLM_WIDE_COMMON
		self.domain_list = list() # DOMAIN --> EX)COMMON
		self.param_list = list() # PLATFORM_DOMAIN --> EX)WIDE_COMMON
		self.slot_list = list() # 모든 SLOT이 담기게 될 리스트

		self.LANG = lang # 사용 Language
		self.PLATFORM = PLATFORM # 사용 PLATFORM
		self.ACMOD = acmod # 사용 Acoustic Model
		self.USECLC = useclc # clc 사용 여부
		self.slot_weight = slot_weight
		self.none_weight = 1
		self.tool = tool
		self.clc = clc
		self.domain = domain

		if self.tool != "4.11":
			self.tools = "..\\tools_{}\\arpaslmcontextcpl.exe".format(self.tool)
			self.slotNames = "specialWordClasses"
			self.bufferFilepath = "--slmContextFilepath"
		else:
			self.tools = "..\\tools_{}\slmcpl.exe".format(self.tool)
			self.slotNames = "slotNames"
			self.bufferFilepath = "--contextBufferFilepath"


	# INIT 폴더 안에있는 domain 별 corpus file을 탐색하는 메소드
	def searchFile(self, dirname):

		filenames = os.listdir(dirname) # 처음 실행한 디렉토리를 전달 받음
		for i in filenames:
			self.full_name = os.path.join(dirname, i)
			if os.path.isdir(self.full_name):
				if os.path.split(self.full_name)[-1] == "INIT":
					self.full_name = os.path.join(self.full_name, self.LANG)
					try:
						for j in os.listdir(self.full_name):
							if j.split(".")[0].split("_")[1] == self.PLATFORM:

								# INIT 안에있는 파일들을 DOMAIN으로 나눠서 저장
								self.save_list.append(j.split(".")[0])
					except:
						return None

				else: # 디렉토리가 INIT 일 때까지 재귀
					self.searchFile(self.full_name)

	def inputCheck(self):
		if not self.save_list:
			return False

	def independent(self):

		del self.save_list
		self.save_list = list()
		self.save_list.append("SLM_{0}_{1}".format(self.PLATFORM, self.domain))

	# domain_list와 param_list에 값 할당
	def createList(self):

		for list in self.save_list:
			list = list.split("_")
			self.domain_list.append("_".join(list[2:]))
			self.param_list.append("_".join(list[1:]))

		with open("SLOT_FULL_LIST.txt", "r", encoding='utf-8') as sf:
			tline = sf.read().splitlines()
			for i in tline:
				self.slot_list.append(i.split("="))


	# 해당 경로에 디렉토리 생성 메소드
	def makeDir(self):

		for list in CorpusCC.RESULT_FILE_LIST:
			call(["mkdir", "..\SRILM\data\corpus\{0}\{1}\{2}"\
				.format(self.LANG, list, self.PLATFORM)], shell=True)

		for i in CorpusCC.FILE_LIST:
			call(["mkdir", ".\corpus\{0}\{1}".format(i, self.LANG)], shell=True)

	# ModifyCorpus.exe를 실행하기위해 CONFIG.txt를 수정하는 메소드
	def configCreate(self):

		with open("SLOT_FULL_LIST.txt", "w+") as clearf:
			clearf.write("")

		check = False
		for ref_file in self.save_list:
			ref_file = ref_file.split(".")[0]
			s_ref_file = ref_file.split("_")[1:]
			s_ref_file = "_".join(s_ref_file[:]) # EX) WIDE_COMMON

			with open("CONFIG.txt", "w") as cf:
				cf.write("LANG = {0}\n".format(self.LANG))
				cf.write("CORPUS_FILE = {0}.txt".format(ref_file))

			moc = MDCorpus.ModifyCorpus()
			moc.start()

			# 해당 PLATFORM의 모든 SLOTLIST를 담을 txt 작성
			with open("SLOTLIST.txt", "r") as slf:
				tline = slf.read().splitlines()
				tline_PLATFORM = ref_file.split("_")[1]

				try: # FULL_LIST.txt가 아무 내용도 없는지 Check
					with open("SLOT_FULL_LIST.txt", "r") as checkf:
						cline = checkf.read().splitlines()[0].split("=")[0].split("_")[0]
						if cline == tline_PLATFORM:
							check = True
						else:
							check = False

				except: # 아무 내용도 없으면
					with open("SLOT_FULL_LIST.txt", "w+") as sff:
						for i in tline:
							sff.write("{0}={1}\n".format(s_ref_file, i))

				else:	# 내용이 존재하면
					if check: # 기존의 PLATFORM과 새로 쓰여질 PLATFORM 비교
						with open("SLOT_FULL_LIST.txt", "a") as sff:
							for i in tline:
								sff.write("{0}={1}\n".format(s_ref_file, i))
					else:
						with open("SLOT_FULL_LIST.txt", "w") as sff:
							for i in tline:
								sff.write("{0}={1}\n".format(s_ref_file, i))

			print("{0} 생성".format(ref_file))

	# configCreate()의 결과물들을 다른 디렉토리로 복사하는 메소드
	def copy(self):

		for ref_file in self.save_list:
			ref_file = ref_file.split(".")[0]
			for i in range(6):
				call(["COPY", "corpus\{0}\{1}\{2}.txt".format(CorpusCC.FILE_LIST[i]\
					, self.LANG, ref_file), "..\\SRILM\\data\\corpus\\{0}\\{1}\\{2}\\{3}.txt"\
					.format(self.LANG, CorpusCC.RESULT_FILE_LIST[i], self.PLATFORM,\
					 ref_file)], shell=True)
			print("{0} 복사완료 \n".format(ref_file))

	# 메소드들을 순서대로 동작 하는 메소드
	def generate(self, current):

		self.searchFile(current)
		if self.inputCheck() == False:
			return False
		self.makeDir()
		self.configCreate()
		self.createList()
		print("-------------------생성 끝----------------------")
		self.copy()
		return True

	def indeGenerate(self, current):

		self.searchFile(current)
		if self.inputCheck() == False:
			return False
		self.makeDir()
		self.independent()
		self.configCreate()
		self.createList()
		print("-------------------생성 끝----------------------")
		self.copy()
		return True

	def frontCheck(self, current):
		self.searchFile(current)
		return self.inputCheck()

class Srilm():

	# 생성자
	def __init__(self, instance_file):

		# CorpusCC 클래스에서 생성된 멤버 변수들을 그대로 쓰기 위함
		self.init = instance_file # 객체를 받아 멤버변수 생성
		self.slot_weight = self.init.slot_weight
		self.none_weight = self.init.none_weight
		self.tool = self.init.tool
		self.slotNames = self.init.slotNames
		self.bufferFilepath = self.init.bufferFilepath
		self.tools = self.init.tools

	# Input 파일 존재 여부 체크


	# 결과 파일들을 저장할 디렉토리 생성 메서드
	def makeDir(self):

		call(["mkdir", "..\SRILM\data\{0}\{1}".format(self.init.PLATFORM, self.init.LANG)], shell=True)
		for i in self.init.param_list:
			call(["mkdir", "..\__Batch\out\{0}\{1}\{2}".format(self.init.PLATFORM,\
				self.init.LANG, i)], shell=True)

	# .fsr file 생성 메서드
	def createFsr(self):

		for i in self.init.domain_list:
			if i != "COMMON": # Domain Name이 "COMMON" 이 아니라면
				with open("..\SRILM\data\{0}\{1}\{0}_{2}.fsr"\
					.format(self.init.PLATFORM, self.init.LANG, i), "w+") as cf:
					self.none_weight = self.init.none_weight

					if self.init.LANG in ("ENU", "ENG"):
						for j in range(6):
							cf.write("..\SRILM\data\corpus\{0}\{1}\{2}\SLM_{2}_{3}.txt	{4}\n"\
								.format(self.init.LANG, self.init.RESULT_FILE_LIST[j],\
									self.init.PLATFORM, i, self.none_weight))
							if j == 2:
								cf.write("\n")
								self.none_weight = self.slot_weight
					else:
						cf.write("..\SRILM\data\corpus\{0}\{1}\{2}\SLM_{2}_{3}.txt	{4}\n"\
							.format(self.init.LANG, self.init.RESULT_FILE_LIST[0],\
								self.init.PLATFORM, i, self.init.none_weight))
						cf.write("\n")
						cf.write("..\SRILM\data\corpus\{0}\{1}\{2}\SLM_{2}_{3}.txt	{4}\n"\
							.format(self.init.LANG, self.init.RESULT_FILE_LIST[3],\
								self.init.PLATFORM, i, self.init.slot_weight))

			# Language가 "ENU", "ENG"이고 Domain Name이 "COMMON"인 경우
			# if self.init.LANG == "ENU" and i == "COMMON":
			elif i == "COMMON":
				with open("..\SRILM\data\{PLATFORM}\{lang}\{PLATFORM}_COMMON.fsr"\
					.format(PLATFORM=self.init.PLATFORM, lang=self.init.LANG), "w+") as cmf:
					if self.init.LANG in ("ENU", "ENG"):
						cmf.write("..\SRILM\data\corpus\{0}\SLM_BASE_ETRI_Tunning.txt	1\n"\
								.format(self.init.LANG))
						cmf.write("..\SRILM\data\corpus\{0}\SLM_BASE_DRAMA_Tunning.txt	1\n"\
								.format(self.init.LANG))
						cmf.write("\n")

						self.none_weight = self.init.none_weight
						for j in range(6):
							cmf.write("..\SRILM\data\corpus\{0}\{1}\{2}\SLM_{2}_{3}.txt	{4}\n"\
							.format(self.init.LANG, self.init.RESULT_FILE_LIST[j],\
								self.init.PLATFORM, "COMMON", self.none_weight))
							if j == 2:
								cmf.write("\n")
								self.none_weight = self.slot_weight
					else:
						cmf.write("..\SRILM\data\corpus\{0}\{1}\{2}\SLM_{2}_{3}.txt	{4}\n"\
							.format(self.init.LANG, self.init.RESULT_FILE_LIST[0],\
								self.init.PLATFORM, i, self.init.none_weight))
						cmf.write("\n")
						cmf.write("..\SRILM\data\corpus\{0}\{1}\{2}\SLM_{2}_{3}.txt	{4}\n"\
							.format(self.init.LANG, self.init.RESULT_FILE_LIST[3],\
								self.init.PLATFORM, i, self.init.slot_weight))


		# PLATFORM_MESSAGEBODY.fsr 은 따로 생성
		"""
		with open("..\SRILM\data\{0}\{1}\{0}_MESSAGEBODY.fsr"\
			.format(self.init.PLATFORM, self.init.LANG), "w+") as mf:
			mf.write("..\SRILM\data\corpus\{0}\SLM_BASE_ETRI_Tunning.txt	1\n"\
					.format(self.init.LANG))
			mf.write("..\SRILM\data\corpus\{0}\SLM_BASE_DRAMA_Tunning.txt	1\n"\
					.format(self.init.LANG))
		"""

	# .param file 생성 메서드
	def createParam(self):

		check = True
		temp = list()
		slot_string = ""
		for i in self.init.param_list:
			with open("..\SRILM\data\{0}\{1}\{2}.param"\
				.format(self.init.PLATFORM, self.init.LANG, i), "w+") as pf:
				pf.write("[ParameterSpecification Version=1.1 Encoding=ascii] \n")
				pf.write("modelSpec={0} \n".format(self.init.ACMOD))
				pf.write("clcSpec={0} \n".format(self.init.clc))
				pf.write("grammarName={0} \n".format("_".join(i.split("_")[1:])))
				pf.write("useclc={0} \n".format(self.init.USECLC))
				pf.write("startToken=<s> \n")
				pf.write("endToken=</s> \n")
				if "_".join(i.split("_")[1:]) != ("BT_FULL_FIRST" or "BT_REVERSE_LAST"):
					pf.write("dictionaryFilepaths=\"..\SRILM\data\{0}\{1}\{1}.dct\" \n"\
							.format(self.init.PLATFORM, self.init.LANG))
				for j in self.init.slot_list: # ['PLATFORM_DOMAIN','SLOT_NAME']
					if i == j[0]:
						temp.append(j[1])
						slot_string = ",".join(temp)
						check = True
					elif not temp:
						check = False
				if check:
					pf.write(self.slotNames+"={0}".format(slot_string))
				else:
					pf.write("#slotNames=")
				temp = []

		with open("..\SRILM\data\{0}\{1}\{0}_MESSAGEBODY.param"\
			.format(self.init.PLATFORM, self.init.LANG), "w+") as mf:
			mf.write("[ParameterSpecification Version=1.1 Encoding=ascii] \n")
			mf.write("modelSpec={0} \n".format(self.init.ACMOD))
			mf.write("grammarName=BASE \n")
			mf.write("useclc={0} \n".format(self.init.USECLC))
			mf.write("startToken=<s> \n")
			mf.write("endToken=</s> \n")

	# SRILM_Batch 실행 메서드
	def srilmBatch(self):

		# SRILM Batch 실행
		for i in self.init.param_list:
			call(["..\SRILM\SRILM_Batch.exe", "{res_file}".format(res_file=i),\
					"..\SRILM\data\{PLATFORM}\{lang}\{res_file}.fsr"\
					.format(PLATFORM=self.init.PLATFORM, lang=self.init.LANG, res_file=i),\
					"..\SRILM\\result", "..\SRILM"], shell=True)

			print(i)

		# 생성된 결과 파일 이동
			call(["MOVE", "..\SRILM\\result\{0}.arpa".format(i)\
				,"..\__Batch\out\{0}\{1}\{2}\{2}.arpa".format(self.init.PLATFORM,\
				 	self.init.LANG, i)], shell=True)

			call(["MOVE", "..\SRILM\\result\{0}.vocab".format(i)\
			 	,"..\__Batch\out\{0}\{1}\{2}\{2}.vocab".format(self.init.PLATFORM,\
				 	self.init.LANG, i)], shell=True)

			call(["MOVE", "..\SRILM\\result\{0}.count".format(i)\
			 	,"..\__Batch\out\{0}\{1}\{2}\{2}.count".format(self.init.PLATFORM,\
				 	self.init.LANG, i)], shell=True)

	# slmcpl.exe 실행 메서드
	def slmcpl(self):

		for i in self.init.param_list:
			call([self.tools, "-p", "..\SRILM\data\{0}\{1}\{2}.param"\
				.format(self.init.PLATFORM, self.init.LANG, i),\
					"--lmFilepath=..\__Batch\out\{0}\{1}\{2}\{2}.arpa"\
				.format(self.init.PLATFORM, self.init.LANG, i),\
					self.bufferFilepath+"=..\__Batch\out\{0}\{1}\{2}\{2}.LCF"\
				.format(self.init.PLATFORM, self.init.LANG, i)], shell=True)

	# 작동 메서드
	# def generate(self):
    #
	# 	self.makeDir()
	# 	self.createFsr()
	# 	self.createParam()
	# 	self.srilmBatch()
	# 	self.slmcpl()

"""
if __name__=='__main__':

	CURRENT = os.getcwd() # 현재 경로

	# 인스턴스 생성
	corcpus_cc = CorpusCC(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4], \
							sys.argv[5], sys.argv[6], sys.argv[7])
	srilm = Srilm(corcpus_cc)

	# 작동 메소드 실행
	corcpus_cc.generate(CURRENT)
	srilm.generate()
"""
