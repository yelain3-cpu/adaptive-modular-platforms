#include <Servo.h>  // 引用随机功能库头文件,控制PWM电子开关用
Servo C, X, P;      // C 充气电子阀插D5; X 吸气电子阀插D6; P 真空泵插D8;

int air_delay = 0;
float timer = 0;
float amount = 0;

void setup() {

  Serial.begin(115200);

  pinMode(LED_BUILTIN, OUTPUT);    // 板子上电会先运行1次这里的代码,进行初始化
  digitalWrite(LED_BUILTIN, LOW);  // 设置开发板板载LED信号灯GPIO为输出
  C.attach(5, 500, 2500);
  C.write(0);  // 呼气充气电磁阀插D5针脚,0断电,端与金属端相通
  X.attach(7, 500, 2500);
  X.write(0);  // 吸气放气电磁阀插D6针脚,0断电,端与金属端相通
  P.attach(3, 500, 2500);
  P.write(0);  // 真空泵插D8针脚,0断电,建议5V1a+手机充电头或电脑USB3.0

  int fsr = 0;
  pinMode(A0, INPUT);
  Serial.begin(9600);
  C.write(0);
  X.write(180);
  delay(10000);
  C.write(180);
  X.write(0);
  P.write(180);
  delay(10000);
}



void loop() {

  if (Serial.available()) {
    air_delay = Serial.read();
  }

  int fsr = analogRead(A0);
  Serial.println(fsr);

  if (fsr > 300 && timer <= 200) {

    pump(1, air_delay);
    timer++;
    amount++;
  }

  if (fsr > 300 && timer >= 200) {
    pump(2, air_delay);
  }

  if (fsr < 300 && amount > 0) {
    pump(0, 10);
    amount--;
    if (amount == 0) {
      timer = 0;
    }
  }

  if (fsr < 300 && amount == 0) {
    pump(2, 10);
  }

  //   if (timer <= 10000) {
  //     pump(2, air_delay);
  //   } else if (timer > 10000) {
  //     pump(0, air_delay);
  //   }


  delay(10);  // Delay a little bit to improve simulation performance
}

void pump(int cmd, int tDelay) {
  switch (cmd) {
    case 0:           //放气
      C.write(0);     // 呼气充气阀0断电,端与金属端气球相通,侧端封闭
      X.write(180);   // 吸气放气阀180上电,端与金属端气球相通,与金属端气球封闭
      P.write(180);   // 真空泵180上电运行,系的侧孔吸气,顶孔出气
      delay(tDelay);  // 延时2.0秒等待吸气放气
      //timer -= tDelay * 1.9;
      break;

    case 1:           //吹气
      C.write(255);   // 呼气充气阀180上电,端与金属端相通,与金属端气球封闭
      X.write(0);     // 吸气放气阀0断电,端与金属端气球相通,侧端封闭
      P.write(255);   // 真空泵180上电运行,系的侧孔吸气,顶孔出气
      delay(tDelay);  // 延时2.0秒等待吸气放气
      //timer += tDelay;
      break;

    case 2:           //不动
      C.write(0);     // 呼气充气阀0断电,端与金属端气球相通,侧端封闭
      X.write(0);     // 吸气放气阀0断电,端与金属端气球相通,侧端封闭
      P.write(0);     // 真空泵0断电,系的侧孔封闭,顶孔封闭
      delay(tDelay);  // 延时2.0秒等待吸气放气
      break;
  }
}