import os
import json
import requests
from PyQt5.QtWidgets import QDialog,\
 							QApplication, \
							QWidget, \
							QMessageBox,\
							QTableWidgetItem, \
							QTextEdit
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, \
						Qt
from urllib import request


class ServerForm(QDialog):


	def __init__(self, platform, lang, parent=None):
		QDialog.__init__(self, parent)
		QDialog.setFixedSize(self, 890, 485)
		self.ui2 = uic.loadUi('platforms\serverList.ui', self)
		self.ui2.show()
		self.ui2.table.setColumnWidth(0, 150)
		self.ui2.table.setColumnWidth(1, 100)
		self.ui2.table.setColumnWidth(4, 150)
		self.ui2.table.setColumnWidth(5, 250)
		self.platform = platform
		self.lang = lang
		self.data = ""

		try:
			result = request.urlopen("https://spreadsheets.google.com/feeds/list/14qU4DS9qOuVQ8Sp_o2bSMXymbbNUp17JVaqGphkyLs4/od6/public/values?alt=json")
			self.result_data = json.loads(result.read())
			self.setTable()
		except requests.exceptions.HTTPError as error:
			QMessageBox.about(self, "ServerError", error)
			self.close()

	@pyqtSlot()
	def close2(self):
		self.ui2.close()

	def setTable(self):
		count = 1
		row_count = 0
		for lists in self.result_data["feed"]["entry"]:
			if lists["gsx$platform"]["$t"] == self.platform and\
				lists["gsx$nation"]["$t"] == self.lang:
				self.ui2.table.setRowCount(count)
				self.ui2.table.setItem(row_count, 0, QTableWidgetItem(lists["gsx$timestamp"]["$t"]))
				self.ui2.table.setItem(row_count, 1, QTableWidgetItem(lists["gsx$author"]["$t"]))
				self.ui2.table.setItem(row_count, 2, QTableWidgetItem(lists["gsx$platform"]["$t"]))
				self.ui2.table.setItem(row_count, 3, QTableWidgetItem(lists["gsx$nation"]["$t"]))
				self.ui2.table.setItem(row_count, 4, QTableWidgetItem(lists["gsx$data"]["$t"]))
				self.ui2.table.setItem(row_count, 5, QTableWidgetItem(lists["gsx$description"]["$t"]))
				count += 1
				row_count +=1

	@pyqtSlot()
	def server_ok_button(self):
		self.data = self.ui2.table.item(self.ui2.table.currentRow(), 4).text()
		self.ui2.close()
		QMessageBox.about(self, "Succes", "체크리스트 다운 완료")

	@pyqtSlot()
	def open_data(self):
		data = self.ui2.table.item(self.ui2.table.currentRow(), 4).text()
		self.open_popup = OpenData(data)


	def get_value(self):
		return self.data

class OpenData(QWidget):

	def __init__(self, data):
		super().__init__()
		QWidget.setFixedSize(self, 500, 500)
		self.data = data

		self.initUI()
		self.show()

	def initUI(self):
		self.setGeometry(500, 500, 500, 500)
		self.setWindowTitle("Data")

		self.textedit = QTextEdit(self)
		self.textedit.resize(self.width(), self.height())
		self.textedit.setReadOnly(True)
		self.textedit.setText(self.data)

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Escape:
			self.close()
