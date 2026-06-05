# 개요

자율주행로봇 필드엔지니어 직무에 지원하기 위해 만든 포트폴리오입니다.

처음부터 거창하게 잘 만든 프로젝트만 보여주기보다는, 제가 프로젝트를 진행하면서 어떤 부분을 맡았고 문제를 어떻게 확인했는지 정리하려고 했습니다. 아직 부족한 부분도 있지만, 현장에서 장비 상태를 확인하고 필요한 내용을 기록해서 전달하는 일을 해보고 싶다는 방향을 담았습니다.

포트폴리오 주소: https://purejuly.github.io/PureJuly/

PDF 파일: `안효민_포트폴리오.pdf`

## 프로젝트

### 1. 스마트 분리수거 쓰레기통

객체 인식으로 쓰레기 종류를 확인하고, RFID 인증 후 알맞은 쓰레기통을 여는 프로젝트입니다.

제가 맡은 부분은 아래와 같습니다.

- HuskyLens 객체 인식 학습
- RFID 태그 UID 확인 흐름 구성
- Arduino와 Raspberry Pi 간 블루투스 통신 연결
- SQLite DB와 웹 대시보드 연동
- 기능 통합 과정에서 디버깅

상세 페이지: `project-smart-bin.html`

### 2. 공기질 연동 자율주행 공기청정 로봇

미세먼지 센서로 공기질을 확인하고, 자율주행 로봇이 오염 구역으로 이동하는 프로젝트입니다.

이 프로젝트에서는 개발 전체를 맡았다기보다 하드웨어 쪽 확인과 통합 테스트 과정에 더 많이 참여했습니다.

- Arduino, ESP-01, PMS7003 센서 모듈 조립
- 전원부와 배선 상태 확인
- 통합 테스트 중 하드웨어 동작 상태 점검
- 시연 전 문제 상황 확인
- 프로젝트 시연 영상 제작

상세 페이지: `project-air-robot.html`

## 역량

기술과 도구

- 리눅스
- Git
- 네트워크
- 로그 확인

기타

- 문서 작성
- MS 오피스
- 고객 대응
- 운전 가능

## 파일 구조

```text
PureJuly/
├── images/
│   ├── profile.jpg
│   ├── project-1.jpg
│   └── project-2.jpg
│
├── 프로젝트_1_스마트 쓰레기통/
│   ├── arduino/
│   │   └── smart_trash_can.ino
│   │
│   └── python backend/
│       ├── templates/
│       │   ├── base.html
│       │   ├── login.html
│       │   ├── logs.html
│       │   ├── main.html
│       │   └── manage_user.html
│       │
│       ├── connector.py
│       ├── dashboard_server.py
│       ├── db_server.py
│       ├── session.db
│       └── trashbin.db
│
├── 프로젝트_3_군집 자율주행 피킹로봇/
│   ├── RobotArmCase.ino
│   ├── RobotArm_MQTT 통신.docx
│   ├── arm_keyboard.py
│   ├── mqtt_gateway_lite.py
│   └── pip install pyserial, paho-mqtt.docx
│
├── IdeaProjects.zip
├── README.md
├── group4_ws.zip
├── index.html
├── portfolio-pdf.css
├── portfolio-pdf.html
├── project-air-robot.html
├── project-smart-bin.html
├── script.js
├── style.css
└── 안효민_포트폴리오.pdf
```
* 상위폴더에서 IdeaProjects.zip, group4_ws.zip는 두번째 프로젝트 입니다.

## 실행

별도의 설치나 빌드 과정은 필요하지 않습니다.

1. 저장소를 내려받습니다.
2. `index.html` 파일을 브라우저에서 엽니다.

HTML, CSS, JavaScript로만 만든 정적 사이트라 GitHub Pages에서 바로 볼 수 있습니다.

## 사이트 구성

- 메인 소개
- 해결 방식
- 역량
- 프로젝트 2개
- 프로젝트 상세 페이지
- PDF 제출용 페이지
- 연락처

## 연락처

- Email: mymin8724@gmail.com
- GitHub: https://github.com/PureJuly
