# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1047, 773)
        self.centralwidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_11 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_11.setMargin(1)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setStyleSheet(_fromUtf8(""))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.East)
        self.tabWidget.setTabShape(QtGui.QTabWidget.Rounded)
        self.tabWidget.setDocumentMode(False)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setEnabled(True)
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab)
        self.gridLayout_2.setMargin(6)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.left_frame = QtGui.QFrame(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.left_frame.sizePolicy().hasHeightForWidth())
        self.left_frame.setSizePolicy(sizePolicy)
        self.left_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.left_frame.setFrameShadow(QtGui.QFrame.Plain)
        self.left_frame.setObjectName(_fromUtf8("left_frame"))
        self.gridLayout_4 = QtGui.QGridLayout(self.left_frame)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.frame_6 = QtGui.QFrame(self.left_frame)
        self.frame_6.setFrameShape(QtGui.QFrame.Box)
        self.frame_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        self.gridLayout_6 = QtGui.QGridLayout(self.frame_6)
        self.gridLayout_6.setMargin(5)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.sensor_container = QtGui.QGridLayout()
        self.sensor_container.setObjectName(_fromUtf8("sensor_container"))
        self.gridLayout_6.addLayout(self.sensor_container, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.frame_6, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.left_frame, 0, 0, 1, 1)
        self.right_frame = QtGui.QFrame(self.tab)
        self.right_frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.right_frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.right_frame.setObjectName(_fromUtf8("right_frame"))
        self.gridLayout = QtGui.QGridLayout(self.right_frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(self.right_frame)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_7 = QtGui.QGridLayout(self.frame)
        self.gridLayout_7.setMargin(5)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.camera_container = QtGui.QGridLayout()
        self.camera_container.setObjectName(_fromUtf8("camera_container"))
        self.gridLayout_7.addLayout(self.camera_container, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 4)
        self.frame_3 = QtGui.QFrame(self.right_frame)
        self.frame_3.setFrameShape(QtGui.QFrame.Box)
        self.frame_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout_9 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_9.setMargin(5)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.map_container = QtGui.QGridLayout()
        self.map_container.setObjectName(_fromUtf8("map_container"))
        self.gridLayout_9.addLayout(self.map_container, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 1, 2, 1, 2)
        self.frame_2 = QtGui.QFrame(self.right_frame)
        self.frame_2.setFrameShape(QtGui.QFrame.Box)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_8 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_8.setMargin(5)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.joystick_container = QtGui.QGridLayout()
        self.joystick_container.setObjectName(_fromUtf8("joystick_container"))
        self.gridLayout_8.addLayout(self.joystick_container, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_2, 1, 1, 1, 1)
        self.frame_5 = QtGui.QFrame(self.right_frame)
        self.frame_5.setFrameShape(QtGui.QFrame.Box)
        self.frame_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_5.setObjectName(_fromUtf8("frame_5"))
        self.gridLayout_5 = QtGui.QGridLayout(self.frame_5)
        self.gridLayout_5.setMargin(5)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.stop_container = QtGui.QGridLayout()
        self.stop_container.setObjectName(_fromUtf8("stop_container"))
        self.gridLayout_5.addLayout(self.stop_container, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_5, 2, 1, 1, 3)
        self.frame_4 = QtGui.QFrame(self.right_frame)
        self.frame_4.setFrameShape(QtGui.QFrame.Box)
        self.frame_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.gridLayout_10 = QtGui.QGridLayout(self.frame_4)
        self.gridLayout_10.setMargin(5)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.reading_container = QtGui.QGridLayout()
        self.reading_container.setContentsMargins(0, -1, 0, -1)
        self.reading_container.setObjectName(_fromUtf8("reading_container"))
        self.label_9 = QtGui.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_9.setFont(font)
        self.label_9.setTextFormat(QtCore.Qt.LogText)
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.reading_container.addWidget(self.label_9, 0, 0, 1, 1)
        self.gridLayout_10.addLayout(self.reading_container, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_4, 1, 0, 2, 1)
        self.gridLayout.setRowStretch(0, 4)
        self.gridLayout.setRowStretch(1, 4)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout_2.addWidget(self.right_frame, 0, 1, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 9)
        self.gridLayout_2.setColumnStretch(1, 48)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setMargin(9)
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.map_val = QtGui.QLineEdit(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.map_val.sizePolicy().hasHeightForWidth())
        self.map_val.setSizePolicy(sizePolicy)
        self.map_val.setMaxLength(100)
        self.map_val.setObjectName(_fromUtf8("map_val"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.map_val)
        self.label_2 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_4 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lineEdit_4)
        self.label_3 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_5 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.lineEdit_5)
        self.label_4 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_6 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.lineEdit_6)
        self.label_5 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_5)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(5, QtGui.QFormLayout.SpanningRole, spacerItem)
        self.groupBox = QtGui.QGroupBox(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_7)
        self.map_name = QtGui.QLineEdit(self.groupBox)
        self.map_name.setObjectName(_fromUtf8("map_name"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.map_name)
        self.label_6 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_6)
        self.lat = QtGui.QLineEdit(self.groupBox)
        self.lat.setObjectName(_fromUtf8("lat"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.lat)
        self.generate = QtGui.QPushButton(self.groupBox)
        self.generate.setObjectName(_fromUtf8("generate"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.SpanningRole, self.generate)
        self.label_8 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_8)
        self.lng = QtGui.QLineEdit(self.groupBox)
        self.lng.setObjectName(_fromUtf8("lng"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.lng)
        self.formLayout.setWidget(6, QtGui.QFormLayout.SpanningRole, self.groupBox)
        self.lineEdit_7 = QtGui.QLineEdit(self.tab_2)
        self.lineEdit_7.setObjectName(_fromUtf8("lineEdit_7"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.lineEdit_7)
        self.gridLayout_3.addLayout(self.formLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout_11.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1047, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label_9.setText(_translate("MainWindow", "Sensor Readings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Main", None))
        self.label.setText(_translate("MainWindow", "Default Map", None))
        self.label_2.setText(_translate("MainWindow", "TextLabel", None))
        self.label_3.setText(_translate("MainWindow", "TextLabel", None))
        self.label_4.setText(_translate("MainWindow", "TextLabel", None))
        self.label_5.setText(_translate("MainWindow", "TextLabel", None))
        self.groupBox.setTitle(_translate("MainWindow", "Map Generation", None))
        self.label_7.setText(_translate("MainWindow", "Map Name:", None))
        self.label_6.setText(_translate("MainWindow", "Latitude:", None))
        self.generate.setText(_translate("MainWindow", "Generate New Map", None))
        self.label_8.setText(_translate("MainWindow", "Longitude:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Setings", None))

