# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainScreen.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(800, 480)
        self.frame_networkAndConnectNotify = QtWidgets.QFrame(Frame)
        self.frame_networkAndConnectNotify.setGeometry(QtCore.QRect(2, 426, 320, 51))
        self.frame_networkAndConnectNotify.setStyleSheet("border-style:solid;\n"
"border-width:0px;\n"
"background-color: rgb(44, 0, 255);")
        self.frame_networkAndConnectNotify.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_networkAndConnectNotify.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_networkAndConnectNotify.setObjectName("frame_networkAndConnectNotify")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
