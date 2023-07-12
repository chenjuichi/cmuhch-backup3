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
      <v-card width="86vw">
        <v-data-table
          :headers="headers"
          :items="desserts"
          :item-class="setRowStyle"
          :options.sync="pagination"
          class="elevation-1"

          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>入庫標籤資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="860px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on" v-show="currentUser.perm<=2">
                    <v-icon left dark>mdi-table-plus</v-icon>新增入庫標籤資料
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>

                  <v-card-text>
                    <v-container>
                      <!-- 第1列-->
                      <v-row>
                        <v-col cols="12" md="4">
                          <v-tooltip v-model="errorShowForEmployer" top color="error">
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                v-model="editedItem.stockInTag_EmpID"
                                :value="stockInTag_EmpID"
                                label="員工編號"
                                readonly
                              ></v-text-field>
                            </template>
                            <span>員工編號錯誤!</span>
                          </v-tooltip>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="editedItem.stockInTag_Employer"
                            :value="fromStockInTagEmpIdDisp"
                            label="入庫人員"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-menu
                            v-model="fromDateMenu"
                            :close-on-content-click="false"
                            :nudge-right="40"

                            transition="scale-transition"
                            offset-y

                            max-width="290px"
                            min-width="290px"
                          >
                            <template v-slot:activator="{ on }">
                              <v-text-field
                                label="入庫日期"
                                prepend-icon="event"
                                readonly
                                :value="fromDateDisp"
                                v-model="editedItem.stockInTag_Date"
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-date-picker
                              locale="zh-TW"
                              :min="minDate"
                              :max="maxDate"
                              v-model="fromDateVal"
                              no-title
                              @input="fromDateMenu = false"
                            ></v-date-picker>
                          </v-menu>
                        </v-col>
                      </v-row>

                      <!-- 第2列-->
                      <v-row>
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="editedItem.stockInTag_reagID"
                            :value="fromReagIdDisp"
                            label="資材碼"
                            @blur="listGridForCheck"
                          ></v-text-field>
                          <small class="msgErr" v-text= "IDErrMsg"></small>
                        </v-col>

                        <v-col cols="12" md="4">
                          <v-autocomplete
                            v-model="editedItem.stockInTag_reagName"
                            :items="autocomplete_items"
                            :value="fromReagNameDisp"
                            :loading="autocomplete_loading"
                            :search-input.sync="autocomplete_search"

                            color="blue"
                            label="品名"
                            solo
                          >
                          </v-autocomplete>
                        </v-col>

                        <v-col cols="12" md="2">
                          <v-menu
                            v-model="fromDateMenuP"
                            :close-on-content-click="false"
                            :nudge-right="40"

                            transition="scale-transition"
                            offset-y

                            max-width="290px"
                            min-width="290px"
                          >
                            <template v-slot:activator="{ on }">
                              <v-text-field
                                label="效期"
                                prepend-icon="event"
                                readonly
                                :value="fromDateDispP"
                                v-model="editedItem.stockInTag_reagPeriod"
                                v-on="on"
                              ></v-text-field>
                            </template>
                            <v-date-picker
                              locale="zh-TW"
                              :min="minDate"
                              :max="maxDate"
                              v-model="fromDateValP"
                              no-title
                              @input="fromDateMenuP = false"

                            ></v-date-picker>
                          </v-menu>
                        </v-col>

                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="editedItem.stockInTag_reagTemp"
                            :value="editedItem.stockInTag_reagTemp"
                            label="保存溫度"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="editedItem.stockInTag_batch"
                            :value="editedItem.stockInTag_batch"
                            label="批號"
                          ></v-text-field>
                          <small class="msgErr" v-text= "BatchErrMsg"></small>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="save" :disabled='checkDataForSaveButton'>確定</v-btn>
                    <v-tooltip v-model="tosterOK" bottom :position-x="toster_pos_x" :position-y="toster_pos_y" color="error">
                      <span>資材碼重複!</span>
                    </v-tooltip>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-dialog v-model="dialogDelete" max-width="500px">
                <v-card>
                  <v-card-title class="text-h5">確定刪除這筆資料?</v-card-title>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeDelete">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="deleteItemConfirm">刪除</v-btn>
                    <v-spacer></v-spacer>
                  </v-card-actions>
                </v-card>
              </v-dialog>

              <v-dialog v-show="rightDialog"
                v-model="rightDialog"
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
                    <v-btn text @click="rightCloseFun"> 取消 </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <!-- 更改數量 -->
          <template v-slot:[`item.stockInTag_cnt`]="{ item }">
            <v-text-field
              v-model="item.stockInTag_cnt"
              type="number"
              value="item.stockInTag_cnt"
              min=1


              @input="getdata(item)"
              :disabled="currentUser.perm>2"
            ></v-text-field>
          </template>

          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)" style="color: blue;">
              mdi-pencil
            </v-icon>
            <v-icon small  @click="deleteItem(item)" style="color: red;">
              mdi-delete
            </v-icon>
          </template>
          <!--
          <template v-slot:no-data>
            <v-btn color="primary" @click="initialize">Reset</v-btn>
          </template>
          -->

          <template v-slot:no-data>
            <strong><font color='red'>目前沒有資料</font></strong>
          </template>

        </v-data-table>
      </v-card>
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

