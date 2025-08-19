from tkgpio import TkCircuit
import serial
import sys

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


check = True


configuration = {
    "width": 500,
    "height": 200,
    "leds": [
        {"x": 50, "y": 40, "name": "Fan", "pin": 21},
        {"x": 100, "y": 40, "name": "Motor", "pin": 22},
        {"x": 150, "y": 40, "name": "SWCT", "pin": 23},
        {"x": 200, "y": 40, "name": "Status", "pin": 24},
    ],
    "buttons": [
        {"x": 50, "y": 130, "name": "Start", "pin": 1},
        {"x": 100, "y": 130, "name": "Reset", "pin": 2},
        {"x": 150, "y": 130, "name": "EMO", "pin": 3},
    ],
    "lcds": [
        {
            "x": 200,
            "y": 110,
            "name": "LCD16x2",
            "pins": [2, 3, 4, 5, 6, 7],
            "columns": 16,
            "lines": 2,
        },
    ],
}

circuit = TkCircuit(configuration)


@circuit.run
def main():
    def pressstartfun():
        led1.toggle()
        if led1.is_active:
            ser.write(b"c")
            lcd.clear()
            lcd.message("B6617769 FAN ON\nChaiyapat P.")
        elif not led1.is_active:
            ser.write(b"d")
            lcd.clear()
            lcd.message("B6617769 FAN OFF\nChaiyapat P.")

    def pwm():
        ser.write(b"a")
        adc = ser.readline().decode().strip()
        led2.value = float(adc) / 1023.0

    def ledtoggle():
        ser.write(b"x")
        swstatus = ser.readline().decode().strip()
        if swstatus == "1":
            led3.on()
        elif swstatus == "0":
            led3.off()

    def emotoggle():
        sleep(0.3)
        ser.write(b"d")
        led1.blink(0.2, 0.2)
        led2.blink(0.2, 0.2)
        led3.blink(0.2, 0.2)
        led4.blink(0.2, 0.2)
        lcd.clear()
        lcd.message("Warning!\nWarning!")
        global check
        check = False

    def reset():
        global check
        check = False
        led1.off()
        led2.off()
        led3.off()
        led4.blink(0.2, 0.2)
        sleep(4)
        led4.off()
        lcd.clear()
        lcd.message("Hello\nEmbedded System")

    from gpiozero import LED, Button, PWMLED
    from time import sleep
    from Adafruit_CharLCD import Adafruit_CharLCD

    sw1 = Button(1)
    sw2 = Button(2, hold_time=3)
    sw3 = Button(3)

    led1 = LED(21)
    led2 = PWMLED(22)
    led3 = LED(23)
    led4 = LED(24)

    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    lcd.clear()
    lcd.message("Hello\nEmbedded System")

    sw1.when_pressed = pressstartfun
    sw2.when_held = reset
    sw3.when_pressed = emotoggle

    while True:
        if check == True:
            pwm()
            ledtoggle()
        elif check == False:
            pass
        sleep(0.5)