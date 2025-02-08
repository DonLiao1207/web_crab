import sys
from PyQt5 import QtWidgets, uic

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/webrobin.ui", self)  # 讀取 UI 檔案
        self.setWindowTitle("PyQt UI Loader Example")  # 設定視窗標題
        self.show()  # 顯示 UI

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
