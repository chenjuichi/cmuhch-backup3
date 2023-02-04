<template>
  <v-app ref="barcode">
    <v-container class="scroll-y">
      <v-layout align-center justify-center id="layout">
        <v-flex xs12>
          <v-col class="text-right">
            <!--
            <v-btn color="primary" dark class="mb-2" v-print="printObj" @click="printBarcode">
              <v-icon left dark>mdi-printer</v-icon>列印
            </v-btn>
            -->
            <v-btn color="primary" dark class="mb-2" @click="printBarcode">
              <v-icon left dark>mdi-printer</v-icon>列印
            </v-btn>

          </v-col>
          <v-btn v-scroll="onScroll" v-show="fab" fab dark fixed bottom right color="primary"
              @click="toTop"
          >
            <v-icon>keyboard_arrow_up</v-icon>
          </v-btn>
        </v-flex>
      </v-layout>

      <v-layout align-center justify-center>
        <v-flex xs12>
          <v-card id="printMe">
          <div v-for="(field, index) in barcode_data" :key="index" class="container_barcode">
            <!--<div>中國醫藥大學新竹附設醫院</div>-->
            <ul>
              <li>{{field.stockInTag_reagName }}</li>
            </ul>

            <barcode :value="field.stockInTag_reagID"></barcode>
            <div style="font-size: 10px; display: flex; justify-content: flex-start; margin-left:20px;">
              LOT: {{ field.stockInTag_batch }}
            </div>
            <div class="word">
              <span style="font-size: 12px; margin-left:20px; position: relative; top: -10px;">
                入庫日期: {{ field.stockInTag_Date }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              </span>
              <span style="font-size: 32px; position: relative; top: 15px;">
                {{ field.stockInTag_alpha }}
              </span>
            </div>
            <div style="font-size: 12px; font-weight:600; display: flex; justify-content: flex-start; margin-left:20px; position: relative; top: -15px;">
              入庫人員: {{ field.stockInTag_Employer }}
            </div>
            <div style="font-size: 12px; display: flex; justify-content: flex-start; margin-left:20px; position: relative; top: -15px;">
              保存溫度: {{ field.stockInTag_Employer }}
            </div>
            <v-spacer></v-spacer>
          </div>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-app>
</template>

<script>
import VueBarcode from 'vue-barcode';
import * as easings from 'vuetify/lib/services/goto/easing-patterns';
//import print from 'vue-print-nb';

import axios from 'axios';
import Common from '../mixin/common.js'

export default {
  name: 'BarCode',

  mixins: [Common],

  components: {
    'barcode': VueBarcode,
  },

  props: ['barcode_data'],

  //directives: {
  //  print
  //},

  mounted() {
    console.log("BarCode, mounted()...");

    this.startTimer();
  },

  created() {
    console.log("BarCode, created()...");

    this.initAxios();
  },

  computed: {

  },

  watch: {
    barcode_data (val) {
      if ('stockInTag_cnt' in this.barcode_data[0]) {
        this.temp_barcode_data =  JSON.parse(JSON.stringify(this.barcode_data));
        console.log("----bar1, ", this.barcode_data);
        console.log("----bar2, ", this.temp_barcode_data);
      } else {
        let temp_len = this.barcode_data.length;
        this.temp_barcode_data= [];
        for (let i=0; i < temp_len; i++) {
          let obj= {
            stockInTag_reagID: this.barcode_data[i].stockOutTag_reagID,
            stockInTag_batch: this.barcode_data[i].stockOutTag_batch,
            stockInTag_Date: this.barcode_data[i].stockOutTag_Out_Date,        //在列印條碼時, 此對應道出庫日期
            stockInTag_Employer: this.barcode_data[i].stockOutTag_Employer,
            stockInTag_reagTemp: this.barcode_data[i].stockOutTag_reagTemp,
            stockInTag_alpha: this.barcode_data[i].stockOutTag_alpha,
            stockInTag_cnt: this.barcode_data[i].stockOutTag_cnt,
            stockInTag_reagName: this.barcode_data[i].stockOutTag_reagName,
          }
          this.temp_barcode_data.push(obj);
        }
        console.log("----bar1, ", this.barcode_data);
        console.log("----bar2, ", this.temp_barcode_data);
      }
    }
  },

  data() {
    return {
      fab: false,

      tosterOK: false,

      myTimer: '',            //在component內設定timer, timer的handle
      myTimerId: '',          //timer的id
      svg_change: true,
      temp_barcode_data: []
    };
  },

  destoyed() {
    clearInterval(this.myTimer);
  },

  beforeRouteLeave(to, from, next) {
    clearInterval(this.myTimer);
    next();
  },

  methods: {
    printBarcode() {
      console.log("click, printBarcode()...", this.barcode_data);
      this.exportToCSV();
      this.$emit('pressPrint', true);
    },

    exportToCSV() {
     //let object_Desserts = Object.assign([], this.barcode_data);
      let barcode_Desserts = Object.assign([], this.barcode_data);

      let object_Desserts = barcode_Desserts.map(({
        stockInTag_reagID,
        stockInTag_batch,
        stockInTag_Date,
        stockInTag_Employer,
        stockInTag_reagTemp,
        stockInTag_alpha,
        stockInTag_cnt,
        stockInTag_reagName,
      }) => ({
        stockInTag_reagID,
        stockInTag_batch,
        stockInTag_Date,
        stockInTag_Employer,
        stockInTag_reagTemp,
        stockInTag_alpha,
        stockInTag_cnt,
        //stockInTag_reagName,
        name1: stockInTag_reagName.length > 25 ? stockInTag_reagName.slice(0,25) : stockInTag_reagName,
        name2: stockInTag_reagName.length > 25 ? stockInTag_reagName.slice(25) : ' '
      }))
      console.log("StockInTagPrint, exportToCSV, Axios post data..., ", barcode_Desserts, object_Desserts);

      const path = '/exportToCSVForStockIn';
      var payload= {
        blocks: object_Desserts,
        count: object_Desserts.length,
      };
      axios.post(path, payload)
      .then((res) => {
        console.log("export into csv status: ", res.data.status, res.data.outputs)
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          //this.snackbar_color='#008184';
          //this.snackbar=true;
          //this.snackbar_info= '庫存記錄('+ res.data.outputs + ')轉檔完成!';
          //this.snackbar_icon_color= "#ffffff";
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
          //this.snackbar_color='red accent-2';
          //this.snackbar=true;
          //this.snackbar_info= '存檔錯誤!';
          //this.snackbar_icon_color= '#adadad';
        }
      })
      .catch((error) => {
        console.error("axios error, code: ",error);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        //this.snackbar_color='red accent-2';
        //this.snackbar=true;
        //this.snackbar_info= '存檔錯誤!';
        //this.snackbar_icon_color= '#adadad';
      });
    },

    startTimer() {
      this.myTimer = setInterval(() => {
        //if (this.svg_change) {
          let bars = document.getElementsByClassName('container_barcode');

          for (let j=0; j<bars.length; j++) {
            let dot = bars[j].childNodes[1].childNodes[0];
            dot.setAttribute("height", "90px");

            this.svg_change=false;
          }
        //}

        let elem = document.querySelector('#layout');
        if(!elem) return;
        let myPos=elem.getBoundingClientRect().top;
        //console.log('calling handleScroll: ', myPos);
        this.fab = myPos <= 10;
      }, 500);

      this.myTimerId = this.myTimer._id;
    },

    onScroll (e) {
      //if (typeof window === 'undefined') return
      //const top = window.pageYOffset || e.target.scrollTop || 0
      //this.fab = top > 20
    },

    toTop () {
      //this.$vuetify.goTo(0)
      document.getElementById("layout").scrollIntoView();
    },
  },
}
</script>

<style scoped>
ul {
  list-style-type: none;
}

li{
  max-width:200px;
  word-wrap:break-word;
  font-size: 14px;
  bottom: -20px;
  position: relative;
  margin-left:20px;
}

container_barcode {
  text-align:center;
}

newSvgAttr {
  height: 80px !important;
}

.word {
  display:table-cell;
  vertical-align:middle;
  /*display: flex;
  justify-content: flex-start;
  float: left;*/
  height: 36px;
}
</style>