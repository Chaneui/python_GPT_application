# 1
import sys
import time
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QThread, pyqtSignal
from pynput import keyboard, mouse

# 2
class ClickMacro(QtWidgets.QMainWindow):
    def __init__(self):
        super(ClickMacro, self).__init__()
        # 3
        uic.loadUi(r'여기에 소스코드와 함께 제공된 click_macro.ui 파일의 경로를 입력합니다', self)
        
        # 4
        self.click_speed = 1
        self.click_number = 0
        self.click_count = 0
        self.click_position = (0, 0)
        self.running = False

        self.show()

        # 5
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()

        # 6
        self.mouse_controller = mouse.Controller()

        # 7
        self.location_log = self.findChild(QtWidgets.QTextBrowser, 'location_log')
        self.click_counter = self.findChild(QtWidgets.QTextBrowser, 'click_counter')
        self.click_speed_input = self.findChild(QtWidgets.QLineEdit, 'click_speed')
        self.click_number_input = self.findChild(QtWidgets.QLineEdit, 'click_number')

    def on_press(self, key):
        try:
            # 8
            if key == keyboard.Key.f5:
                self.click_position = self.mouse_controller.position
                QtCore.QMetaObject.invokeMethod(
                    self.location_log,
                    "append",
                    QtCore.Qt.QueuedConnection,
                    QtCore.Q_ARG(str, f"클릭할 좌표: {self.click_position}")
                )
            # 9
            elif key == keyboard.Key.f6:
                self.start_macro()
        except AttributeError:
            pass

    def start_macro(self):
        # 10
        try:
            self.click_speed = float(self.click_speed_input.text())
            self.click_number = int(self.click_number_input.text())
        except ValueError:
            self.location_log.append("잘못된 수치를 입력했습니다")
            return

        self.click_count = 0
        self.running = True
        
        # 11
        self.click_thread = QThread()
        self.worker = ClickWorker(self.click_speed, self.click_number, self.click_position)
        self.worker.moveToThread(self.click_thread)


        self.worker.update_counter.connect(self.update_click_counter)
        self.worker.finished.connect(self.click_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.click_thread.finished.connect(self.click_thread.deleteLater)


        self.click_thread.started.connect(self.worker.run)
        self.click_thread.start()
    
    # 12
    def update_click_counter(self, count):
        self.click_counter.setText(f"클릭 횟수: {count}")

# 13
class ClickWorker(QtCore.QObject):
    update_counter = pyqtSignal(int)
    finished = pyqtSignal()

    def __init__(self, click_speed, click_number, click_position):
        super().__init__()
        self.click_speed = click_speed
        self.click_number = click_number
        self.click_position = click_position
        self.mouse_controller = mouse.Controller()

    # 14
    def run(self):
        for i in range(self.click_number):
            if not self.click_speed > 0:
                break
            self.mouse_controller.position = self.click_position
            self.mouse_controller.click(mouse.Button.left, 1)
            self.update_counter.emit(i + 1)
            time.sleep(1 / self.click_speed)
        self.finished.emit()


app = QtWidgets.QApplication(sys.argv)
window = ClickMacro()
app.exec_()