<template>
  <v-app>
  <v-container fluid>
    <v-snackbar v-model="snackbar" :color="snackbar_color" :right='snackbar_right' :top='snackbar_top'>
      {{ snackbar_info }}
      <template v-slot:action="{ attrs }">
        <v-btn icon :color="snackbar_icon_color" @click="snackbar= false">
          <v-icon dark>mdi-close-circle</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
    <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
      <v-card class="overflow-hidden mx-auto mt-3" width="95vw">
        <v-toolbar flat color="#7DA79D" height="90vw" >
          <v-row dense style="margin-bottom: -36px; margin-top: -12x;">
            <v-col cols="12" md="2" class="mr-1" style="position: relative; top: -15px;">
              <v-text-field
                v-model="stockOutTag_reagID"
                label="資材碼"

                style="position:relative; top: 15px;"
                :value="stockOutTag_reagID"
                @keyup.native.enter="handleUpdateItem($event)"
                @keyup.native.backspace="handleBackspace($event)"
                @paste="handlePaste"
              ></v-text-field>

              <!--<v-select
                :items="reagentForSelect"
                label="資材碼"
                style="position:relative; top: 10px;"
                dense
                outlined
                item-color="red"
                v-model="stockOutTag_reagID"
              ></v-select>-->
            </v-col>

            <v-col cols="12" md="3" class="mr-2">
              <v-text-field
                v-model="stockOutTag_reagName"
                label="品名"
                :value="stockOutTag_reagName"
                readonly
                style="width: 300px !important; max-width: 270px !important;"
              ></v-text-field>
            </v-col>

            <v-col cols="12" md="2"
              class="mr-2"
              style="position: relative; top: 5px; left:20px; font-weight: bold; width: 120px !important; max-width: 120px !important;">
              {{stockOutTag_station}}站/{{stockOutTag_layout}}層/{{stockOutTag_pos}}格
            </v-col>

            <v-col cols="12" md="1" align="right" style="position: relative; top: 5px;">
              <!--<span class="text-decoration-underline">&nbsp;&nbsp;領料數量</span>-->
              <span class="stockout_str" style="display:table-cell; vertical-align:middle; font-weight: bold; font-size: 1em;">領料數量</span>
            </v-col>

            <v-col cols="12" md="2" align="left" class="pl-0 mx-1" style="max-width:120px; width=120px;">
              <vue-numeric-input
                v-model="stockOutTag_cnt"
                :min="1"
                :max="stockOutTag_max_cnt"
                :step="1"
                size="small"
                align="center"
              ></vue-numeric-input>
              <span class="stockout_str" style="position: relative; top: -20px; right: -105px; font-weight: bold; font-size: 1em;">
                {{stockOutTag_unit}}
              </span>
            </v-col>

            <v-col cols="12" md="1" align="right" class="pl-0 mx-1" style="max-width: 70px; width=120px; text-align: center; position:relative; top:-10px;">
              <!--<img v-show="stockOutTag_reagID!=''" v-on:click="redirect_to_mqtt" :src="home_url" alt="Loading" style="height: 3vw;" v-bind:alt="pic">-->
              <img v-show="stockOutTag_reagID!=''" @click="redirect_to_mqtt" :src="home_url" alt="Loading" style="height: 3vw;">
            </v-col>

            <v-col cols="12" md="1" align="center" class="pl-0 mx-1" style="text-align: center; position:relative; top:-12px;">
              <!--<v-btn v-show="isOK" @click="redirect_ok" color="success" rounded style="font-weight: bold; font-size: 0.9em;">-->
              <v-btn
                  v-show="isOK"
                  @click="mqttForStationOff"
                  color="success"
                  rounded
                  style="font-weight: bold; font-size: 0.9em; position:relative; top:10px;">
                  <!--<v-icon>mdi-domain</v-icon>-->完成
              </v-btn>
            </v-col>
          </v-row>
        </v-toolbar>
        <v-sheet class="overflow-y-auto" max-height="600">
          <v-container>
            <v-list three-line>
              <v-list-item-group v-model="model" mandatory color="indigo" @change="listActionClick_m(model)">
                <!--<template v-for="(item, index) in items">-->
                  <!--<v-list-item :key="item.stockOutTag_reagName">-->
                <!--<template v-for="(item, index) in filteredItems">-->
                <template v-for="(item, index) in items">
                  <v-list-item>
                    <template v-slot:default="{ active }">
                      <v-list-item-content>
                        <!--<v-list-item-title class="font-weight-bold" v-text="`品名:${item.stockOutTag_reagName}    領料數量: ${item.stockOutTag_cnt}`"></v-list-item-title>-->
                        <v-list-item-title class="font-weight-bold">
                          <span>資材碼:{{item.stockOutTag_reagID}}</span>&nbsp;&nbsp;
                          <span>品名:{{item.stockOutTag_reagName}}</span>&nbsp;&nbsp;
                          <span class="text-decoration-underline">領料數量: {{item.stockOutTag_cnt}}&nbsp;&nbsp;{{item.stockOutTag_unit}}</span>
                        </v-list-item-title>
                        <v-list-item-subtitle class="mb-3" v-text="`效期:${item.stockOutTag_reagPeriod}  保存溫度: ${item.stockOutTag_reagTemp}  批號: ${item.stockOutTag_batch}`"></v-list-item-subtitle>

                        <v-list-item-subtitle class="text--primary font-weight-bold" v-text="`領料人員: ${item.stockOutTag_Employer}  領料日期: ${item.stockOutTag_Date}`"
                        ></v-list-item-subtitle>
                      </v-list-item-content>

                      <v-list-item-action>
                      <!--<v-list-item-action @click="listActionClick(index, active)">-->
                        <!--<v-list-item-action-text v-text="item.stockOutTag_batch"></v-list-item-action-text>-->
                        <!--<img v-show="active" :src="home_url" alt="Loading" style="height: 2.5vw;">-->
                        <v-icon v-if="!active" color="grey lighten-1">
                          mdi-star-outline
                        </v-icon>
                        <v-icon v-else color="yellow darken-3">
                          mdi-star
                        </v-icon>
                        <div v-show="active">{{item.grid_station}}站/{{item.grid_layout}}層/{{item.grid_pos}}格</div>
                      </v-list-item-action>
                    </template>
                  </v-list-item>

                  <v-divider v-if="index < items.length - 1" :key="index"></v-divider>
                </template>
              </v-list-item-group>
            </v-list>
          </v-container>
        </v-sheet>
      </v-card>

      <v-dialog
        v-model="isEmptyRecord"
        transition="dialog-bottom-transition"
        persistent
        max-width="600"
      >
        <v-card>
          <v-toolbar
            color="primary"
            dark
          >訊息!</v-toolbar>
          <v-card-text>
            <div class="text-h4 pa-12">領料完成或暫無待出庫試劑...</div>
          </v-card-text>
          <v-card-actions class="justify-end">
            <v-spacer></v-spacer>
            <v-btn text @click="routeNavbar"> 離開 </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>

    <v-row align="center" justify="space-around" v-else>
        <v-dialog
          v-model="permDialog"
          transition="dialog-bottom-transition"
          max-width="500"
        >
          <v-card>
            <v-toolbar
              color="primary"
              dark
            >錯誤訊息!</v-toolbar>
            <v-card-text>
              <div class="text-h4 pa-12">使用這項功能, 請通知管理人員...</div>
            </v-card-text>
            <v-card-actions class="justify-end">
              <v-spacer></v-spacer>
              <v-btn text @click="permCloseFun"> 取消 </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
    </v-row>
  </v-container>
   </v-app>
