# -*- coding: utf-8 -*-
"""
ListCheckUp Tool
Latest Date : 2018-09-27
Version : v3.0
Develop by Park June Woo

- Platform, Language 별 Release 파일 존재 여부(Zero size 또한) 체크

"""
import os
import sys
import requests
import serverForm
from PyQt5.QtWidgets import QFileDialog, \
							QDialog, \
							QApplication, \
							QWidget, \
							QMessageBox,\
							QTableWidgetItem

from PyQt5 import QtGui, \
					uic
from PyQt5.QtCore import pyqtSlot, \
						QUrl, \
						Qt
from urllib import request
from subprocess import call
from collections import OrderedDict

class Form(QDialog):


	def __init__(self, parent=None):
		"""
		- Window Form Dialog 초기화
		"""
		QDialog.__init__(self, parent)
		QDialog.setFixedSize(self, 800, 870)
		self.ui = uic.loadUi('platforms\CheckList.ui', self)
		self.ui.show()
		self.list_status = ""
		self.table = self.ui.tableWidget
		self.table.setColumnWidth(0, 280)
		self.table.setColumnWidth(1, 120)
		self.table.setColumnWidth(2, 80)
		self.setButtonStatus(False)
		self.ret = False
		self.EUR = ['CZC','DAD','DUN','ENG','FRF','GED','ITI',\
						'NON','PLP','PTP','RUR','SPE','SWS','TRT',\
						'TTS_HUH', 'TTS_SKS', 'TTS_KOK']
		self.USA = ['ENU','FRC','SPM', 'TTS_KOK']
		self.KOK = ['KOK']
		self.VW_TTS = ["custom", "hyeryun", "dayoung"]
		self.Nuance_TTS = ["common", "languages"]
		self.server_data = ""
		self.current_path = os.getcwd()
		self.ui.pushButton.setStyleSheet("background : transparent;")

	@pyqtSlot(int, int)
	def double_click_slot(self, row, col):
		"""
		- Table 항목들을 더블 클릭했을 시 Signal
		- 항목이 들어있는(필요한) 경로를 Open
		"""
		url_path = self.files+self.valid_list[row]
		path = QUrl.fromLocalFile(url_path)
		url = QtGui.QDesktopServices.openUrl(path)

	@pyqtSlot()
	def checklist_load_slot(self):
		"""
		- 향지 선택 후 '설정' 버튼 Signal
		- 해당 향지의 CheckList.txt를 Load함
		"""
		self.lang = self.ui.comboBox.currentText()
		self.platform = self.ui.comboBox_2.currentText()
		if self.ui.on_button.isChecked():
			try:
				self.checkList = "checklist\\tempList.txt"
			except:
				QMessageBox.about(self, "ServerError", "checklist not downloaded")
				return None
		else:
			self.checkList = "checklist\CheckList_{0}_{1}.txt".\
				format(self.lang, self.platform)
		if os.path.isfile(self.checkList):
			self.setButtonStatus(True)
			self.ui.loadButton.setEnabled(False)
			self.ui.comboBox.setEnabled(False)
			self.ui.comboBox_2.setEnabled(False)
			self.ui.lineEdit.setText("체크를 진행하세요")
		else:
			# CheckList가 checklist 경로에 존재하지 앟는 경우
			QMessageBox.about(self, "Error",\
							"{0} File not Found".format(self.checkList))
			return
		if self.lang == "KOK":
			self.ui.checkBox_VW.setChecked(True)
		else:
			self.ui.checkBox_Nuance.setChecked(True)

	@pyqtSlot()
	def reset_slot(self):
		"""
		- 리셋 버튼 활성화시 버튼 Signal
		- 버튼 클릭시 CheckList 로드 Signal 빼고 전부 비활성화
		"""
		self.setButtonStatus(False) # 설정 후 SDCARD/Work 버튼 비/활성화 설정
		self.sdcardSetButtonStatus(False)
		self.workSetButtonStatusFixed(False)
		self.workSetButtonStatusDynamic(False)
		self.ui.loadButton.setEnabled(True)
		self.ui.comboBox.setEnabled(True)
		self.ui.comboBox_2.setEnabled(True)
		self.ui.make_checklist.setEnabled(False)
		self.ui.off_button.setChecked(True)
		self.ui.checkBox_Nuance.setChecked(False)
		self.ui.checkBox_VW.setChecked(False)
		self.server_check()
		self.table.clearContents()
		os.chdir(self.current_path)
		self.ui.lineEdit.setText("향지/플랫폼 설정을 하세요!")

	def setButtonStatus(self, load_status):
		"""
		- load_status 변수에 따라서 버튼 활성/비활성화 시키는 메서드
		"""
		self.ui.resetButton.setEnabled(load_status)
		self.ui.sdcard_set_button.setEnabled(load_status)
		self.ui.work_set_button_fixed.setEnabled(load_status)
		self.ui.work_set_button_dynamic.setEnabled(load_status)

	# SDCARD 디렉토리 설정 후 활성화 버튼
	def sdcardSetButtonStatus(self, load_status):
		self.ui.sdcardButton.setEnabled(load_status)
		self.ui.sdcardButton_2.setEnabled(load_status)

	# Work 디렉토리 설정 후 활성화 버튼 - 가변부
	def workSetButtonStatusDynamic(self, load_status):
		self.ui.nandButton.setEnabled(load_status)
		self.ui.nandButton_2.setEnabled(load_status)

	# Work 디렉토리 설정 후 활성화 버튼 - 고정부
	def workSetButtonStatusFixed(self, load_status):
		self.tts_check()
		self.ui.iniButton.setEnabled(load_status)
		self.ui.iniButton_2.setEnabled(load_status)
		self.ui.checkBox_VW.setEnabled(load_status)
		self.ui.checkBox_Nuance.setEnabled(load_status)

	@pyqtSlot()
	def sdcard_check(self):
		"""
		- SDCARD 목록 로드 이후 체크 버튼 Signal
		- 사이즈 체크 및 파일 존재 여부 체크
		"""
		tempList = list()
		tempList2 = list()
		if self.list_status != "sdcard":
			QMessageBox.about(self, "Error", "SD CARD목록을 LOAD 하세요")
			return

		try:
			for i in self.txt_list: # ChecList.txt에 있는 목록들이 존재하는 List
				if i in self.sdcard_list: # 사용자 경로에 있는 모든 파일 List
					tempList.append("OK")
				else:
					tempList.append("NOT Exist")

			for j, i in enumerate(self.full_path):
				if i.split("\\")[-1] in self.txt_list:
					size = round((os.stat(i).st_size))
					if size == 0: # File Size가 0인 경우
						tempList2.append("Zero Size")
					else:
						size = str(round(size/1024))
						if size == "0":
							size = str(round(os.stat(i).st_size))
							tempList2.append(size+ " Byte")
						else:
							tempList2.append(size+ " KB")

			for i, j in enumerate(tempList):
				if j == "NOT Exist" or j == "Zero Size":
					tempList2.insert(i, j)

			for i, j in enumerate(self.txt_list):
				self.table.setItem(i, 1, QTableWidgetItem(tempList2[i]))
				if tempList2[i] == "NOT Exist" or tempList2[i] == "Zero Size":
					self.table.item(i, 0).setBackground(QtGui.QColor(255, 120, 228))
					self.table.item(i, 1).setBackground(QtGui.QColor(255, 120, 228))
					self.table.item(i, 2).setBackground(QtGui.QColor(255, 120, 228))
		except:
			QMessageBox.about(self, "Error", "File Not Found")
			return


	@pyqtSlot()
	def sdcard_slot(self):
		"""
		- SDCARD 목록 로드 버튼 Signal
		- checkList.txt -> self.txt_list
		- self.list_status -> Load한 목록이 어떤 것인지 상태 저장
		"""
		self.txt_list = list()
		self.valid_list = list() # CheckList.txt에 있는 파일의 경로 List
		self.sdcard_path_list = list()
		self.list_status = "sdcard"

		with open(self.checkList, "r") as cf:
			lines = cf.readlines()
			for j, i in enumerate(lines):
				i = i.replace("\n", "")
				i = i.replace("[", "").replace("]", "")
				lang = i.split("\\")[-1].split("\t")[-1]
				i = i.split("\\")[-1].split("\t")[0]
				if i == "SDCARD":
					self.table.setRowCount(j)
					continue
				else:
					if i == "NAND": # [NAND] 가 나오기 전까지 Load
						break
					self.sdcard_path_list.append(os.path.split(lines[j])[0])
					self.valid_list.append(os.path.split(lines[j])[0])
					self.table.setRowCount(j)
					self.table.setItem(j-1, 0, QTableWidgetItem(i))
					self.table.setItem(j-1, 2, QTableWidgetItem(lang))
					self.txt_list.append(i)
		self.sdcard_path_list = list(OrderedDict.fromkeys(self.sdcard_path_list))
		self.sdcardLoadList()

	def sdcardLoadList(self):
		"""
		- SDCARD 체크가 필요한 경로에 있는 모든 파일 체크
		- 모든 파일들을 self.sdcard_list에 추가하여 추후 비교할 때 사용
		- self.full_path -> self.sdcard_list + 파일들의 전체 경로를 담고 있는 list
		"""
		self.sdcard_list = list()
		self.full_path = list()
		try:
			for i in self.sdcard_path_list:
				full_name = self.files+i
				filenames = os.listdir(full_name)
				for j in filenames:
					self.sdcard_list.append(j) # 순서가 없다.
					self.full_path.append(os.path.join(full_name, j))

		except:
			# sdcard_path의 경로가 존재하지 않는경우
			QMessageBox.about(self, "Error", "SDcard list path error")
			return


	"""
	이하 메서드들은 위의 sdcard 메서드들과 같은 형식으로 이루어져 있음
	( ChckList.txt를 어디까지 읽는지만 다르다)
	"""
	@pyqtSlot()
	def nand_check(self):
		tempList = list()
		tempList2 = list()
		if self.list_status != "nand":
			QMessageBox.about(self, "Error", "NAND/DB 목록을 LOAD 하세요")
			return

		try:
			for i in self.txt_list:
				if i in self.nand_list:
					tempList.append("OK")
				else:
					tempList.append("NOT Exist")

			for index, i in enumerate(self.full_path):
				if self.nand_list[index] in self.txt_list:
					size = round((os.stat(i).st_size))
					if size == 0:
						tempList2.append("Zero Size")
					else:
						size = str(round(size/1024))

						if size == "0":
							size = str(round(os.stat(i).st_size))
							tempList2.append(size+ " Byte")
						else:
							tempList2.append(size+ " KB")

			for i, j in enumerate(tempList):
				if j == "NOT Exist" or j == "Zero Size":
					tempList2.insert(i, j)

			for i, j in enumerate(self.txt_list):
				self.table.setItem(i, 1, QTableWidgetItem(tempList2[i]))
				if tempList2[i] == "NOT Exist" or tempList2[i] == "Zero Size":
					self.table.item(i, 0).setBackground(QtGui.QColor(255, 120, 228))
					self.table.item(i, 1).setBackground(QtGui.QColor(255, 120, 228))
					self.table.item(i, 2).setBackground(QtGui.QColor(255, 120, 228))

		except Exception:
			QMessageBox.about(self, "Error", "File Not Found")
			return

	@pyqtSlot()
	def nand_slot(self):
		self.txt_list = list()
		self.valid_list = list()
		self.nand_path_list = list()
		self.list_status = "nand"
		count = 0
		check = False
		with open(self.checkList, "r") as cf:
			lines = cf.readlines()
			for j, i in enumerate(lines):
				i = i.replace("\n", "")
				i = i.replace("[", "").replace("]", "")
				lang = i.split("\\")[-1].split("\t")[-1]
				i = i.split("\t")[0]
				if i == "NAND":
					check = True
					self.table.setRowCount(count)
					count = count + 1
					continue
				else:
					if check:
						if i == "INI":
							break
						else:
							self.nand_path_list.append(os.path.split(lines[j])[0])
							self.valid_list.append(os.path.split(lines[j])[0])
							self.table.setRowCount(count)
							self.table.setItem(count-1, 0, QTableWidgetItem(i.split("\\")[-1]))
							self.table.setItem(count-1, 2, QTableWidgetItem(lang))
							i = i.replace("\\", "/")
							self.txt_list.append(i)
							count = count + 1
					continue
		self.nand_path_list = OrderedDict.fromkeys(self.nand_path_list)
		self.nandLoadList()

	def nandLoadList(self):
		self.nand_list = list()
		self.full_path = list()
		try:
			for i in self.nand_path_list:
				full_name = (self.files+i).replace("\\", "/")
				try:
					filenames = os.listdir(full_name)
					print(filenames)
					for j in filenames:
						temp = "/".join(os.path.join(i, j).split("/")[:])
						self.nand_list.append(temp.replace("\\", "/"))
						self.full_path.append(os.path.join(full_name, j).replace("\\", "/"))
				except:
					pass
		except Exception:
			QMessageBox.about(self, "Error", "Nand list path error")
			return False


	@pyqtSlot()
	def ini_check(self):
		tempList = list()
		tempList2 = list()
		if self.list_status != "ini":
			QMessageBox.about(self, "Error", "INI 목록을 LOAD 하세요")
			return

		try:
			for i in self.txt_list:
				print(i)
				if i in self.ini_list:
					tempList.append("OK")
				else:
					tempList.append("NOT Exist")

			for index, i in enumerate(self.full_path):
				if self.ini_list[index] in self.txt_list:
					size = round((os.stat(i).st_size))
					if size == 0:
						tempList2.append("Zero Size")
					else:
						size = str(round(size/1024))
						if size == "0":
							size = str(round(os.stat(i).st_size))
							tempList2.append(size+ " Byte")
						else:
							tempList2.append(size+ " KB")

			for i, j in enumerate(tempList):
				if j == "NOT Exist" or j == "Zero Size":
					tempList2.insert(i, j)

			for i, j in enumerate(self.txt_list):
				self.table.setItem(i, 1, QTableWidgetItem(tempList2[i]))
				if tempList2[i] == "NOT Exist" or tempList2[i] == "Zero Size":
					self.table.item(i, 0).setBackground(QtGui.QColor(255, 120, 228))
					self.table.item(i, 1).setBackground(QtGui.QColor(255, 120, 228))
					self.table.item(i, 2).setBackground(QtGui.QColor(255, 120, 228))
		except Exception as e:
			QMessageBox.about(self, "Error", "File Not Found")
			return

	@pyqtSlot()
	def ini_slot(self):
		self.txt_list = list()
		self.valid_list = list()
		self.ini_path_list = list()
		self.list_status = "ini"
		count = 0
		check = False
		with open(self.checkList, "r") as cf:
			lines = cf.readlines()
			for j, i in enumerate(lines):
				i = i.replace("\n", "")
				i = i.replace("[", "").replace("]", "")
				lang = i.split("\\")[-1].split("\t")[-1]
				i = i.split("\t")[0]
				if i == "INI":
					check = True
					self.table.setRowCount(count)
					count = count + 1
					continue
				else:
					if check and i == "":
						break
					elif check and i != "":
						if self.ui.checkBox_VW.isChecked(): # VW TTS 인경우(내수)
							if not any(words in os.path.split(lines[j])[0]\
							 	for words in self.Nuance_TTS):
								self.tts_common(lines, j, i, lang, count)
								count = count + 1
						elif self.ui.checkBox_Nuance.isChecked(): # Nuance TTS(북미/유럽)
							if not any(words in os.path.split(lines[j])[0]\
							 	for words in self.VW_TTS):
								self.tts_common(lines, j, i, lang, count)
								count = count + 1
						else: # Nothing check
							self.tts_common(lines, j, i, lang, count)
							count = count + 1
					continue
		self.ini_path_list = OrderedDict.fromkeys(self.ini_path_list)
		self.iniLoadList()

	def iniLoadList(self):
		self.ini_list = list()
		self.full_path = list()
		count = 0
		try:
			for i in self.ini_path_list:
				full_name = (self.files+i).replace("\\", "/")
				try:
					filenames = os.listdir(full_name)
					count +=1
					for j in filenames:
						temp = os.path.join(i, j).replace("\\", "/")
						self.ini_list.append(temp.replace("\\", "/"))
						self.full_path.append(os.path.join(full_name, j))
				except Exception:
					pass
		except:
			QMessageBox.about(self, "Error", "Ini List path error")
			return False

	##### Create checklist
	@pyqtSlot()
	def checklist_directory_set(self):
		self.check_files = QFileDialog.getExistingDirectory(self,"QFileDialog.getOpenFileNames()")
		try:
			self.ui.make_checklist.setEnabled(True)
		except:
			pass


	@pyqtSlot()
	def slot_makech(self):
		"""
		- 향지 선택시 언어전체를 갖고오는 메서드
		  ex) USA -> [ENU, SPM, FRC]
		"""
		langs = ""
		platform = self.ui.comboBox_2.currentText()
		if self.ui.comboBox.currentText() == "KOK":
			langs = self.KOK[:]
		elif self.ui.comboBox.currentText() == "USA":
			langs = self.USA[:]
		else:
			langs = self.EUR[:]

		self.make_list_func(langs, platform)



	def make_list_func(self, langs, platform):
		"""
		- 향지/플랫폼 별 체크리스트 생성 메서드
		"""
		sd_card = ".\SD_CARD"
		work = ".\Work"
		if os.path.exists("checklist/CheckList_{0}_{1}.txt".\
			format(self.ui.comboBox.currentText(), platform)):
			self.ret = QMessageBox.question(self, 'Warning',\
			 	"checklist_{}파일이 존재합니다. 덮어 씌우겠습니까?".\
				format(self.ui.comboBox.currentText()), QMessageBox.Yes|QMessageBox.No)
		else:
			self.ret = True

		try:
			if self.ret==QMessageBox.Yes or self.ret==True:
				with open("checklist/CheckList_{0}_{1}.txt".\
					format(self.ui.comboBox.currentText(), platform),\
				 			"w+",encoding='utf-8') as ck:
					ck.write("[SDCARD]\n")
					os.chdir(self.check_files)
					for lang in langs:
						for x, y, z in os.walk(sd_card):
							if os.path.split(x)[-1] == lang:
								for i in os.listdir(os.path.abspath(x)):
									path = os.path.join(x, i)
									path = path.replace(sd_card, "")
									ck.write(path+"\t"+lang+"\n")

					ck.write("[NAND]\n")

					for x, y, z in os.walk(work):
						if os.path.split(x)[-1] == "BIN":
							for i in os.listdir(os.path.abspath(x)):
								path = os.path.join(x, i)
								path = path.replace(work, "")
								ck.write(path+"\tBIN"+"\n")
						for lang in langs:
							if os.path.split(x)[-1] == lang:
								if x.split("\\")[-2] == "DATA":
									for i in os.listdir(os.path.abspath(x)):
										if not os.path.isdir(os.path.join(x, i)):
											path = os.path.join(x, i)
											path = path.replace(work, "")
											temp = path.split("\\")
											temp[2] = path.split("\\")[2].replace("TTS_", "")
											temp = "\\".join(temp)
											path = temp
											ck.write(path+"\t"+lang+"\n")
								if x.split("\\")[-2] == "LEX":
									for i in os.listdir(os.path.abspath(x)):
										path = os.path.join(x, i)
										path = path.replace(work, "")
										ck.write(path+"\t"+lang+"\n")
					ck.write("[INI]\n")

					for x, y, z in os.walk(work):
						if os.path.split(x)[-1] == "BASE":
							for i in os.listdir(os.path.abspath(x)):
								if not os.path.isdir(os.path.join(os.path.abspath(x), i).replace("\\", "/")):
									path = os.path.join(x, i)
									path = path.replace(work, "")
									ck.write(path+"\tDAT"+"\n")
						for lang in langs:
							if os.path.split(x)[-1] == lang:
								if x.split("\\")[-2] == "ASR":
									for i in os.listdir(os.path.abspath(x)):
										path = os.path.join(x, i)
										path = path.replace(work, "")
										ck.write(path+"\t"+lang+"\n")
						if x.split("\\")[-2] =="TTS":
							for a,b,c in os.walk(x):
								if c and self.ui.comboBox.currentText() != "KOK":
									if "languages" in a:
										if any(words.lower() in "\\".join(a.split("\\")[:7]) for words in langs):
											[ck.write(sentence.replace(work, "")+"\tTTS"+"\n")\
												for sentence in [os.path.join(a, temp)\
												for temp in c]]
									else:
										if not any(word in a for word in self.VW_TTS):
											[ck.write(sentence.replace(work, "")+"\tTTS"+"\n")\
												for sentence in [os.path.join(a, temp)\
												for temp in c]]

								elif c and self.ui.comboBox.currentText() == "KOK":
									if not any(word in a for word in self.Nuance_TTS):
										[ck.write(sentence.replace(work, "")+"\tTTS"+"\n")\
											for sentence in [os.path.join(a, temp)\
											for temp in c]]

				if self.ret==QMessageBox.Yes or self.ret==True:
					QMessageBox.about(self, "Success", "체크리스트 만들어짐")

			os.chdir(self.current_path)
		except Exception as e:
			print(e)
			return
	#################

	### TTS Engine Check
	@pyqtSlot()
	def tts_check(self):
		"""
		- TTS 엔진 체크박스 비/활성화 메서드
		- 둘 중에 하나 or 선택 안하는 경우만 가능
		"""
		if self.ui.checkBox_VW.isChecked():
			self.ui.checkBox_Nuance.setEnabled(False)
			self.ui.checkBox_Nuance.setChecked(False)
		else:
			self.ui.checkBox_Nuance.setEnabled(True)

		if self.ui.checkBox_Nuance.isChecked():
			self.ui.checkBox_VW.setEnabled(False)
			self.ui.checkBox_VW.setChecked(False)
		else:
			self.ui.checkBox_VW.setEnabled(True)


	def tts_common(self, lines, j, i, lang, count):
		"""
		- TTS 엔진으로 분류하여 체크 진행시 중복되는 부분을 메서드화
		- 파일의 디렉토리 경로를 리스트에 append
		- 파일명을 테이블에 삽입
		"""
		self.ini_path_list.append(os.path.split(lines[j])[0])
		self.valid_list.append(os.path.split(lines[j])[0])
		self.table.setRowCount(count)
		self.table.setItem(count-1, 0, QTableWidgetItem(i.split("\\")[-1]))
		self.table.setItem(count-1, 2, QTableWidgetItem(lang))
		self.txt_list.append(i.replace("\\", "/"))

	################

	### Directory Setting
	@pyqtSlot()
	def sdcard_setup(self):
		self.files = QFileDialog.getExistingDirectory(self,"SD_Card 경로")
		if self.files:
			self.sdcardSetButtonStatus(True)
			self.workSetButtonStatusFixed(False)
			self.workSetButtonStatusDynamic(False)

	@pyqtSlot()
	def work_setup_fixed(self):
		self.files = QFileDialog.getExistingDirectory(self,"Work - 고정부 경로")
		if self.files:
			self.workSetButtonStatusFixed(True)
			self.sdcardSetButtonStatus(False)
			self.workSetButtonStatusDynamic(False)

	@pyqtSlot()
	def work_setup_dynamic(self):
		self.files = QFileDialog.getExistingDirectory(self, "Work - 가변부 경로")
		if self.files:
			self.workSetButtonStatusDynamic(True)
			self.sdcardSetButtonStatus(False)
			self.workSetButtonStatusFixed(False)

	##########

	##### Server
	@pyqtSlot()
	def server_check(self):
		if self.ui.on_button.isChecked():
			self.ui.server_upload_button.setEnabled(True)
			self.ui.server_download_button.setEnabled(True)
			self.ui.description_text.setEnabled(True)
			self.ui.upload_name.setEnabled(True)
			self.ui.loadButton.setEnabled(False)
			self.ui.serverloadButton.setEnabled(True)
			self.url_pass = 'https://script.google.com/macros/s/AKfycbza31Nunahnp2E7T1f0vVxRIoSH-bnhkLRWsEDjhavvwixP7m34/exec'
		if self.ui.off_button.isChecked():
			self.ui.description_text.setEnabled(False)
			self.ui.loadButton.setEnabled(True)
			self.ui.upload_name.setEnabled(False)
			self.ui.server_download_button.setEnabled(False)
			self.ui.server_upload_button.setEnabled(False)
			self.ui.serverloadButton.setEnabled(False)
			self.url_pass = ""

	@pyqtSlot()
	def checklist_download(self):
		platform = self.ui.comboBox_2.currentText()
		lang = self.ui.comboBox.currentText()
		self.server = serverForm.ServerForm(platform, lang)


	@pyqtSlot()
	def server_load(self):
		try:
			self.server_data = self.server.get_value()
			try:
				with open("checklist/tempList.txt", "w+", encoding='utf-8') as tempf:
					tempf.write(self.server_data)
				QMessageBox.about(self, 'Loaded', '서버 설정 적용완료!')
			except:
				QMessageBox.about(self, "File Error", "File create Error")
			self.checklist_load_slot()
		except:
			QMessageBox.about(self, "ServerError", "Checklist doesn't downloaded")

	@pyqtSlot()
	def checklist_upload(self):
		lang = self.ui.comboBox.currentText()
		platform = self.ui.comboBox_2.currentText()
		name = self.ui.upload_name.text()
		description = self.ui.description_text.text()
		if name == "":
			QMessageBox.about(self, "Error", "Name can't be null")
			return None

		try:
			checklist = "checklist/checkList_{0}_{1}.txt".format(lang, platform)
			with open(checklist, "r", encoding='utf-8-sig') as cf:
				all_line = cf.read()
				DATA = {
					'author' : name,
					'platform' : platform,
					'nation' : lang,
					'data' : all_line,
					'description' : description
				}
		except:
			QMessageBox.about(self, "Error", "CheckList_{0}_{1} is not exist".\
				format(lang, platform))
		try:
			response = requests.post(url=self.url_pass, data=DATA)
			if response.status_code == requests.codes.ok:
				QMessageBox.about(self, "Success", "  전송 성공  ")

		except requests.exceptions.RequestException as error:
			er = "Error code "+str(requests.status_codes.code)
			QMessageBox.about(self, "Error", er)

	############

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			try:
				if os.path.exists('checklist\\tempList.txt'):
					os.system("del /q checklist\\tempList.txt")
			except:
				pass
			self.close()

	@pyqtSlot()
	def final_exit(self):
		try:
			if os.path.exists('checklist\\tempList.txt'):
				os.system("del /q checklist\\tempList.txt")
		except:
			pass
		QApplication.exit()

	@pyqtSlot()
	def easter_egg(self):
		QMessageBox.about(self, "NLP Dev", "Develop by Park June Woo")

if __name__=='__main__':

	app = QApplication(sys.argv)
	form = Form()
	sys.exit(app.exec_())
