import socket
import paho.mqtt.client as mqtt
import threading
import configparser

CONFIGFILENAME = 'mqttbridge.cfg'

# 설정 파일 로드
config = configparser.ConfigParser()
config.read(CONFIGFILENAME)

# TCP 설정
TCP_IP = config.get('RS485', 'socket_server')
TCP_PORT = config.getint('RS485', 'socket_port')

# MQTT 설정
MQTT_BROKER = config.get('MQTT', 'mqtt_server')
MQTT_PORT = config.getint('MQTT', 'mqtt_port')
MQTT_USERNAME = config.get('MQTT', 'mqtt_username')
MQTT_PASSWORD = config.get('MQTT', 'mqtt_password')

# MQTT TOPIC 설정
MQTT_TOPIC_RECEIVE = config.get('TOPIC', 'receive')
MQTT_TOPIC_SEND = config.get('TOPIC', 'send')

# 기타 설정
BUFFER_SIZE = config.getint('GENERAL', 'buffer_size')

# TCP 소켓 생성 및 연결
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((TCP_IP, TCP_PORT))

# MQTT 클라이언트 생성 및 설정
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

def on_message(client, userdata, msg):
    try:
        # MQTT 메시지를 받을 때 호출되는 콜백 함수
        data = msg.payload.decode('utf-8').strip()  # payload를 문자열로 디코딩 및 공백 제거
        print(f"Received from MQTT: {data}")

        # 디버그: 수신된 데이터를 그대로 출력
        # print(f"Raw MQTT data: {repr(msg.payload)}")

        # 데이터가 16진수 문자열로 유효한지 확인
        if len(data) % 2 == 0 and all(c in "0123456789abcdefABCDEF" for c in data):
            tcp_socket.send(bytes.fromhex(data))
            print(f"Sent to TCP: {data}")
        else:
            # 문자열을 16진수로 변환할 수 없는 이유를 더 명확히 알기 위해 디버깅 정보를 추가합니다.
            invalid_chars = [c for c in data if c not in "0123456789abcdefABCDEF"]
            print(f"Invalid hex string received: {data}, invalid characters: {invalid_chars}")

    except ValueError as e:
        print(f"Error converting to hex: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

mqtt_client.on_message = on_message

# MQTT 연결 설정 및 구독 시작
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC_RECEIVE)
mqtt_client.loop_start()

def tcp_listener():
    while True:
        try:
            data = tcp_socket.recv(BUFFER_SIZE)
            if data:
                hex_data = data.hex()

                # 수신한 패킷을 모두 전송
                # mqtt_client.publish(MQTT_TOPIC_SEND, hex_data)
                # print(f"Received from TCP and sent to MQTT: {hex_data}")

                # "aa55"로 시작하고 "0d0d"로 끝나는 패킷을 추출하여 순차적으로 전송
                packets = hex_data.split("aa55")[1:]  # "aa55" 기준으로 패킷 분리
                for packet in packets:
                    if packet.endswith("0d0d"):
                        full_packet = "aa55" + packet
                        mqtt_client.publish(MQTT_TOPIC_SEND, full_packet)
                        print(f"Received from TCP and sent to MQTT: {full_packet}")
        except Exception as e:
            print(f"Error receiving data from TCP: {e}")

# TCP 리스너 스레드 시작
tcp_thread = threading.Thread(target=tcp_listener)
tcp_thread.start()

# 메인 스레드는 MQTT 클라이언트 루프를 계속 실행
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Exiting...")
finally:
    tcp_socket.close()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
