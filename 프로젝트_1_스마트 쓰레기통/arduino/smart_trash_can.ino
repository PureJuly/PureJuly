#include <Servo.h>
#include "HUSKYLENS.h"
#include "Wire.h"
#include <SoftwareSerial.h>
#include <SPI.h>
#include <MFRC522.h>

#define BT_RXD A0
#define BT_TXD 8

#define RST_PIN 9 
#define SS_PIN 10 


HUSKYLENS huskylens;
// const int common_LED = 0;
// const int buzzerPin = 1; 

SoftwareSerial bluetooth(BT_RXD, BT_TXD);
MFRC522 rfid(SS_PIN, RST_PIN);

char btInput[15];
byte btCount = 0;
bool huskyConnected = false;
char currentUserUID[15] = {0};
const char hex_chars[] = "0123456789ABCDEF"; 

bool isSystemActive = false;
bool isWatingMsg = false;
unsigned long lastActivityTime = 0;
const unsigned long System_timeout = 10000; // 10초동안 활성화 유지


unsigned long lastDetected = 0;
int detectedBin = 0;
const unsigned long detectThreshold = 500;

class SmartBin {
  private:
    String binName;
    int servoPin;
    int wavePin;
    int echoPin;

    Servo lidServo;
    bool isOpen;
    bool isFull;
    unsigned long openTime;

    bool isDetectingFull;
    unsigned long fullStartTime;
    bool isDetectingEmpty;
    unsigned long emptyStartTime;

    const double Full_distance = 3.5;
    const double Empty_distance = 6.0;
    const int Open_timer = 3000;
    const int State_timer = 3000;

  public:
    SmartBin(String name, int spin, int wpin, int epin) {
      binName = name;
      servoPin = spin;
      wavePin = wpin;
      echoPin = epin;
      isOpen = false;
      isFull = false;
      isDetectingFull = false;
      fullStartTime = 0;
      isDetectingEmpty = false;
      emptyStartTime = 0;
    }
  
  void init() {
    pinMode(wavePin, OUTPUT);
    pinMode(echoPin, INPUT);
    lidServo.attach(servoPin);
    lidServo.write(0); // 뚜껑 초기 각도
  }

  void openLid() {
    if (!isOpen) {
      if(isFull) {
        Serial.println("[" + binName + "] 통이 꽉 찼습니다.");
        for (int i=0; i<3; i++) {
          // digitalWrite(common_LED, LOW);
          delay(100);
          // digitalWrite(common_LED, HIGH);
          delay(100);
        }
      }
      lidServo.write(90); // 뚜껑 open 각도
      isOpen = true;
      Serial.println("[" + binName + "] 뚜껑이 열렸습니다.");
    }
    openTime = millis();
  }

  void closeLid() {
    if (isOpen && (millis() - openTime >= Open_timer)) {
      lidServo.write(0); // 뚜껑 다시 닫기
      isOpen = false;
      Serial.println("[" + binName + "] 뚜껑이 닫혔습니다.");
    }
    check_state();
  }

  void check_state() {
    long duration;
    double distance;
    digitalWrite(wavePin, LOW);
    delayMicroseconds(2);
    digitalWrite(wavePin, HIGH);
    delayMicroseconds(10);
    digitalWrite(wavePin, LOW);

    duration = pulseIn(echoPin, HIGH, 5000); //50ms 타임 아웃(정지 방지)
    if (duration == 0) return; // 센서 오류 or 범위 초과 시 무시

    distance = (double)duration * 0.034/2; // cm단위로 거리 계산

    // 꽉 참(Full) 감지
    if (distance > 0 && distance <= Full_distance) {
      isDetectingEmpty = false;
      
      if (!isDetectingFull) {
        isDetectingFull = true;
        fullStartTime = millis();
      } else {
        if (!isFull && (millis() - fullStartTime >= State_timer)) {
          isFull = true;
          Serial.println("[" + binName + "]이(가) 꽉참");
          bluetooth.print(F("full+"));
          bluetooth.println(binName);
        }
      }
    } 
    // 비워짐(Empty) 감지 로직
    else if (distance >= Empty_distance) {
      isDetectingFull = false;
      
      if (!isDetectingEmpty) {
        isDetectingEmpty = true;
        emptyStartTime = millis();
      } else {
        if (isFull && (millis() - emptyStartTime >= State_timer)) {
          isFull = false;
          Serial.println("[" + binName + "]이(가) 비워짐");
          bluetooth.print(F("empty+"));
          bluetooth.println(binName);
        }
      }
    } 
    // 버퍼 구간 로직
    else {
      // 버퍼 구간이므로 두 타이머를 모두 초기화하여 현재 상태 유지
      isDetectingFull = false;
      isDetectingEmpty = false;
    }
  }
  String getName() { return binName; }
  bool getIsFull() { return isFull; }
};

void activateSystem() {
  isSystemActive = true;
  lastActivityTime = millis();
  Serial.println("카드키 인증 완료. 카메라 활성화");
}

void deactivateSystem() {
  isSystemActive = false;
  
  currentUserUID[0] = '\0'; // char 배열 초기화
  Serial.println("카메라 비활성화");
}

