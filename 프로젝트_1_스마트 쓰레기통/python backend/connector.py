import socket
import time

import requests

PORT = 1
BD_ADDR = "98:DA:60:0C:D8:4A"
# BD_ADDR = "98:DA:60:0C:D7:F9"

ENDPOINT = "http://localhost:5000"


def open_bin(msg) -> tuple[str, str]:
    key = msg[5:]
    resp = None
    try:
        resp = requests.get(f"{ENDPOINT}/open?key={key}")
        if resp.status_code == 200:
            return "ok", resp.text
        else:
            return "rejected", resp.text
    except:
        if resp:
            return "rejected", resp.text
        else:
            return "rejected", "error while request"


def close_bin(msg) -> str:
    key = msg[6:]
    resp = None
    if key == "auto":
        url = f"{ENDPOINT}/close"
    else:
        url = f"{ENDPOINT}/close?key={key}"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.text
        else:
            return resp.text
    except:
        if resp:
            return resp.text
        else:
            return "error while request"


BIN_NAME = {
    "plastic": 1,
    "paper": 2,
    "general": 3,
}


def full_bin(msg) -> str:
    resp = None
    if msg[5:] in BIN_NAME:
        number = BIN_NAME[msg[5:]]
    else:
        return "invalid key"
    try:
        resp = requests.get(f"{ENDPOINT}/full?number={number}")
        if resp.status_code == 200:
            return resp.text
        else:
            return resp.text
    except:
        if resp:
            return resp.text
        else:
            return "error while request"


def empty_bin(msg) -> str:
    resp = None
    number = BIN_NAME[msg[6:]]
    try:
        resp = requests.get(f"{ENDPOINT}/empty?number={number}")
        if resp.status_code == 200:
            return resp.text
        else:
            return resp.text
    except:
        if resp:
            return resp.text
        else:
            return "error while request"


def main():

    # 블루투스 RFCOMM 소켓 생성
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    print(f"{BD_ADDR}에 연결 시도 중...")
    try:
        sock.connect((BD_ADDR, PORT))
        print("연결 성공")

        sock.settimeout(0.5)  # 블로킹 방지를 위한 타임아웃 설정
        buffer = ""

        while True:
            try:
                # 데이터 수신
                data = sock.recv(1024).decode("utf-8")
                if data:
                    buffer += data
                    if "\n" in buffer:
                        lines = buffer.split("\n")
                        for line in lines[:-1]:
                            reply = None
                            msg = line.rstrip()
                            print(msg)
                            if msg.startswith("open+"):
                                reply, result = open_bin(msg)
                            elif msg.startswith("close+"):
                                result = close_bin(msg)
                            elif msg.startswith("full+"):
                                result = full_bin(msg)
                            elif msg.startswith("empty+"):
                                result = empty_bin(msg)

                            print("result", result)
                            if reply:
                                reply += "\n"
                                print("reply:", reply, end="")
                                sock.sendall(reply.encode())

                        buffer = lines[-1]
            except socket.timeout:
                pass  # 수신 데이터가 없는 상태 (정상)
            except Exception as e:
                print(f"통신 중 오류 발생: {e}")
                break

            time.sleep(0.1)

    except Exception as e:
        print(f"연결 실패: {e}")
    finally:
        sock.close()
        print("소켓 종료됨")


if __name__ == "__main__":
    main()
