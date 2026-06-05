"""
arm_keyboard.py — 키보드로 로봇팔 수동 조작 (jog)
====================================================
터미널에서 키 하나로 채널 선택·각도 조절. MQTT로 명령 발행하므로
mqtt_gateway_lite.py(게이트웨이)가 켜져 있어야 한다.

    [이 키보드 도구] --MQTT--> [게이트웨이] --USB--> [아두이노] --> 팔

조작키:
    a / d : 채널 선택 (이전 / 다음)
    w / s : 선택 채널 값 올리기 / 내리기 (STEP 도씩)
    x     : 긴급정지 ↔ 해제 (토글)
    o / p : 이동 속도 빠르게 / 느리게
    q     : 종료

실행:
    python3 arm_keyboard.py                # 브로커 localhost
    python3 arm_keyboard.py 192.168.0.187  # 브로커 IP 지정

의존성:
    sudo apt install -y python3-paho-mqtt
"""

import sys, time
import paho.mqtt.client as mqtt

# ── 키 입력: 윈도우(msvcrt) / 리눅스·맥(termios) 자동 선택 ──
try:
    import msvcrt  # 윈도우
    def getch():
        ch = msvcrt.getch()
        try:
            return ch.decode("utf-8", "ignore")
        except Exception:
            return ""
except ImportError:
    import termios, tty  # 리눅스 / 맥
    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return ch

BROKER = sys.argv[1] if len(sys.argv) > 1 else "192.168.0.187"  # 기본: 라파이 브로커
TOPIC  = "pack/arm/cmd"
STEP   = 5     # w/s 한 번에 바뀌는 각도

# 채널: (번호, 이름, 최소, 최대)
CHANNELS = [
    (5,  "그리퍼",   0,  50),
    (7,  "손목회전", 40, 130),
    (9,  "손목굽힘", 70, 180),
    (11, "팔꿈치",   0,  90),
    (13, "어깨",     20, 140),
    (15, "베이스",   0, 180),
]
# 현재 값(홈 기준 초기화)
values = {5: 0, 7: 130, 9: 90, 11: 60, 13: 120, 15: 150}

idx   = 0      # 선택된 채널 인덱스
speed = 25     # ms/도 (작을수록 빠름)
ems   = False  # 긴급정지 상태


# MQTT (paho 1.x/2.x 호환)
try:
    cli = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
except (AttributeError, TypeError):
    cli = mqtt.Client()
cli.connect(BROKER, 1883, 60)
cli.loop_start()

def send(msg):
    cli.publish(TOPIC, msg)


def draw():
    """현재 상태 화면 출력."""
    print("\033[2J\033[H", end="")   # 화면 지우기
    print("=== 로봇팔 키보드 조작 ===")
    print(f"브로커:{BROKER}  속도:{speed}ms/도  ", end="")
    print("\033[31m[긴급정지]\033[0m" if ems else "\033[32m[동작가능]\033[0m")
    print("-" * 40)
    for i, (ch, name, lo, hi) in enumerate(CHANNELS):
        cur = "▶" if i == idx else " "
        bar = f"{values[ch]:3d} ({lo}~{hi})"
        print(f" {cur} CH{ch:<2} {name:<6} : {bar}")
    print("-" * 40)
    print("a/d:채널  w/s:값±  x:정지토글  o/p:속도  q:종료")


def main():
    global idx, speed, ems
    draw()
    while True:
        c = getch().lower()

        if c == 'q':
            break

        # 긴급정지 토글
        elif c == 'x':
            ems = not ems
            send("0" if ems else "R")

        # 속도 (o=빠르게, p=느리게)
        elif c == 'o':
            speed = max(5, speed - 5)
            send(f"SP {speed}")
        elif c == 'p':
            speed = min(200, speed + 5)
            send(f"SP {speed}")

        # EMS 중엔 이동/채널 무시 (x로 풀어야 함)
        elif ems:
            pass

        # 채널 선택
        elif c == 'a':
            idx = (idx - 1) % len(CHANNELS)
        elif c == 'd':
            idx = (idx + 1) % len(CHANNELS)

        # 값 조절
        elif c == 'w' or c == 's':
            ch, name, lo, hi = CHANNELS[idx]
            v = values[ch] + (STEP if c == 'w' else -STEP)
            v = max(lo, min(hi, v))      # 안전범위 클램프
            values[ch] = v
            send(f"{ch} {v}")            # 아두이노로 전송

        draw()

    cli.loop_stop()
    cli.disconnect()
    print("\n종료.")


if __name__ == "__main__":
    main()
