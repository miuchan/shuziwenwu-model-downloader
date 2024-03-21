# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'form.ui'
#
# Created by: Qt User Interface Compiler version 6.6.2
#
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QRect,
)
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
)


class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName("Widget")
        Widget.resize(600, 200)
        self.pushButton = QPushButton(Widget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(QRect(250, 130, 100, 30))
        self.lineEdit = QLineEdit(Widget)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setGeometry(QRect(82, 50, 481, 31))
        self.label = QLabel(Widget)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(30, 50, 51, 31))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)

    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(
            QCoreApplication.translate("Widget", "Widget", None)
        )
        self.pushButton.setText(
            QCoreApplication.translate("Widget", "\u4e0b\u8f7d", None)
        )
        self.label.setText(
            QCoreApplication.translate(
                "Widget", "\u6a21\u578b\u7f51\u5740", None
            )
        )

    # retranslateUi
