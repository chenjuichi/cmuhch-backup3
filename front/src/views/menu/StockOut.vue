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
      <v-card class="overflow-hidden mx-auto mt-3" width="88vw">
        <v-toolbar flat color="#7DA79D" height="80vw" >
          <v-row dense style="margin-bottom: -36px; margin-top: -12x;">
            <v-col cols="12" md="2" class="mr-1" style="position: relative; top: -15px;">
              <v-text-field
                v-model="stockOutTag_reagID"
                label="資材碼"
                style="position:relative; top: 15px;"
                :value="stockOutTag_reagID"
                @keyup.native.enter="handleUpdateItem($event)"
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
                style="width: 300px !important; max-width: 300px !important;"
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
              <vue-numeric-input v-model="stockOutTag_cnt" :min="1" :max="stockOutTag_max_cnt" :step="1" size="small" align="center"></vue-numeric-input>
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
    stockOutTag_min_cnt: 0,
    stockOutTag_max_cnt: 0,
    stockOutTag_unit: '', //add

    current_cnt:0,

    currentIndex: 0,
    currentLedStation: 1,
    currentLedLayout: 1,
    currentLedPos: 1,
    currentLedRange_begin: 1,
    currentLedRange_end: 2,
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

    //selected: [2],
    model: 0,

    items: [
      /*
      {
        //id: 1,
        stockOutTag_reagID: '123456789',
        stockOutTag_reagName: 'ABC',
        stockOutTag_reagPeriod: '111/10/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_Date: '111/06/01',
        stockOutTag_EmpID: 'N12345',
        stockOutTag_Employer: '陳健南',
        stockOutTag_batch: '1110012345B123400066',
        stockOutTag_cnt: 4,
        active: false,
      },
      {
        //id: 2,
        stockOutTag_reagID: '234567891',
        stockOutTag_reagName: 'ABCD1',
        stockOutTag_reagPeriod: '111/12/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_Date: '111/06/01',
        stockOutTag_EmpID: 'N12345',
        stockOutTag_Employer: '陳健南',
        stockOutTag_batch: '1110012345C123400055',
        stockOutTag_cnt: 2,
        active: false,
      },
      {
        //id: 3,
        stockOutTag_reagID: '234567892',
        stockOutTag_reagName: 'A11',
        stockOutTag_reagPeriod: '111/12/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_Date: '111/06/01',
        stockOutTag_EmpID: 'N12345',
        stockOutTag_Employer: '陳健南',
        stockOutTag_batch: '1110012345B123400033',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 4,
        stockOutTag_reagID: '234567893',
        stockOutTag_reagName: 'A12',
        stockOutTag_reagPeriod: '112/6/30',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_Date: '111/06/01',
        stockOutTag_EmpID: 'N12345',
        stockOutTag_Employer: '陳健南',
        stockOutTag_batch: '1110012345B123400033',
        stockOutTag_cnt: 1,
        active: false,
      },
      {
        //id: 5,
        stockOutTag_reagID: '234567894',
        stockOutTag_reagName: 'B2233',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '2~8度C',
        stockOutTag_Date: '111/06/01',
        stockOutTag_EmpID: 'N12345',
        stockOutTag_Employer: '陳健南',
        stockOutTag_batch: '1110012345B123400022',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 6,
        stockOutTag_reagID: '234567897',
        stockOutTag_reagName: 'B3344',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/03/10',
        stockOutTag_EmpID: 'T12345',
        stockOutTag_Employer: '林成興',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 1,
        active: false,
      },
      {
        //id: 7,
        stockOutTag_reagID: '234567898',
        stockOutTag_reagName: 'B3341',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/03/10',
        stockOutTag_EmpID: 'T12345',
        stockOutTag_Employer: '林成興',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 8,
        stockOutTag_reagID: '234567899',
        stockOutTag_reagName: 'B3342',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/03/10',
        stockOutTag_EmpID: 'T12345',
        stockOutTag_Employer: '林成興',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 5,
        active: false,
      },
      {
        //id: 9,
        stockOutTag_reagID: '214567897',
        stockOutTag_reagName: 'B3343',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/03/10',
        stockOutTag_EmpID: 'T12345',
        stockOutTag_Employer: '林成興',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 10,
        stockOutTag_reagID: '214567898',
        stockOutTag_reagName: 'B3345',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/03/10',
        stockOutTag_EmpID: 'T12345',
        stockOutTag_Employer: '林成興',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 2,
        active: false,
      },
      {
        //id: 11,
        stockOutTag_reagID: '214567899',
        stockOutTag_reagName: 'B3346',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/06/25',
        stockOutTag_EmpID: 'T87654',
        stockOutTag_Employer: '吳仲偉',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 12,
        stockOutTag_reagID: '224567897',
        stockOutTag_reagName: 'B3347',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/06/25',
        stockOutTag_EmpID: 'T87654',
        stockOutTag_Employer: '吳仲偉',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 20,
        active: false,
      },
      {
        //id: 13,
        stockOutTag_reagID: '224567898',
        stockOutTag_reagName: 'B3348',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/06/25',
        stockOutTag_EmpID: 'T87654',
        stockOutTag_Employer: '吳仲偉',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 10,
        active: false,
      },
      {
        //id: 14,
        stockOutTag_reagID: '224567899',
        stockOutTag_reagName: 'B3349',
        stockOutTag_reagPeriod: '111/8/31',
        stockOutTag_reagTemp: '常溫',
        stockOutTag_Date: '111/06/25',
        stockOutTag_EmpID: 'T87654',
        stockOutTag_Employer: '吳仲偉',
        stockOutTag_batch: '1110012345A123400001',
        stockOutTag_cnt: 10,
        active: false,
      },
      */
    ],
    temp_items : [],

    reagentForSelect: [],
    stockout_record: {},

    mqtt_topic:['station1','station2','station3'],

    load_SingleTable_ok: false, //for get employer table data
    load_2thTable_ok: false,    //for get reagent table data
    load_3thTable_ok: false,
    load_4thTable_ok: false,
    load_5thTable_ok: false,
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
      //let matchResult = this.items.find(x => x.stockOutTag_reagID === this.stockOutTag_reagID);
      //if (typeof(matchResult) == 'undefined') {
      //  console.log("stockOutTag_reagID is undefined...");
      //}

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
        this.home_url=this.default_home_url;    //2023-1-12 add

      }
    },
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm == 0) {
      this.permDialog=true;
      //console.log("router undefine!")
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page;

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listStockOutItems();

    //this.initialize();
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listStockOutItems();
      //this.liststockOutGrids();
      /*
      this.grids = [
        {
          //id: 1,
          grid_reagID: '123456789',
          grid_reagName: 'ABC',
          grid_station: 1,
          grid_layout: 4,
          grid_pos: 4,
        },
        {
          //id: 2,
          grid_reagID: '234567891',
          grid_reagName: 'ABCD',
          grid_station: 1,
          grid_layout: 4,
          grid_pos: 5,
        },
        {
          //id: 3,
          grid_reagID: '234567892',
          grid_reagName: 'A11',
          grid_station: 2,
          grid_layout: 1,
          grid_pos: 6,
        },
        {
          //id: 4,
          grid_reagID: '234567893',
          grid_reagName: 'A12',
          grid_station: 2,
          grid_layout: 3,
          grid_pos: 5,
        },
        {
          //id: 5,
          grid_reagID: '234567894',
          grid_reagName: 'B2233',
          grid_station: 3,
          grid_layout: 2,
          grid_pos: 2,
        },
        {
          //id: 6,
          grid_reagID: '234567897',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 1,
          grid_pos: 6,
        },
        {
          //id: 7,
          grid_reagID: '234567898',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 2,
          grid_pos: 6,
        },
        {
          //id: 8,
          grid_reagID: '234567899',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 3,
          grid_pos: 6,
        },
        {
          //id: 9,
          grid_reagID: '214567897',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 4,
          grid_pos: 6,
        },
        {
          //id: 10,
          grid_reagID: '214567898',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 6,
        },
        {
          //id: 11,
          grid_reagID: '214567899',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 7,
        },
        {
          //id: 13,
          grid_reagID: '224567897',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 8,
        },
        {
          //id: 14,
          grid_reagID: '224567898',
          grid_reagName: 'B3344',
          grid_station: 3,
          grid_layout: 5,
          grid_pos: 8,
        },
        {
          //id: 15,
          grid_reagID: '224567899',
          grid_reagName: 'B3344',
          grid_station: 1,
          grid_layout: 5,
          grid_pos: 8,
        },

      ];
      */
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

      const path='/addStockOutItem';
      let object = Object.assign({}, this.stockout_record);
      console.log("OutTagID: ", object, this.stockOutTag_cnt)
      let cnt = object.stockOutTag_cnt!=this.stockOutTag_cnt ? Math.abs(object.stockOutTag_cnt - this.stockOutTag_cnt):this.stockOutTag_cnt;

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
        let path='/mqtt/station';
        let temp_layout=this.currentLedLayout;
        let range_begin=this.currentLedRange_begin;
        let range_end=this.currentLedRange_end;
        console.log("station: " +"layout: " + temp_layout + " pos: " + range_begin + " , " + range_end)
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
      let path='/mqtt/station';
      let temp_layout='0';
      let range_begin='0';
      let range_end='0';
      let temp_sw= 'off';
      let myTopic=this.pre_topic;
      let payload= {
        topic: myTopic,
        layout: temp_layout,
        pos_begin: range_begin,
        pos_end: range_end,
        msg: temp_sw,
      };

      try {
        let res = await axios.post(path, payload);
        console.log("off led, mqtt ok", res.data.status);
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

    listActionClick_m(index) {
      if (this.items.length==0) {
        console.log("HELLO...", index, this.items[index]);

        this.home_url=this.default_home_url;
        this.isOK=false;

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
    /*
    listActionClick(index, active) {
      console.log("list action: ", index, active);

      this.currentIndex=index;
      this.currentLedStation=this.items[index].grid_station;
      this.currentLedLayout=this.items[index].grid_layout;
      this.currentLedPos=this.items[index].grid_pos;
      this.currentLedRange_begin=this.items[index].range0;
      this.currentLedRange_end=this.items[index].range1;

      this.isSort=false;
      if (active) {
        this.stockOutTag_cnt=0;
        this.stockOutTag_max_cnt=0;
        this.stockOutTag_min_cnt=0;

        this.stockOutTag_reagID='';
        this.stockOutTag_reagName='';

        this.stockOutTag_station='';
        this.stockOutTag_layout='';
        this.stockOutTag_pos='';
      } else {
        this.stockOutTag_cnt=this.items[index].stockOutTag_cnt;
        this.stockOutTag_max_cnt=this.items[index].stockOutTag_cnt;

        this.stockOutTag_min_cnt=1;
        this.stockOutTag_reagID=this.items[index].stockOutTag_reagID;
        this.stockOutTag_reagName=this.items[index].stockOutTag_reagName;

        this.stockOutTag_station=this.items[index].grid_station;
        this.stockOutTag_layout=this.items[index].grid_layout;
        this.stockOutTag_pos=this.items[index].grid_pos;
      }

      //this.items[index].active=!this.items[index].active;
    },
    */
    /*
    toggle(index) {
      const i = this.selected.indexOf(index)

      if (i > -1) {
          this.selected.splice(i, 1)
      } else {
          this.selected.push(index)
      }
    },
    */
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

          this.current_unit=this.items[0].stockOutTag_unit; //add
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
      console.log("hello click image button...", this.model);
      this.isOK=true;
      /*
      let temp_sw=this.items[this.model].grid_station;
      switch (temp_sw) {
        case 1:
          this.home_url=this.home_url_R;
          break;
        case 2:
          this.home_url=this.home_url_Y;
          break;
        case 3:
          this.home_url=this.home_url_G;
          break;
      }
      this.redirect_ok();
      */
      let temp_sw=this.items[this.model].grid_station;
      console.log("temp_sw", temp_sw);
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
          this.isEmptyRecord=true;
        }
      } else {
        this.items[this.model].stockOutTag_cnt=this.items[this.model].stockOutTag_cnt - this.stockOutTag_cnt;
        this.stockOutTag_cnt=this.items[this.model].stockOutTag_cnt;
        this.stockOutTag_max_cnt=this.items[this.model].stockOutTag_cnt;
        this.stockout_record=this.items[this.model];
      }

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