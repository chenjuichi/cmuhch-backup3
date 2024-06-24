import socket
import json
import ctypes     # 2022-12-31 add

# --------------------------

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_mqtt import Mqtt

# --------------------------

from ajax.getTable import getTable
from ajax.createTable import createTable
from ajax.updateTable import updateTable
from ajax.deleteTable import deleteTable
from ajax.listTable import listTable
from ajax.excelTable import excelTable

#from ajax.webRTC import webRTC, init_app   # 2023-12-08 add

# --------------------------

app = Flask(__name__)  # 初始化Flask物件

hostName = socket.gethostname()             # 2023-08-09 unmark
local_ip = socket.gethostbyname(hostName)   # get local ip address, 2023-08-09 add
print('\n' + 'Lan ip: ' + '\033[0m' + '\033[46m' + local_ip + '\033[0m')  # 2023-12-08 modify
print('Build:  ' + '\033[0;37;42m' + '2024-03-27' + '\033[0m' + '\n')
host_ip = local_ip     # 2023-08-09 add

# this will prevent the screen saver or sleep.
ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
# your code and operations
# ctypes.windll.kernel32.SetThreadExecutionState(0x80000000) #set the setting back to normal

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

mqttTopic_for_reconnect = "reconnect"
mqttTopic_for_online = "online"

# --------------------------

app.register_blueprint(getTable)
app.register_blueprint(updateTable)
app.register_blueprint(deleteTable)
app.register_blueprint(createTable)
app.register_blueprint(listTable)
app.register_blueprint(excelTable)

###
# -------------------------- 2023-12-08 add the following block
#app.register_blueprint(webRTC, url_prefix='/webrtc')      # 使用絕對路徑, 並定義呼叫的url_prefix
#init_app(app)     # 初始化 Socket.IO
# --------------------------
###

CORS(app, resources={r'/*': {'origins': '*'}})

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
    # 2023-11-21 add the following block
    if message.topic == mqttTopic_for_reconnect:
      print(f"Received message: {message.payload.decode()}")
    if message.topic == mqttTopic_for_online:
      print(f"Received message: {message.payload.decode()}")
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


@app.route('/hello', methods=['GET'])
def hello():
    print("fetch hello....")
    output = {"name": ""}
    return jsonify(output)


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


@app.route("/mqtt/station", methods=['POST'])
def mqtt_station():
    request_data = request.get_json()
    myTopic = request_data['topic']
    myLayout = request_data['layout']
    myPosBegin = str(request_data['pos_begin'])
    myPosEnd = str(request_data['pos_end'])
    myMsg = request_data['msg']

    myReturnMsg = myTopic + ' success'

    print("hello /mqtt/station: " + myTopic + " , welcome you!")
    #print(type(myTopic))
    print('\033[46m' + 'message: ' + '\033[0m' +
          '\033[91m' + myTopic +
          '\033[0m'  + ' ' + myLayout +' '+ myPosBegin + ' ' + myPosEnd + ' ' + myMsg)

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

  app.run(host=host_ip, port=6060, debug=True)