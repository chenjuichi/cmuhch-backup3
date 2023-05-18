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
      <v-card width="72vw">
        <!-- desserts為dataTable的資料源-->
        <!-- :sort-by.sync="sortBy" -->
        <v-data-table
          :headers="headers"
          :items="desserts"
          :item-class="setRowStyle"
          :options.sync="pagination"
          class="elevation-1"
          @current-items="currentItems"

          @click:row="booking_clicked"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>出庫標籤資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="1000px">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on" v-show="currentUser.perm<=2">
                    <v-icon left dark>mdi-table-plus</v-icon>新增領料標籤資料
                  </v-btn>
                </template>

                <v-card width="82vw">
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                <!-- 進度條 -->
                    <ul class="list-unstyled multi-steps">
                      <li id="step-1" style="font-size: 16px; font-weight: 600;" :class="{'is-active': active1}">
                        領料日期
                        <div class="progress-bar progress-bar--success">
                          <div class="progress-bar__bar" :class="{'progress-bar__trans':step_trans>0}"></div>
                        </div>
                      </li>
                      <li id="step-2" style="font-size: 16px; font-weight: 600;" :class="{'is-active': active2}">
                        主要產品
                        <div class="progress-bar progress-bar--success">
                          <div class="progress-bar__bar" :class="{'progress-bar__trans':step_trans>1}"></div>
                        </div>
                      </li>
                      <li id="step-3" style="font-size: 16px; font-weight: 600;" :class="{'is-active': active3}">
                        供應商
                        <div class="progress-bar progress-bar--success">
                          <div class="progress-bar__bar" :class="{'progress-bar__trans':step_trans>2}"></div>
                        </div>
                      </li>
                      <li id="step-4" style="font-size: 16px; font-weight: 600;" :class="{'is-active': active4}">
                        在庫試劑
                      </li>
                    </ul>
                <!-- -->
                  </v-card-title>

                  <v-card-text style="position: relative; top: -20px; right: -15px;">
                    <v-container fluid>
                      <!-- 第1列-->
                      <v-row align="center" justify="center" >
                        <v-col cols="12" md="3">
                          <v-tooltip v-model="errorShowForEmployer" top color="error">
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                v-model="editedItem.stockOutTag_EmpID"
                                :value="stockOutTag_EmpID"
                                label="員工編號"
                                readonly
                              ></v-text-field>
                            </template>
                            <span>員工編號錯誤!</span>
                          </v-tooltip>
                        </v-col>
                        <v-col cols="12" md="3">
                          <v-text-field
                            v-model="editedItem.stockOutTag_Employer"
                            :value="fromstockOutTagEmpIdDisp"
                            label="領料人員"
                            readonly
                          ></v-text-field>
                        </v-col>
                        <!--
                        <v-col cols="12" md="2">
                          <v-select
                            :items="['盒', '包', '袋', '瓶', '個', '條']"
                            label="領用單位"
                            v-model="editedItem.stockOutTag_unit"
                          ></v-select>
                        </v-col>
                        -->
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
                                label="領料日期"
                                prepend-icon="event"
                                readonly
                                :value="fromDateDisp"
                                v-model="editedItem.stockOutTag_Date"
                                v-on="on"
                                @blur="setStep1"

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

                      <v-row>
                      </v-row>

                      <!-- 第2列-->
                      <v-row mt-n5 align="center" justify="center">
                          <label for="main" class="adjLabel">
                            <!--<i class="fas fa-align-left"></i>-->
                            主要產品 (共{{label_count}}項)
                          </label>
                          <v-col cols="12" md="8" ml="2" class="adjTopForSlide">
                            <v-sheet>
                              <v-slide-group
                                multiple
                                show-arrows
                                v-model="selectedCatalogs">
                                <!-- products為slide-item的資料源-->
                                <v-slide-item
                                  v-for="(product, index) in products"
                                  :key="index"
                                  v-slot="{ active, toggle }"
                                >
                                  <v-btn
                                    class="mx-2 product-style"
                                    :input-value="active"
                                    active-class="primary"
                                    depressed
                                    rounded
                                    @click="toggle"
                                    @blur="setStep2"
                                  >
                                    {{ product }}
                                  </v-btn>
                                </v-slide-item>
                              </v-slide-group>
                            </v-sheet>
                          </v-col>
                          <v-col cols="12" md="4" ml="2" class="adjTopForSelect">
                            <!-- suppliers為v-select的資料源-->
                            <v-select
                            @change="checkSelect"
                            :items="suppliers"
                            label="供應商"
                            outlined
                            multiple
                            class="mt-1 ml-3 mx-auto"
                            style="width:100px; height:20px;"
                            v-model="selectSuppliers"

                          ></v-select>
                          </v-col>
                      </v-row>

                      <!-- 第3列-->
                      <v-row mt-10 align="center" justify="center" >
                        <template>
                          <v-data-table
                            dense
                            v-model="stock_selected"
                            :headers="stock_headers"
                            :items="stock_desserts"
                            :item-class="setRowStyleForStockOut"
                            @item-selected="booking_selected"
                            style="width: 870px;"
                            item-key="id"
                            show-select
                            :single-select="stock_singleSelect"
                            class="elevation-1"
                            no-data-text=""
                            :footer-props="{
                              'itemsPerPageText': '每頁的資料筆數',
                              'items-per-page-options':[5]
                            }"
                          >
                            <template v-slot:[`item.count`]="{ item }">
                              <div class="adjNumeric">
                              <vue-numeric-input
                                v-model="item.count"
                                min=1
                                max=10
                                :step="1"
                                align="center"
                                size="small"
                              ></vue-numeric-input>
                              </div>
                            </template>

                          </v-data-table>
                        </template>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions style="position: relative; top: -20px;">
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                    <v-btn
                      color="blue darken-1"
                      text
                      @click="save"
                      :disabled="check_stock_selected"
                    >
                      確定
                    </v-btn>
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
            </v-toolbar>
          </template>
          <!--
          <template v-slot:[`item.stockOutTag_cnt`]="{ item, index }">
            <v-text-field
              v-model="item.stockOutTag_cnt"
              :readonly="getStockOut(item, index)"

              type="number"
              min=1
              :max="item.stockOutTag_max_cnt"

              @input="getData(item)"
            ></v-text-field>
          </template>
          -->
          <template v-slot:[`item.stockOutTag_cnt`]="{ item }">
            <v-text-field
              v-model="item.stockOutTag_cnt"
              type="number"
              value="item.stockOutTag_cnt"
              @input="getdata(item)"
              min=1

              :max="item.stockOutTag_cnt_max"

              :disabled="currentUser.perm>2"
            ></v-text-field>
          </template>




          <template v-slot:[`item.actions`]="{ item, index }">

            <v-icon small class="mr-2" @click="editItem(item)" style="color: blue;">
              mdi-pencil
            </v-icon>

            <v-icon
              small
              @click="deleteItem(item)"
              style="color: red;"

            >
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
import VueNumericInput from 'vue-numeric-input';

