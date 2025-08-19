from PyQt5 import QtCore, QtGui, QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
from B6617769 import Ui_MainWindow
import serial
import pyqtgraph as pg
from time import sleep, ctime
import numpy as np

ser = serial.Serial(
    port="COM3",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    xonxoff=False,
    rtscts=True,
    dsrdtr=True,
)

while not ser.isOpen():
    try:
        ser.open()
        ser.flush()
    except Exception as e:
        print(f"Error Open port {ser.portstr} with -> {e}")
        sys.exit(True)
print(f"Connect to {ser.portstr} Success !")


class myclass(Ui_MainWindow):
    def __init__(self):
        super().setupUi(MainWindow)
        self.gcn()
        self.timer()
        self.graphinit()
        
    def graphinit(self):
        self.mygraph = pg.PlotWidget(self.centralwidget)
        self.mygraph.setGeometry(QtCore.QRect(370, 380, 681, 331))
        self.mygraph.setYRange(0, 4095)

    # สร้างเส้นกราฟ 2 เส้น
        self.graph1 = self.mygraph.plot(pen='r')  # เส้น ADC33
        self.graph2 = self.mygraph.plot(pen='b')  # เส้น Volt33

  
        self.x = np.arange(20)
        self.y1 = np.zeros(20)  # ADC33
        self.y2 = np.zeros(20)  # Volt33


    def timer(self):
        self.tm1 = QtCore.QTimer()
        self.tm1.timeout.connect(self.autoread)
        self.tm1.setInterval(500)
        self.tm1.start()

        self.tm2 = QtCore.QTimer()
        self.tm2.timeout.connect(self.sw)
        self.tm2.setInterval(200)
        self.tm2.start()

        self.tm3 = QtCore.QTimer()
        self.tm3.timeout.connect(self.adc33)
        self.tm3.setInterval(1000)
        self.tm3.start()
        
        self.tm4 = QtCore.QTimer()
        self.tm4.timeout.connect(self.toggle_led)
        self.tm4.setInterval(1000)
        self.led_state = False  # เก็บสถานะ LED2

    def gcn(self):
        self.start.clicked.connect(self.st_func)
        self.stop.clicked.connect(self.sp_func)
        self.slider.sliderReleased.connect(self.sl_func)

    def st_func(self):
        self.tm4.stop()
        self.led_state = 1
        self.status.setText("START")
        self.status.setStyleSheet("background-color: rgb(0, 255, 0);")
        ser.write("c".encode())
        self.start.setDisabled(True)
        self.slider.setDisabled(True)
        self.stop.setDisabled(False)
        self.tm1.stop()
        self.tm2.stop()
        self.tm3.stop()
        self.pwmval = self.slider.value()
        ser.write(("p" + str((self.pwmval))).encode())
        self.percent = int((self.pwmval / 255) * 100)
        self.pwm.setNum(self.percent)
        sleep(0.1)
        self.tm1.start()
        self.tm2.start()
        self.tm3.start()
   

    def sp_func(self):
        self.status.setText("STOP")
        self.status.setStyleSheet("background-color: rgb(255, 0, 0);")
        ser.write("d".encode())
        self.stop.setDisabled(True)
        self.start.setDisabled(False)
        self.slider.setDisabled(False)
        self.tm4.start()
        
    def toggle_led(self):
        self.tm1.stop()
        self.tm2.stop()
        self.tm3.stop()
        self.led_state = not self.led_state
        if self.led_state:
            ser.write(b"p0")     # เปิด LED2
            sleep(1)
        else:
            ser.write(b"p255")   # ปิด LED2
            sleep(1)
        self.tm1.start()
        self.tm2.start()
        self.tm3.start()
            
    def sl_func(self):
        self.tm1.stop()
        self.tm2.stop()
        self.tm3.stop()
        self.pwmval = self.slider.value()
        ser.write(("p" + str((self.pwmval))).encode())
        self.percent = int((self.pwmval / 255) * 100)
        self.pwm.setNum(self.percent)
        sleep(0.1)
        self.tm1.start()
        self.tm2.start()
        self.tm3.start()

    def autoread(self):
        ser.write("a".encode())
        sleep(0.1)
        self.dataADC32 = ser.readline().decode().strip()
        self.adc32.setText(self.dataADC32)
        self.volt = round((float(self.dataADC32) / 1023) * 3.3, 2)
        self.volt32.setNum(self.volt)

    def sw(self):
        ser.write("x".encode())
        self.data_sw = ser.readline().decode().strip()
        # print(self.data_sw)
        if self.data_sw == "1":
            self.read_sw.setText("ON")
        elif self.data_sw == "0":
            self.read_sw.setText("OFF")

    def adc33(self):
        ser.write('s'.encode())
        raw_data = ser.readline().decode().strip()

        if raw_data.isdigit():
            adc_val = int(raw_data)
            volt_val = round((adc_val / 4095) * 3.3, 2)

        # แสดงใน text box
            self.plainTextEdit.appendPlainText(
                f"{ctime()}: ADC33 = {adc_val}, Volt33 = {volt_val}"
        )

        # เลื่อนข้อมูลเก่าออกแล้วเพิ่มข้อมูลใหม่
            self.x = np.append(self.x[1:], self.x[-1] + 1)
            self.y1 = np.append(self.y1[1:], adc_val)
            self.y2 = np.append(self.y2[1:], volt_val)

        # อัปเดตกราฟ
            self.graph1.setData(self.x, self.y1)
            self.graph2.setData(self.x, self.y2)
      

if __name__ == "__main__":
    myob = myclass()
    MainWindow.show()
    sys.exit(app.exec_())