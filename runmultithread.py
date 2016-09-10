import sys
import os
import multiprocessing
import subprocess
from PySide import QtGui, QtCore


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(400, 500)

		self.centralwidget = QtGui.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		self.vLayout = QtGui.QVBoxLayout(self.centralwidget)
		self.vLayout.setObjectName("vLayout")

		#self.label = QtGui.QLabel('A label', self.centralwidget)
		#self.label.setObjectName('label')
		#self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

		MainWindow.setCentralWidget(self.centralwidget)

		bin_layout = QtGui.QHBoxLayout()
		bin_layout.addStretch()

		bin_name_label = QtGui.QLabel('Select a .exe to use')
		add_bin_btn = QtGui.QPushButton('Select .exe')

		bin_layout.addWidget(bin_name_label)
		bin_layout.addWidget(add_bin_btn)

		add_file_layout = QtGui.QHBoxLayout()
		add_file_layout.addStretch(1)

		add_file_btn = QtGui.QPushButton('Add file')
		add_dir_btn = QtGui.QPushButton('Add Folder')
		input_filter_line = QtGui.QLineEdit()
		input_filter_line.setPlaceholderText('Extensions to filter files')

		add_file_btn.clicked.connect(self.add_file)
		add_dir_btn.clicked.connect(self.add_folder_files)

		add_file_layout.addWidget(input_filter_line)
		add_file_layout.addWidget(add_file_btn)
		add_file_layout.addWidget(add_dir_btn)

		process_vlayout = QtGui.QVBoxLayout()
		waiting_files_qlist = QtGui.QListWidget()
		running_process_qlist = QtGui.QListWidget()
		finished_process_qlist = QtGui.QListWidget()

		process_vlayout.addWidget(waiting_files_qlist)
		process_vlayout.addWidget(running_process_qlist)
		process_vlayout.addWidget(finished_process_qlist)

		run_layout = QtGui.QHBoxLayout()
		run_layout.addStretch(1)

		cpu_count_label = QtGui.QLabel('CPU Threads to use')
		cpu_count = multiprocessing.cpu_count()
		cpu_spinbox = QtGui.QSpinBox()
		cpu_spinbox.setMinimum(1)
		cpu_spinbox.setValue(multiprocessing.cpu_count())
		run_btn = QtGui.QPushButton('Run')

		run_layout.addWidget(cpu_count_label)
		run_layout.addWidget(cpu_spinbox)
		run_layout.addWidget(run_btn)

		self.vLayout.addLayout(bin_layout)
		self.vLayout.addLayout(add_file_layout)
		self.vLayout.addLayout(process_vlayout)
		self.vLayout.addLayout(run_layout)


	def add_file(self):
		filename, _ = QtGui.QFileDialog.getOpenFileName()
		if filename:
			print filename

	def add_folder_files(self):
		foldername = QtGui.QFileDialog.getExistingDirectory()
		if foldername:
			for filename in os.listdir(foldername):
				print filename

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(
			QtGui.QApplication.translate(
				"MainWindow", "MainWindow", None,
				QtGui.QApplication.UnicodeUTF8
			)
		)


class ControlMainWindow(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(ControlMainWindow, self).__init__(parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)


def main():
	app = QtGui.QApplication(sys.argv)
	frame = ControlMainWindow()
	frame.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()