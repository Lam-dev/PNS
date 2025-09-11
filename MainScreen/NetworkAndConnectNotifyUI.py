# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CacThongBaoKetNoi.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(320, 51)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_intensity = QtWidgets.QLabel(Frame)
        self.label_intensity.setGeometry(QtCore.QRect(6, 4, 40, 40))
        self.label_intensity.setStyleSheet("")
        self.label_intensity.setText("")
        self.label_intensity.setPixmap(QtGui.QPixmap("../../icon/wait40.gif"))
        self.label_intensity.setObjectName("label_intensity")
        self.label_network = QtWidgets.QLabel(Frame)
        self.label_network.setGeometry(QtCore.QRect(62, 4, 43, 25))
        self.label_network.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 57 bold 14pt \"Ubuntu\";")
        self.label_network.setObjectName("label_network")
        self.label_spn = QtWidgets.QLabel(Frame)
        self.label_spn.setGeometry(QtCore.QRect(62, 28, 113, 25))
        self.label_spn.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 40 bold 10pt \"Arial\";")
        self.label_spn.setObjectName("label_spn")
        self.label_internetStatus = QtWidgets.QLabel(Frame)
        self.label_internetStatus.setGeometry(QtCore.QRect(106, 2, 25, 25))
        self.label_internetStatus.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 57 bold 14pt \"Ubuntu\";")
        self.label_internetStatus.setText("")
        self.label_internetStatus.setPixmap(QtGui.QPixmap("../../icon/warning25.png"))
        self.label_internetStatus.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_internetStatus.setObjectName("label_internetStatus")
        self.label_serverStatus = QtWidgets.QLabel(Frame)
        self.label_serverStatus.setGeometry(QtCore.QRect(258, 2, 21, 21))
        self.label_serverStatus.setStyleSheet("background-color: rgb(150, 150, 150);\n"
"border-radius:10px")
        self.label_serverStatus.setText("")
        self.label_serverStatus.setObjectName("label_serverStatus")
        self.label_5 = QtWidgets.QLabel(Frame)
        self.label_5.setGeometry(QtCore.QRect(240, 28, 60, 20))
        self.label_5.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 57 bold 11pt \"Arial\";")
        self.label_5.setObjectName("label_5")
        self.label_gpsStatus = QtWidgets.QLabel(Frame)
        self.label_gpsStatus.setGeometry(QtCore.QRect(194, 2, 21, 21))
        self.label_gpsStatus.setStyleSheet("background-color: rgb(150, 150, 150);\n"
"border-radius:10px")
        self.label_gpsStatus.setText("")
        self.label_gpsStatus.setObjectName("label_gpsStatus")
        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(178, 28, 61, 20))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 57 bold 11pt \"Arial\";")
        self.label.setObjectName("label")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label_network.setText(_translate("Frame", "LTE"))
        self.label_spn.setText(_translate("Frame", "vinaphone"))
        self.label_5.setText(_translate("Frame", "Máy chủ"))
        self.label.setText(_translate("Frame", "Định vị"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
