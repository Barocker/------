#include <Preferences.h>
Preferences mymem;
TaskHandle_t serialget_task;
TaskHandle_t control_task;
#define LED1 2
#define LED2 4
#define SW1 25
#define SW2 26
#define ADC1 32
#define ADC2 33
int st = 1;
volatile char receive = 0;
void setup() {

  mymem.begin("swst", false);
  st = mymem.getInt("state", 1);
  mymem.end();

  Serial.begin(115200);
  Serial.setTimeout(50);
  xTaskCreatePinnedToCore(serialget, "serialget", 10000, NULL, 1, &serialget_task, 1);
  xTaskCreatePinnedToCore(Control, "control", 10000, NULL, 1, &control_task, 1);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(SW1, INPUT_PULLUP);
  ledcAttachChannel(LED2, 1000, 8, 1);
}

void serialget(void*pvParameter) {
  while (1) {
    if (Serial.available() > 0) {
      receive = Serial.read();
    }
    vTaskDelay(100);
  }
}
void Control(void*pvParameter) {
  while (1) {
    if (receive == 'x') {
      digitalWrite(LED1, HIGH);
    } else if (receive == 'd') {
      digitalWrite(LED1, LOW);
    } else if (receive == 'p') {
      int pwm = Serial.readString().toInt();
      ledcWrite(LED2, pwm);
    } else if (receive == 'x') {
      if (digitalRead(SW1) == 0) {
        st = !st;
        mymem.begin("swst", false);
        mymem.putInt("state", st);
        mymem.end();
      }
      Serial.println(st);
    }

    else if (receive == 'a') {
      int adcval = analogRead(ADC1);
      int adccal = map(adcval, 0, 4095, 0, 1023);
      Serial.println(adccal);
      // Serial.println(receive);
    } else if (receive == 's') {
      int adcval2 = analogRead(ADC2);
      // int adccal2 = map(adcval2, 0, 4095, 0, 1023);
      Serial.println(adcval2);
    }
    receive = 0;
    vTaskDelay(50);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
}