# -*- coding:utf-8 -*-

"""
Latest Date : 2018-04-27
Developer by Park June woo

Above the keyboard where the dust did not accumulate.
AKNA

"""
import os
import sys
from time import sleep
import pandas as pd
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from subprocess import call
from PyQt5.QtWidgets import QFileDialog, \
							QDialog, \
							QApplication, \
							QWidget, \
							QMessageBox

from PyQt5.QtCore import pyqtSlot, \
						QThread, \
						pyqtSignal, \
						QMutex, \
						Qt


class GenCorpus():

	def __init__(self, PLATFORM, lang):
		try:
			if PLATFORM.split('(')[1] != None:
				self.platform_real = PLATFORM
				self.platform = PLATFORM.split('(')[0]
				self.platform_my = PLATFORM
		except:
			self.platform = PLATFORM
			self.platform_real = PLATFORM

		self.lang = lang
		self.domain = ""
		self.gen_print = ""
		self.domain_list = list()
		call(["mkdir", ".\Corpus\corpus\INIT\{0}".format(self.lang)], shell=True)

	def generate_corpus(self, data, i):

		temp_domain = ""
		check = True
		platfom_check = True

		data_platform = data.ix[i].Platform.upper()
		try:
			if self.platform_my:
				if self.platform_my not in data_platform.replace(" ", "").split(','):
					platfom_check = False
					return
				try:
					if self.platform in data_platform.replace(" ", "")\
						.split(',') or\
						self.platform_my in data_platform.replace(" ", "")\
						.split(','):
						temp_domain = data.ix[i].Domain.split(',')[1]

				except:
					if self.platform in data_platform or\
						self.platform_my in data_platform:
						temp_domain = data.ix[i].Domain.split('.')[1]

		except:
			if self.platform:
				try:
					if self.platform in data_platform.replace(" ", "").split(','):
						temp_domain = data.ix[i].Domain.split('.')[1]
				except:
					if self.platform in data_platform:
						temp_domain = data.ix[i].Domain.split('.')[1]
			else:
				print("No match Platform name")


		finally:
			if platfom_check == False:
				return False

			if temp_domain =="":
				return

			if not temp_domain in self.domain_list:
				self.domain_list.append(temp_domain)

			if (self.gen_print != temp_domain)&(temp_domain != ""):
				self.gen_print = temp_domain
				print("SLM_{0}_{1} 생성중..".format(self.platform_real, temp_domain))

			try:
				with open("SLM_{0}_{1}.txt".format(self.platform_real, temp_domain),\
					"r", encoding='utf-8') as checkf:
					check = True
			except:
				with open("SLM_{0}_{1}.txt".format(self.platform_real, temp_domain),\
					"w+", encoding='utf-8') as tf:
					if "SLM" in data.ix[i].Type:
						tf.write("{datain}\n".format(datain=data.ix[i].Corpus))
						check = False
			else:
				if check:
					with open("SLM_{0}_{1}.txt".format(self.platform_real, temp_domain),\
						"a", encoding='utf-8') as af:
						if "SLM" in data.ix[i].Type:
							af.write("{datain}\n".format(datain=data.ix[i].Corpus))
				else:
					pass

	def merge_text(self):

		print("File Merge.....")
		try:
			with open("SLM_{0}_HELP_PHONE.txt".format(self.platform_real), "a",\
					encoding='utf-8') as HPf:
					with open("SLM_{0}_BT_FULL_FIRST.txt".format(self.platform_real), "r",\
						encoding='utf-8') as BTf:
						for line in BTf.readlines():
							HPf.write(line)
					with open("SLM_{0}_BT_REVERSE_LAST.txt".format(self.platform_real), "r",\
						encoding='utf-8') as BRf:
						for line in BRf.readlines():
							HPf.write(line)

		except:
			print("File open Error, no match File 'HELP_PHONE' ")

		try:
			with open("SLM_{0}_COMMON.txt".format(self.platform_real), "a",\
					encoding='utf-8') as HPf:
					with open("SLM_{0}_BT_FULL_FIRST.txt".format(self.platform_real), "r",\
						encoding='utf-8') as BTf:
						for line in BTf.readlines():
							HPf.write(line)
					with open("SLM_{0}_BT_REVERSE_LAST.txt".format(self.platform_real), "r",\
						encoding='utf-8') as BRf:
						for line in BRf.readlines():
							HPf.write(line)


		except:
			print("File open Error, no match File 'COMMON'")

	def delete_file(self):

		call(["del", "SLM_{0}_BT_FULL_FIRST.txt".format(self.platform_real)], shell=True)
		call(["del", "SLM_{0}_BT_REVERSE_LAST.txt".format(self.platform_real)], shell=True)
		self.domain_list.remove("BT_FULL_FIRST")
		self.domain_list.remove("BT_REVERSE_LAST")

	def move_file(self):

		for i in self.domain_list:
			call(["move", "/y", "./SLM_{0}_{1}.txt".format(self.platform_real, i),\
			 		"./Corpus/corpus/INIT/{0}".format(self.lang)], shell=True)

	def start(self):

		if self.lang not in("KOK"):
			self.merge_text()
			self.delete_file()
		self.move_file()

