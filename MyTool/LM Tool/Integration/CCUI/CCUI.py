import os
import sys
from Corpus import CC
from PyQt5.QtWidgets import QFileDialog,\
 							QDialog,\
							QApplication,\
							QWidget,\
							QMessageBox
from PyQt5 import QtGui,\
                  QtCore,\
				  uic
from PyQt5.QtCore import pyqtSlot,\
                         Qt,\
						 QThread,\
						 pyqtSignal,\
						 QMutex,\
						 QUrl


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

class Form(QDialog):


	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		print("--------"*5+"진행 화면 입니다"+"--------"*5)

		self.ui = uic.loadUi('platforms/CC.ui', self)
		self.all_start = True
		self.ui.show()
		self.slot_lineEdit()
		os.chdir("Corpus")


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
		os.chdir(',,')
		os.system('cls')
		QApplication.exit()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			os.chdir('..')
			os.system('cls')
			self.close()

# if __name__=='__main__':
#
# 	app = QApplication(sys.argv)
# 	form = Form()
# 	sys.exit(app.exec())