import Common from '../../mixin/common.js'

import { Calendar }  from '../../mixin/calendar.js';

//import TypeaheadAutocomplete from "typeahead-autocomplete";
//import VueBootstrapTypeahead from 'vue-bootstrap-typeahead'

export default {
  name: 'StockInTag',

  mixins: [Common],

  components: {
  //  TypeaheadAutocomplete,
  //VueBootstrapTypeahead,
  },

  mounted() {
    // if back button is pressed
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));
    };
  },

  data: () => ({
    currentUser: {},
    permDialog: false,
    rightDialog: false,
    //2023-04-14 add
    autocomplete_loading: false,
    autocomplete_items: [],
    autocomplete_select: null,
    autocomplete_search: null,
    redirectTimeout: null, //2023-05-04 add
    //isOpen: false,
    //arrowCounter: -1,

    temp_autocomplete_items: [],
    //
    snackbar: false,
    snackbar_color: 'success',
    snackbar_right: true,
    snackbar_top: true,
    snackbar_info: '',
    snackbar_icon_color: '#adadad',

    stockInTag_EmpID: '',   //入庫人員之員工編號

    errorShowForEmployer: false,
    errorShowForReagName: false,
    IDErrMsg: '',
    BatchErrMsg: '',

    fromDateMenu: false,
    fromDateVal: '',
    //fromDateVal: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
    clickMenu: false,

    fromDateMenuP: false,
    //fromDateValP: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
    fromDateValP: '',
    clickMenuP: false,

    minDate: "2012-07-01",
    maxDate: "2042-06-30",

    dialog: false,
    dialogDelete: false,

    pagination: {},

    tosterOK: false,
    toster_pos_x: 1000,
    toster_pos_y: 400,
    toster_delay:3,

    //資料表頭
    headers: [
      { text: '資料ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'stockInTag_reagID', width: '6%' },
      { text: '品名', sortable: true, value: 'stockInTag_reagName', width: '200px' },
      { text: '效期', sortable: true, value: 'stockInTag_reagPeriod', width: '90px' },
      { text: '保存溫度', sortable: false, value: 'stockInTag_reagTemp', width: '10%' },
      { text: '入庫日期', sortable: true, value: 'stockInTag_Date', width: '90px' },
      { text: '入庫人員', sortable: true, value: 'stockInTag_Employer', width: '10%' },
      { text: '批號', sortable: true, value: 'stockInTag_batch', width: '180px' },
      { text: '數量', sortable: false, value: 'stockInTag_cnt', width: '50px' },
      { text: 'Actions', sortable: false, value: 'actions', width: '10%', align: 'center' },
    ],

    max: 1,

    /*
    stockInTag_employer_desserts: [
      {
        //id: 1,
        stkIn_empID: 'A12345',
        stkIn_empName: '陳瑞琪',
      },
      {
        //id: 2,
        stkIn_empID: 'A12342',
        stkIn_empName: '林政仰',
      },
      {
        //id: 3,
        stkIn_empID: 'N12345',
        stkIn_empName: '陳健南',
      },
      {
        //id: 4,
        stkIn_empID: 'N12345',
        stkIn_empName: '周明慶',
      },
      {
        //id: 5,
        stkIn_empID: 'D12345',
        stkIn_empName: '顏榮俊',
      },
      {
        //id: 6,
        stkIn_empID: 'T12345',
        stkIn_empName: '林成興',
      },
      {
        //id: 7,
        stkIn_empID: 'T87654',
        stkIn_empName: '吳仲偉',
      },
    ],
    */
    /*
    stockInTag_Desserts: [
      {
        //id: 1,
        stockInTag_reagID: '123456789',
        stockInTag_reagName: 'ABC',
        stockInTag_reagPeriod: '111/10/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345D123400888',
        stockInTag_cnt: 1,
      },
      {
        //id: 2,
        stockInTag_reagID: '234567891',
        stockInTag_reagName: 'ABCD',
        stockInTag_reagPeriod: '111/12/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345D123405555',
        stockInTag_cnt: 1,
      },
      {
        //id: 3,
        stockInTag_reagID: '234567892',
        stockInTag_reagName: 'A11',
        stockInTag_reagPeriod: '111/12/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345D123400011',
        stockInTag_cnt: 1,
      },
      {
        //id: 4,
        stockInTag_reagID: '234567893',
        stockInTag_reagName: 'A12',
        stockInTag_reagPeriod: '112/6/30',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345B123400012',
        stockInTag_cnt: 1,
      },
      {
        //id: 5,
        stockInTag_reagID: '234567894',
        stockInTag_reagName: 'B2233',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345B123400022',
        stockInTag_cnt: 1,
      },
      {
        //id: 6,
        stockInTag_reagID: '234567897',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 7,
        stockInTag_reagID: '234567898',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 8,
        stockInTag_reagID: '234567899',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 9,
        stockInTag_reagID: '214567897',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 10,
        stockInTag_reagID: '214567898',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 11,
        stockInTag_reagID: '214567899',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '室溫',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 12,
        stockInTag_reagID: '224567897',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 13,
        stockInTag_reagID: '224567898',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '2~8度C',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
      {
        //id: 14,
        stockInTag_reagID: '224567899',
        stockInTag_reagName: 'B3344',
        stockInTag_reagPeriod: '111/8/31',
        stockInTag_reagTemp: '室溫',
        stockInTag_batch: '1110012345A123400001',
        stockInTag_cnt: 1,
      },
    ],
    */
    in_newTags: 0,
    in_drafTags: 0,

    desserts: [],
    temp_desserts: [],

    //reagentForSelect: [],
    reagent_Desserts: [],
    temp_reagent_Desserts: [],

    editedIndex: -1,
    editedItem: {
      id: 0,
      stockInTag_reagID: '',
      stockInTag_reagName: '',
      stockInTag_reagPeriod: '',
      stockInTag_reagTemp: '',
      stockInTag_Date: '',
      stockInTag_EmpID: '',
      stockInTag_Employer: '',
      stockInTag_batch: '',
      stockInTag_cnt: '',
      stockInTag_cnt_max: '',
    },
    temp_editedItem: {
      id: 0,
      stockInTag_reagID: '',
      stockInTag_reagName: '',
      stockInTag_reagPeriod: '',
      stockInTag_reagTemp: '',
      stockInTag_Date: '',
      stockInTag_EmpID: '',
      stockInTag_Employer: '',
      stockInTag_batch: '',
      stockInTag_cnt: '',
      stockInTag_max: '',
    },
    last_id: 0,
    defaultItem: {
      id: 0,
      stockInTag_reagID: '',
      stockInTag_reagName: '',
      stockInTag_reagPeriod: '',
      stockInTag_reagTemp: '',
      stockInTag_Date: '',
      stockInTag_EmpID: '',
      stockInTag_Employer: '',
      stockInTag_batch: '',
      stockInTag_cnt: '',
      stockInTag_cnt_max: '',
    },

    load_SingleTable_ok: false,
    load_2thTable_ok: false,
    load_3thTable_ok: false,

    load_4thTable_ok: false,  //2023-04-14 add
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },

    fromStockInTagEmpIdDisp() {
      if (this.stockInTag_EmpID != '') {
        if (this.editedItem.stockInTag_EmpID == '') {
          this.editedItem.stockInTag_EmpID=this.currentUser.empID;
          this.editedItem.stockInTag_Employer=this.currentUser.name;
        }
        this.errorShowForEmployer=false;
        return this.editedItem.stockInTag_Employer;
      } else {
        this.this.editedItem.stockInTag_EmpID='';
        this.editedItem.stockInTag_Employer='';
        this.errorShowForEmployer=true;
        return '';
      }
    },

    fromReagIdDisp() {  //show reagent name, by id
      if (this.editedItem.stockInTag_reagID != '') {
        //console.log("result 0...", this.editedItem.stockInTag_reagID, this.reagent_Desserts);

        const result = this.reagent_Desserts.find(x => x.reag_id === this.editedItem.stockInTag_reagID);
        //const result = this.temp_desserts.find(x => x.reag_id === this.editedItem.stockInTag_reagID);

        console.log("fromReagIdDisp, result 1...", result);

        if (result != 'undefined' && result != null) {
          console.log("result 2...", result, this.editedIndex);
          if (this.editedIndex == -1) {
            this.editedItem.stockInTag_reagName=result.reag_name;
            this.editedItem.stockInTag_reagTemp=result.reag_temp;
          }
          //this.editedItem.stockInTag_reagPeriod='';
          this.errorShowForReagName=false;
          console.log("result 22...", result, this.editedIndex, this.editedItem);
          this.autocomplete_search=this.editedItem.stockInTag_reagName;
          return this.editedItem.stockInTag_reagName;
        } else {
          console.log("result 3...", result);
          this.editedItem.stockInTag_reagName='';
          this.editedItem.stockInTag_reagPeriod='';
          this.editedItem.stockInTag_reagTemp='';
          this.errorShowForReagName=true;
          this.autocomplete_search=null;
          return '';
        }
      } else {
          this.editedItem.stockInTag_reagName='';
          this.editedItem.stockInTag_reagPeriod='';
          this.editedItem.stockInTag_reagTemp='';
          this.errorShowForReagName=true;
          this.autocomplete_search=null;
          return '';
      }
    },

    fromReagNameDisp() {  //show reagent id, by name
      //if (this.autocomplete_search !=null)
      //  this.editedItem.stockInTag_reagName = this.autocomplete_search;
      this.autocomplete_search = this.editedItem.stockInTag_reagName;
      if (this.editedItem.stockInTag_reagName != '' || this.editedItem.stockInTag_reagName != null) {
        const result = this.reagent_Desserts.find(x => x.reag_name === this.editedItem.stockInTag_reagName);
        console.log("fromReagNameDisp, result 1...", this.autocomplete_search, result);

        if (result != 'undefined' && result != null) {
          console.log("fromReagNameDisp, result 2-1...", result, this.editedIndex);
          if (this.editedIndex == -1) {
            this.editedItem.stockInTag_reagID=result.reag_id;
            this.editedItem.stockInTag_reagTemp=result.reag_temp;
          }
          //this.editedItem.stockInTag_reagPeriod='';
          this.errorShowForReagName=false;
          console.log("fromReagNameDisp, result 2-2...", result, this.editedIndex, this.editedItem);

          return this.editedItem.stockInTag_reagID;
        } else {
          console.log("fromReagNameDisp, result 3...", result);
          this.editedItem.stockInTag_reagID='';
          this.editedItem.stockInTag_reagPeriod='';
          this.editedItem.stockInTag_reagTemp='';
          this.errorShowForReagName=true;
          return '';
        }
      }
    },

    fromDateDisp() {  //output: editedItem.stockInTag_Date
      console.log("con 1...", "edit: ", this.editedItem.stockInTag_Date, "fromDateVal: ", this.fromDateVal, "index: ", this.editedIndex, "click: ", this.clickMenu);
      //test, prototype chain在javascript
      let dateDisp= new Calendar(this.editedItem.stockInTag_Date, this.fromDateVal, this.editedIndex, this.clickMenu);
      dateDisp.form();
      console.log("function get: ",  dateDisp.myEdit,  dateDisp.myValue,  dateDisp.myIndex,  dateDisp.myClick)
      console.log("con 111...", "edit: ", this.editedItem.stockInTag_Date, "fromDateVal: ", this.fromDateVal, "index: ", this.editedIndex, "click: ", this.clickMenu);

      //新增
      if (this.editedItem.stockInTag_Date == '' && this.fromDateVal == '' && this.editedIndex==-1) {
        //console.log("con 2...");
        this.fromDateVal=(new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10);
        //console.log("con 21...", this.fromDateVal);

        let yy_value=this.fromDateVal.substring(0, 4);
        let mmdd_value=this.fromDateVal.substring(5, this.fromDateVal.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.editedItem.stockInTag_Date = yy_value + '/' + mmdd_value;
        this.fromDateVal='';
        return;
      }

      if (this.clickMenu) {
        console.log("con 3...");
        if (!(this.editedItem.stockInTag_Date != '' && this.fromDateVal == '')) {
          let yy_value=this.fromDateVal.substring(0, 4);
          let mmdd_value=this.fromDateVal.substring(5, this.fromDateVal.length);
          mmdd_value=mmdd_value.replace('-','/');
          let b = parseInt(yy_value);
          b = b - 1911;
          yy_value = b.toString()
          this.editedItem.stockInTag_Date = yy_value + '/' + mmdd_value;
          this.fromDateVal = '';
        }
        this.clickMenu=false;
        return;
      }
      if (this.editedItem.stockInTag_Date != '' && this.fromDateVal == '') {
        console.log("con 4...",this.editedItem.stockInTag_Date, this.fromDateVal);
        return;
      }

    },

    fromDateDispP() {  //output: editedItem.stockInTag_reagPeriod
      console.log("con p1...", "edit: ", this.editedItem.stockInTag_reagPeriod, "fromDateVal: ", this.fromDateValP, "index: ", this.editedIndex, "click: ", this.clickMenuP);

      if (this.editedItem.stockInTag_reagPeriod == '' && this.fromDateValP == '' && this.editedIndex==-1) {
        this.fromDateValP=(new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10);

        let S_yy_value=this.fromDateValP.substring(0, 4);
        let I_yy_value=parseInt(S_yy_value) + 3  //效期: 當年 + 3
        let yy_value=I_yy_value.toString()
        let S_mm_value=this.fromDateValP.substring(5, 7);
        let I_mm_value=parseInt(S_mm_value);
        let mm_value=I_mm_value.toString()

        let d = new Date(I_yy_value, I_mm_value, 0);
        let dd_value=d.getDate().toString()
        let mmdd_value=mm_value + '/' + dd_value;

        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.editedItem.stockInTag_reagPeriod = yy_value + '/' + mmdd_value;
        this.fromDateValP='';
        return;
      }
      if (this.clickMenuP) {
        if (!(this.editedItem.stockInTag_reagPeriod != '' && this.fromDateValP == '')) {
          let yy_value=this.fromDateValP.substring(0, 4);
          let mmdd_value=this.fromDateValP.substring(5, this.fromDateValP.length);
          mmdd_value=mmdd_value.replace('-','/');
          let b = parseInt(yy_value);
          b = b - 1911;
          yy_value = b.toString()
          this.editedItem.stockInTag_reagPeriod = yy_value + '/' + mmdd_value;
          this.fromDateValP = '';
        }
        this.clickMenuP=false;
        return;
      }
      if (this.editedItem.stockInTag_reagPeriod != '' && this.fromDateValP == '') {
        return;
      }
    },

    checkDataForSaveButton() {
      if (!!this.editedItem.stockInTag_reagID && !!this.editedItem.stockInTag_EmpID &&
          !!this.editedItem.stockInTag_batch &&
          !this.errorShowForEmployer && !this.errorShowForReagName) {
        //return this.snackbar ? true : false;
        if (this.snackbar)
          this.close();
          //return true;
        return false;
      } else {
        return true
      }
    },
  },

  watch: {
    /*
    'editedItem.stockInTag_reagName': function () {
      if (this.editedItem.stockInTag_reagName !== "") {
        this.filterResults();
        this.isOpen = true;
      } else {
        this.isOpen = false;
      }
    },
    */
    'editedItem.stockInTag_reagID': function () {
      //let isEmpIDRule = /^\w{1,9}$/;
      let isEmpIDRule = /^[A-Za-z0-9.]{1,9}$/;

      this.IDErrMsg = '';
      let result = this.editedItem.stockInTag_reagID.search(isEmpIDRule);
      //let len=this.editedItem.reag_id.length
      console.log("reg: ", result);
      //if (result != -1 || len==0) {
      if (this.editedIndex ==-1) {
        this.IDErrMsg = '';
        return;
      }

      if (result != -1) {
        this.IDErrMsg = '';
      } else {
        this.IDErrMsg = '資料格式錯誤!';
      }
    },

    'editedItem.stockInTag_batch': function () {
      let isEmpBatchRule = /^[A-Za-z0-9]{1,14}$/;

      this.BatchErrMsg = '';
      let result = this.editedItem.stockInTag_batch.search(isEmpBatchRule);
      console.log("reg: ", result);
      if (this.editedIndex ==-1) {
        this.BatchErrMsg = '';
        return;
      }

      if (result != -1) {
        this.BatchErrMsg = '';
      } else {
        this.BatchErrMsg = '錯誤! 資料格式為大小寫英文字或數字';
      }
    },

    fromDateMenu(newValue, oldValue) {
      console.log("fromDateMenu: ", newValue, oldValue)
      if (newValue && !oldValue)
        this.clickMenu=false;
      if (!newValue && oldValue)
        this.clickMenu=true;
      console.log("this.clickMenu: ", this.clickMenu)
    },

    fromDateMenuP(newValue, oldValue) {
      console.log("fromDateMenuP: ", newValue, oldValue)
      if (newValue && !oldValue)
        this.clickMenuP=false;
      if (!newValue && oldValue)
        this.clickMenuP=true;
      console.log("this.clickMenuP: ", this.clickMenuP)
    },

    'item.stockInTag_cnt': function () {
      this.max=this.item.stockInTag_cnt_max;
    },

    dialog (val) {
      val || this.close()

      if (this.editedIndex==-1) {
        this.stockInTag_EmpID = this.currentUser.empID;
      } else {
        this.stockInTag_EmpID = this.editedItem.stockInTag_EmpID;
      }
    },

    dialogDelete (val) {
      val || this.closeDelete();

      if (this.editedIndex==-1) {
        this.stockInTag_EmpID = this.currentUser.empID;
      } else {
        this.stockInTag_EmpID = this.editedItem.stockInTag_EmpID;
      }
    },

    load_SingleTable_ok(val) {
      console.log("load_SingleTable_ok, val: ", val);

      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);

        this.load_SingleTable_ok=false;
        this.listReagents();
      }
    },

    load_2thTable_ok(val) {
      console.log("load_2thTable_ok, val: ", val);

      if (val) {
        this.reagent_Desserts = Object.assign([], this.temp_reagent_Desserts);
        this.load_2thTable_ok=false;
        this.listGridForCheckByReagentName(); // 2023-05-03 add
      }
    },

    load_3thTable_ok(val) {
      console.log("load_3thTable_ok, val: ", val, this.temp_editedItem);

      if (val) {
        this.temp_editedItem.id=this.last_id;
        this.temp_editedItem.stockInTag_cnt=1;
        this.desserts.push(this.temp_editedItem);
        this.temp_desserts.push(this.temp_editedItem); //2023-2-1 add
        this.load_2thTable_ok=false;
      }
    },
    // 2023-04-14 add
    load_4thTable_ok(val) {
      console.log("load_4thTable_ok, val: ", val);

      if (val) {
        this.autocomplete_items = Object.assign([], this.temp_autocomplete_items);
        this.load_4thTable_ok = false;
      }
    },

    autocomplete_search(val) {
      val && val !== this.autocomplete_select && this.querySelections(val)
    },
    //
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }

    this.stockInTag_EmpID = this.currentUser.empID;

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listStockInData();
    //this.initialize()
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listStockInData();

    },

    listStockInData() {
      const path = '/listStockInData';
      console.log("listStockInData, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_SingleTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_SingleTable_ok=false;
      });
    },

    listReagents() {
      const path = '/listReagents';
      console.log("listReagents, Axios get data...")
      axios.get(path)
      .then((res) => {
        let temp_len=res.data.outputs.length
        console.log("GET ok, total records:", temp_len);
        for (let i=0; i<temp_len; i++) {
          let temp_obj = {
            reag_id: res.data.outputs[i]['reag_id'],
            reag_name: res.data.outputs[i]['reag_name'],
            reag_temp: res.data.outputs[i]['reag_temp'],
          }
          this.temp_reagent_Desserts.push(temp_obj);
        }

        ////this.reagentForSelect = this.temp_reagent_Desserts.map(function(p) {  //
        ////  return p.reag_id;
        ////});
        ////this.reagentForSelect = [...new Set(this.reagentForSelect)];  //去除重複項目

        this.load_2thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_2thTable_ok=false;
      });
    },

    listGridForCheck() {
      console.log("listGridForCheck, Axios post data...", this.editedItem.stockInTag_reagID)
      const path = '/listGridForCheck';
      this.editedItem.stockInTag_reagID=this.editedItem.stockInTag_reagID.trim()  //2023-06-15  add
      if (this.editedItem.stockInTag_reagID.length ==0)  //2023-06-15 add
        return
      var payload= {
        reag_id:  this.editedItem.stockInTag_reagID,
      };
      axios.post(path, payload)
      .then((res) => {
        console.log("GET ok, status: ", res.data.status);
        if (!res.data.status) {
          this.snackbar=true;
          this.snackbar_color='red accent-2';
          this.snackbar_info= '資材暫無儲位資料, 請先設定儲位資料!';
          this.snackbar_icon_color= '#adadad';
        }
      })
      .catch((error) => {
        console.error(error);
        console.log("通訊錯誤!");
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '通訊錯誤!';
        this.snackbar_icon_color= '#adadad';
      });
    },
    //2023-04-14 add
    listGridForCheckByReagentName() {
      console.log("listGridForCheckByReagentName, Axios post data...", this.editedItem.stockInTag_reagName)
      const path = '/listGridForCheckByReagentName';

      var payload= {
        reag_name:  this.editedItem.stockInTag_reagName,
      };
      axios.post(path, payload)
      .then((res) => {
        console.log("GET ok, status: ", res.data.status);
        //if (res.data.status) {
          this.temp_autocomplete_items=res.data.outputs;
          this.load_4thTable_ok=true;
        //} else {
        //  this.snackbar_color='red accent-2';
        //  this.snackbar=true;
        //  this.snackbar_info= '無資材資料!';
        //  this.snackbar_icon_color= '#adadad';
        //
        //  this.load_2thTable_ok=false;
        //}
      })
      .catch((error) => {
        console.error(error);
        console.log("通訊錯誤!");

        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '通訊錯誤!';
        this.snackbar_icon_color= '#adadad';

        this.load_4thTable_ok=false;
      });
    },
    //2023-04-14 add
    querySelections (v) {
      this.autocomplete_loading = true
      // Simulated ajax query
      this.redirectTimeout = setTimeout(() => {
        this.autocomplete_items = this.temp_autocomplete_items.filter(e => {
          return (e || '').toLowerCase().indexOf((v || '').toLowerCase()) > -1
        })
        this.autocomplete_loading = false;
      }, 500)
    },
    //
    setRowStyle(item) {
      return 'style-1';
    },

    closeDateP() {
      console.log("closeDateP");
    },

    getdata(item) {
      console.log("getdata");

      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.desserts.indexOf(item);

      console.log(this.desserts[this.editedIndex].stockInTag_cnt);
      console.log(this.temp_desserts);
      console.log("editedIndex: ", this.editedIndex);
      this.temp_desserts[this.editedIndex]['stockInTag_cnt'] = this.desserts[this.editedIndex].stockInTag_cnt;
      console.log(this.temp_desserts);

      this.updateStockInByCnt(this.desserts[this.editedIndex]);
    },
    /*
    checkPerm() {
      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }
    },
    */
    editItem (item) {
      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      console.log("edit item: ", item, this.editedItem)
    },

    deleteItem (item) {
      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.desserts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
      console.log("delete item: ", item, this.editedItem)
    },

    deleteItemConfirm () {
      //this.removeStockIn(this.editedItem.emp_id);
      this.removeStockIn(this.editedItem);

      if (!this.tosterOK) {
        this.desserts.splice(this.editedIndex, 1)
        console.log("deleteItem: ", this.editedItem);

        this.closeDelete()
      }
    },

    //removeStockIn(id) {  //依user id來刪除後端table資料
    removeStockIn(object) {  //依user id來刪除後端table資料
      console.log("---click remove_stockIn data---", object);

      const  path='/removeStockIn';
      let payload = Object.assign({}, object);

      //let payload= {
      //  ID: id,
      //};
      axios.post(path, payload)
      .then(res => {
        console.log("remove stockIn status: ", res.data.status);
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem)
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err)
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
      });
    },

    close () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.fromDateVal='';
        this.fromDateValP='';
        this.editedIndex = -1
      })
    },

    closeDelete () {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save() {
      console.log("click save button, editedIndex: ", this.editedIndex, this.editedItem);

      if (this.editedIndex == -1) {    //add
        console.log("click save, add")
        this.load_3thTable_ok=false;
        this.createStockIn(this.editedItem);
        if (!this.tosterOK) {
          //console.log("SAVE_1: ", this.editedItem)
          //this.desserts.push(this.editedItem);
          //console.log("SAVE_2: ", this.desserts);
          this.in_drafTags++;
          this.close();
        }
      } else {    //edit
        console.log("click save, update")
        this.updateStockIn(this.editedItem);
        if (!this.tosterOK) {
          Object.assign(this.desserts[this.editedIndex], this.editedItem)
          this.close();
        }
      }
      /*
      if (this.editedIndex > -1) {
        Object.assign(this.desserts[this.editedIndex], this.editedItem)
      } else {
        //this.editedItem.id=this.desserts.length+1;
        this.desserts.push(this.editedItem);
        this.in_drafTags++;
      }
      this.close()
      */
    },

    updateStockIn(object) {  //編輯 後端table資料
      console.log("---click update_stockIn data---", object);

      const path='/updateStockIn';
      let payload = Object.assign({}, object);

      axios.post(path, payload)
      .then(res => {
        console.log("update StockIn data, status: ", res.data.status);
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem);
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
      });
    },

    updateStockInByCnt(object) {  //編輯 後端table資料
      console.log("---click update_stockIn_by_cnt data---", object);

      const path='/updateStockInByCnt';
      let payload = Object.assign({}, object);

      axios.post(path, payload)
      .then(res => {
        console.log("update StockIn data, status: ", res.data.status);
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem);
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
      });
    },

    createStockIn(object) {  //新增 後端table資料
      console.log("---click createStockIn data---, editdata:", object);
      this.temp_editedItem = Object.assign({}, object);

      //const defaultPassword='a12345678';
      const path='/createStockIn';
      object.stockInTag_cnt=1;
      let payload = Object.assign({}, object);
      axios.post(path, payload)
      .then(res => {
        console.log("save StockIn data, status: ", res.data.status, res.data.last_id);
        if (res.data.status) {
          //object.id = res.data.last_id;
          this.last_id = res.data.last_id;
          console.log("HELLO_1 createStockIn, ", object);
          //this.temp_editedItem = Object.assign({}, object);
          console.log("HELLO_2 createStockIn, ", this.temp_editedItem);
          this.editedItem = Object.assign({}, this.defaultItem);
          //this.editedItem.id = res.data.last_id;
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面

          this.load_3thTable_ok=true;
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
          this.load_3thTable_ok=false;
        }
      })
      .catch(err => {
        console.error(err);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        this.load_3thTable_ok=false;
      });
    },

    tags_draftButton() {
      console.log("press draf Button...");

      localStorage.setItem("tags_draft", JSON.stringify(this.desserts));

      this.$router.push({
        name: 'Navbar',
        params: {
          in_drafTags: this.in_drafTags,
        }
      });
    },

    tags_saveButton () {
      console.log("press save Button...");

    },

    permCloseFun () {
      this.permDialog = false
      console.log("press permission Close Button...");
      this.$router.push('/navbar');
    },
    rightCloseFun() {
      this.rightDialog = false
      console.log("press permission Close Button...");
    },
  },

  beforeDestroy() {
    if (this.redirectTimeout) {
      clearTimeout(this.redirectTimeout);
    }
  },
}
</script>

<style lang="scss" scoped>
@import url(
  'https://fonts.googleapis.com/css?family=Noto+Sans+TC:400,500&display=swap&subset=chinese-traditional'
);

div.v-toolbar__title {
  margin: 0;
  font-family: "Noto Sans TC", "Microsoft Yahei", "微軟雅黑", sans-serif;
}

small.msgErr {
  font-size: 80%;
  color: red;
  margin-top: -10px;
}

::v-deep .v-data-table-header {
  background-color: #7DA79D;
}

::v-deep .v-label {
  font-size: 1em
}
::v-deep .v-label--active {
  font-size: 1.2em;
  font-weight: bold;
}

::v-deep .style-1 td {
  padding-left: 8px !important;
  padding-right: 0px !important;
}

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
  text-align: start !important;
}
::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th:nth-last-child(1) {
  padding-right: 8px !important;
  text-align: center !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}

::v-deep .v-data-table-header th:nth-last-child(2) span {
  color: #1f4788 !important;
}
/*  2023-04-18 add  */
::v-deep span.v-list-item__mask {
  background: #87CEFA !important;
}
</style>