</template>

<script>
import axios from 'axios';
import VueNumericInput from 'vue-numeric-input';

//import logo from '../../assets/image/icons8-light-on.gif'
import logo from '../../assets/image/icons8-light-on-unscreen.gif'
import logoR from '../../assets/image/icons8-light-on-R-m.gif'
import logoY from '../../assets/image/icons8-light-on-Y-m.gif'
import logoG from '../../assets/image/icons8-light-on-G-m.gif'
import _ from 'lodash'

import Common from '../../mixin/common.js'

export default {
  name: 'StockOut',

  mixins: [Common],

  components: {
    VueNumericInput,
  },

  mounted() {
    // if back button is pressed
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));
    };
    //
    //this.stockOutTag_cnt=this.items[this.model].stockOutTag_cnt;
    //this.stockOutTag_max_cnt=this.items[this.model].stockOutTag_cnt;

    //this.stockOutTag_min_cnt=1;
    //this.stockOutTag_reagID=this.items[this.model].stockOutTag_reagID;
    //this.stockOutTag_reagName=this.items[this.model].stockOutTag_reagName;
    //this.items[this.model].active=true;
    //
  },

  data: () => ({
    currentUser: {
      	//empID: null,
        //name: null,
				//dep: null,
        //perm: 0,    //member: 2, admin: 1, none:0
    },
    permDialog: false,

    snackbar: false,
    snackbar_color: 'success',
    snackbar_right: true,
    snackbar_top: true,
    snackbar_info: '',
    snackbar_icon_color: '#adadad',

    default_home_url: logo,
    home_url: logo,
    home_url_R: logoR,
    home_url_Y: logoY,
    home_url_G: logoG,

    stockOutTag_reagID: '',
    stockOutTag_reagName: '',

    stockOutTag_station: '',
    stockOutTag_layout: '',
    stockOutTag_pos: '',

    stockOutTag_cnt: 0,
    current_cnt:0,
    stockOutTag_min_cnt: 0,
    stockOutTag_max_cnt: 0,
    stockOutTag_unit: '', //add

    currentIndex: 0,
    currentLedStation: 1,
    currentLedLayout: 1,
    currentLedPos: 1,
    currentLedRange_begin: 1,
    currentLedRange_end: 2,

    all_station: 1,     // 2023-10-31 add
    all_layout: 1,      // 2023-10-31 add

    current_unit: '',   //add

    pre_topic: 0,

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },

    grids: [],
    temp_grids : [],

    isSort: true,   //textfield輸入資材碼
    isOK: false,    //是否顯示領料完成的按鍵
    isEmptyRecord: false,
    emptyRecordReady: false,

    //selected: [2],
    model: 0,

    items: [ ],
    temp_items : [],

    reagentForSelect: [],
    stockout_record: {},

    mqtt_topic:['station1','station2','station3'],

    load_SingleTable_ok: false, //for get employer table data
    load_2thTable_ok: false,    //for get reagent table data
    load_3thTable_ok: false,
    load_4thTable_ok: false,
    load_5thTable_ok: false,

    load_6thTable_ok: false,    // 2023-11-1 add
    load_7thTable_ok: false,    // 2023-11-1 add
  }),

  computed: {
    filteredItems() {
    //透過filter()函式的第一參數, 進行callback函式所指定的過濾條件，並返回一個新陣列
    //透過includes(), 回傳是否包含該元素的Boolean值，true代表包含，false則代表不包含
      let temp_array=[];
      temp_array=
        _.orderBy(this.items.filter(item => {
        return item.stockOutTag_reagID.toLowerCase().includes(this.stockOutTag_reagID.toLowerCase());
      }), 'stockOutTag_reagID');
      //console.log("filter: ", temp_array)
      return temp_array;
    },
  },

  watch: {
    stockOutTag_reagID (val) {
      this.fromReagIdDisp();
    },

    currentIndex(newVal, oldVal) {
      console.log("new/old currentIndex: ", newVal, oldVal)
    },

    load_SingleTable_ok(val) {
      console.log("load_SingleTable_ok, desserts: ", val);

      if (val) {
        this.items = Object.assign([], this.temp_items);
        this.load_SingleTable_ok=false;

        this.listStockOutGrids();
      }
    },

    load_2thTable_ok(val) {
      console.log("load_2thTable_ok, products: ", val)

      if (val) {
        this.grids = Object.assign([], this.temp_grids);

        this.load_2thTable_ok=false;

        this.addGrids();
      }
    },

    load_3thTable_ok(val) {
      console.log("load_3thTable_ok: ", val);

      if (val) {
        this.load_3thTable_ok=false;
        this.addStockOutItem();
      }
    },

    load_4thTable_ok(val) {
      console.log("load_4thTable_ok: ", val);

      if (val) {
        this.load_4thTable_ok=false;
      }
    },

    load_5thTable_ok(val) {
      console.log("load_5thTable_ok: ", val);

      if (val) {
        this.load_5thTable_ok=false;
        this.isOK=false;
        console.log("StockIn, load_5thTable_ok, isOk: ", this.isOK);
        this.home_url=this.default_home_url;    //2023-1-12 add

        if (this.emptyRecordReady)      //2023-02-14 add
          this.isEmptyRecord = true;    //2023-02-14 add
      }
    },
    // 2023-11-1 add these watches
    load_6thTable_ok(val) {
      console.log("load_6thTable_ok: ", val);

      if (val) {
        this.load_6thTable_ok=false;
        this.mqttForAllStationOff();
      }
    },

    load_7thTable_ok(val) {
      console.log("load_7thTable_ok: ", val);

      if (val) {
        this.load_7thTable_ok=false;
        this.mqttForAllStationHWOff();
      }
    },
    //
  },

  created () {
    console.log('%cStockOut.vue create()...', 'background-color: yellow; font-size: larger;');

    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm == 0) {
      this.permDialog=true;
      //console.log("router undefine!")
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page;
    //this.load_SingleTable_ok=false;     // 2023-10-30
    this.initAxios();

    //this.listStockOutItems();           // 2023-10-30

    this.initialize();                    // 2023-10-30
  },

  methods: {
    initialize () {
      this.mqttForAllStationHWOff();      // 2023-11-1 add

      this.load_SingleTable_ok=false;
      this.listStockOutItems();
    },

    listStockOutItems() {
      const path = '/listStockOutItems';
      console.log("listStockOutItems, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_items = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        if (!res.data.status) {
          this.isEmptyRecord=true;
        } else {
          this.reagentForSelect = this.temp_items.map(function(p) {  //
            return p.stockOutTag_reagID;
          });
          this.reagentForSelect = [...new Set(this.reagentForSelect)];  //去除重複項目
          this.load_SingleTable_ok=true;
        }
      })
      .catch((error) => {
        console.error(error);
        console.log("通訊錯誤!");
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '通訊錯誤!';
        this.snackbar_icon_color= '#adadad';
        this.load_SingleTable_ok=false;
      });
    },

    listStockOutGrids() {
      const path = '/listStockOutGrids';
      console.log("listStockOutGrids, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_grids = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_2thTable_ok = true;
      })
      .catch((error) => {
        console.error(error);
        console.log("通訊錯誤!");
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '通訊錯誤!';
        this.snackbar_icon_color= '#adadad';
        this.load_2thTable_ok = false;
      });
    },

    routeNavbar() {
      this.isEmptyRecord = false;
      this.$router.push('Navbar');
    },

    addStockOutItem() {  //新增 後端table資料
      console.log("---click addStockOutItem data---", this.stockout_record);

      const path='/addStockOutItem_m';
      let object = Object.assign({}, this.stockout_record);
      console.log("OutTagID: ", object, this.stockOutTag_cnt)
      let cnt = object.stockOutTag_cnt!=this.stockOutTag_cnt ? Math.abs(object.stockOutTag_cnt - this.stockOutTag_cnt):this.stockOutTag_cnt;
      console.log("OutTagID, cnt: ", cnt)
      var payload= {
        OutTagID: object.id,
        OutTagCount: object.stockOutTag_cnt,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("add StockOut data, status: ", res.data.status);
        //this.tosterOK = res.data.status? false:true;  ////false: 關閉錯誤訊息畫面
        this.load_4thTable_ok = true;
      })
      .catch(err => {
        console.error(err);
        //this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        this.load_4thTable_ok = false;
      });
    },

    handlePaste (evt) {
      console.log('on paste', evt.clipboardData.getData('text'))

      //console.log('on paste', evt.clipboardData.getData('text/plain'))
    },

    handleBackspace (e) {
      console.log("press backspace...");
      this.stockOutTag_reagID='';
    },

    handleUpdateItem (e) {
      console.log("press return...");

      let matchResult = this.items.find(x => x.stockOutTag_reagID === this.stockOutTag_reagID);
      if (typeof(matchResult) == 'undefined') {
        console.log("stockOutTag_reagID is undefined...");

        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '領料資材碼錯誤!';
        this.snackbar_icon_color= '#adadad';
        this.load_SingleTable_ok=false;
      }
      //else {
        this.fromReagIdDisp();
      //}
    },

    async mqttForStation() {
      console.log("mqttForStation...");

      let path='/mqtt/station';
      let temp_layout=this.currentLedLayout;
      let range_begin=this.currentLedRange_begin;
      let range_end=this.currentLedRange_end;
      console.log("station: " +"layout: " + temp_layout + " begin: " + range_begin + " end: " + range_end, this.model, this.items[this.model])
      let temp_sw= 'flash';
      let myTopic=this.mqtt_topic[parseInt(this.currentLedStation) - 1]
      let payload= {
        topic: myTopic,
        layout: temp_layout,
        pos_begin: range_begin,
        pos_end: range_end,
        msg: temp_sw,
      };

      try {
        let res = await axios.post(path, payload);
        console.log("mqtt ok", res.data.status);
        this.pre_topic=myTopic;     //2023-1-5 add
        this.load_3thTable_ok=true;
      } catch (err) {
        console.error(err)
        console.log("通訊錯誤!");
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '通訊錯誤!';
        this.snackbar_icon_color= '#adadad';
        this.load_3thTable_ok=false;
      }
    },

    async mqttForStationOff() {
      console.log("mqttForStationOff...");

      let path='/mqtt/station';
      // 2023-10-31 modify the following block
      let temp_sw= 'off';
      let temp_layout=this.currentLedLayout;
      let range_begin=this.currentLedRange_begin;
      let range_end=this.currentLedRange_end;
      let myTopic=this.mqtt_topic[parseInt(this.currentLedStation) - 1]
      console.log("station: " +"layout: " + temp_layout + " begin: " + range_begin + " end: " + range_end, this.model, this.items[this.model])
      let payload= {
        topic: myTopic,
        layout: temp_layout,
        pos_begin: range_begin,
        pos_end: range_end,
        msg: temp_sw,
      };
      //
      try {
        let res = await axios.post(path, payload);
        console.log("Led has been powered off, mqtt ok", res.data.status);
        this.load_5thTable_ok=true;
      } catch (err) {
        console.error(err)
        console.log("通訊錯誤!");
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '通訊錯誤!';
        this.snackbar_icon_color= '#adadad';
        this.load_5thTable_ok=false;
      }
    },
    // 2023-10-31 add the following methods
    async mqttForAllStationHWOff() {
      console.log("mqttForAllStationHWOff...");

      let path='/mqtt/station';
      let myTopic=this.mqtt_topic[parseInt(this.all_station) - 1]
      console.log("Get ready to turn off all stations led by HW => " + "station: " + this.all_station)

      let payload= {
        topic: myTopic,
        layout: '0',
        pos_begin: '0',
        pos_end: '0',
        msg: 'off',
      };

      try {
        let res = await axios.post(path, payload);
        console.log("All stations led has been powered off by HW, mqtt ok", res.data.status);
        if (this.all_station>=3) {
          this.all_layout=1;
          this.all_station=1;
          this.mqttForAllStationOff();           // 2023-10-31 add
        } else {
          this.all_station = this.all_station + 1;
          this.load_7thTable_ok=true;
        }
      } catch (err) {
        console.error(err)
        console.log("通訊錯誤!");
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '通訊錯誤!';
        this.snackbar_icon_color= '#adadad';
        this.load_7thTable_ok=false;
      }
    },

    async mqttForAllStationOff() {
      console.log("mqttForAllStationOff...");

      let path='/mqtt/station';
      let temp_layout=this.all_layout;
      let myTopic=this.mqtt_topic[parseInt(this.all_station) - 1]
      console.log("Get ready to turn off all stations led => " + "station: " + this.all_station + " ,layout: " + this.all_layout)

      let payload= {
        topic: myTopic,
        layout: temp_layout.toString(),
        pos_begin: '1',
        pos_end: '30',
        msg: 'off',
      };

      try {
        let res = await axios.post(path, payload);
        console.log("All stations led has been powered off, mqtt ok", res.data.status);
        if (this.all_layout>=5) {
          this.all_layout=1;
          if (this.all_station>=3) {
            this.load_6thTable_ok=false;
          } else {
            this.all_station = this.all_station + 1;
            this.load_6thTable_ok=true;
          }
        } else {
          this.all_layout = this.all_layout + 1;
          this.load_6thTable_ok=true;
        }
      } catch (err) {
        console.error(err)
        console.log("通訊錯誤!");
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '通訊錯誤!';
        this.snackbar_icon_color= '#adadad';
        this.load_6thTable_ok=false;
      }
    },
    //
    listActionClick_m(index) {
      if (this.items.length==0) {
        console.log("HELLO1...", index, this.items[index]);

        this.home_url=this.default_home_url;
        //this.isOK=false;    //2023-04-27 mark

        this.stockOutTag_cnt=0;
        this.stockOutTag_max_cnt=0;
        this.stockOutTag_min_cnt=0;

        this.stockOutTag_unit='';   //add

        this.stockOutTag_reagID='';
        this.stockOutTag_reagName='';

        this.stockOutTag_station='';
        this.stockOutTag_layout='';
        this.stockOutTag_pos='';
      } else {
        console.log("HELLO2...", index, this.items[index]);

        this.currentIndex=index;
        this.currentLedStation=this.items[index].grid_station;
        this.currentLedLayout=this.items[index].grid_layout;
        this.currentLedPos=this.items[index].grid_pos;
        this.currentLedRange_begin=this.items[index].range0;
        this.currentLedRange_end=this.items[index].range1;

        this.current_unit=this.items[index].stockOutTag_unit; //add

        console.log("id, current: ",this.items[index].id, this.currentIndex, this.currentLedStation, this.currentLedLayout, this.currentLedPos, this.currentLedRange_begin, this.currentLedRange_end)

        this.isSort=false;
        this.stockOutTag_cnt=this.items[index].stockOutTag_cnt;

        this.stockOutTag_max_cnt=this.items[index].stockOutTag_cnt;
        this.stockOutTag_min_cnt=1;

        this.stockOutTag_unit=this.items[index].stockOutTag_unit;   //add

        this.stockOutTag_reagID=this.items[index].stockOutTag_reagID;
        this.stockOutTag_reagName=this.items[index].stockOutTag_reagName;

        this.stockOutTag_station=this.items[index].grid_station;
        this.stockOutTag_layout=this.items[index].grid_layout;
        this.stockOutTag_pos=this.items[index].grid_pos;
      }
    },

    fromReagIdDisp() {
      if (this.stockOutTag_reagID != '' && this.isSort) {
        console.log("result 1-1...", this.items);
        const objIndex = this.items.findIndex((obj => obj['active'] == true));
        console.log("result 1-1-1...", objIndex);
        if (objIndex != -1)
          this.items[objIndex].active = false;
        const fromIndex = this.items.map(object => object.stockOutTag_reagID).indexOf(this.stockOutTag_reagID);
        const toIndex = 0;
        console.log("result 1-2...", fromIndex);
        if (fromIndex != -1) {
          const element = this.items.splice(fromIndex, 1)[0];
          this.items.splice(toIndex, 0, element);
          this.model=0;
          this.items[0].active = true;
          this.current_cnt=this.stockOutTag_cnt
          this.stockOutTag_cnt=this.items[0].stockOutTag_cnt;
          this.stockOutTag_max_cnt=this.items[0].stockOutTag_cnt;
          this.stockOutTag_min_cnt=1;
          this.current_unit=this.items[0].stockOutTag_unit;  //add

          this.stockOutTag_reagName=this.items[0].stockOutTag_reagName;
          //add
          this.stockOutTag_station=this.items[0].grid_station;
          this.stockOutTag_layout=this.items[0].grid_layout;
          this.stockOutTag_pos=this.items[0].grid_pos;

          this.currentIndex=0;
          this.currentLedStation=this.items[0].grid_station;
          this.currentLedLayout=this.items[0].grid_layout;
          this.currentLedPos=this.items[0].grid_pos;

          this.currentLedRange_begin=this.items[0].range0;  //2023-1-12 add
          this.currentLedRange_end=this.items[0].range1;  //2023-1-12 add

          //this.current_unit=this.items[0].stockOutTag_unit; //2023-04-27 remove
        }
        //if (index != -1) {
        //  console.log("result 2...", index);
        //  this.model=index;
        //}
      } else {
        this.isSort=true;
        if (this.stockOutTag_reagID == '') {
          this.stockOutTag_cnt=0;
          this.stockOutTag_max_cnt=0;
          this.stockOutTag_min_cnt=0;
          this.stockOutTag_unit='';     //add

          this.stockOutTag_reagName='';
          //add
          this.stockOutTag_station='';
          this.stockOutTag_layout='';
          this.stockOutTag_pos='';
        }
      }
    },

    addGrids() {
      for (let i = 0; i < this.items.length; i++) {
        let obj = this.grids.find(o => o.grid_reagID === this.items[i].stockOutTag_reagID)
        console.log("i, grid: ", i, obj)
        if (typeof(obj) !== 'undefined') {
          this.items[i].grid_station=obj.grid_station;
          this.items[i].grid_layout=obj.grid_layout;
          //this.items[i].grid_id=obj.grid_id,
          this.items[i].grid_id=obj.id,
          this.items[i].grid_pos=obj.grid_pos;
          this.items[i].seg_id=obj.seg_id;
          this.items[i].range0=obj.range0;
          this.items[i].range1=obj.range1;
        }
      };

      this.stockOutTag_cnt=this.items[this.model].stockOutTag_cnt;
      this.stockOutTag_max_cnt=this.items[this.model].stockOutTag_cnt;

      this.stockOutTag_unit=this.items[this.model].stockOutTag_unit;  //add

      this.stockOutTag_min_cnt=1;
      this.stockOutTag_reagID=this.items[this.model].stockOutTag_reagID;
      this.stockOutTag_reagName=this.items[this.model].stockOutTag_reagName;

      this.stockOutTag_station=this.items[this.model].grid_station;
      this.stockOutTag_layout=this.items[this.model].grid_layout;
      this.stockOutTag_pos=this.items[this.model].grid_pos;

      this.items[this.model].active=true;
    },

    redirect_to_mqtt() {
      console.log("redirect_to_mqtt, hello click image button...", this.model);
      console.log("current: ", this.currentLedLayout, "  ", this.currentLedRange_begin, "  ", this.currentLedRange_end);

      this.isOK=true;

      let temp_sw=this.items[this.model].grid_station;
      console.log("StockOut: isOK, temp_sw",this.isOK, temp_sw);
      if (temp_sw==1) {
        this.home_url=this.home_url_R;
      }
      if (temp_sw==2) {
        //console.log("color: ", temp_sw, this.home_url)
        this.home_url=this.home_url_Y;
      }
      if (temp_sw==3) {
        //console.log("color: ", temp_sw, this.home_url)
        this.home_url=this.home_url_G;
      }
      this.redirect_ok();
    },

    redirect_ok() {
      //this.isOK=false;                          //2023-1-12 mark
      //this.home_url=this.default_home_url;      //2023-1-12 mark
      console.log("redirect_ok: ", this.items.length, this.model)
      if (this.stockOutTag_cnt==this.items[this.model].stockOutTag_cnt) {
        this.stockout_record=this.items[this.model];
        let removedEl = this.items.splice(this.model, 1); //remove object(index: this.model) from array(this.items)
        this.stockout_record=removedEl[0];

        this.model=(this.model-1>= 0) ? this.model-1 : 0;

        this.stockOutTag_reagID = '';
        this.stockOutTag_cnt=0;
        this.stockOutTag_max_cnt=0;
        this.stockOutTag_min_cnt=0;

        this.stockOutTag_unit=''; //add

        this.stockOutTag_reagName='';
        //add
        this.stockOutTag_station='';
        this.stockOutTag_layout='';
        this.stockOutTag_pos='';

        if (this.items.length>0) {
          this.stockOutTag_cnt=this.items[this.model].stockOutTag_cnt;
          this.stockOutTag_max_cnt=this.items[this.model].stockOutTag_cnt;
          this.stockOutTag_min_cnt=1;
          this.stockOutTag_unit=this.items[this.model].stockOutTag_unit;  //add

          this.stockOutTag_reagID=this.items[this.model].stockOutTag_reagID;
          this.stockOutTag_reagName=this.items[this.model].stockOutTag_reagName;

          this.stockOutTag_station=this.items[this.model].grid_station;
          this.stockOutTag_layout=this.items[this.model].grid_layout;
          this.stockOutTag_pos=this.items[this.model].grid_pos;

          this.items[this.model].active=true;
        } else {
          this.emptyRecordReady=true; //2023-02-14 add
          //this.isEmptyRecord=true;  //2023-02-14 mark
        }
      } else {
        this.items[this.model].stockOutTag_cnt=this.items[this.model].stockOutTag_cnt - this.stockOutTag_cnt;
        this.stockOutTag_cnt=this.items[this.model].stockOutTag_cnt;
        this.stockOutTag_max_cnt=this.items[this.model].stockOutTag_cnt;
        this.stockout_record=this.items[this.model];
      }
      console.log("current, mqttForStation: ", this.currentLedLayout, "  ", this.currentLedRange_begin, "  ", this.currentLedRange_end);

      this.mqttForStation();
    },

    permCloseFun () {
      this.permDialog = false
      console.log("press permission Close Button...");
      this.$router.push('/navbar');
    },
  },
}
</script>

<style lang="scss" scoped>
html {
  overflow: hidden !important;
}

span.text-decoration-underline {
  margin-top: 13px;
}

span.stockout_str {
  margin-top: 13px;
}

.v-card {
  display: flex !important;
  flex-direction: column;
}

.v-card__text {
  flex-grow: 1;
  overflow: auto;
}

.v-card.on-hover.theme--dark {
  background-color: rgba(255, 255, 255, 0.8);
}

.v-card.on-hover.theme--dark > .v-card__text {
    color: #000;
}
</style>