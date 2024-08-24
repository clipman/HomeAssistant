#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import platform
import threading
import queue
import random
import json
import paho.mqtt.client as mqtt
import logging
import configparser

# define -------------------------------
SW_VERSION = '2024.03.12'
CONFIG_FILE = 'kocom_call.cfg'
BUF_SIZE = 100

read_write_gap = 0.03  # minimal time interval between last read to write
polling_interval = 300  # polling interval

header_h = 'aa55'
trailer_h = '0d0d'
packet_size = 21  # total 21bytes
chksum_position = 18  # 18th byte

type_t_dic = {'30b':'send', '30d':'ack', '7a9':'call'}
seq_t_dic = {'c':1, 'd':2, 'e':3, 'f':4}
device_t_dic = {'01':'wallpad', '02':'home', '08':'gate', '0e':'light', '2c':'gas', '36':'thermo', '3b': 'plug', '44':'elevator', '48':'fan'}
cmd_t_dic = {'00':'state', '01':'on', '02':'off', '3a':'query'}
room_t_dic = {'00':'livingroom', '01':'room1', '02':'room2', '03':'room3'}

type_h_dic = {v: k for k, v in type_t_dic.items()}
seq_h_dic = {v: k for k, v in seq_t_dic.items()}
device_h_dic = {v: k for k, v in device_t_dic.items()}
cmd_h_dic = {v: k for k, v in cmd_t_dic.items()}
room_h_dic = {'livingroom':'00', 'myhome':'00', 'room1':'01', 'room2':'02', 'room3':'03'}

# mqtt functions ----------------------------

def init_mqttc():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqttc.on_message = mqtt_on_message
    mqttc.on_subscribe = mqtt_on_subscribe
    mqttc.on_connect = mqtt_on_connect
    mqttc.on_disconnect = mqtt_on_disconnect

    if config.get('MQTT','mqtt_allow_anonymous') != 'True':
        logtxt = "[MQTT] connecting (using username and password)"
        mqttc.username_pw_set(username=config.get('MQTT','mqtt_username',fallback=''), password=config.get('MQTT','mqtt_password',fallback=''))
    else:
        logtxt = "[MQTT] connecting (anonymous)"

    mqtt_server = config.get('MQTT','mqtt_server')
    mqtt_port = int(config.get('MQTT','mqtt_port'))
    for retry_cnt in range(1,31):
        try:
            logging.info(logtxt)
            mqttc.connect(mqtt_server, mqtt_port, 60)
            mqttc.loop_start()
            return mqttc
        except:
            logging.error('[MQTT] connection failure. #' + str(retry_cnt))
            time.sleep(10)
    return False

def mqtt_on_subscribe(mqttc, obj, mid, granted_qos, properties):
    logging.info("[MQTT] Subscribed: " + str(mid) + " " + str(granted_qos))

def mqtt_on_log(mqttc, obj, level, string):
    logging.info("[MQTT] on_log : "+string)

def mqtt_on_connect(mqttc, userdata, flags, rc, properties):
    if rc == 0:
        logging.info("[MQTT] Connected - 0: OK")
        mqttc.subscribe('kocom/#', 0)
    else:
        logging.error("[MQTT] Connection error - {}: {}".format(rc, mqtt.connack_string(rc)))

def mqtt_on_disconnect(mqttc, userdata,rc=0):
    logging.error("[MQTT] Disconnected - "+str(rc))

# serial/socket communication class & functions--------------------

