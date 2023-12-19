<template>
    <div>
      <!-- ... (其他部分不變) -->
      <input v-model="message" placeholder="Type a message" />
      <button @click="sendMessage">Send Message</button>
    </div>
  </template>

  <script>
  import io from 'socket.io-client';

  export default {
    // ... (其他部分不變)
    methods: {
      initWebSocket() {
        let _host=window.location.host;
        _host = _host.slice(0, _host.lastIndexOf(":"));
        let _protocol=window.location.protocol;
        this.socket = io(_protocol + "//"+ _host + ':6060' +'/webrtc');  // 修改 URL
        this.socket.on('message', (message) => {
          console.log('Received message from server:', message);
          // 在這裡處理從伺服器接收到的訊息
        });
      },
      // ... (其他部分不變)
    },
  };
  </script>