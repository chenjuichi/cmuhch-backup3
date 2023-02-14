import socket
import pathlib
import json

import threading  # 2022-12-31 add
import logging    # 2022-12-31 add
import ctypes     # 2022-12-31 add

##import wmi        # 2023-01-31 add
##c = wmi.WMI()     # 2023-01-31 add
# --------------------------

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mqtt import Mqtt

#from flask_restful import Api

# --------------------------

from ajax.getTable import getTable
from ajax.createTable import createTable
from ajax.updateTable import updateTable
from ajax.deleteTable import deleteTable

from ajax.listTable import listTable

from ajax.excelTable import excelTable


# --------------------------


app = Flask(__name__)  # 初始化Flask物件

#api = Api(app)
hostName = socket.gethostname()
local_ip = socket.getaddrinfo(hostName, None)
temp_size = len(local_ip)
for i in range(temp_size):
    print("<AddressFamily: ", local_ip[i])

host_ip_for_wifi = local_ip[1][4][0]  # for 無線網卡
print("<AddressFamily: ", local_ip[1][4])
print('system Lan ip: ' + '\033[46m' + host_ip_for_wifi + '\033[0m')

# --------------------------
'''
hostName = socket.gethostname()
local_ip = socket.getaddrinfo(hostName, None)
print("system Lan ip:" + host_ip_for_lan, ", and wifi ip:" + host_ip_for_wifi)

host_ip_for_lan = local_ip[3][4][0]  # for 有線網卡
host_ip_for_wifi = local_ip[1][4][0]  # for 無線網卡
print("system Lan ip:" + host_ip_for_lan, ", and wifi ip:" + host_ip_for_wifi)
'''
# --------------------------

# host_ip = '192.168.0.12'    # for home #//////2/2-
# host_ip = '10.108.249.107'  # for cmuhch #//////2/2-
host_ip = '192.168.32.178'  # for zh  #//////2/2-
# host_ip = '192.168.43.117'  # for mobile  #//////2/2-
# host_ip = '192.168.200.171' # for pmc guest

# host_ip = '10.108.249.100'  # for cmuhch 正式


# for test
#drive = pathlib.Path.home().drive
# print(drive)

# this will prevent the screen saver or sleep.
ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
# your code and operations
# ctypes.windll.kernel32.SetThreadExecutionState(0x80000000) #set the setting back to normal

##user32 = ctypes.windll.User32
##OpenDesktop = user32.OpenDesktopA
##SwitchDesktop = user32.SwitchDesktop
##DESKTOP_SWITCHDESKTOP = 0x0100


# --------------------------


app.config['MQTT_BROKER_URL'] = host_ip
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'cmu_hch_mqtt'
#app.config['TEMPLATES_AUTO_RELOAD'] = True
#app.config['MQTT_REFRESH_TIME'] = 1.0
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
# app.config['MQTT_KEEPALIVE'] = 30       # Set KeepAlive time in seconds
# If your server supports TLS, set it True
app.config['MQTT_TLS_ENABLED'] = False


# 建立 MQTT Client 物件
mqtt_client = Mqtt(app, connect_async=True)

# --------------------------

app.register_blueprint(getTable)
app.register_blueprint(updateTable)
app.register_blueprint(deleteTable)
app.register_blueprint(createTable)

app.register_blueprint(listTable)

app.register_blueprint(excelTable)

# --------------------------

CORS(app, resources={r'/*': {'origins': '*'}})
# CORS(app)


# --------------------------


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # mark, not display message
    #print("=== MQTT Subscribe===")
    # print(data)
    #print("topic: ", data['topic'])
    #print(data['payload'], " on line...")
    #print("=== MQTT ===")
    #


@mqtt_client.on_connect()
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # mqtt_client.connected_flag = True  # set flag
        print('Connected successfully')
        # 每次連線之後，重新設定訂閱主題
        mqtt_client.subscribe("on_line")
    else:
        print('Bad connection. Code:', rc)


@mqtt_client.on_log()
def handle_logging(client, userdata, level, buf):
    if level == 16:
        #print('MQTT_LOG_DEBUG: {}'.format(buf))
        pass  # MQTT_LOG_DEBUG
    else:
        print('Error: {}'.format(buf))
    # pass


# --------------------------


@app.route("/")
def helloWorld():
    return "Hello..."


@app.route("/mqtt/stationA", methods=['POST'])
def mqtt_stationA():
    request_data = request.get_json()
    print("hello /mqtt/stationA: " + request_data['topic'])
    print("message: " + request_data['layout'] + ' ' +
          request_data['led'] + ' ' + request_data['msg'])

    # 發布訊息至 Layout/Led 主題
    MQTT_MSG = json.dumps(
        {"Layout": request_data['layout'], "Led": request_data['led'], "Msg": request_data['msg']})
    mqtt_client.publish('Station1', MQTT_MSG)

    return jsonify({
        'status': 'stationA success',
    })


# @app.route("/mqtt/station1", methods=['POST'])
# def mqtt_station1():
@app.route("/mqtt/station", methods=['POST'])
def mqtt_station():
    request_data = request.get_json()
    myTopic = request_data['topic']
    myLayout = request_data['layout']
    myPosBegin = str(request_data['pos_begin'])
    myPosEnd = str(request_data['pos_end'])
    myMsg = request_data['msg']

    myReturnMsg = myTopic + ' success'

    print("hello /mqtt/station: " + myTopic)
    print('\033[46m' +  'message: ' + '\033[0m' +
          myTopic + ' ' + myLayout +' '+ myPosBegin + ' ' + myPosEnd + ' ' + myMsg)

    # 發布訊息主題myTopic
    MQTT_MSG = json.dumps(
        {"Layout": myLayout, "Begin": myPosBegin, "End": myPosEnd, "Msg": myMsg})
    #mqtt_client.publish('Station1', MQTT_MSG)
    mqtt_client.publish(myTopic, MQTT_MSG)

    return jsonify({
        'status': myReturnMsg,
    })

# --------------------------


if __name__ == '__main__':
    #    app.run(host='0.0.0.0', port=2020, debug=True)
    app.run(host=host_ip, port=6060, debug=True)