void resetSystemTime() {
  if (isSystemActive) {
    lastActivityTime = millis();
  }
}

void checkCameraTimeout() {
  if (isSystemActive && (millis() - lastActivityTime >= System_timeout)) {
    bluetooth.println(F("close+auto"));
    deactivateSystem();
  }
}

SmartBin binPlastic("plastic", A1, 2, 3);
SmartBin binPaper("paper", A2, 4, 5);
SmartBin binGeneral("general", A3, 6, 7);

void setup() {
  Serial.begin(9600);

  // pinMode(common_LED, OUTPUT);
  // digitalWrite(common_LED, LOW);
  bluetooth.begin(9600);
  Wire.begin();
  SPI.begin();      
  rfid.PCD_Init();
  huskylens.begin(Wire);

  binPlastic.init();
  binPaper.init();
  binGeneral.init();

  // 카메라 연동
  Wire.begin();
  while (!huskylens.begin(Wire)) {
    Serial.println("카메라 연결 실패");
    delay(100);
  }
  Serial.println(" ==== 시스템 시작 ==== ");
}

void loop() {
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    char scannedUID[15] = {0}; // 읽어온 UID를 임시 저장할 배열
    byte idx = 0;

    for (byte i = 0; i < rfid.uid.size; i++) 
    {
      // if (i > 0) scannedUID[idx++] = ' '; // 중간에 공백 추가
      scannedUID[idx++] = hex_chars[rfid.uid.uidByte[i] >> 4];   // 앞자리
      scannedUID[idx++] = hex_chars[rfid.uid.uidByte[i] & 0x0F]; // 뒷자리
    }
    scannedUID[idx] = '\0'; // 문자열 마무리

    Serial.print(F("\n[태그 인식됨] UID: "));
    Serial.println(scannedUID);

    if (isSystemActive) 
    {
      Serial.println(F("뚜껑을 닫고 최종 데이터를 서버로 전송합니다."));

      bluetooth.print(F("close+"));
      bluetooth.println(currentUserUID);

      // tone(buzzerPin, 400, 200);

      // 상태 초기화
      deactivateSystem();
      // isLidOpen = false;
    }
    else 
    {
      // Serial.println(F("[서버로 인증 요청(UID) 전송]"));
      bluetooth.print(F("open+"));
      bluetooth.println(scannedUID);

      // String 대신 strcpy로 안전하게 복사
      strcpy(currentUserUID, scannedUID);
    }

    // 카드 읽기 중지
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }

  while (bluetooth.available() > 0) {
    char c = bluetooth.read();
    
    if (c == '\n' || c == '\r') 
    {
      if (btCount > 0) 
      {
        btInput[btCount] = '\0'; 
        Serial.print(F("\n[서버 응답 수신]: "));
        Serial.println(btInput);

        if (strcmp(btInput, "ok") == 0) 
        {
          Serial.println(F("인증 성공! 뚜껑을 엽니다."));
          // successMelody();

          // isLidOpen = true;
          isSystemActive = true;
          // 💡 서보모터 열기 코드 작성
        } 
        else if (strcmp(btInput, "rejected") == 0) 
        {
          Serial.println(F("인증 실패!"));
          // failMelody();
          currentUserUID[0] = '\0'; // 인증 실패 시 임시 UID 삭제
        }

        btCount = 0;
        memset(btInput, 0, sizeof(btInput)); 
      }
    }
    else 
    {
      if (btCount < 14) 
      {
        btInput[btCount] = c;
        btCount++;
      }
    }
  }

  if (isSystemActive) { // 시스템이 활성화되고
    if (huskylens.request() && huskylens.available()) { // 카메라와 통신이 성공하면
      HUSKYLENSResult result = huskylens.read(); // 인식 결과 가져오기
      if (result.command == COMMAND_RETURN_BLOCK) {
        // 1 : 플라스틱, 2 : 종이, 3 : 일반 쓰레기
        // if (result.ID == 1) {
        // binPlastic.openLid();
        //   resetSystemTime();
        // } else if (result.ID == 2) {
        //   binPaper.openLid();
        //   resetSystemTime();
        // } else if (result.ID == 3) {
        //   binGeneral.openLid();
        //   resetSystemTime();
        // }

        if (result.ID != detectedBin) {
          lastDetected = millis();
          detectedBin = result.ID;
        } else if (millis()-lastDetected >= detectThreshold) {
          if (result.ID == 1) {
          binPlastic.openLid();
            resetSystemTime();
          } else if (result.ID == 2) {
            binPaper.openLid();
            resetSystemTime();
          } else if (result.ID == 3) {
            binGeneral.openLid();
            resetSystemTime();
          }

          lastDetected = millis();
        }
      }
    }
  }
  checkCameraTimeout();
  
  binPlastic.closeLid();
  binPaper.closeLid();
  binGeneral.closeLid();

  // if (binPlastic.getIsFull() || binPaper.getIsFull() || binGeneral.getIsFull()) {
  //   digitalWrite(common_LED, HIGH);
  // } else {
  //   digitalWrite(common_LED, LOW);
  // }

  delay(300);
}