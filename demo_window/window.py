import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
import sys
class WindowDemo(QWidget):
    def __init__(self):
        super(WindowDemo, self).__init__()
        btn1 = QPushButton(u'run camera', self)
        btn2 = QPushButton(u'stop running', self)

        btn1.clicked.connect(self.handle_event)
        btn2.clicked.connect(self.handle_event)

        hbox = QHBoxLayout()
        hbox.addWidget(btn1)
        hbox.addWidget(btn2)
        hbox.addStretch(0)
        self.setLayout(hbox)
        self.setWindowTitle("have a nice day!")

    def handle_event(self):

        sender = self.sender()
        clickevent = sender.text()
        if clickevent == u'run camera':
            p1 = subprocess.Popen('ls -l', shell=True)

        else:
            p2 = subprocess.Popen('ls -a', shell=True)
            print('hello')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WindowDemo()
    win.show()
    sys.exit(app.exec_())
