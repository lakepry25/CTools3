# ctools.py

"""CTools is a GUI toolset to interact with your CTERA Environment"""

import sys, os

from status import run_status

from windows.RunCmdWindow import runCmdWindow
from windows.ShowStatusWindow import showStatusWindow

from PySide2.QtCore import Qt

from PySide2.QtWidgets import (
    QApplication,
    QStackedWidget
)

def main():
    """PyCalc's main function."""

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    ctoolsApp = QApplication(sys.argv)
    
    
    widget = QStackedWidget()
    
    run_cmd = runCmdWindow(widget)
    widget.addWidget(run_cmd)   # create an instance of the first page class and add it to stackedwidget

    show_status = showStatusWindow(widget) 
    widget.addWidget(show_status)   # adding second page

    widget.setCurrentWidget(run_cmd)   # setting the page that you want to load when application starts up. you can also use setCurrentIndex(int)

    widget.show()

    ctoolsApp.exec_()

    

if __name__ == "__main__":
    main()