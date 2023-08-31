import logging
from log_setter import set_logging
from unlock import enable_telnet
## STEP4a - import the tool function from the file you imported into the CTOOLS3 project folder
from ui_help import gen_tool_layout, gen_custom_tool_layout, create_tool_bar
from login import global_admin_login
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QMainWindow,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QTextEdit,
    QFrame,
)
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500
OUTPUT_HEIGHT = 250
class enableTelnetWindow(QMainWindow):
    """PyCalc's main window (GUI or view)."""
    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.setWindowTitle("CTools 3.0")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.generalLayout = QVBoxLayout()
        self.top = QLabel("<h2>Welcome to CTools!</h2>")
        self.mainContent = QHBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self.generalLayout.addWidget(self.top)
        self.generalLayout.addLayout(self.mainContent)
        self._createToolBar()
        self._createToolViewLayout()
    def _createToolBar(self):
        tools = create_tool_bar(self.widget, 4)
        # Add line separator between Tool List and Tool View
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setLineWidth(1)
        self.mainContent.addLayout(tools)
        self.mainContent.addWidget(line)
    def _createToolViewLayout(self):
        toolView = QVBoxLayout()
        # Step3 - You will change the next two lines according to the KB
        EnableTelnetLayout, self.input_widgets = gen_custom_tool_layout(["Device Name", "Tenant Name", "Required Code for Telnet"], ["Ignore Cert Warnings for Login", "Verbose Logging"])
        toolView.addLayout(EnableTelnetLayout)
        # Create action buttons
        actionButtonLayout = QHBoxLayout()
        self.cancel = QPushButton("Cancel")
        self.start = QPushButton("Start")
        actionButtonLayout.addWidget(self.cancel)
        actionButtonLayout.addWidget(self.start)
        toolView.addLayout(actionButtonLayout)
        # Add button listeners
        self.start.clicked.connect(self.enable_telnet)
        # Create Output box
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        toolView.addWidget(self.output)
        self.mainContent.addLayout(toolView)
    def enable_telnet(self):
        portal_address = self.input_widgets[0].text()
        portal_username = self.input_widgets[1].text()
        portal_password = self.input_widgets[2].text()
        device_name = self.input_widgets[3].text()
        tenant_name = self.input_widgets[4].text()
        code = self.input_widgets[5].text()
        ignore_cert = self.input_widgets[6].isChecked()
        verbose = self.input_widgets[7].isChecked()
        if verbose:
            set_logging(logging.DEBUG, 'debug-log.txt')
        else:
            set_logging()
        global_admin = global_admin_login(portal_address, portal_username, portal_password, ignore_cert)
        ## Step4b - Run the tool here
        enable_telnet(global_admin, device_name, tenant_name, code)
        self._updateOutput()
    def _updateOutput(self):
        file = open("output.tmp", 'r')
        with file:
            text = file.read()
            self.output.setText(text)
        self.output.verticalScrollBar().setValue(self.output.verticalScrollBar().maximum())