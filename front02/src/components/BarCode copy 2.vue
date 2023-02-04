<template>
  <v-app ref="barcode">
    <v-container class="scroll-y">
      <v-layout align-center justify-center>
        <v-flex xs12>
          <v-col class="text-right">             
          <!--
          <v-btn color="primary" dark class="mb-2" @click="printBarcode">
            <v-icon left dark>mdi-keyboard-return</v-icon>返回
          </v-btn>
          &nbsp;&nbsp;
          -->
            <v-btn color="primary" dark class="mb-2" @click="printBarcode">
              <v-icon left dark>mdi-printer</v-icon>列印
            </v-btn>
          </v-col>
          <v-btn v-scroll="onScroll" v-show="fab" fab dark fixed bottom right color="primary"
            @click="$vuetify.goTo(target, options)" 
          >                     
            <v-icon>keyboard_arrow_up</v-icon>
          </v-btn>
    
        <!--<v-row align="center" justify="center" v-scroll.self="onScroll1">-->            
          <v-card width="24vw">
            <div v-for="(field, index) in barcode_data" :key="index" style="text-align:center" ref="card">
              <div>中國醫藥大學新竹附設醫院</div>
              <barcode :value="field.stockInTag_reagID">
                Show this if the rendering fails.
              </barcode>
              <span>入庫人員: {{ field.stockInTag_Employer }}</span>
              <v-spacer></v-spacer>
            </div>  
            <!--
            <div>中國醫藥大學新竹附設醫院</div>
            <barcode :value="1234567890" lineColor="#007bff"></barcode>
            <span>入庫人員: {{}}</span>
            -->
          </v-card>          
        <!--</v-row>-->
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>  

<script>
import VueBarcode from 'vue-barcode';
import * as easings from 'vuetify/lib/services/goto/easing-patterns';

export default {
  name: 'BarCode',

  components: {
    'barcode': VueBarcode,
  },

  props: ['barcode_data'],

  mounted() {
    console.log("BarCode, mounted()...");

    //this.startTimer();

    
    



    //document.addEventListener("scroll", this.handleScroll);

    //let elem = document.querySelector('#scroll-target');
    //this.rect = elem.getBoundingClientRect();
    
    //let myScroll = document.querySelector("#scroll-target");
    //is.myScroll.addEventListener("scroll", this.handleScroll);
    //window.addEventListener("scroll", this.handleScroll);
    //let elem = document.querySelector('#scroll-target');
    //this.rect = elem.getBoundingClientRect();
    /*
    this.myScroll.addEventListener("scroll", event => {
      output.innerHTML = `scrollTop: ${this.myScroll.scrollTop}`;
    }, { passive: true });
    */
    //document.querySelector('#scroll-target').addEventListener('scroll', function() { alert("HOVER2") })
  },

  created() {
    console.log("BarCode, created()...");
  },

  computed: {
    target () {
      const value=80;
      return value;
    },

    options () {
      return {
        duration: this.duration,
        offset: this.offset,
        easing: this.easing,
      }
    },
    element () {
      //return this.$refs.card;
      //return this.$refs.myNavDrawer;
      //if (this.selected === 'Button') return this.$refs.button
      //else if (this.selected === 'Radio group') return this.$refs.radio
      //else return null
    },
  },
  
  watch: {
    'rect': function () {
      console.log("position: ", this.rect.top);
    },

  },
  
  data() {
    return {
      fab: false,

      rect: [],
      myTimer: '',            //在component內設定timer, timer的handle
      myTimerId: '',          //timer的id

      myScroll: null,

      duration: 300,
      offset: 0,
      easing: 'easeInOutCubic',
      easings: Object.keys(easings),
    };
  },

  methods: {
    printBarcode() {
      console.log("click, printBarcode()...");    
    },

    startTimer() {
      this.myTimer = setInterval(() => {
        let elem = document.querySelector('#myNavDrawer');
        if(!elem) return;
        let myPos=elem.getBoundingClientRect().top;
        console.log('calling handleScroll: ', myPos);
        this.fab = myPos <= -100;

        //if (elem.getBoundingClientRect().top <= -100 || null) {
        //  console.log('calling handleScroll...');
        //  this.fab=true;
          //console.log('calling handleScroll: ', this.rect.top);
          //if (this.rect.top < -300)
          //  this.$vuetify.goTo(target, options);
        //}
      }, 500 );

      this.myTimerId = this.myTimer._id;
    },

    onScroll (e) {      
      if (typeof window === 'undefined') return
      const top = window.pageYOffset || e.target.scrollTop || 0
      this.fab = top > 20
    },

    //onScroll1 (e) {
    //  console.log("onScroll.... ", e.target.scrollTop);      
//
    //},

    handleScroll(e) {
    //  // Any code to be executed when the window is scrolled
    //  this.isUserScrolling = (window.scrollY > 0);
    //console.log('calling handleScroll: ', this.myScroll.pageYOffset, this.myScroll.scrollY, e.target.scrollTop);
    //console.log('calling handleScroll: ', window.top.scrollY, e.target.scrollTop, e.clientHeight, this.rect);
    
    //let elem = document.querySelector('#scroll-target');
    //this.rect = elem.getBoundingClientRect();
    //console.log('calling handleScroll: ', this.rect.top);

    //const left = this.$refs.card.clientHeight
    //const top = this.$refs.card.getBoundingClientRect().top;
    //window.top.scrollY /* or: e.target.documentElement.scrollTop */
    },
    //toTop () {
    //  this.$vuetify.goTo(0)
    //  //this.$vuetify.goTo(this.$refs.actions, { container: this.$refs.card });
    //}
  },

  beforeDestroy() {
    // Detach the listener when the component is gone
    //this.myScroll.removeEventListener('scroll', this.handleScroll)
    
    //document.removeEventListener('scroll', this.handleScroll)
  },

  //destoyed() {
  //  clearInterval(this.myTimer);
  //}, 

  //beforeRouteLeave(to, from, next) {    
  //  clearInterval(this.myTimer);
  //  next();
  //},  
}
</script>

<style scoped>
#scroll-target {
  overflow: scroll;
}
</style>