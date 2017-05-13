# -*- coding: utf-8 -*-

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from PyQt4.QtGui import QColor

class MyTable(QtGui.QTableWidget):
    def __init__(self, data, tableItemChangedCallback,tableItemSelectedCallback,*args):
        QtGui.QTableWidget.__init__(self, *args)
        self.tableItemChangedCallback = tableItemChangedCallback
        self.tableItemSelectedCallback = tableItemSelectedCallback
        self.verticalHeader().setDefaultSectionSize(10)
        self.setAutoFillBackground(True)

        self.data = data
        self.setmydata()
        self.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
        self.horizontalHeader().setStretchLastSection(True)
        

    def setmydata(self):
        horHeaders = []
        for y, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for x, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
               # newitem.setBackground(QtGui.QColor(255,255,255))
                self.setItem(x, y, newitem)
               
        self.setHorizontalHeaderLabels(horHeaders)
        


    def create_bilingual_table(self,data):
        
        data["unmodified_target"] = data["target"]
        for key in data.keys():
            if key == "source": y = 0
            if key == "unmodified_target": y = 1
            if key == "target": y = 2
            
            for x, item in enumerate(data[key]):
                
                tableItem = QtGui.QTextEdit()
                tableItem.setText(item)
                tableItem.setMaximumHeight(50) # SHOULD BE DINAMICALLY ADJUSTED
                if key != "target": tableItem.setReadOnly(True)
                tableItem.mousePressEvent =  (lambda event= tableItem, tableItem= tableItem,x=x, y=y: self.tableItemSelectedCallback(event, tableItem,x,y))
                tableItem.textChanged.connect(lambda tableItem= tableItem,x=x, y=y: self.tableItemChangedCallback(tableItem,x,y))
                self.setCellWidget(x,y, tableItem)
                self.resizeRowsToContents()
        self.setColumnHidden(1, True)
        self.setHorizontalHeaderLabels(QtCore.QString("Source/MT;Post-edited;Post-edited;").split(";"))
        self.setTextElideMode(QtCore.Qt.ElideNone)#P
        self.resizeColumnsToContents()#P
        self.resizeRowsToContents()#P
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)#P 

    def create_monolingual_table(self,data):
      
        for y in range (0,2):
            if y == 0: key = "source"
            if y == 1: key = "target"
            
            for x, item in enumerate(data["target"]):               
                tableItem = QtGui.QTextEdit()
                tableItem.setText(item)
                tableItem.setMaximumHeight(50) # SHOULD BE DINAMICALLY ADJUSTED
                if y == 0: tableItem.setReadOnly(True)
                tableItem.mousePressEvent =  (lambda event= tableItem, tableItem= tableItem,x=x, y=y: self.tableItemSelectedCallback(event, tableItem,x,y))
                tableItem.textChanged.connect(lambda tableItem= tableItem,x=x, y=y: self.tableItemChangedCallback(tableItem,x,y))
                self.setCellWidget(x,y, tableItem)
        self.setHorizontalHeaderLabels(QtCore.QString("Source/MT;Post-edited;").split(";"))
        self.setTextElideMode(QtCore.Qt.ElideNone)#P
        self.resizeColumnsToContents()#P
        self.resizeRowsToContents()#P
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)#P  


    def set_post_editing_table_data(self, data, bilingual = False):
        self.clear()
        if bilingual: 
            self.create_bilingual_table(data)
        else: 
            self.create_monolingual_table(data)
        self.resizeColumnsToContents() 
        self.setColumnHidden(2, not bilingual)
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
        self.resizeRowsToContents()

    def set_differences_table_data(self, data):
        horHeaders = []
        for key in data.keys():
            if key == "source": y = 0
            if key == "target": y = 1
            horHeaders.insert(y,key)
            for x, item in enumerate(data[key]):                
                tableItem = QtGui.QTextEdit()
                tableItem.setText(item)
                tableItem.setMaximumHeight(50) # SHOULD BE DINAMICALLY ADJUSTED
                if key != "target": tableItem.setReadOnly(True)
                tableItem.mousePressEvent =  (lambda event= tableItem, tableItem= tableItem,x=x, y=y: self.tableItemSelectedCallback(event, tableItem,x,y))
                tableItem.textChanged.connect(lambda tableItem= tableItem,x=x, y=y: self.tableItemChangedCallback(tableItem,x,y))
                self.setCellWidget(x,y, tableItem)
        self.setHorizontalHeaderLabels(horHeaders)
        self.setTextElideMode(QtCore.Qt.ElideNone)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)