import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/js/all.js';

import StepProgress from 'vue-step-progress';
import 'vue-step-progress/dist/main.css';

import axios from 'axios';

import Common from '../../mixin/common.js'

export default {
  name: 'stockOutTag',

  mixins: [Common],

  components: {
    VueNumericInput,
    'step-progress': StepProgress
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
    /*
        mySteps: ['Step 1', 'Step 2', 'Step 3'],
        currentStep: 0,
        activeColor: 'red',
        passiveColor: 'gray',
        lineThickness: 2,
        activeThickness: 2,
        passiveThickness: 2,
    */
//--stock-datatable--//
    label_count: 0,
    active1: true,
    active2: false,
    active3: false,
    active4: false,
    step: 'step0',
    step_trans: 0,

    //activedField: false,

    editedStockIndex: -1,

    stock_singleSelect: false,
    stock_selected: [],
    stock_headers: [
      { text: '資料ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', value: 'stockIn_reagent_id', align: 'start', sortable: true, width: '120px' },
      { text: '品名', value: 'stockIn_reagent_name', sortable: false, width: '180px' },
      { text: '批號', value: 'stockIn_batch', sortable: false, width: '80px' },
      { text: '供應商', value: 'stockIn_supplier', sortable: true, width: '120px' },
      { text: '效期', value: 'stockIn_reagent_period', sortable: true, width: '75px' },
      { text: '入庫日期', value: 'stockIn_date', sortable: true, width: '75px' },
      //{ text: '批號', value: 'protein', sortable: false, width: '18%' },
      { text: '領料單位', value: 'stockIn_reagent_Out_unit', sortable: false, width: '70px' },
      { text: '領料數量', value: 'stockIn_reagent_Out_cnt', sortable: false, width: '16%' },
    ],
    stock_desserts: [ ],
    temp_stock_desserts: [],
//--
    currentUser: {},
    permDialog: false,
    rightDialog: false,

    snackbar: false,
    snackbar_color: 'success',
    snackbar_right: true,
    snackbar_top: true,
    snackbar_info: '',
    snackbar_icon_color: '#adadad',

    stockOutTag_EmpID: '',   //出庫人員之員工編號

    errorShowForEmployer: false,
    errorShowForReagName: false,

    fromDateMenu: false,
    fromDateVal: null,
    minDate: "2012-07-01",
    maxDate: "2042-06-30",

    dialog: false,
    dialogDelete: false,

    selectedCatalogs: [],

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },

    //資料表頭
    headers: [
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'stockOutTag_reagID', width: '90px' },
      { text: '品名', sortable: true, value: 'stockOutTag_reagName', width: '120px' },
      { text: '批號', sortable: true, value: 'stockOutTag_batch', width: '60px' },
      { text: '供應商', sortable: true, value: 'stockOutTag_supplier', width: '120px' },
      { text: '效期', sortable: true, value: 'stockOutTag_reagPeriod', width: '75px' },
      { text: '入庫日期', sortable: true, value: 'stockOutTag_InDate', width: '75px' },
      { text: '領料日期', sortable: true, value: 'stockOutTag_Date', width: '75px' },
      { text: '領料人員', sortable: true, value: 'stockOutTag_Employer', width: '75px' },
      { text: '領料單位', sortable: false, value: 'stockOutTag_unit', width: '65px', align: 'start' },
      { text: '領料數量', sortable: false, value: 'stockOutTag_cnt', width: '65px', align: 'start', class: 'my-header-style' },
      { text: 'Actions', sortable: false, value: 'actions', width: '60px', class: 'my-header-style' },
    ],

    sortBy: ['stockOutTag_reagID', 'stockOutTag_reagName'],
    max: 1,

    currentItems_desserts: [],

    desserts: [],         //dataTable的資料
    temp_desserts: [],
    desserts_max_cnt: [],

    products: [],         //slide-item的主要產品資料
    temp_products: [],

    suppliers: [],        //v-select的供應商資料
    temp_suppliers: [],

    items: [],
    temp_items: [],

    editedIndex: -1,
    editedItem: {
      //id: 0,
      stockOutTag_ID: '',
      stockOutTag_reagID: '',
      stockOutTag_reagName: '',
      stockOutTag_reagPeriod: '',
      //stockOutTag_reagTemp: '',
      stockOutTag_InDate: '',
      stockOutTag_unit: '',
      stockOutTag_Date: '',
      stockOutTag_EmpID: '',
      stockOutTag_Employer: '',
      //stockOutTag_batch: '',
      stockOutTag_cnt_max: '',  //2023-02-13 add
      stockOutTag_cnt: '',
    },

    defaultItem: {
      stockOutTag_ID: '',
      stockOutTag_reagID: '',
      stockOutTag_reagName: '',
      stockOutTag_reagPeriod: '',
      //stockOutTag_reagTemp: '',
      stockOutTag_InDate: '',
      stockOutTag_unit: '',
      stockOutTag_Date: '',
      stockOutTag_EmpID: '',
      stockOutTag_Employer: '',
      //stockOutTag_batch: '',
      stockOutTag_cnt_max: '',  //2023-02-13 add
      stockOutTag_cnt: '',

    },

    deleteObject: {},

    isAllSelected: false,
    selectSuppliers: [],

    load_SingleTable_ok: false, //true: temp_desserts ok
    load_2thTable_ok: false,    //true: temp_products ok
    load_3thTable_ok: false,    //true: temp_suppliers ok
    load_4thTable_ok: false,    //true: temp_suppliers ok
    load_5thTable_ok: false,    //true: temp_stock_desserts ok
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },

    fromstockOutTagEmpIdDisp() {
      if (this.stockOutTag_EmpID != '') {
        if (this.editedItem.stockOutTag_EmpID == '') {
          this.editedItem.stockOutTag_EmpID=this.currentUser.empID;
          this.editedItem.stockOutTag_Employer=this.currentUser.name;
        }
        this.errorShowForEmployer=false;
        return this.editedItem.stockOutTag_Employer;
      } else {
        this.this.editedItem.stockOutTag_EmpID='';
        this.editedItem.stockOutTag_Employer='';
        this.errorShowForEmployer=true;
        return '';
      }
    },
    /*
    fromReagIdDisp() {
      if (this.editedItem.stockOutTag_reagID != '') {
        //console.log("result 1...");
        const result = this.stockOutTag_Desserts.find(x => x.stockOutTag_reagID === this.editedItem.stockOutTag_reagID);
        //console.log("result 1-2...", result);

        if (result != 'undefined' && result != null) {
          console.log("result 2...", result);
          this.editedItem.stockOutTag_reagName=result.stockOutTag_reagName;
          this.editedItem.stockOutTag_reagPeriod=result.stockOutTag_reagPeriod;
          //this.editedItem.stockOutTag_reagTemp=result.stockOutTag_reagTemp;
          this.errorShowForReagName=false;
          return result.stockOutTag_reagName;
        } else {
          this.editedItem.stockOutTag_reagName='';
          this.editedItem.stockOutTag_reagPeriod='';
          //this.editedItem.stockOutTag_reagTemp='';
          this.errorShowForReagName=true;
          return '';
        }
      }
    },
    */
    fromDateDisp() {  //output: editedItem.stockOutTag_Date
      if (this.fromDateVal != null) {
        let yy_value=this.fromDateVal.substring(0, 4);
        let mmdd_value=this.fromDateVal.substring(5, this.fromDateVal.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.editedItem.stockOutTag_Date = yy_value + '/' + mmdd_value;
      }
      return this.fromDateVal;
    },

    check_stock_selected() {
      if (this.stock_selected.length == 0)
        return true;
      else
        return false;
    },

  },

  watch: {
    dialog (val) {
      val || this.close();

      if (this.editedIndex==-1) {
        this.stockOutTag_EmpID = this.currentUser.empID;
      } else {
        this.stockOutTag_EmpID = this.editedItem.stockOutTag_EmpID;
      }
    },

    dialogDelete (val) {
      val || this.closeDelete()
    },

    //selectSuppliers(val) {
    //  let uniqueArray_for_suppliers = val.filter(function(item, pos, self) {
    //      return self.indexOf(item) == pos;
    //  });
    //
    //  this.selectSuppliers=uniqueArray_for_suppliers;
    //},
    stock_selected(val) {
      if (val.length > 0 && this.step=='step3')
        this.next();
    },

    //selectedCatalogs(val) {
    selectedCatalogs(newValue, oldValue) {
      console.log("hello....selectedCatalogs: ", newValue, oldValue, newValue.length)
      //if (newValue!=oldValue) {
        this.selectSuppliers=[];

        this.load_4thTable_ok=false;
        this.listSuppliersBySelect();
      //}
    },

    selectSuppliers(newValue, oldValue) {
      console.log("hello....selectSuppliers: ", newValue, oldValue, newValue.length)
      //console.log("2.check...", this.temp_suppliers);

      //if (newValue!=oldValue) {
        this.load_5thTable_ok=false;    //reset read_flag, false: ready to read, true: readed ok
        this.listStockInDataBySelect();
      //}
    },

    'item.stockOutTag_cnt': function () {
      this.max=this.item.stockOutTag_cnt_max;
    },

    load_5thTable_ok(val) {
      console.log("load_5thTable_ok, suppliers: ", val)

      if (val) {
        this.load_5thTable_ok=false;
        this.stock_desserts = Object.assign([], this.temp_stock_desserts);
      }
    },

    load_4thTable_ok(val) {
      console.log("load_4thTable_ok, suppliers: ", val)

      if (val) {
        this.load_4thTable_ok=false;
        this.suppliers = Object.assign([], this.temp_suppliers);
        //
        //this.selectSuppliers = [];
        //for (let i=0; i<this.suppliers.length; i++) {
        //  this.selectSuppliers.push(this.suppliers[i])
        //}
        //this.isAllSelected = true;
        //
        this.stock_desserts = Object.assign([], this.temp_stock_desserts);
      }
    },

    load_3thTable_ok(val) {
      console.log("load_3thTable_ok, suppliers: ", val)

      if (val) {
        this.load_3thTable_ok=false;
        console.log("b, load_3thTable_ok, supplier: ", this.suppliers)
        this.suppliers = this.temp_suppliers.map(item => Object.values(item)[4]); //從object中copy value至array

        this.suppliers.unshift('全部');  //將'全部'push到陣列的第1個, //2023-02-15 add

        console.log("a, load_3thTable_ok, supplier: ", this.suppliers)
      }
    },

    load_2thTable_ok(val) {
      console.log("load_2thTable_ok, products: ", val)

      if (val) {
        this.label_count=this.temp_products.length
        this.products = Object.assign([], this.temp_products);

        this.load_2thTable_ok=false;
        this.listSuppliers();
      }
    },

    load_SingleTable_ok(val) {
    console.log("load_SingleTable_ok, desserts: ", val)

      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);

        this.desserts = this.desserts.map(v => ({...v, isOnTable: true})) //新增object內的key(isOnTable), true: 資料來自table

        this.load_SingleTable_ok=false;

        this.listProducts();
      }
    },
  },

  created () {
    //console.log("stockOutTag, created()...");

    //load 員工與權限資料
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }
    this.stockOutTag_EmpID = this.currentUser.empID;
    //console.log("empID: ", this.currentUser.empID, this.stockOutTag_EmpID)

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listStockOutData();
    //this.initialize()
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listStockOutData();
      /*
      this.desserts = [

        {
          //id: 1,
          stockOutTag_reagID: '123456789',
          stockOutTag_reagName: 'ABC',
          stockOutTag_reagPeriod: '111/10/31',
          //stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          //stockOutTag_batch: '1110012345B123400066',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '2',
        },
        {
          //id: 2,
          stockOutTag_reagID: '234567891',
          stockOutTag_reagName: 'ABCD',
          stockOutTag_reagPeriod: '111/12/31',
          //stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          //stockOutTag_batch: '1110012345C123400055',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '4',
        },
        {
          //id: 3,
          stockOutTag_reagID: '234567892',
          stockOutTag_reagName: 'A11',
          stockOutTag_reagPeriod: '111/12/31',
          //stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '111/01/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          //stockOutTag_batch: '1110012345B123400033',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 4,
          stockOutTag_reagID: '234567893',
          stockOutTag_reagName: 'A12',
          stockOutTag_reagPeriod: '112/6/30',
          //stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '110/12/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          //stockOutTag_batch: '1110012345B123400033',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 5,
          stockOutTag_reagID: '234567894',
          stockOutTag_reagName: 'B2233',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '2~8度C',
          stockOutTag_InDate: '110/10/01',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          //stockOutTag_batch: '1110012345B123400022',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '5',
        },
        {
          //id: 6,
          stockOutTag_reagID: '234567897',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/01/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '4',
        },
        {
          //id: 7,
          stockOutTag_reagID: '234567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 8,
          stockOutTag_reagID: '234567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '110/09/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 9,
          stockOutTag_reagID: '214567897',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '10',
        },
        {
          //id: 10,
          stockOutTag_reagID: '214567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '110/12/01',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 11,
          stockOutTag_reagID: '214567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '2',
        },
        {
          //id: 12,
          stockOutTag_reagID: '224567897',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/02/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 13,
          stockOutTag_reagID: '224567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/03/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
        {
          //id: 14,
          stockOutTag_reagID: '224567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          //stockOutTag_reagTemp: '常溫',
          stockOutTag_InDate: '111/05/01',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          //stockOutTag_batch: '1110012345A123400001',
          stockOutTag_unit: '盒',
          stockOutTag_cnt: '1',
        },
      ];
      */

      //this.items = [
      //  '全部',
      // 'pmcA', 'pmcB', '3234', 'pmcC', 'pmcD'
      //]
    },

    listStockOutData() {    //從後端讀取dataTable的資料
      const path = '/listStockOutData';
      console.log("listStockOutData, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_SingleTable_ok=true;    //true: dataTable的資料ok
      })
      .catch((error) => {
        console.error(error);
        this.load_SingleTable_ok=false;
      });
    },

    listSuppliers() {       //從後端讀取v-select的供應商資料
      const path = '/listSuppliers';
      console.log("listSuppliers, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_suppliers = res.data.outputs;
        console.log("GET ok, total temp_suppliers: ",this.temp_suppliers, res.data.outputs.length);

        //this.temp_suppliers.unshift('全部');  //將'全部'push到陣列的第1個, //2023-02-15 add

        this.load_3thTable_ok=true;   //true: v-select的供應商資料ok
      })
      .catch((error) => {
        console.error(error);
        this.load_3thTable_ok=false;
      });
    },

    listSuppliersBySelect() {       //從後端讀取v-select的供應商資料及v-data-table的stockIn資料
      console.log("listSuppliersBySelect, Axios post data...")
      const path = '/listSuppliersBySelect';

      let arr_for_products=[]
      for (let i=0; i<this.selectedCatalogs.length; i++) {
        arr_for_products.push(this.products[this.selectedCatalogs[i]])
      }

      var payload= {
        //catalogs: this.selectedCatalogs,
        catalogs: arr_for_products,
        //suppliers: arr_for_suppliers,
      };
      axios.post(path, payload)
      .then((res) => {
        this.temp_stock_desserts = res.data.outputs_for_stockOut;

        //console.log("aa0.check...", this.temp_suppliers);

        this.temp_suppliers = res.data.outputs_for_supplier.filter(function(item, pos, self) {
          return self.indexOf(item) == pos;
        });

        //console.log("aa1.check...", this.temp_suppliers);

        this.temp_suppliers.unshift('全部');  //將'全部'push到陣列的第1個

        //console.log("aa2.check...", this.temp_suppliers);

        console.log("POST ok, and return total records: (supplier)", res.data.outputs_for_supplier.length, " (stock)", res.data.outputs_for_stockOut.length);
        this.load_4thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_4thTable_ok=false;
      });
    },

    listStockInDataBySelect() {
      console.log("listStockInDataBySelect, Axios post data...")
      const path = '/listStockInDataBySelect';

      let arr_for_suppliers=[];
      for (let i=0; i<this.selectSuppliers.length; i++) {
        arr_for_suppliers.push(this.selectSuppliers[i])
      }
      //console.log("3.check...", this.temp_suppliers);

      let arr_for_products=[]
      for (let i=0; i<this.selectedCatalogs.length; i++) {
        arr_for_products.push(this.products[this.selectedCatalogs[i]])
      }

      // 2023-05-17 add block, for remove all duplicates from an array of objects
      //console.log("before => arr_for_products, arr_for_suppliers payload: ", arr_for_products, arr_for_suppliers)
      arr_for_products = arr_for_products.filter((value, index, self) =>
        index === self.findIndex((t) => (t.id === value.id && t.stockIn_id === value.stockIn_id))
      )
      console.log("after => arr_for_products, arr_for_suppliers payload: ", arr_for_products, arr_for_suppliers)
      // end block

      //console.log("3-1.check...", this.temp_suppliers);

      var payload= {
        catalogs:  arr_for_products,
        suppliers: arr_for_suppliers,
        //suppliers: new_arr_for_suppliers,
      };
      axios.post(path, payload)
      .then((res) => {
        this.temp_stock_desserts = res.data.outputs_for_stockOut;

        console.log("output: ", res.data.outputs_for_stockOut)
        //console.log("4.check...", this.temp_suppliers);

        /*
        this.temp_stock_desserts = res.data.outputs_for_stockOut.filter((value, index, self) =>
          index === self.findIndex((t) => (
            //t.stockIn_reagent_id === value.stockIn_reagent_id
            t.stockIn_id === value.stockIn_id
          ))
        )
        console.log("POST ok, and return total records: ", "(temp)", res.data.outputs_for_stockOut.length, "(real)", this.temp_stock_desserts.length);
        */
        this.load_5thTable_ok=true;       //true: dataTable的stockIn資料ok
      })
      .catch((error) => {
        console.error(error);
        this.load_5thTable_ok=false;   //true: slide-item的主要產品資料ok
      });
    },

    listProducts() {    //從後端讀取slide-item的主要產品資料
      const path = '/listProducts';
      console.log("listProducts, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_products = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_2thTable_ok=true;   //true: slide-item的主要產品資料ok
      })
      .catch((error) => {
        console.error(error);
        this.load_2thTable_ok=false;
      });
    },

    booking_clicked(item, value){
      console.log("booking_clicked: ", item, value);
    },

    booking_selected(item, value) {
      console.log("booking_selected: ", item, value);
    },

    currentItems(item) {
      console.log("currentItems: ", item);
      this.currentItems_desserts =[];
      this.currentItems_desserts = Object.assign([], item);
    },

    setRowStyle(item) {
      //for (let i=0; i<this.stock_selected.length; i++) {
        if (!("isOnTable" in item)) {

        //if (item.stockOutTag_reagID === this.stock_selected[i].stockIn_reagent_id && !item.isOnTable) {
          //item.stockOutTag_cnt=this.stock_selected[i].stockIn_reagent_Out_cnt-item.stockOutTag_cnt;
          return 'style-1';
        //}
      }

      return '';
    },

    setRowStyleForStockOut(item) {
      return 'style-for-data-table';
    },

    getActive(index) {
      let ss=this.currentUser.name != this.currentItems_desserts[index].stockOutTag_Employer?true:false;
      return ss;
    },

    getdata(item) {
      console.log("getdata");

      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      let index = this.desserts.indexOf(item);

      console.log("hello getData, DESSERT data is", this.desserts[index])
      /*
      if (parseInt(this.desserts[index].stockOutTag_cnt)>=this.desserts[index].stockOutTag_cnt_max) {
        console.log("##hello getData, ", this.desserts[index].stockOutTag_cnt, typeof(this.desserts[index].stockOutTag_cnt))
        //console.log("##hello getData, ", this.desserts[index].stockOutTag_cnt_max, typeof(this.desserts[index].stockOutTag_cnt_max))
        this.desserts[index].stockOutTag_cnt=this.desserts[index].stockOutTag_cnt_max.toString().slice()
        console.log("##%%hello getData, ", this.desserts[index].stockOutTag_cnt, typeof(this.desserts[index].stockOutTag_cnt))
        //return;
      }
      if (parseInt(this.desserts[index].stockOutTag_cnt)<=1) {
        //console.log("hello getData, ", this.desserts[index].stockOutTag_cnt, typeof(this.desserts[index].stockOutTag_cnt))
        //console.log("hello getData, ", this.desserts[index].stockOutTag_cnt_max, typeof(this.desserts[index].stockOutTag_cnt_max))
        this.desserts[index].stockOutTag_cnt="1"
        //return;
      }
      */

      if (this.desserts[index].stockOutTag_cnt=='') {
        //this.desserts[index].stockOutTag_cnt==this.desserts[index].stockOutTag_cnt_max  ////2023-02-13 add
        //console.log("hello getData, index is blank...")
        return; //2023-02-13 mark
      }

      console.log("getdata, updateStockOutAndStockInData---");

      const path='/updateStockOutAndStockInData';
      var payload= {
        stockOut_array: this.desserts[index],
        stockOut_count: 1,
      };

      axios.post(path, payload)
      .then(res => {
        console.log("update outTag data status: ", res.data.status)
      })
      .catch(err => {
        console.error(err);
      });
    },
    /*
    getStockOut(item) {
    //#getStockOut(index) {
      //let rr=(this.pagination.page-1)*this.pagination.itemsPerPage+index;
      //let ss=this.currentUser.name != this.desserts[rr].stockOutTag_Employer?true:false;
      if (("isOnTable" in item))
        return true;
      else
        return false;

      //#let ss=this.currentUser.name != this.currentItems_desserts[index].stockOutTag_Employer?true:false;
      //#return ss;
    },
    */
    checkSelect(e) {
      let ck=e.includes('全部');
      console.log('checkSelect..., ', e, ck, this.isAllSelected);
      if (ck) {  //press全部, 且不是全部的狀態
        if (this.isAllSelected) {
          console.log('hello begin...');
          this.isAllSelected = false;
          this.selectSuppliers = [];
          for (let i=1; i<e.length; i++) {
            this.selectSuppliers.push(e[i])
          }
        } else {
          console.log('Select all...');
          this.selectSuppliers = [];
          for (let i=0; i<this.suppliers.length; i++) {
            this.selectSuppliers.push(this.suppliers[i])
          }
          this.isAllSelected = true;
        }
      } else if (this.isAllSelected) {  //取消全部, 且不是全部的狀態
        console.log('Remove all...');
        this.selectSuppliers = [];
        this.isAllSelected = false;
      } else {  //取消全部, 且不是全部的狀態
        console.log('Click some item...');
        this.selectSuppliers = [];
        for (let i=0; i<e.length; i++) {
          let jj=this.suppliers.includes(e[i])
          console.log('item1...', jj);
          if (jj) {
            this.selectSuppliers.push(e[i])
            console.log('item2...', e[i]);
          }
        }
        console.log('length...', e.length, this.suppliers.length);
        if (e.length==this.suppliers.length-1) {
            console.log('Hello end...');
            this.selectSuppliers.unshift('全部')
            this.isAllSelected = true;
        }
      } //end else if

      console.log("setStep3, set step is...");

      if (this.step=='step2') {
        this.next();
      }
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
    },

    deleteItem (item) {
      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.desserts.indexOf(item)
      //this.editedItem = Object.assign({}, item)
      this.deleteObject = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm () {
      this.desserts.splice(this.editedIndex, 1)

      this.closeDelete()

      const path='/deleteStockOutAndStockInData';
      var payload= {
        stockOut_array: this.deleteObject,
        stockOut_count: 1,
      };

      axios.post(path, payload)
      .then(res => {
        console.log("delete outTag data status: ", res.data.status)
      })
      .catch(err => {
        console.error(err);
      });
    },

    close () {
      //清除領料的資料暫存
      //this.stock_desserts=[];
      this.stock_selected=[];
      this.selectSuppliers=[];
      //this.products=[]
      //this.selectedCatalogs=[]; //2023-02-15 mark
      //

      this.active1 = true;
      this.active2 = false;
      this.active3 = false;
      this.active4 = false;
      this.step = 'step0';
      this.step_trans = 0;


      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })

      //console.log("1.check...", this.temp_suppliers);
    },

    closeDelete () {
      this.stock_selected=[];
      this.selectSuppliers=[];
      this.selectedCatalogs=[];

      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save() {
      console.log("save...");
      this.desserts = this.desserts.map(v => ({...v, isOnTable: true}))
      //console.log("save...");

      const i0=this.stock_selected.length;

      let temp_stockOutTag=[]
      for (let i=0; i<i0; i++) {
        let obj = {
          stockOutTag_reagID:  this.stock_selected[i].stockIn_reagent_id,
          stockOutTag_reagName: this.stock_selected[i].stockIn_reagent_name,
          stockOutTag_supplier: this.stock_selected[i].stockIn_supplier,
          stockOutTag_reagPeriod: this.stock_selected[i].stockIn_reagent_period,
          stockOutTag_InDate:  this.stock_selected[i].stockIn_date,
          stockOutTag_Date: this.editedItem.stockOutTag_Date,
          stockOutTag_Employer: this.editedItem.stockOutTag_Employer,
          stockOutTag_cnt: this.stock_selected[i].stockIn_reagent_Out_cnt,
          stockOutTag_cnt_max: this.stock_selected[i].stockIn_reagent_Out_cnt,
          stockOutTag_unit: this.stock_selected[i].stockIn_reagent_Out_unit,
          stockOutTag_InID: this.stock_selected[i].stockIn_id,
          stockOutTag_max_cnt: this.stock_selected[i].stockIn_reagent_Out_cnt,
        };
        this.desserts.push(obj);
        let temp_obj = {
          stockOutTag_Date: this.editedItem.stockOutTag_Date,
          stockOutTag_Employer: this.editedItem.stockOutTag_Employer,
          stockOutTag_cnt: this.stock_selected[i].stockIn_reagent_Out_cnt,
          stockOutTag_unit: this.stock_selected[i].stockIn_reagent_Out_unit,
          stockOutTag_InID: this.stock_selected[i].stockIn_id,
        }
        temp_stockOutTag.push(temp_obj);
      }

      this.close()

      const path='/createStockOut';
      var payload= {
        stockOut_array: temp_stockOutTag,
        stockOut_count: i0,
      };

      axios.post(path, payload)
      .then(res => {
        console.log("create outTag data status: ", res.data.status)
        let i_de=this.desserts.length-1;
        let i_out=res.data.return_outTag_ID.length-1;
        for (let i=0; i<i0; i++) {
          this.desserts[i_de - i].stockOutTag_ID=res.data.return_outTag_ID[i_out - i];
        }
      })
      .catch(err => {
        console.error(err);
      });
    },
    /*
    tags_draftButton () {
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
    */
    setStep1() {
      console.log("setStep1, set step is...");
      if (this.step=='step0') {
        this.next();
      }
    },

    setStep2() {
      console.log("setStep2, set step is...");
      if (this.step=='step1') {
        this.next();
      }
    },

    next() {
      if (this.step === 'step0') {
        //console.log("(領用日期)current step0...., next step1",this.step_trans);
        this.step = 'step1';
        this.step_trans++;
        this.active1=false;
        this.active2=true;
        return;
      }
      if (this.step === 'step1') {
        //console.log("(主要產品)current step1...., next step2",this.step_trans);
        this.step = 'step2';
        this.step_trans++;
        this.active2=false;
        this.active3=true;
        return;
      }
      if (this.step === 'step2') {
        //console.log("(供應商)current step2...., next step3", this.step_trans);
        this.step = 'step3';
        this.step_trans++;
        this.active3=false;
        this.active4=true;
        return;
      }
      if (this.step === 'step3') {
        //console.log("(在庫產品)current step3....", this.step_trans);
        this.step = 'step4';
        this.step_trans++;
        //this.active3=false;
        //this.active4=true;
        //this.active3=false;
        this.active4=false;
        return;
      }
      if (this.step === 'step4') {
        //console.log("current step4....", this.step_trans);
        this.step = 'complete';
        this.active4=false;
        return;
      }
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

::v-deep .v-select__selections {
  overflow-y: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-height: 50px;
}

.adjTopForSelect {
  top: -33px;
  left: 100px;
}

.adjTopForSlide {
  top: -13px;
  left: 100px;
  border-color: gray;
  border-style: solid;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  border-bottom-right-radius: 10px;
  border-bottom-left-radius: 10px;
}

.adjLabel {
  position: absolute;
  top: 70px;
  z-index: 11;
  left: 140px;
  background-color: white;
  padding: 0 5px;
  font-weight: 600;
}

::v-deep div.vue-numeric-input.small {
  width: 6vw !important;
  height: 4vh !important;
}

::v-deep .multi-steps > li.is-active ~ li:before, .multi-steps > li.is-active:before {
  content: counter(stepNum);
  font-family: inherit;
  font-weight: 700;
}

::v-deep .multi-steps > li.is-active ~ li:after, .multi-steps > li.is-active:after {
  background-color: #e1e1e1;
}
::v-deep .multi-steps {
  display: table;
  table-layout: fixed;
  width: 100%;
}

::v-deep .multi-steps > li {
  counter-increment: stepNum;
  text-align: center;
  display: table-cell;
  position: relative;
  color: #7DA79D; //#027f00;
  z-index: 2;
}

::v-deep .multi-steps > li:before {
  content: "";
  content: "✓;";
  content: "𐀃";
  content: "𐀄";
  content: "✓";
  display: block;
  margin: 0 auto 4px;
  background-color: #7DA79D; //#027f00;
  width: 36px;
  height: 36px;
  line-height: 32px;
  text-align: center;
  font-weight: bold;
  border-width: 2px;
  border-style: solid;
  border-color: #7DA79D; //#027f00;
  border-radius: 50%;
  color: white;
}

::v-deep .multi-steps > li:last-child:after {
  display: none;
}

::v-deep .multi-steps > li.is-active:before {
  background-color: #fff;
  border-color: #7DA79D; //#027f00;
  color: #7DA79D; //#027f00;
  animation: pulse 2s infinite;
  z-index: 2; //
}

::v-deep .multi-steps > li.is-active ~ li {
  color: #808080;
}

::v-deep .multi-steps > li.is-active ~ li:before {
  background-color: #e1e1e1;
  border-color: #e1e1e1;
  color: #808080;
  z-index: 2; //
}

::v-deep .is-complete {
  //background: linear-gradient(to right, #027f00 50%, #e1e1e1 50%);
  background: linear-gradient(to right, #7DA79D 50%, #e1e1e1 50%);
  background-size: 200% 100%;
  background-position: right bottom;
  transition: all 0.5s ease-out;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 #7DA79D; //#027f0070;
  }
  100% {
    box-shadow: 0 0 0 10px #027f0000;
  }
}
@keyframes nextStep {
  0% {
    width: 0%;
  }
  100% {
    width: 100%;
  }
}

::v-deep .progress-bar {
  cursor: pointer;
  user-select: none;
}

::v-deep .progress-bar {
  background-color: #e1e1e1;
  height: 7px;
  overflow: hidden;
  position: absolute;
  left: 50%;
  bottom: calc(50% + 7px);
  width: 100%;
  z-index: 1; //-1
}

::v-deep .progress-bar--success {
  background-color: #7DA79D; //#027f00;
  z-index: -1;
}

::v-deep .progress-bar__bar {
  background-color: #e1e1e1;
  bottom: 0;
  left: 0;
  position: absolute;
  right: 0;
  top: 0;
  transition: all 500ms ease-out;
}

::v-deep .progress-bar__trans {
  transform: translateX(100%);
}

::v-deep .style-1 > td {
  background-color: rgb(255,255,240)
}

::v-deep .v-data-table__wrapper > table > tbody > tr > td {
//::v-deep .style-1 > td {
  padding-left: 8px !important;
  padding-right: 0px !important;
}

::v-deep .v-data-table__wrapper > table > tbody > tr > td:nth-last-child(2) > .v-text-field>.v-input__control {
  width: 36px;
  max-width: 36px
}

::v-deep .style-for-data-table td {
  padding-left: 8px !important;
  padding-right: 0px !important;
}

::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
  padding-left: 8px !important;
  padding-right: 0px !important;
  text-align: start !important;
}

/*
::v-deep .v-data-table-header th:nth-last-child(2) span {
  color: #1f4788 !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}
*/

::v-deep .my-header-style {
  color: #1f4788 !important;
}

::v-deep button.product-style {
  border-style: solid !important;
  border-color: coral !important;
}
</style>