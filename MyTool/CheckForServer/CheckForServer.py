# -*- coding: utf-8 -*-
import os
import sys
import JSONParser
from subprocess import call

class CheckFor:


	def __init__(self, LANG):
		# Language Init
		self.LANG = LANG

		# Input path
		self.input_result = ".\Input\{0}\{0}_Result_out.txt".format(self.LANG)
		self.input_correct = ".\Input\{0}\{0}_Correct.txt".format(self.LANG)

		# Output path
		self.output_result = ".\Output\{0}\{0}_Result.txt".format(self.LANG)

		# Dictionary init
		"""
		result_dict -> Result_out.txt 를 Load
		correct_dict -> Correct.txt 를 Load
		total_dict -> 비교후에 Result_out의 결과를 Save
		"""
		self.result_dict = {}
		self.correct_dict = {}
		self.total_dict = {}

		# Correct check Number
		"""
		totalTrue -> 모두 맞는 경우 'O'
		totalFalse -> Domain, Intetion이 다른 경우 'X'
		totalMid -> Domain, Intention은 같지만 Slot이 다른경우
		total -> True + False + Mid 총합
		"""
		self.totalTrue = 0
		self.totalFalse = 0
		self.totalMid = 0
		self.total = 0

	def compareTo(self):
		"""
		- Result_out 파일을 Load해서 Dictionary에 적재
		- count를 통해 100 단위로 Check, File Write
		- 모두 소문자로 치환
		"""
		with open(self.input_result, "r", encoding='utf-8-sig') as inputF:
			count = 0
			lines = inputF.readlines()
			for i in lines:
				if count < 100:
					i = i.lower().replace("\n", "").rstrip()
					i = i.split("\t")
					self.result_dict[i[0]] = i[1:]
				else:
					count = 0
					self.checkTo()
					self.writeTo()
				count += 1

	def loadCorrect(self):
		"""
		- Correct 파일을 Load해서 Dictionary에 적재
		- 모두 소문자로 치환
		"""
		with open(self.input_correct, "r", encoding='utf-8-sig') as inputF:
			lines = inputF.readlines()
			for i in lines:
				i = i.lower().replace("\n", "").rstrip()
				i = i.split("\t")
				self.correct_dict[i[0]] = i[1:]



	def checkTo(self):
		"""
		- all_check -> Domain, Intetion 체크 Boolean
		- mid_check -> Slot 체크 Boolean
		- non_slot -> Slot 존재 여부 체크 Boolean(Correct 파일 기준)
		- check_symbol -> 최종 결과 표시
		"""
		for i in self.result_dict:
			if i in self.correct_dict:
				all_check = False
				mid_check = False
				non_slot = False
				check_symbol = ""

				# Domain Check
				if self.result_dict[i][3] == self.correct_dict[i][1]:
					all_check = True
				else:
					all_check = False

				# Intention Check
				if (all_check==True) & (self.result_dict[i][5] == self.correct_dict[i][2]):
					all_check = True
				else:
					all_check = False

				# Slot check
				if all_check:

					try: # Slot이 Correct에 존재하는지 여부
						if self.correct_dict[i][3]:

							try: # Slot이 Result_out에 존재하는지 여부
								if self.result_dict[i][8]:

									# Result_out의 Slot이 Correct에 존재하는지 여부
									for j in self.result_dict[i][8:]:
										if j in self.correct_dict[i][3]:
											mid_check = True
											break
										else:
											mid_check = False
							except: # Slot이 Correct엔 존재하지만 Result_out에 없음
								non_slot = False

					# Slot이 Correct에 없는 경우(정답에 Slot이 없음)
					except IndexError:
						try: # Result_out에는 Slot이 존재
							if self.result_dict[i][8]:
								non_slot = False
						except:
							non_slot = True

				# SLOT이 없고 Domain과 Intetion이 일치하는 경우
				if (non_slot==True) & (all_check==True) & (mid_check==False):
					check_symbol = "O"
					self.totalTrue = self.totalTrue + 1

				# SLOT이 존재하고 Domain과 Intetion이 일치하지만 SLOT이 다른 경우
				elif (non_slot==False) & (all_check==True) & (mid_check==False):
					self.totalMid = self.totalMid + 1
					check_symbol = "#"


				# SLOT이 존재하고 Domain, Intetion, Slot이 모두 일치
				elif (non_slot==False) & (mid_check==True) & (all_check==True):
					check_symbol = "O"
					self.totalTrue = self.totalTrue + 1

				# Domain과 Intetion이 다른 경우
				else:
					check_symbol = "X"
					self.totalFalse = self.totalFalse + 1

				# check 결과와 Result_out 문장을 Dictionary에 적재
				self.total_dict[i] = [check_symbol, self.result_dict[i]]


	def writeTo(self):
		"""
		- Symbol, Correct-Domain, Result_out 문장 Txt에 write
		"""
		with open(self.output_result, "a", encoding='UTF-8') as wf:
			for i in self.total_dict:
				wf.write(self.total_dict[i][0]+"\t"+i+"\t"+self.correct_dict[i][1])
				wf.writelines("\t%s\t" % item for item in self.total_dict[i][1])
				wf.write("\n")


	def writeTotal(self):
		"""
		- Check 유형별 Total 및 총합 Txt에 write
		"""
		self.total = self.totalTrue + self.totalMid +self.totalFalse
		with open(self.output_result, "a") as wf:
			wf.write("===========================TOTAL==================================\n")
			wf.write("'O' Total : %d   %.2f%%\n" % (self.totalTrue, (self.totalTrue/self.total)*100))
			wf.write("'#' Total : %d   %.2f%%\n" % (self.totalMid, (self.totalMid/self.total)*100))
			wf.write("'X' Total : %d   %.2f%%\n" % (self.totalFalse, (self.totalFalse/self.total)*100))

	def makeTxt(self):
		"""
		- Write할 txt파일 생성
		"""
		with open(self.output_result, "w+") as makeF:
			pass

	def parsingTo(self):

		JSONParser.parsingToJson(self.LANG)
		JSONParser.jsonToText(self.LANG)

	def logWriteAndremove(self):

		with open("error_log.txt", "r") as ef:
			with open(self.output_result, "a") as lf:
				efLines = ef.readlines()
				lf.write("===========================ERROR==================================\n")
				for i in efLines:
					lf.write(i+"\n")

	def clearTxt(self):

		call(["del", "Test_{}.txt".format(self.LANG)], shell=True)
		call(["del", "error_log.txt"], shell=True)
		# call(["del", self.input_result], shell=True)

if __name__=="__main__":

	check = CheckFor(sys.argv[1])
	check.parsingTo()
	check.loadCorrect()
	check.makeTxt()
	check.compareTo()
	check.writeTotal()
	check.logWriteAndremove()
	check.clearTxt()