class ThreadValue(QThread):


	change_value = pyqtSignal(int)
	change_bool = pyqtSignal(bool)
	change_str = pyqtSignal(str)
	change_color = pyqtSignal(str)


	def __init__(self, data, platform, sheet_name, lang, domain):
		QThread.__init__(self)
		self.mutex = QMutex()
		self.excel = data
		self.platform = platform
		self.sheet_name = sheet_name
		self.lang = lang
		self.domain = domain
		self.running = False


	def __del__(self):
		self.wait()

	def run(self):
		self.data = pd.read_excel(self.excel, sheet_name=self.sheet_name, header=0)
		self.gen_init = GenCorpus(self.platform, self.lang)
		self.change_bool.emit(False)
		self.temp = 0
		self.running = True
		self.change_str.emit("Init 생성 중!")
		self.change_color.emit("color: rgb(0, 0, 0);")
		for i in self.data.index:

			self.mutex.lock()
			self.temp = (i/self.data.index.size)*100
			self.change_value.emit(self.temp)
			if self.gen_init.generate_corpus(self.data, i) == False:
				self.change_bool.emit(True)
				self.running = False
				self.change_str.emit("존재하지 않는 플랫폼!")
				self.change_color.emit("color: rgb(209, 0, 3);")
				break
			self.mutex.unlock()

		if self.running:
			self.gen_init.start()
			self.temp = 100
			self.change_value.emit(self.temp)
			self.change_bool.emit(True)


	def checkStop(self):
		self.temp = 100