class RS485Wrapper:
    def __init__(self, serial_port=None, socket_server=None, socket_port=0):
        if socket_server == None:
            self.type = 'serial'
            self.serial_port = serial_port
        else:
            self.type = 'socket'
            self.socket_server = socket_server
            self.socket_port = socket_port
        self.last_read_time = 0
        self.conn = False

    def connect(self):
        self.close()
        self.last_read_time = 0
        if self.type=='serial':
            self.conn = self.connect_serial(self.serial_port)
        elif self.type=='socket':
            self.conn = self.connect_socket(self.socket_server, self.socket_port)
        return self.conn

    def connect_serial(self, SERIAL_PORT):
        if SERIAL_PORT==None:
            os_platfrom = platform.system()
            if os_platfrom == 'Linux':
                SERIAL_PORT = '/dev/ttyUSB0'
            else:
                SERIAL_PORT = 'com3'
        try:
            ser = serial.Serial(SERIAL_PORT, 9600, timeout=1)
            ser.bytesize = 8
            ser.stopbits = 1
            if ser.is_open == False:
                raise Exception('Not ready')
            logging.info('[RS485] Serial connected : {}'.format(ser))
            return ser
        except Exception as e:
            logging.error('[RS485] Serial open failure : {}'.format(e))
            return False

    def connect_socket(self, SOCKET_SERVER, SOCKET_PORT):
        sock = socket.socket()
        sock.settimeout(10)
        try:
            sock.connect((SOCKET_SERVER, SOCKET_PORT))
        except Exception as e:
            logging.error('[RS485] Socket connection failure : {} | server {}, port {}'.format(e, SOCKET_SERVER, SOCKET_PORT))
            return False
        logging.info('[RS485] Socket connected | server {}, port {}'.format(SOCKET_SERVER, SOCKET_PORT))
        sock.settimeout(None)   #sock.settimeout(polling_interval+15)   # set read timeout a little bit more than polling interval
        return sock

    def read(self):
        if self.conn == False:
            return ''
        ret = ''
        if self.type=='serial':
            for i in range(polling_interval+15):
                try:
                    ret = self.conn.read()
                except AttributeError:
                    raise Exception('exception occured while reading serial')
                except TypeError:
                    raise Exception('exception occured while reading serial')
                if len(ret) != 0:
                    break
        elif self.type=='socket':
            ret = self.conn.recv(1)

        if len(ret) == 0:
            raise Exception('read byte errror')
        else:
            self.last_read_time = time.time()
        return ret

    def write(self, data):
        if self.conn == False:
            return False
        if self.last_read_time == 0:
            time.sleep(1)
        while time.time() - self.last_read_time < read_write_gap:
            #logging.debug('pending write : time too short after last read')
            time.sleep(max([0, read_write_gap - time.time() + self.last_read_time]))
        if self.type=='serial':
            return self.conn.write(data)
        elif self.type=='socket':
            return self.conn.send(data)
        else:
            return False

    def close(self):
        ret = False
        if self.conn != False:
            try:
                ret = self.conn.close()
                self.conn = False
            except:
                pass
        return ret

    def reconnect(self):
        self.close()
        while True: 
            logging.info('[RS485] reconnecting to RS485...')
            if self.connect() != False:
                break
            time.sleep(10)

def send_packet(send_data):
    send_lock.acquire()
    ret = False
    try:
        if rs485.write(bytearray.fromhex(send_data)) == False:
            raise Exception('Not ready')
        ret = send_data
    except Exception as ex:
        logging.error("[RS485] Write error.[{}]".format(ex) )
    logging.info('[SEND] {}'.format(send_data))

    if ret == False:
        logging.info('[RS485] send failed. closing RS485. it will try to reconnect to RS485 shortly.')
        rs485.close()
    send_lock.release()
    return ret

# hex parsing --------------------------------
#home call
#aa55 7a9 d 02 0200 ffff ff ff31ffffff0101a4 55 0d0d
#aa55 7a9 e 02 0200 ffff ff ff31ffffff010129 f6 0d0d
#gate call
#aa55 7a9 d 02 0800 ffff ff ffffffffff010187 84 0d0d
#aa55 7a9 e 02 0800 ffff ff ffffffffff01010a 27 0d0d
#home_open command
#aa55 79b c 02 0200 31ff ff ff61ffffff030008 d3 0d0d(home phone)
#aa55 79b c 02 0200 31ff ff ff61ffffff240097 a2 0d0d(home open)
#aa55 79b c 02 0200 31ff ff ff61ffffff040091 44 0d0d(home exit)
#gate_open command
#aa55 79b c 08 0200 ffff ff ff61ffffff030026 95 0d0d(gate phone)
#aa55 79b c 08 0200 ffff ff ff61ffffff2400b9 e4 0d0d(gate open)
def parse(hex_data):
    header_h = hex_data[:4]    # aa55
    type_h = hex_data[4:7]    # send/ack : 30b(send) 30d(ack) 7a9(call)
    seq_h = hex_data[7:8]    # sequence : c(1st) d(2nd)
    monitor_h = hex_data[8:10] # sequence : 00(wallpad) 02(KitchenTV)
    dest_h = hex_data[10:14] # dest addr : 0100(wallpad0) 0e00(light0) 3600(thermo0) 3601(thermo1) 3602(thermo2) 3603(thermo3) 4800(fan) 4400(elevator) 0200(door) 0800(gate)
    src_h = hex_data[14:18]   # source addr  
    cmd_h = hex_data[18:20]   # command : 3e(query)
    value_h = hex_data[20:36]  # value
    chksum_h = hex_data[36:38]  # checksum
    trailer_h = hex_data[38:42]  # trailer

    data_h = hex_data[4:36]
    payload_h = hex_data[18:36]
    cmd = cmd_t_dic.get(cmd_h)

    ret = { 'header_h':header_h, 'type_h':type_h, 'seq_h':seq_h, 'monitor_h':monitor_h, 'dest_h':dest_h, 'src_h':src_h, 'cmd_h':cmd_h, 
            'value_h':value_h, 'chksum_h':chksum_h, 'trailer_h':trailer_h, 'data_h':data_h, 'payload_h':payload_h,
            'type':type_t_dic.get(type_h),
            'seq':seq_t_dic.get(seq_h), 
            'dest':device_t_dic.get(dest_h[:2]),
            'dest_subid':str(int(dest_h[2:4], 16)),
            'src':device_t_dic.get(src_h[:2]),
            'src_subid':str(int(src_h[2:4], 16)),
            'cmd':cmd if cmd!=None else cmd_h,
            'value':value_h,
            'time': time.time(),
            'flag':None}
    return ret

