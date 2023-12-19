<template>
    <div>
      <video ref="localVideo" autoplay></video>
      <video ref="remoteVideo" autoplay></video>
      <button @click="startCall">Start Call</button>
      <input v-model="message" placeholder="Type a message" />
      <button @click="sendMessage">Send Message</button>
    </div>
  </template>

  <script>
  //import io from 'socket.io-client';

	import SocketIO from 'socket.io-client';
	import VueSocketIO from 'vue-socket.io';

  export default {
    data() {
      return {
        localStream: null,
        remoteStream: null,

        socket: null,
        message: '',
      };
    },
    mounted() {
			console.log("webRTC created()")
      this.initLocalVideo();

			// 在 /notification 命名空間中觸發 notf1 事件
			//this.socket.emit('/notification/notf1', { data: 'Notification 1 data from client' });

			// 在 /chat 命名空間中觸發 chat1 事件
			//this.socket.emit('/chat/chat1', { data: 'Chat 1 data from client' });
    },
		created() {
			console.log("webRTC created...")
			this.initWebSocket();
    	// 發送訊息到服務器
    	//this.socket.emit('message', { text: 'Hello, server!' });
  	},
    methods: {
      async initLocalVideo() {
        // ... (與之前相同的初始化本地影像的邏輯)
      },
      startCall() {
        // ... (WebRTC 連接的邏輯)
      },
      initWebSocket() {
				console.log("begin webRTC mountting...")
				let _host = window.location.host;
				_host = _host.slice(0, _host.lastIndexOf(":"));
				console.log(_host);
				let _protocol = window.location.protocol;
				console.log(_protocol);
				let wsProtocol = _protocol === 'https:' ? 'wss:' : 'ws:';
				let _port = 6060;
				// 在這裡進行 Socket.IO 的區域宣告
				this.socket = SocketIO(`${_protocol}//${_host}:${_port}/webrtc`);
				//this.socket = SocketIO('http://192.168.32.50:6060/webrtc');
				this.socket.connect();
				console.log("end webRTC mountting...")

      },

      sendMessage() {
        if (this.message.trim() !== '') {
        	console.log('Send message from client:', this.message);

          this.socket.emit('message', this.message);
          //this.socket.emit('message', this.message);
          this.message = '';
        }
      },
      // ... (其他 WebRTC 相關邏輯)
    },
  };
  </script>

  <style>
  /* 在這裡添加樣式 */
  </style>