class Form(QDialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		QDialog.setFixedSize(self, 450, 350)
		print("--------"*5+"진행 화면 입니다"+"--------"*5)
		self.ui = uic.loadUi('platforms\AWND.ui', self)
		self.ui.show()
		self.wide_check = False
		self.data = ""
		self.count = 0

	@pyqtSlot()
	def slot_button(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()"\
			, "","Excel Files (*.xlsx)", options=options)

		try:
			self.ui.lineEdit.setText(self.files[0])
			self.ui.Input_button_2.setEnabled(True)
		except:
			pass


	@pyqtSlot()
	def slot_data_gen(self):
		self.tempList = list()
		try:
			self.excel = pd.ExcelFile(self.files[0])
			self.ui.comboBox.clear()
			self.ui.comboBox.setEnabled(True)
			for i in self.excel.sheet_names:
				self.ui.comboBox.addItem(i)
			self.ui.lineEdit_4.setText("데이터 생성 끝 시트를 선택해주세요!")
			self.ui.Input_button_2.setEnabled(False)
			self.ui.sheetSelect.setEnabled(True)
			self.ui.arrowLabel.move(360, 170)
			self.ui.arrowLabel.setStyleSheet("color:rgb(0,0,0);")
			self.ui.Input_button.setEnabled(False)
			self.ui.Input_button_2.setEnabled(False)
			self.ui.lineEdit.setEnabled(False)
		except:
			QMessageBox.about(self, "Error", "올바른 Input File을 선택해주세요!")

	@pyqtSlot()
	def slot_sheet_select(self):
		self.df = self.excel.parse(sheet_name=self.ui.comboBox.currentText())
		self.ui.lineEdit_4.setText("플랫폼을 선택해주세요!")
		self.platform_parse()
		self.ui.arrowLabel.move(360,210)
		self.ui.comboBox.setEnabled(False)
		self.ui.sheetSelect.setEnabled(False)
		self.ui.platformSelect.setEnabled(True)

	def platform_parse(self):
		self.ui.comboBox2.clear()
		self.ui.comboBox2.setEnabled(True)
		for i in self.df.Platform:
			for j in i.replace(" ", "").split(","):
				if not j in self.tempList:
					if not j == "-":
						self.tempList.append(j)
		for i in self.tempList:
			self.ui.comboBox2.addItem(i)

	@pyqtSlot()
	def slot_platform_select(self):
		self.tempList2 = list()
		self.ui.absCheck.setEnabled(True)
		for i in self.df.Domain:
			if not i in self.tempList2 and i != '30.DelSpec':
				self.tempList2.append(i)
		for i in self.tempList2:
			self.ui.comboBox3.addItem(i)

	@pyqtSlot()
	def slot_reset(self):
		try:
			if self.files:
				self.files.clear()
		except:
			pass
		self.ui.comboBox.clear()
		self.ui.comboBox2.clear()
		self.ui.comboBox2.setEnabled(False)
		self.ui.absCheck.setEnabled(False)
		self.ui.absCheck.setChecked(False)
		self.ui.climateCheck.setChecked(False)
		self.ui.Input_button.setEnabled(True)
		self.ui.Input_button_2.setEnabled(True)
		self.ui.platformSelect.setEnabled(False)
		self.ui.lineEdit.setEnabled(True)
		self.ui.arrowLabel.setStyleSheet('color:rgb(255,255,255);')
		self.ui.lineEdit_4.setText("Input File 을 넣고 데이터 생성을 누르세요!")
		self.ui.lineEdit.clear()
		self.ui.comboBox3.clear()
		self.ui.comboBox3.setEnabled(False)



	@pyqtSlot()
	def slot_wide(self):
		if not self.wide_check:
			QDialog.setFixedSize(self, 590, 350)
			self.ui.wideButton.setText("<")
			self.wide_check = True
		else:
			QDialog.setFixedSize(self, 450, 350)
			self.ui.wideButton.setText(">")
			self.wide_check = False

	@pyqtSlot()
	def slot_abs_domain(self):
		if self.ui.absCheck.isChecked():
			self.ui.comboBox3.setEnabled(True)
		else:
			self.ui.comboBox3.setEnabled(False)


	@pyqtSlot()
	def slot_start(self):
		if self.ui.absCheck.isChecked():
			self.domain = self.ui.comboBox3.currentText()
		self.sheet_name = self.ui.comboBox.currentText()
		self.lang = self.ui.comboBox.currentText().split('_')[0]
		self.platform = self.ui.comboBox2.currentText()
		self.th = ThreadValue(self.excel, self.platform, self.sheet_name,\
		 						self.lang, self.domain)
		self.ui.OK_button.setEnabled(False)
		self.ui.Input_button_2.setEnabled(False)
		self.th.start()
		self.th.change_value.connect(self.ui.progressBar.setValue)
		self.th.change_bool.connect(self.ui.comboBox.setEnabled)
		self.th.change_bool.connect(self.ui.comboBox2.setEnabled)
		self.th.change_bool.connect(self.ui.OK_button.setEnabled)
		self.th.change_bool.connect(self.ui.Input_button_2.setEnabled)
		self.th.change_str.connect(self.ui.lineEdit_4.setText)
		self.th.change_color.connect(self.ui.lineEdit_4.setStyleSheet)


	@pyqtSlot()
	def exec_qt(self):
		QApplication.exit()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			os.system('cls')
			self.close()


if __name__=='__main__':

	app = QApplication(sys.argv)
	form = Form()
	sys.exit(app.exec())
