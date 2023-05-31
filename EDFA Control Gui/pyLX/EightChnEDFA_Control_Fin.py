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
        height = 700
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

        self.CreateButton_close_app()
        self.CreateButton_EDFA2_on()
        self.CreateButton_EDFA2_off()

        #utilize dynamic programming to generate EDFA control lines
        for i in range(len(ILX.EDFA1_channels)):
            self.Make_EDFA1_Interface(i)
        for i in range(len(ILX.EDFA2_channels)):
            self.Make_EDFA2_Interface(i)



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

    # EDFA1,2 buttons definition
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
        button.setGeometry(QRect(25, 300, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.EDFA2_on)

    def CreateButton_EDFA2_off(self):
        button = QPushButton("EDFA2 Off", self)
        # button.move(50,50)
        button.setGeometry(QRect(25, 325, 100, 25))
        button.setIcon(QtGui.QIcon(self.iconName))
        button.setIconSize(QtCore.QSize(40, 40))
        # button.setToolTip("<h2>This is Click Me button<h2>")
        button.clicked.connect(self.EDFA2_off)



    #Dynamically define EDFA1 Interface functions:
    def Make_EDFA1_Interface(self,index):
        def _EDFA1_line(self):
            line_edit = QLineEdit('0', self)
            line_edit.setGeometry(250, 125+index*25, 100, 25)
            line_label = QLabel('Ch. ' + str(ILX.EDFA1_channels[index]) + ': [mA]', self)
            line_label.setGeometry(150, 125+index*25, 100, 25)
            line_label.setWordWrap(False)
            line_edit.returnPressed.connect(lambda: EDFA1_line1_action(self))
            def EDFA1_line1_action(self):
                value_line1 = line_edit.text()
                ILX.LDI_set(ILX.EDFA1_channels[index], float(value_line1))
                self.beep()
        return _EDFA1_line(self)


    #Dynamically define EDFA2 Interface functions:
    def Make_EDFA2_Interface(self,index):
        def _EDFA2_line(self):
            line_edit = QLineEdit('0',self)
            line_edit.setGeometry(250, 300+index*25, 100, 25)
            line_label = QLabel('Ch. ' + str(ILX.EDFA2_channels[index]) + ': [mA]', self)
            line_label.setGeometry(150, 300+index*25, 100, 25)
            line_label.setWordWrap(False)
            line_edit.returnPressed.connect(lambda: EDFA2_line1_action(self))
            def EDFA2_line1_action(self):
                value_line1 = line_edit.text()
                ILX.LDI_set(ILX.EDFA2_channels[index], float(value_line1))
                self.beep()
        return _EDFA2_line(self)





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
        ILX.EDFA2_on()
        # print("EDFA1 ON/OFF")
        # sys.exit()

    def EDFA2_off(self):
        ILX.EDFA2_off()

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