def home_call_parse(value):
    state = 'on' if value[2:4] == '31' and value[10:14] == '0101' else 'off'
    return { 'state': state }

def gate_call_parse(value):
    state = 'on' if value[10:14] == '0101' else 'off'
    return { 'state': state }

#===== parse MQTT --> send hex packet =====

def mqtt_on_message(mqttc, obj, msg):
    command = msg.payload.decode('ascii')
    topic_d = msg.topic.split('/')

    # do not process other than command topic
    if topic_d[-1] != 'command':
        return

    logging.info("[MQTT RECV] " + msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    # home_call off : kocom/myhome/home_call/command
    if 'home_call' in topic_d:
        dev_id = device_h_dic['home'] + room_h_dic.get(topic_d[1])
        if command == 'PRESS':
            send_packet('aa5579bc02020031ffffff61ffffff030008d30d0d')
            time.sleep(1)
            send_packet('aa5579bc02020031ffffff61ffffff240097a20d0d')
            time.sleep(0.1)
            send_packet('aa5579bc02020031ffffff61ffffff040091440d0d')
    # gate_call off : kocom/myhome/gate_call/command
    elif 'gate_call' in topic_d:
        dev_id = device_h_dic['gate'] + room_h_dic.get(topic_d[1])
        if command == 'PRESS':
            send_packet('aa5579bc080200ffffffff61ffffff030026950d0d')
            time.sleep(0.5)
            send_packet('aa5579bc080200ffffffff61ffffff2400b9e40d0d')
    # home_bell off : kocom/myhome/home_bell/command
    elif 'home_bell' in topic_d:
        dev_id = device_h_dic['home'] + room_h_dic.get(topic_d[1])
        if command == 'PRESS':
            send_packet('aa5579bc02020031ffffff61ffffff030008d30d0d')
            time.sleep(1)
            send_packet('aa5579bc02020031ffffff61ffffff040091440d0d')

#===== parse hex packet --> publish MQTT =====

def publish_status(p):
    threading.Thread(target=packet_processor, args=(p,)).start()

def packet_processor(p):
    logtxt = ""
    if p['type']=='call' and p['dest']=='home':
        state = home_call_parse(p['value'])
        logtxt='[MQTT publish|home_call] data[{}]'.format(state)
        mqttc.publish("kocom/myhome/home_call/state", json.dumps(state))
    elif p['type']=='call' and p['dest']=='gate':
        state = gate_call_parse(p['value'])
        logtxt='[MQTT publish|gate_call] data[{}]'.format(state)
        mqttc.publish("kocom/myhome/gate_call/state", json.dumps(state))

    if logtxt != "" and config.get('Log', 'show_mqtt_publish') == 'True':
        logging.info(logtxt)

#===== publish MQTT Devices Discovery =====
#https://www.home-assistant.io/docs/mqtt/discovery/
#<discovery_prefix>/<component>/<object_id>/config
def discovery():
    device_info = {
        'name': '코콤 스마트 월패드',
        'ids': 'kocom_smart_wallpad',
        'mf': 'KOCOM',
        'mdl': '스마트 월패드',
        'sw': SW_VERSION
    }

    topics_payloads = [
        ('homeassistant/button/kocom_open_door/config', {
            'name': 'Kocom Open Door',
            'ic': 'mdi:gesture-tap',
            'cmd_t': 'kocom/myhome/home_call/command',
            'qos': 0,
            'uniq_id': 'kocom_open_door',
            'device': device_info
        }),
        ('homeassistant/button/kocom_open_gate/config', {
            'name': 'Kocom Open Gate',
            'ic': 'mdi:gesture-tap',
            'cmd_t': 'kocom/myhome/gate_call/command',
            'qos': 0,
            'uniq_id': 'kocom_open_gate',
            'device': device_info
        }),
        ('homeassistant/button/kocom_bell_door/config', {
            'name': 'Kocom Bell Door',
            'ic': 'mdi:gesture-tap',
            'cmd_t': 'kocom/myhome/home_bell/command',
            'qos': 0,
            'uniq_id': 'kocom_bell_door',
            'device': device_info
        }),
        ('homeassistant/sensor/kocom_home_call/config', {
            'name': 'Kocom Home Call',
            'ic': 'mdi:bell-ring-outline',
            'stat_t': 'kocom/myhome/home_call/state',
            'val_tpl': '{{ value_json.state }}',
            'qos': 0,
            'uniq_id': 'kocom_home_call',
            'device': device_info
        }),
        ('homeassistant/sensor/kocom_gate_call/config', {
            'name': 'Kocom Gate Call',
            'ic': 'mdi:bell-ring-outline',
            'stat_t': 'kocom/myhome/gate_call/state',
            'val_tpl': '{{ value_json.state }}',
            'qos': 0,
            'uniq_id': 'kocom_gate_call',
            'device': device_info
        })
    ]

    for topic, payload in topics_payloads:
        logtxt = '[MQTT Discovery data[{}]'.format(topic)
        mqttc.publish(topic, json.dumps(payload))
        if logtxt != "" and config.get('Log', 'show_mqtt_publish') == 'True':
            logging.info(logtxt)

#===== thread functions ===== 

def read_serial():
    buf = ''
    not_parsed_buf = ''
    while True:
        try:
            d = rs485.read()
            hex_d = '{0:02x}'.format(ord(d))

            buf += hex_d
            if buf[:len(header_h)] != header_h[:len(buf)]:
                not_parsed_buf += buf
                buf=''
                frame_start = not_parsed_buf.find(header_h, len(header_h))
                if frame_start < 0:
                    continue
                else:
                    not_parsed_buf = not_parsed_buf[:frame_start]
                    buf = not_parsed_buf[frame_start:]
            
            if not_parsed_buf != '':
                logging.info('[comm] not parsed '+not_parsed_buf)
                not_parsed_buf = ''

            if len(buf) == packet_size*2:
                if buf[-len(trailer_h):] == trailer_h:
                    if msg_q.full():
                        logging.error('msg_q is full. probably error occured while running listen_hexdata thread. please manually restart the program.')
                    msg_q.put(buf)  # valid packet
                    buf=''
                else:
                    logging.info("[comm] invalid packet {} expected".format(buf))
                    frame_start = buf.find(header_h, len(header_h))
                    # if there's header packet in the middle of invalid packet, re-parse from that posistion
                    if frame_start < 0:
                        not_parsed_buf += buf
                        buf=''
                    else:
                        not_parsed_buf += buf[:frame_start]
                        buf = buf[frame_start:]
        except Exception as ex:
            logging.error("*** Read error.[{}]".format(ex) )
            del cache_data[:]
            rs485.reconnect()

def listen_hexdata():
    while True:
        d = msg_q.get()

        if config.get('Log', 'show_recv_hex') == 'True':
            logging.info("[recv] " + d)
 
        p_ret = parse(d)

        # store recent packets in cache
        cache_data.insert(0, p_ret)
        if len(cache_data) > BUF_SIZE:
            del cache_data[-1]

        if p_ret['data_h'] in ack_data:
            ack_q.put(d)
            continue
 
        if wait_target.empty() == False:
            if p_ret['dest_h'] == wait_target.queue[0] and p_ret['type'] == 'ack':
            #if p_ret['src_h'] == wait_target.queue[0] and p_ret['type'] == 'send':
                if len(ack_data) != 0:
                    logging.info("[ACK] No ack received, but responce packet received before ACK. Assuming ACK OK")
                    ack_q.put(d)
                    time.sleep(0.5)
                wait_q.put(p_ret)
                continue
        publish_status(p_ret)

#========== Main ==========

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s[%(asctime)s]:%(message)s ', level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    if config.get('RS485', 'type') == 'serial':
        import serial
        rs485 = RS485Wrapper(serial_port = config.get('RS485', 'serial_port', fallback=None))
    elif config.get('RS485', 'type') == 'socket':
        import socket
        rs485 = RS485Wrapper(socket_server = config.get('RS485', 'socket_server'), socket_port = int(config.get('RS485', 'socket_port')))
    else:
        logging.error('[CONFIG] invalid type value in [RS485]: only "serial" or "socket" is allowed. exit')
        exit(1)
    if rs485.connect() == False:
        logging.error('[RS485] connection error. exit')
        exit(1)

    mqttc = init_mqttc()
    if mqttc == False:
        logging.error('[MQTT] conection error. exit')
        exit(1)

    msg_q = queue.Queue(BUF_SIZE)
    ack_q = queue.Queue(1)
    ack_data = []
    wait_q = queue.Queue(1)
    wait_target = queue.Queue(1)
    send_lock = threading.Lock()

    cache_data = []

    thread_list = []
    thread_list.append(threading.Thread(target=read_serial, name='read_serial'))
    thread_list.append(threading.Thread(target=listen_hexdata, name='listen_hexdata'))
    for thread_instance in thread_list:
        thread_instance.start()

    discovery()
