from PyQt5 import QtCore, QtGui, QtWidgets
import sys
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
from LS import Ui_MainWindow
from serial import Serial
from time import sleep
import pyqtgraph as pg
import numpy as np


class myclass(Ui_MainWindow):
    def __init__(self) -> None:
        super().setupUi(MainWindow)
        self.gcn()
    def gcn(self):
        self.PrintBT.clicked.connect(self.func_pmID)
        self.DataBT.clicked.connect(self.func_add_data)
        self.STBT.clicked.connect(self.func_start)


        self.Plus.clicked.connect(self.func_add)
        self.Minus.clicked.connect(self.func_sub)
        self.Multi.clicked.connect(self.func_multi)
        self.Divide.clicked.connect(self.func_divi)
        self.More.clicked.connect(self.func_greater)
        self.Less.clicked.connect(self.func_less)


        self.Num1.setDisabled(1)
        self.Num2.setDisabled(1)


        self.Plus.setDisabled(1)
        self.Minus.setDisabled(1)
        self.Multi.setDisabled(1)
        self.Divide.setDisabled(1)
        self.More.setDisabled(1)
        self.Less.setDisabled(1)


        self.Num1.textChanged.connect(self.cal)
        self.Num2.textChanged.connect(self.cal)


    def func_pmID(self):
        print("My ID is B6617769")
   
    def func_add_data(self):
        id = self.EnterID.text()
        name = self.EnterName.toPlainText()
        surename = self.EnterSure.toPlainText()
        print("You add data: %s %s %s to Database.....!!"%(id,name,surename))


    def func_start(self):
        self.Num1.setEnabled(1)
        self.Num2.setEnabled(1)


        self.Plus.setEnabled(1)
        self.Minus.setEnabled(1)
        self.Multi.setEnabled(1)
        self.Divide.setEnabled(1)
        self.More.setEnabled(1)
        self.Less.setEnabled(1)
   
    def func_add(self):
        self.OPLABEL.setText("+")
        self.operator = "+"
        self.cal()
    def func_sub(self):
        self.OPLABEL.setText("-")
        self.operator = "-"
        self.cal()
    def func_multi(self):
        self.OPLABEL.setText("x")
        self.operator = "x"
        self.cal()
    def func_divi(self):
        self.OPLABEL.setText("÷")
        self.operator = "÷"
        self.cal()
    def func_greater(self):
        self.OPLABEL.setText(">")
        self.operator = ">"
        self.cal()
    def func_less(self):
        self.OPLABEL.setText("<")
        self.operator = "<"
        self.cal()


    def cal(self):
        try:
            self.t1 = float(self.Num1.text())
            self.t2 = float(self.Num2.text())
       
            if(self.operator == "+"):
                self.ans = self.t1+self.t2
                self.ANS.setText(str(self.ans))


            elif(self.operator == "-"):
                self.ans = self.t1-self.t2
                self.ANS.setText(str(self.ans))


            elif(self.operator == "x"):
                self.ans = self.t1*self.t2
                self.ANS.setText(str(self.ans))


            elif(self.operator == "÷"):
                self.ans = round(self.t1/self.t2,3)
                self.ANS.setText(str(self.ans))
           
            elif(self.operator == ">"):
                self.ans = self.t1 > self.t2
                self.ANS.setText(str(self.ans))


            elif(self.operator == "<"):
                self.ans = self.t1 < self.t2
                self.ANS.setText(str(self.ans))
               
        except(ZeroDivisionError,ValueError):
            self.ANS.setText("N/A")
            # print("Somting worning")
            pass




if __name__ == "__main__":
    myob = myclass()
    MainWindow.show()
    sys.exit(app.exec_())
