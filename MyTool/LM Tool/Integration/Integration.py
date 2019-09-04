import os
import sys
import pandas as pd
from Corpus import CC, \
					MDCorpus
from PyQt5 import QtGui
from PyQt5 import uic
from PyQt5 import QtCore
from subprocess import call
from PyQt5.QtWidgets import QFileDialog, \
							QDialog, \
							QApplication, \
							QWidget, \
							QMessageBox, \
							QPushButton

from PyQt5.QtCore import pyqtSlot, \
						QThread, \
						pyqtSignal, \
						QMutex, \
						Qt


class Integration(QDialog):


	def __init__(self):
		QDialog.__init__(self)
		self.ui = uic.loadUi('platforms/tools.ui', self)
		self.ui.show()

	@pyqtSlot()
	def AWND(self):
		self.AWND = AWND()

	@pyqtSlot()
	def CCUI(self):
		self.CCUI = CCUI()


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
					tf.write("{datain}\n".format(datain=data.ix[i].Corpus))
					check = False
			else:
				if check:
					with open("SLM_{0}_{1}.txt".format(self.platform_real, temp_domain),\
						"a", encoding='utf-8') as af:
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


	def __init__(self, data, platform, sheet_name, lang):
		QThread.__init__(self)
		self.mutex = QMutex()
		self.excel = data
		self.platform = platform
		self.sheet_name = sheet_name
		self.lang = lang
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
				self.change_color.emit("color: rgb(255, 120, 228);")
				break
			self.mutex.unlock()

		if self.running:
			self.gen_init.start()
			self.temp = 100
			self.change_value.emit(self.temp)
			self.change_bool.emit(True)


	def checkStop(self):
		self.temp = 100

