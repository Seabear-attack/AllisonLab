# GUI for commanding ILX 16-ch diode controller.
# Calls methods of class ILXcontrol in ILXcontrol_FTIR.py
#
# Jay Rutledge, 10.20.2022

from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QLineEdit, QLabel
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QRect
from ILXcontrol_FTIR2 import ILXcontrol

# Instantiate ILX class object, for calling ILXcontrol.py methods throughout
ILX = ILXcontrol()


# Define the GUI class
class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Specify window title and dimensions/placement
        title = "ILX 16-Ch laser diode controller"
        left = 500
        top = 200
        width = 400
        height = 1000
        self.iconName = "home.png"

        # Realize window settings
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(left, top, width, height)

        # Create buttons
        self.CreateButton_open_serial()
        self.CreateButton_close_serial()
        self.CreateButton_beep()
        self.CreateButton_EDFA1_on()
        self.CreateButton_EDFA1_off()
        self.CreateButton_preAmp_on()
        self.CreateButton_preAmp_off()
        self.CreateButton_FTIR_on()
        self.CreateButton_FTIR_off()
        self.CreateButton_close_app()
        self.CreateButton_EDFA2_on()
        self.CreateButton_EDFA2_off()


        self.EDFA1_line1()
        self.EDFA1_line2()
        self.EDFA1_line3()
        self.EDFA1_line4()

        self.EDFA2_line1()
        self.EDFA2_line2()
        self.EDFA2_line3()
        self.EDFA2_line4()

        self.preAmp_line1()

        self.FTIR_line1()

        self.CreateButton_menu_all()
        self.menu_ch_line()


        self.show()

    # Define Event buttons -------------------------------------------------------

    def CreateButton_open_serial(self):
        button = QPushButton("Connect", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 25, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.open_serial)

    def CreateButton_close_serial(self):
        button = QPushButton("Disconnect", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 50, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.close_serial)

    def CreateButton_beep(self):
        button = QPushButton("Beep", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 75, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.beep)

    # EDFA1 (Ch's fwd: 1+2, bwd: 7+8)
    def CreateButton_EDFA1_on(self):
        button = QPushButton("EDFA1 On", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 125, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.EDFA1_on)

    def CreateButton_EDFA1_off(self):
        button = QPushButton("EDFA1 Off", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 150, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.EDFA1_off)

    def CreateButton_EDFA2_on(self):
        button = QPushButton("EDFA2 On", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 500, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.EDFA1_on)

    def CreateButton_EDFA2_off(self):
        button = QPushButton("EDFA2 Off", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 525, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.EDFA1_off)


    # preAmp (Ch 3)
    def CreateButton_preAmp_on(self):
        button = QPushButton("preAmp On", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 300, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.preAmp_on)

    def CreateButton_preAmp_off(self):
        button = QPushButton("preAmp Off", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 325, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.preAmp_off)

    # FTIR (Ch 10)
    def CreateButton_FTIR_on(self):
        button = QPushButton("FTIR On", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 375, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.FTIR_on)

    def CreateButton_FTIR_off(self):
        button = QPushButton("FTIR Off", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 400, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.FTIR_off)

    def EDFA1_line1(self):
        line_edit = QLineEdit('0', self)
        line_edit.setGeometry(250, 125, 100, 25)
        line_label = QLabel('Ch. ' + str(ILX.EDFA1_channels[0]) + ': [mA]', self)
        line_label.setGeometry(150, 125, 100, 25)
        line_label.setWordWrap(False)
        line_edit.returnPressed.connect(lambda: EDFA1_line1_action())

        def EDFA1_line1_action():
            value_line1 = line_edit.text()
            ILX.LDI_set(ILX.EDFA1_channels[0], float(value_line1))
            self.beep()

    def EDFA1_line2(self):
        line_edit = QLineEdit('0', self)
        line_edit.setGeometry(250, 150, 100, 25)
        line_label = QLabel('Ch. ' + str(ILX.EDFA1_channels[1]) + ': [mA]', self)
        line_label.setGeometry(150, 150, 100, 25)
        line_label.setWordWrap(False)
        line_edit.returnPressed.connect(lambda: EDFA1_line2_action())

        def EDFA1_line2_action():
            value_line2 = line_edit.text()
            ILX.LDI_set(ILX.EDFA1_channels[1], float(value_line2))
            self.beep()

    def EDFA1_line3(self):
        line_edit = QLineEdit('0', self)
        line_edit.setGeometry(250, 175, 100, 25)
        line_label = QLabel('Ch. ' + str(ILX.EDFA1_channels[2]) + ': [mA]', self)
        line_label.setGeometry(150, 175, 100, 25)
        line_label.setWordWrap(False)
        line_edit.returnPressed.connect(lambda: EDFA1_line3_action())

        def EDFA1_line3_action():
            value_line3 = line_edit.text()
            ILX.LDI_set(ILX.EDFA1_channels[2], float(value_line3))
            self.beep()

    def EDFA1_line4(self):
        line_edit = QLineEdit('0', self)
        line_edit.setGeometry(250, 200, 100, 25)
        line_label = QLabel('Ch. ' + str(ILX.EDFA1_channels[3]) + ': [mA]', self)
        line_label.setGeometry(150, 200, 100, 25)
        line_label.setWordWrap(False)
        line_edit.returnPressed.connect(lambda: EDFA1_line4_action())

        def EDFA1_line4_action():
            value_line4 = line_edit.text()
            ILX.LDI_set(ILX.EDFA1_channels[3], float(value_line4))
            self.beep()

    def EDFA2_line1(self):
        line_edit = QLineEdit('0', self)
        line_edit.setGeometry(250, 500, 100, 25)
        line_label = QLabel('Ch. ' + str(ILX.EDFA1_channels[0]) + ': [mA]', self)
        line_label.setGeometry(150, 500, 100, 25)
        line_label.setWordWrap(False)
        line_edit.returnPressed.connect(lambda: EDFA1_line1_action())

        def EDFA2_line1_action():
            value_line1 = line_edit.text()
            ILX.LDI_set(ILX.EDFA1_channels[0], float(value_line1))
            self.beep()

    def EDFA2_line2(self):
        line_edit = QLineEdit('0', self)
        line_edit.setGeometry(250, 525, 100, 25)
        line_label = QLabel('Ch. ' + str(ILX.EDFA1_channels[1]) + ': [mA]', self)
        line_label.setGeometry(150, 525, 100, 25)
        line_label.setWordWrap(False)
        line_edit.returnPressed.connect(lambda: EDFA1_line2_action())

        def EDFA2_line2_action():
            value_line2 = line_edit.text()
            ILX.LDI_set(ILX.EDFA1_channels[1], float(value_line2))
            self.beep()

    def EDFA2_line3(self):
        line_edit = QLineEdit('0', self)
        line_edit.setGeometry(250, 550, 100, 25)
        line_label = QLabel('Ch. ' + str(ILX.EDFA1_channels[2]) + ': [mA]', self)
        line_label.setGeometry(150, 550, 100, 25)
        line_label.setWordWrap(False)
        line_edit.returnPressed.connect(lambda: EDFA1_line3_action())

        def EDFA2_line3_action():
            value_line3 = line_edit.text()
            ILX.LDI_set(ILX.EDFA1_channels[2], float(value_line3))
            self.beep()

    def EDFA2_line4(self):
        line_edit = QLineEdit('0', self)
        line_edit.setGeometry(250, 575, 100, 25)
        line_label = QLabel('Ch. ' + str(ILX.EDFA1_channels[3]) + ': [mA]', self)
        line_label.setGeometry(150, 575, 100, 25)
        line_label.setWordWrap(False)
        line_edit.returnPressed.connect(lambda: EDFA1_line4_action())

        def EDFA2_line4_action():
            value_line4 = line_edit.text()
            ILX.LDI_set(ILX.EDFA1_channels[3], float(value_line4))
            self.beep()



    def preAmp_line1(self):
        line_edit = QLineEdit('0', self)
        line_edit.setGeometry(250, 300, 100, 25)
        line_label = QLabel('Ch. ' + str(ILX.preAmp_channels[0]) + ': [mA]', self)
        line_label.setGeometry(150, 300, 100, 25)
        line_label.setWordWrap(False)
        line_edit.returnPressed.connect(lambda: preAmp_line1_action())

        def preAmp_line1_action():
            value_preAmp = line_edit.text()
            ILX.LDI_set(ILX.preAmp_channels[0], float(value_preAmp))
            self.beep()

    def FTIR_line1(self):
        line_edit = QLineEdit('0', self)
        line_edit.setGeometry(250, 400, 100, 25)
        line_label = QLabel('Ch. ' + str(ILX.FTIR_channels[0]) + ': [mA]', self)
        line_label.setGeometry(150, 400, 100, 25)
        line_label.setWordWrap(False)
        line_edit.returnPressed.connect(lambda: FTIR_line1_action())

        def FTIR_line1_action():
            value_FTIR = line_edit.text()
            ILX.LDI_set(ILX.FTIR_channels[0], float(value_FTIR))
            self.beep()

    def CreateButton_menu_all(self):
        button = QPushButton('Menu: Ch. ALL', self)
        # button.move(50,50)
        button.setGeometry(QRect(225, 25, 125, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.menu_all)

    def menu_ch_line(self):
        line_edit = QLineEdit('1', self)
        line_edit.setGeometry(300, 50, 50, 25)
        line_label = QLabel('Menu: Ch. ', self)
        line_label.setGeometry(225, 50, 100, 25)
        line_label.setWordWrap(False)
        line_edit.returnPressed.connect(lambda: menu_ch_line_action())

        def menu_ch_line_action():
            value_menu = line_edit.text()
            ILX.menu_ch(int(value_menu))
            self.beep()

    def CreateButton_close_app(self):
        button = QPushButton("Close Application", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 600, 150, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.close_app)

    # ------------------------------------------------------------
    # Specify Slot Actions (calls to ILXcontrol.py)-------------------------

    def open_serial(self):
        ILX.open_serial()

    def close_serial(self):
        ILX.close_serial()

    # For testng purposes:
    def beep(self):
        ILX.beep()

    # EDFA 1 -----------------------
    def EDFA1_on(self):
        ILX.EDFA1_on()
        # print("EDFA1 ON/OFF")
        # sys.exit()

    def EDFA1_off(self):
        ILX.EDFA1_off()


    def EDFA2_on(self):
        ILX.EDFA1_on()
        # print("EDFA1 ON/OFF")
        # sys.exit()

    def EDFA2_off(self):
        ILX.EDFA1_off()


    # preAmp -----------------------
    def preAmp_on(self):
        ILX.preAmp_on()

    def preAmp_off(self):
        ILX.preAmp_off()

    # FTIR -----------------------
    def FTIR_on(self):
        ILX.FTIR_on()

    def FTIR_off(self):
        ILX.FTIR_off()

    def close_app(self):
        print('Closing GUI application.')
        sys.exit()

    def menu_all(self):
        ILX.menu_all()
        ILX.beep()


# --------------------------------------------------------------
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
