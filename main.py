#!/usr/bin/python3
# encoding: utf-8

import sys
import os
from PySide2.QtWidgets import QWidget, QDialog, QApplication, QPushButton, QLineEdit, QFileDialog

from PySide2 import QtUiTools
from qet_gen_element import ElementCreate


class AppWindow( ):
    def __init__(self):
        super().__init__()
        self.type_element = 1
        self.dirname = os.path.dirname(os.path.abspath(__file__))

        self.ui = QtUiTools.QUiLoader().load("{}/qet_gen_element.ui".format(self.dirname))

        self.ui.bt_create.clicked.connect(self.creat)
        self.ui.bt_open.clicked.connect(self.openbox)

        self.ui.rdB_type1.clicked.connect(self.define_element_type)
        self.ui.rdB_type2.clicked.connect(self.define_element_type)
        self.ui.rdB_type3.clicked.connect(self.define_element_type)
        self.ui.rdB_type4.clicked.connect(self.define_element_type)
        self.ui.rdB_type5.clicked.connect(self.define_element_type)
        self.ui.rdB_type6.clicked.connect(self.define_element_type)

        self.ui.le_directory.setText(self.dirname)

        self.ui.show()

    def creat(self):
        name_element = self.ui.le_name_element.text()
        pin_name = self.ui.le_pin_name.text()
        pin_sheet = self.ui.spB_pin_sheet.value()
        step = self.ui.spb_step.value()

        ds = ElementCreate(element_name=name_element, list_pin_name=pin_name, pin_to_list=pin_sheet,
                           step=step, type_draw=self.type_element, file_path=self.dirname)
        ds.main()
        print([name_element, pin_name, pin_sheet, step, self.type_element])

    def define_element_type(self):
        if self.ui.rdB_type1.isChecked():
            self.type_element = 1
        if self.ui.rdB_type2.isChecked():
            self.type_element = 2
        if self.ui.rdB_type3.isChecked():
            self.type_element = 3
        if self.ui.rdB_type4.isChecked():
            self.type_element = 4
        if self.ui.rdB_type5.isChecked():
            self.type_element = 5
        if self.ui.rdB_type6.isChecked():
            self.type_element = 6
        
        
        
        print('type_element: ' + str(self.type_element))

    def openbox(self):
        directory = QFileDialog().getExistingDirectory()
        if not directory or len(directory) == 0 or not os.path.exists(directory):
            return
        self.ui.bt_open.setVisible(False)
        self.ui.bt_open.setVisible(True)
        #filename = os.path.basename(self.link())
        #self.dirname = os.path.join(directory)
        self.dirname = directory
        self.ui.le_directory.setText(self.dirname)

        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    print(os.path.dirname(os.path.abspath(__file__)))
    w = AppWindow()
    sys.exit(app.exec_())
