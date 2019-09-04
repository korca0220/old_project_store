import time
import sys
import configparser
from BatchCreate import BatchBatch
from BatchGenerate import BatchGenerate
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QDialog,\
 							QApplication, \
							QMessageBox, \
							QFileDialog
from PyQt5.QtCore import pyqtSlot, \
						Qt, \
						QThread, \
						pyqtSignal, \
						QMutex


class BatchMan(QDialog):


	def __init__(self, parent=None):

		QDialog.__init__(self, parent)
		QDialog.setFixedSize(self, 400, 450)
		self.ui = uic.loadUi('Batch.ui', self)
		self.ui.show()

		self.ui.fileText.setReadOnly(True)
		self.ui.fileText_2.setReadOnly(True)
		self.ui.loadCheck.stateChanged.connect(self.loadChangedCreate)
		self.ui.loadCheck_2.stateChanged.connect(self.loadChangedGenerate)

		self.setInitBox()

	def loadChangedCreate(self):
		"""
		change state(True/False) 'load ini' button
		"""
		# Create Tab - Checked
		if self.ui.loadCheck.isChecked():
			self.ui.loadButton.setEnabled(True)
			self.ui.fileText.setEnabled(True)
			self.ui.fileText.setStyleSheet("color:rgb(255, 255, 255); background:rgb(91, 91, 91)")
			self.ui.loadButton.setStyleSheet("background:rgb(100, 100, 100); color:rgb(255, 255, 255)")

		# Create Tab - unchecked
		else:
			self.ui.loadButton.setEnabled(False)
			self.ui.fileText.setEnabled(False)
			self.ui.fileText.setStyleSheet("background:rgb(139, 139, 139);color:rgb(109, 109, 109)")
			self.ui.loadButton.setStyleSheet("background:rgb(139, 139, 139);color:rgb(109, 109, 109)")

	def loadChangedGenerate(self):
		"""
		change state(True/False) 'load ini' button
		"""
		# Generate Tab - Checked
		if self.ui.loadCheck_2.isChecked():
			self.ui.loadButton_2.setEnabled(True)
			self.ui.fileText_2.setEnabled(True)
			self.ui.fileText_2.setStyleSheet("color:rgb(255, 255, 255); background:rgb(91, 91, 91)")
			self.ui.loadButton_2.setStyleSheet("background:rgb(100, 100, 100); color:rgb(255, 255, 255)")

		# Generate Tab - Unchecked
		else:
			self.ui.loadButton_2.setEnabled(False)
			self.ui.fileText_2.setEnabled(False)
			self.ui.fileText_2.setStyleSheet("background:rgb(139, 139, 139);color:rgb(109, 109, 109)")
			self.ui.loadButton_2.setStyleSheet("background:rgb(139, 139, 139);color:rgb(109, 109, 109)")

	@pyqtSlot()
	def clearSlot(self):
		from subprocess import call

		self.ret = QMessageBox()
		select = self.ret.question(self, "Warning",\
		"""<font color='white'><p><b>__Batch/out 폴더를 삭제하시겠습니까?</b></p>
			<p>'Yes'버튼을 누르면 '__Batch' 경로내의 'out' 폴더가 삭제됩니다!</p>
		""", QMessageBox.Yes|QMessageBox.No)

		if select == QMessageBox.Yes or select==True:
			call(["rmdir", "/S", "/Q", "..\\..\\__Batch\\out"], shell=True)


	@pyqtSlot()
	def fileLoadSlot(self):
		"""
		if 'load ini' checked, can load ini file.
		"""
		ini_path = QFileDialog.getOpenFileName(self, \
			"Ini 경로", "..\\..\\data", "ini Files (*.ini)")

		try:
			self.ui.fileText.setText(ini_path[0])
		except:
			pass

	@pyqtSlot()
	def fileLoadSlot2(self):
		import os
		"""
		if 'load ini' checked, can load ini file.
		"""
		ini_path = QFileDialog.getOpenFileName(self, \
			"Ini 경로", "..\\..\\data", "ini Files (*.ini)")

		try:
			self.ui.fileText_2.setText(ini_path[0])
			split_path = os.path.split(ini_path[0])[0].split("/")[-5:]
			self.ui.platformField_2.setText(split_path[0])
			self.ui.zoneField_2.setText(split_path[1])
			self.ui.langField_2.setText(split_path[2])
			self.ui.carField_2.setText(split_path[3])
			self.ui.descriptionField_2.setText(split_path[4].split("_")[1].split("-")[0])
			self.ui.dateField.setText(split_path[4].split("_")[0])

		except:
			pass

	@pyqtSlot()
	def createSlot(self):

		try:
			platform = self.ui.platformField.text()
			zone = self.ui.zoneField.text()
			lang = self.ui.langField.text()
			car = self.ui.carField.text()
			acmod = self.ui.acmodField.text()
			description = self.ui.descriptionField.text()
			sound_path = self.ui.soundField.text()
			clean_noise = [self.ui.cleanButton.isChecked(), self.ui.noiseButton.isChecked()]

			if self.ui.bnfCheck.isChecked(): context = "bnf"
			else: context = "slm"

			if platform != "" and zone != "" and lang != "" and\
			 	car != "" and acmod !="" and\
				clean_noise != [False, False]: pass
			else: raise Exception

			if self.ui.loadCheck.isChecked() and self.ui.fileText.text() != "":
				load_chedck = self.ui.fileText.text()
			else : load_chedck = False

			if description != "":
				batch_create = BatchBatch(load_chedck, platform, zone, lang, car,\
				 					acmod, sound_path, description)
			else:
				batch_create = BatchBatch(load_chedck, platform, zone, lang, car, \
									acmod, sound_path)
		except Exception as e:
			print(e)
			QMessageBox.about(self, "Error", """<font color='white'><p><b>필수칸을 다 채워주세요</b></p>""")
			return

		batch_create.generate(context, clean_noise)

	@pyqtSlot()
	def generateSlot(self):
		arg_list = [self.ui.platformField_2.text(), self.ui.zoneField_2.text(),\
					self.ui.langField_2.text(), self.ui.carField_2.text(),\
					self.ui.descriptionField_2.text(), self.ui.dateField.text(),\
					self.ui.batchComboBox.currentText()]
		radio_list = [self.ui.cleanOn.isChecked(), self.ui.noiseOn.isChecked(),\
					self.ui.batchOn.isChecked(), self.ui.batchOff.isChecked(),\
					self.ui.bnfOn.isChecked(), self.ui.slmOn.isChecked()]

		batch_generate = BatchGenerate(arg=arg_list, button=radio_list)
		batch_generate.start()

	@pyqtSlot()
	def exec(self):
		self.exportIniParser()
		QApplication.quit()

	def importIniParser(self):
		import configparser

		config = configparser.ConfigParser()
		config.read(".\\config.ini")

		platform = config['CREATE']['PLATFORM']
		zone = config['CREATE']['ZONE']
		lang = config['CREATE']['LANG']
		car = config['CREATE']['CAR']
		acmod = config['CREATE']['ACMOD']
		description = config['CREATE']['DESCRIPTION']
		sound = config['CREATE']['SOUND_PATH']
		version = config['CREATE']['VERSION']
		date = config['CREATE']['DATE']

		return (platform, zone, lang, car, acmod, description, sound, version, date)

	def exportIniParser(self):

		config = configparser.ConfigParser()
		config.read(".\\config.ini")

		config['CREATE']['PLATFORM'] = self.ui.platformField.text()
		config['CREATE']['ZONE'] = self.ui.zoneField.text()
		config['CREATE']['LANG'] = self.ui.langField.text()
		config['CREATE']['CAR'] = self.ui.carField.text()
		config['CREATE']['ACMOD'] = self.ui.acmodField.text()
		config['CREATE']['DESCRIPTION'] = self.ui.descriptionField.text()
		config['CREATE']['SOUND_PATH'] = self.ui.soundField.text()
		config['CREATE']['VERSION'] = self.ui.batchComboBox.currentText()
		config['CREATE']['DATE'] = self.ui.dateField.text()


		with open(".\\config.ini", "w") as configfile:
			config.write(configfile)

	def setInitBox(self):
		from datetime import datetime

		field_list = self.importIniParser()
		self.ui.platformField.setText(field_list[0])
		self.ui.platformField_2.setText(field_list[0])
		self.ui.zoneField.setText(field_list[1])
		self.ui.zoneField_2.setText(field_list[1])
		self.ui.langField.setText(field_list[2])
		self.ui.langField_2.setText(field_list[2])
		self.ui.carField.setText(field_list[3])
		self.ui.carField_2.setText(field_list[3])
		self.ui.acmodField.setText(field_list[4])
		self.ui.descriptionField.setText(field_list[5])
		self.ui.descriptionField_2.setText(field_list[5])
		self.ui.soundField.setText(field_list[6])
		index = self.ui.batchComboBox.findText(field_list[7], QtCore.Qt.MatchFixedString)
		self.ui.batchComboBox.setCurrentIndex(index)
		self.ui.dateField.setText(field_list[8])


	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.exportIniParser()
			self.close()

	def closeEvent(self, event):
		self.exportIniParser()


if __name__=='__main__':

	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	form = BatchMan()
	sys.exit(app.exec_())
