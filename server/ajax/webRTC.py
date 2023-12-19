
from flask import Blueprint, render_template
from flask_socketio import SocketIO, Namespace

# ------------------------------------------------------------------

#webRTC = Blueprint('webRTC', __name__, template_folder='templates', static_folder='static')
webRTC = Blueprint('webRTC', __name__)
#socketio = SocketIO()
socketio = SocketIO(cors_allowed_origins="*")
print("WELCOME webRTC...")

#socketio = SocketIO(app, logger=True, engineio_logger=True)

# ------------------------------------------------------------------

class NotificationNamespace(Namespace):
    def on_notf1(self, data):
        print(f"Received notf1 in /notification namespace: {data}")
        self.emit('response', {'message': 'Notification 1 received'}, namespace='/notification')

    def on_notf2(self, data):
        print(f"Received notf2 in /notification namespace: {data}")
        self.emit('response', {'message': 'Notification 2 received'}, namespace='/notification')

class ChatNamespace(Namespace):
    def on_chat1(self, data):
        print(f"Received chat1 in /chat namespace: {data}")
        self.emit('response', {'message': 'Chat 1 received'}, namespace='/chat')

    def on_chat2(self, data):
        print(f"Received chat2 in /chat namespace: {data}")
        self.emit('response', {'message': 'Chat 2 received'}, namespace='/chat')

@webRTC.route('/')
def index():
    print("Hello webRTC...")
    return "Hello webRTC..."

socketio.on_namespace(NotificationNamespace('/notification'))
socketio.on_namespace(ChatNamespace('/chat'))

def init_app(app):
    socketio.init_app(app, cors_allowed_origins="*")
    #socketio.init_app(app, cors_allowed_origins="http://localhost:6060")