class AWND(QDialog):

	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		print("--------"*5+"진행 화면 입니다"+"--------"*5)
		self.ui = uic.loadUi('platforms\AWND.ui', self)
		self.ui.show()
		self.data = ""
		self.count = 0
		self.closeBtn = QPushButton("Close", self)
		self.closeBtn.clicked.connect(self.closeEvent)
		os.chdir('..')

	@pyqtSlot()
	def slot_button(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()"\
			, "","Excel Files (*.xlsx)", options=options)

		try:
			self.ui.lineEdit.setText(self.files[0])
		except:
			pass


	@pyqtSlot()
	def slot_data_gen(self):
		self.tempList = list()
		self.excel = pd.ExcelFile(self.files[0])
		self.df = self.excel.parse("ENU_SLM")
		self.ui.comboBox.clear()
		self.ui.comboBox2.clear()
		self.ui.comboBox.setEnabled(True)
		self.ui.comboBox2.setEnabled(True)
		for i in self.excel.sheet_names:
			self.ui.comboBox.addItem(i)
		for i in self.df.Platform:
			for j in i.replace(" ", "").split(","):
				if not j in self.tempList:
					self.tempList.append(j)
		for i in self.tempList:
			self.ui.comboBox2.addItem(i)
		self.ui.lineEdit_4.setText("데이터 생성 끝")
		self.ui.OK_button.setEnabled(True)

	@pyqtSlot()
	def slot_start(self):
		self.sheet_name = self.ui.comboBox.currentText()
		self.lang = self.ui.comboBox.currentText().split('_')[0]
		self.platform = self.ui.comboBox2.currentText()
		self.th = ThreadValue(self.excel, self.platform, self.sheet_name, self.lang)
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
			self.close()

	def closeEvent(self, event):
		os.chdir('.\Tools')
		os.system('cls')

class ThreadStart(QThread):


	change_bool = pyqtSignal(bool)


	def __init__(self, *arg):
		QThread.__init__(self)
		self.mutex = QMutex()
		self.check = True

		self.cc, self.start_check, self.is_fsr, self.is_param = arg

	def run(self):
		self.check = True
		self.check_two = True
		self.srilm = CC.Srilm(self.cc)
		self.change_bool.emit(False)

		if self.start_check: # True
			self.check_two = self.cc.generate(os.getcwd())
		else:
			self.check_two = self.cc.indeGenerate(os.getcwd())

		if self.check_two == True:
			self.checkFsrParam()
		else:
			self.change_bool.emit(True)
			self.exec()

		self.change_bool.emit(True)
		print("완료")


	def checkFsrParam(self):

			if self.is_fsr and self.is_param:
				self.srilm.makeDir()
				self.srilm.srilmBatch()
				self.srilm.slmcpl()
			elif self.is_param:
				self.srilm.makeDir()
				self.srilm.createFsr()
				self.srilm.srilmBatch()
				self.srilm.slmcpl()
			elif self.is_fsr:
				self.srilm.makeDir()
				self.srilm.createParam()
				self.srilm.srilmBatch()
				self.srilm.slmcpl()
			else:
				self.srilm.makeDir()
				self.srilm.createFsr()
				self.srilm.createParam()
				self.srilm.srilmBatch()
				self.srilm.slmcpl()

class CCUI(QDialog):


	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		print("--------"*5+"진행 화면 입니다"+"--------"*5)

		self.ui = uic.loadUi('platforms/CC.ui', self)
		self.all_start = True
		self.ui.show()
		self.slot_lineEdit()
		self.closeBtn = QPushButton("Close", self)
		self.closeBtn.clicked.connect(self.closeEvent)
		os.chdir("..\Corpus")


	####### - horizontalSlider Slot 및 connect
	def slot_lineEdit(self):
		self.sl = self.ui.horizontalSlider
		self.sl.valueChanged.connect(self.valuechange)
		self.ui.horizontalBar_line.textChanged.connect(self.setchange)

	def valuechange(self):
		size = self.sl.value()
		self.ui.horizontalBar_line.setText(str(size))

	def setchange(self):
		value = self.ui.horizontalBar_line.text()
		self.sl.setValue(int(value))
	####### - end
	def setBool(self, value):
		self.checker = value

	@pyqtSlot()
	def slot_all_start(self):
		self.currentInit()
		self.corpus = CC.CorpusCC(self.lang, self.platform, self.acmod, self.useclc,\
								self.weight, self.tool, self.clc, self.domain)
		if self.corpus.frontCheck(os.getcwd()) == False:
			del self.corpus
			QMessageBox.about(self, " Error ", "Init 파일이 존재하지 않아요")
			return None
		self.th = ThreadStart(self.corpus, self.all_start, \
					self.ui.fsrCheck.isChecked(), self.ui.paramCheck.isChecked())
		self.th.start()
		self.th.change_bool.connect(self.ui.setEnabled)


	@pyqtSlot()
	def slot_inde_start(self):
		self.currentInit()
		self.all_start = False
		self.corpus = CC.CorpusCC(self.lang, self.platform, self.acmod, self.useclc,\
								self.weight, self.tool, self.clc, self.domain)
		if self.corpus.frontCheck(os.getcwd()) == False:
			del self.corpus
			QMessageBox.about(self, " Error ", "Init 파일이 존재하지 않아요")
			return None
		self.th = ThreadStart(self.corpus, self.all_start, \
					self.ui.fsrCheck.isChecked(), self.ui.paramCheck.isChecked())
		self.th.start()
		self.th.change_bool.connect(self.ui.setEnabled)


	@pyqtSlot()
	def slot_open(self):

		path = QUrl.fromLocalFile("..\__Batch\out")
		url = QtGui.QDesktopServices.openUrl(path)

	def currentInit(self):
		self.domain = self.ui.domainBox.currentText()
		self.lang = self.ui.langBox.currentText()
		self.platform = self.ui.platformBox.currentText()
		self.useclc = self.useclcBox.currentText()
		self.acmod = self.ui.acmodText.text()
		self.clc = self.ui.clcText.text()
		self.weight = self.sl.value()
		self.tool = self.ui.toolBox.currentText()

	@pyqtSlot()
	def exec(self):
		os.chdir('..\Tools')
		os.system('cls')
		QApplication.exit()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()

	def closeEvent(self, event):
		os.chdir('..\Tools')
		os.system('cls')


if __name__=='__main__':

	app = QApplication(sys.argv)
	form = Integration()
	sys.exit(app.exec())
