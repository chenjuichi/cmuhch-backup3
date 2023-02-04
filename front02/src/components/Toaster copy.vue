<template>
  <v-app id="toster">
    <div class="wrap">
      <!--<transition name="fade">-->
      
        <!--<div v-show="show" class="block">--> 
        <div class="block"> 
          {{ content.body }}
          <v-btn icon color="primary" @click="remove">
            <v-icon dark>mdi-close-circle</v-icon>
          </v-btn>                 
        </div>
      <!--</transition>-->
    </div>  
  </v-app>
</template>

<script>

export default {
  name: 'Toaster',

  props: [
    'Title', 'Type', 'Body', 'Timeout' 
  ],

  mounted() {
    //this.initTimer();
  },

  data() {
    return {
      timer: null,
      time: 2,
      show: true,

      defaults: {
        title: 'undefined title',
        body: 'undefined body',
        timeout: 5 
      },

      //content: [],
      content: {},
    };
  },

  created() {
    this.add({ title: this.Title, type: this.Type, body: this.Body, timeout: parseInt(this.Timeout) })
  },

  beforeDestroy () {
    clearInterval(this.timer);
  },

  methods: {
    initTimer() {
      //this.time=3;
      this.timer=setInterval(this.countdown, 1000);
    },

    countdown() {
      //this.time--;
      this.timeout--;
      //if (this.time==0) {
      if (this.timeout==0) {
        clearInterval(this.timer);
        //this.show=false;
        this.remove(0);
      }
    },

    add(params) {
      /*
      for (let key in this.defaults) {
        //console.log("key:", key)
        if (params[key] === undefined) {
          //console.log("b, params[key]:", params[key])
          params[key] = this.defaults[key];
          //console.log("a, default[key]:", this.defaults[key])
        }
      }
      */
      params.created = Date.now();
      //params.id = Math.random();
      params.id = 1;

      console.log("toaster params: ", params);
      
      //params.expire = setTimeout(() => {this.remove(params.id);}, params.timeout * 1000);
      params.expire = setTimeout(() => {this.countdown();}, params.timeout * 1000);

      console.log("params: ", params)
      this.content = Object.assign({}, params);
    },

    remove() {
      //this.content = {};
      this.$emit('removeToaster', false);  
    },

    //index(id) {
    //  for (let key in this.content) {
    //    if (id === this.content.id) {
    //      return key;
    //    }
    //  }
    //},

    type(type) {
      switch (type) {
        case 'error':
          return 'error';
        case 'success':
          return 'success';
        case 'info':
          return 'info';
      }
    },
  },


};
</script>

<style scoped>

#toster {
  position: relative;
  display: block;
  font-size: 1rem; 
  height: 42px;  
}

.wrap {
  width: 300px;
  height: 42px;
  overflow: hidden;
  float: left;
}

.block {
  width: 300px;
  height: 42px;
  text-align: center;
  background-color: #ffc1b0;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 3s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.fade-enter-to, .fade-leave-from {
  opacity: 1;
}

/*
.fade-enter-active {
  animation: fadeIn ease 2s forwards;
}

.fade-leave-active {
  transition: opacity 2s ease-in;
}

.fade-leave-to {
  opacity: 0;
}

@keyframes fadeIn {
  0% {
    visibility: hidden;
    opacity: 0;
  }

  75% {
    visibility: hidden;
    opacity: 0;
  }

  100% {
    visibility: visible;
    opacity: 1;
  }
}
*/
</style>