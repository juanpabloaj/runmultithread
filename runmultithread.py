
import multiprocessing
import os
import subprocess
import sys
import time

from PySide import QtCore, QtGui


def replace_slash(string):
    return string.replace('/', '\\')


class WorkerThread(QtCore.QThread):

    def __init__(self, bin, to_run, count, running, completed):
        super(WorkerThread, self).__init__()
        self.bin = bin
        self.to_run = to_run
        self.running = running
        self.completed = completed
        self.count = count

    def run(self):

        proc_args = [self.bin, self.to_run]
        proc = subprocess.Popen(proc_args)

        task_name = '#{:03} {}'.format(self.count, self.to_run)
        self.running.insertItem(0, task_name)

        while True:
            time.sleep(0.5)
            retcode = proc.poll()
            if retcode is not None:

                item = self.running.findItems(
                    task_name, QtCore.Qt.MatchExactly
                )[0]
                self.running.takeItem(self.running.row(item))
                self.completed.insertItem(0, task_name)

                break


class Monitor(QtCore.QThread):

    def __init__(self, bin, waiting, running, finished, cpus):
        super(Monitor, self).__init__()

        self.create_threads = False
        self.waiting = waiting
        self.running = running
        self.completed = finished
        self.cpus = cpus
        self.threads = []
        self.bin = bin

    def run(self):

        self.active = True
        while self.active:
            time.sleep(0.1)

            if self.create_threads:

                free_cpus = self.running.count() < self.cpus
                if self.waiting.count() > 0 and free_cpus:
                    self.new_thread()

    def new_thread(self):

        new_task = self.waiting.takeItem(
            self.waiting.count() - 1
        ).text()

        threads_count = len(self.threads) + 1
        thread = WorkerThread(
            self.bin, new_task,
            threads_count, self.running, self.completed
        )
        thread.start()
        self.threads.append(thread)


class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)

        self.setObjectName("MainWindow")
        self.resize(400, 500)

        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.vLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vLayout.setObjectName("vLayout")

        self.setCentralWidget(self.centralwidget)

        bin_layout = QtGui.QHBoxLayout()
        bin_layout.addStretch()

        self.bin_path = ''
        self.bin_name_label = QtGui.QLabel('Select a .exe to use')
        add_bin_btn = QtGui.QPushButton('Select .exe')
        add_bin_btn.clicked.connect(self.select_bin_path)

        bin_layout.addWidget(self.bin_name_label)
        bin_layout.addWidget(add_bin_btn)

        add_file_layout = QtGui.QHBoxLayout()
        add_file_layout.addStretch(1)

        add_file_btn = QtGui.QPushButton('Add file')
        add_dir_btn = QtGui.QPushButton('Add folder')
        self.filter_line = QtGui.QLineEdit()
        self.filter_line.setPlaceholderText('Extensions to filter files')

        add_file_btn.clicked.connect(self.add_file)
        add_dir_btn.clicked.connect(self.add_files_from_folder)

        add_file_layout.addWidget(self.filter_line)
        add_file_layout.addWidget(add_file_btn)
        add_file_layout.addWidget(add_dir_btn)

        process_vlayout = QtGui.QVBoxLayout()
        waiting_label = QtGui.QLabel('Input files')
        self.waiting_files = QtGui.QListWidget()
        running_label = QtGui.QLabel('Running')
        self.running_process = QtGui.QListWidget()
        finished_label = QtGui.QLabel('Finished')
        self.finished_process = QtGui.QListWidget()

        process_vlayout.addWidget(waiting_label)
        process_vlayout.addWidget(self.waiting_files)
        process_vlayout.addWidget(running_label)
        process_vlayout.addWidget(self.running_process)
        process_vlayout.addWidget(finished_label)
        process_vlayout.addWidget(self.finished_process)

        run_layout = QtGui.QHBoxLayout()
        run_layout.addStretch(1)

        cpu_count_label = QtGui.QLabel('CPU Threads to use')
        self.cpu_count = multiprocessing.cpu_count()
        self.cpu_spinbox = QtGui.QSpinBox()
        self.cpu_spinbox.valueChanged.connect(self.update_cpu_count)
        self.cpu_spinbox.setMinimum(1)
        self.cpu_spinbox.setValue(self.cpu_count)
        self.run_btn = QtGui.QPushButton('Run')
        self.run_btn.clicked.connect(self.run_start_stop)

        run_layout.addWidget(cpu_count_label)
        run_layout.addWidget(self.cpu_spinbox)
        run_layout.addWidget(self.run_btn)

        self.vLayout.addLayout(bin_layout)
        self.vLayout.addLayout(add_file_layout)
        self.vLayout.addLayout(process_vlayout)
        self.vLayout.addLayout(run_layout)

        self.threads = []

        self.monitor = Monitor(
            self.bin_path,
            self.waiting_files, self.running_process, self.finished_process,
            self.cpu_count
        )
        self.threads.append(self.monitor)
        self.monitor.start()

    def select_bin_path(self):
        if self.running_process.count() > 0 or self.monitor.create_threads:
            return

        filename, _ = QtGui.QFileDialog.getOpenFileName(filter='*.exe')
        if filename:
            filename = replace_slash(filename)
            self.bin_path = filename
            self.monitor.bin = self.bin_path
            self.bin_name_label.setText(filename)

    def add_file(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(
            filter=self.filter_line.text()
        )
        if filename:
            filename = replace_slash(filename)
            self.waiting_files.insertItem(0, filename)

    def add_files_from_folder(self):
        foldername = QtGui.QFileDialog.getExistingDirectory()
        if foldername:
            filters = self.filter_line.text().split()
            it = QtCore.QDirIterator(foldername, filters)

            while it.hasNext():
                it.next()

                filepath = it.filePath()

                if os.path.isfile(filepath):

                    filepath = replace_slash(filepath)
                    self.waiting_files.insertItem(0, filepath)

    def update_cpu_count(self):
        self.cpu_count = self.cpu_spinbox.value()

    def run_start_stop(self):
        if not self.monitor.create_threads:
            if self.bin_path != '' and self.waiting_files.count() > 0:
                self.monitor.create_threads = True
                self.run_btn.setText('Pause')

        else:
            self.monitor.create_threads = False
            self.run_btn.setText('Run')

    def closeEvent(self, event):
        self.monitor.active = False
        self.monitor.quit()
        self.monitor.wait()


def main():
    app = QtGui.QApplication(sys.argv)
    frame = ControlMainWindow()
    frame.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()