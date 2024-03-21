# This Python file uses the following encoding: utf-8
import sys
import traceback
import requests
from download import Downloader
from os import startfile
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_Widget


class MainWindow(QWidget):
    mw_sig = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setup_thread()
        self.ui.lineEdit.textChanged.connect(self.url_changed)
        self.ui.pushButton.clicked.connect(self.download)
        self.url = ""
        self.downloading = False

    def setup_thread(self):
        self.main_thread = QThread(self)
        self.worker_thread = DownloadWorker()
        self.worker_thread.moveToThread(self.main_thread)
        self.worker_thread.trigger.connect(self.stop_thread)
        self.worker_thread.download_trigger.connect(self.show_message_box)
        self.worker_thread.error_trigger.connect(self.handle_download_error)
        self.main_thread.start()

    def stop_thread(self, button_text):
        self.ui.pushButton.setText(button_text)
        self.main_thread.quit()
        self.main_thread.wait()

    def url_changed(self, url):
        self.url = url
        self.ui.pushButton.setText("下载")

    def show_message_box(self, dst_path):
        reply = QMessageBox.question(
            None,
            "下载完成",
            f"文件保存在 {dst_path} 中，要打开该文件夹吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            startfile(dst_path)
        else:
            pass

    def handle_download_error(self, err_msg):
        self.downloading = False
        QMessageBox.warning(self, "下载出错", err_msg)

    def download(self):
        if self.downloading:
            QMessageBox.warning(self, "正在下载", "请等待下载完成再尝试！")
        else:
            if self.url.strip() == "":
                QMessageBox.warning(
                    self, "模型地址不能为空", "请先填写模型地址再尝试！"
                )
            else:
                self.downloading = True
                try:
                    self.worker_thread.download(self.url)
                except (
                    requests.exceptions.MissingSchema
                    or requests.exceptions.InvalidURL
                ):
                    QMessageBox.warning(
                        self, "模型地址错误", "请填写正确的模型地址！"
                    )
                    self.ui.pushButton.setText("下载错误")

                self.downloading = False


class DownloadWorker(QObject):
    trigger = Signal(str)
    download_trigger = Signal(str)
    error_trigger = Signal(str)

    def __init__(self):
        super().__init__()
        self.downloader = Downloader()

    def download(self, url):
        self.trigger.emit("下载中...")
        QApplication.processEvents()
        try:
            self.downloader.download(url)
            self.downloader.convert()
            dst_path = self.downloader.merge_glb()
            self.download_trigger.emit(dst_path)
            self.trigger.emit("下载完成")
        except (
            requests.exceptions.MissingSchema or requests.exceptions.InvalidURL
        ):
            self.error_trigger.emit("模型地址错误，请填写正确的模型地址！")
        except Exception as e:
            self.error_trigger.emit(str(e))
            self.trigger.emit("下载出错")
            traceback.print_exc()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setWindowTitle("模型下载器")
    mainWindow.show()
    sys.exit(app.exec())
