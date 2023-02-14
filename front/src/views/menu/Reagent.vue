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
      <v-card width="96vw" class="pa-md-4  mt-5 mx-lg-auto">
        <v-data-table
          :headers="headers"
          :items="desserts"
          :item-class="setRowStyleForRragent"
          class="elevation-1"
          :options.sync="pagination"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>試劑資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="800px" :content-class="temp_css">
                <template v-slot:activator="{ on, attrs }">
                  <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on" v-show="currentUser.perm<=2">
                    <v-icon left dark>mdi-table-plus</v-icon>
                    新增資料
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
                        <v-col cols="12" md="3">
                          <v-text-field
                            v-model="editedItem.reag_id"
                            label="資材碼"

                            :readonly="formTitle === '編輯資料'"
                            @focus="fieldFocus"
                          ></v-text-field>
                          <small class="msgErr" v-text= "IDErrMsg"></small>
                        </v-col>
                        <v-col cols="12" md="3">
                          <v-text-field
                            v-model="editedItem.reag_name"
                            label="品名"
                            :readonly="formTitle === '編輯資料'"
                            @focus="fieldFocus"
                          ></v-text-field>
                          <small class="msgErr" v-text= "nameErrMsg"></small>
                        </v-col>

                        <v-col class="d-flex" cols="12" md="3">
                          <v-select
                            :items="products"
                            label="資材類別"
                            style="position:relative; top: 10px;"
                            dense
                            outlined

                            v-model="editedItem.reag_product"
                            @blur="listSuppliersByProc()"
                          ></v-select>
                        </v-col>

                        <v-col cols="12" md="3">
                          <!--試劑組別 {{ reag_catalog.selected_item }}-->

                          <!--<div v-if="reag_catalog.selected_item!=='其他'">-->
                            <v-select
                              :items="reagents"

                              v-model="editedItem.reag_catalog"
                              label="組別"
                              style="position:relative; top: 10px;"
                              dense
                              outlined

                              required>
                            </v-select>
                          <!--</div>-->
                          <!--<div v-else>
                            <v-text-field
                              autofocus
                              label="組別"

                              v-model="newItem"
                              v-on:keyup.enter="resetQueue">

                            </v-text-field>
                          </div>-->
                        </v-col>
                      </v-row>

                      <!-- 第2列-->
                      <v-row>
                        <v-col cols="12" md="2">
                          <div v-if="editedItem.reag_In_unit!=='其他'">
                            <v-select
                              :items="InUnits"
                              label="入庫單位"

                              v-model="editedItem.reag_In_unit"
                              @focus="fieldFocus"
                            ></v-select>
                          </div>
                          <div v-else>
                            <v-text-field
                              autofocus
                              label="入庫單位"

                              v-model="newItemIn"
                              v-on:keyup.enter="resetQueueIn">

                            </v-text-field>
                          </div>
                        </v-col>
                        <v-col cols="12" md="2">
                          <div v-if="editedItem.reag_Out_unit!=='其他'">
                            <v-select
                              :items="OutUnits"
                              label="出庫單位"

                              v-model="editedItem.reag_Out_unit"
                              @focus="fieldFocus"
                            ></v-select>
                          </div>
                          <div v-else>
                            <v-text-field
                              autofocus
                              label="出庫單位"
                              v-model="newItemOut"
                              v-on:keyup.enter="resetQueueOut">
                            </v-text-field>
                          </div>
                        </v-col>
                        <v-col cols="12" md="3">
                          <v-text-field
                            v-model="editedItem.reag_scale"
                            label="比例"

                            @focus="fieldFocus"
                          ></v-text-field>
                          <small class="msgErr" v-text= "scaleErrMsg"></small>
                        </v-col>
                        <!--
                        <v-col cols="12" md="5">
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
                                label="效期"
                                prepend-icon="event"
                                readonly
                                :value="fromDateDisp"
                                v-model="editedItem.reag_period"
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
                        -->
                      </v-row>

                      <!-- 第3列-->
                      <v-row>
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="editedItem.reag_stock"
                            label="安全存量"

                            @focus="fieldFocus"
                          ></v-text-field>
                          <small class="msgErr" v-text= "nameErrMsg"></small>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-select
                            :items="['室溫','2~8度C','-20度C']"
                            label="保存溫度"
                            style="position:relative; top: 10px;"
                            dense
                            outlined
                            v-model="editedItem.reag_temp"
                            @focus="fieldFocus"
                          ></v-select>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-select
                            :items="suppliers"
                            style="position:relative; top: 10px;"
                            label="供應商"
                            dense
                            outlined

                            v-model="editedItem.reag_supplier"
                            @focus="fieldFocus"
                            @click="fieldCheck"
                          ></v-select>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="save" :disabled='checkDataForSaveButton'>確定</v-btn>

                    <!-- <v-tooltip v-model="tosterOK" bottom :position-x="toster_pos_x" :position-y="toster_pos_y" color="error">
                      <span>資材碼重複!</span>
                    </v-tooltip> -->
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

export default {
  name: 'Reagent',

  mixins: [Common],

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
    currentUser: { },
    permDialog: false,
    rightDialog: false,

    snackbar: false,
    snackbar_color: 'success',
    snackbar_right: true,
    snackbar_top: true,
    snackbar_info: '',
    snackbar_icon_color: '#adadad',


    fromDateMenu: false,
    //fromDateVal: null,
    //fromDateVal: '',
    fromDateVal: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),

    minDate: "2012-07-01",
    maxDate: "2042-06-30",

    dialog: false,
    dialogDelete: false,

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },

    tosterOK: false,
    toster_pos_x: 1000,
    toster_pos_y: 400,
    toster_delay:3,

	  IDErrMsg: '',
    nameErrMsg: '',
    scaleErrMsg: '',
    stockErrMsg: '',

    //資料表頭
    headers: [
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'reag_id', width: '8%' },
      { text: '品名', sortable: false, value: 'reag_name', width: '20%' },
      { text: '資材類別', sortable: true, value: 'reag_product', width: '9%' },
      { text: '組別', sortable: true, value: 'reag_catalog', width: '9%' },
      { text: '入庫單位', sortable: false, value: 'reag_In_unit', width: '8%' },
      { text: '出庫單位', sortable: false, value: 'reag_Out_unit', width: '8%' },
      { text: '比例', sortable: false, value: 'reag_scale', width: '5%' },
      //{ text: '效期', sortable: true, value: 'reag_period', width: '8%' },
      { text: '安全存量', sortable: false, value: 'reag_stock', width: '8%' },
      { text: '保存溫度', sortable: false, value: 'reag_temp', width: '8%' },
      { text: '供應商', sortable: true, value: 'reag_supplier', width: '10%' },
      { text: 'Actions', sortable: false, value: 'actions', width: '7%' },
    ],

    desserts: [],
    temp_desserts: [],

    suppliers: [],
    temp_suppliers: [],

    products: [],         //slide-item的主要產品資料
    temp_products: [],
    product_item: '',
    selectProduct: false,

    editedIndex: -1,
    editedItem: {
      //id: 0,
      reag_id: '',
      reag_name: '',
      reag_product: '',
      reag_catalog: '',
      reag_In_unit: '',
      reag_Out_unit: '',
      reag_scale: '1',
      //reag_period: '',
      reag_stock: '1',
      reag_temp: '',
      reag_catalog: '',
      reag_supplier: '',
    },
    defaultItem: {
      reag_id: '',
      reag_name: '',
      reag_product: '',
      reag_catalog: '',
      reag_In_unit: '',
      reag_Out_unit: '',
      reag_scale: '1',
      //reag_period: '',
      reag_stock: '1',
      reag_temp: '',
      reag_catalog: '',
      reag_supplier: '',
    },

    reag_catalog: {
      selected_item: '',
    },
    newItemIn: '',
    newItemOut: '',
    InUnits: ['盒', '包', '袋', '瓶', '個', '條', '其他'],
    OutUnits: ['盒', '包', '袋', '瓶', '個', '條', '其他'],
    newItem: '',
    reagents: [],

    load_SingleTable_ok: false,
    load_2thTable_ok: false,
    load_3thTable_ok: false,
    load_4thTable_ok: false,
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },
    /*
    fromDateDisp() {
      //if (this.fromDateVal != null) {
      if (this.fromDateVal != '') {
        let yy_value=this.fromDateVal.substring(0, 4);
        let mmdd_value=this.fromDateVal.substring(5, this.fromDateVal.length);
        mmdd_value=mmdd_value.replace('-','/');
        let b = parseInt(yy_value);
        b = b - 1911;
        yy_value = b.toString()
        this.editedItem.reag_period = yy_value + '/' + mmdd_value;
      }
      return this.fromDateVal;
    },
    */
    checkDataForSaveButton() {
      if (!!this.editedItem.reag_id && !!this.editedItem.reag_name &&
          !!this.editedItem.reag_In_unit && !!this.editedItem.reag_Out_unit &&
        //  !!this.editedItem.reag_scale && !!this.editedItem.reag_period &&
          !!this.editedItem.reag_scale &&
          !!this.editedItem.reag_stock && !!this.editedItem.reag_temp && this.editedItem.reag_supplier &&
          this.IDErrMsg == '' && this.nameErrMsg == '' && this.scaleErrMsg == '') {
        return false;
      } else {
        return true
      }
    },
  },

  watch: {
    dialog (val) {
      !val || this.fieldFocus();
      val || this.close();
    },

    dialogDelete (val) {
      val || this.closeDelete()
    },

    'editedItem.reag_id': function () {
      //let isEmpIDRule = /^\w{1,9}$/;
      let isEmpIDRule = /^[A-Za-z0-9.]{1,9}$/;

      this.IDErrMsg = '';
      let result = this.editedItem.reag_id.search(isEmpIDRule);
      //let len=this.editedItem.reag_id.length
      console.log("reg: ", result);

      let matchResult = this.desserts.find(x => x.reag_id === this.editedItem.reag_id);
      console.log("desserts: ", matchResult);

      //if (result != -1 || len==0) {
      if (result != -1) {
        if (typeof(matchResult) != 'undefined') {
          console.log("typeof is undefined...");
          this.IDErrMsg = '資材碼與 ' + matchResult.reag_name + ' 重複!';
        } else {
          this.IDErrMsg = '';
        }
      } else {
        this.IDErrMsg = '資料格式錯誤!';
      }
    },

    'editedItem.reag_name': function () {
      //let isNameRule = /^\w{1,50}$/;
      let isNameRule = /^[A-Za-z0-9_-]{1,50}$/;

      this.nameErrMsg = '';
      let result = this.editedItem.reag_name.search(isNameRule);
      let len=this.editedItem.reag_name.length
      console.log("reg: ", result, len);
      //if (len<=50) {
      if (this.editedIndex ==-1) {
        this.nameErrMsg = '';
        return;
      }

      if (result != -1) {
        this.nameErrMsg = '';
      } else {
        this.nameErrMsg = '資料格式錯誤!';
      }
    },

    'editedItem.reag_scale': function () {
      let isScaleRule = /^[0-9]+(.[0-9]{0,2})?$/;

      this.scaleErrMsg = '';
      let result = this.editedItem.reag_scale.toString().search(isScaleRule);
      //let len=this.editedItem.reag_name.length
      console.log("reg: ", result);

      if (this.editedIndex ==-1) {
        this.nameErrMsg = '';
        return;
      }

      if (result != -1) {
        this.scaleErrMsg = '';
      } else {
        this.scaleErrMsg = '資料格式錯誤!';
      }
    },

    'editedItem.reag_stock': function () {
      let isStockRule = /^[0-9]+(.[0-9]{0,2})?$/;

      this.stockErrMsg = '';
      let result = this.editedItem.reag_stock.toString().search(isStockRule);
      //let len=this.editedItem.reag_name.length
      console.log("reg: ", result);
      if (result != -1) {
        this.stockErrMsg = '';
      } else {
        this.stockErrMsg = '資料格式錯誤!';
      }
    },

    load_4thTable_ok(val) {
      if (val) {
        this.suppliers = Object.assign([], this.temp_suppliers);
        //this.editedItem.reag_product=this.product_item;
        //this.editedItem.reag_supplier=this.product_item;
        this.selectProduct=false
        this.load_4thTable_ok=false;
      }
    },

    load_3thTable_ok(val) {
      if (val) {
        this.products = Object.assign([], this.temp_products);
        this.load_3thTable_ok=false;
      }
    },

    load_2thTable_ok(val) {
      if (val) {
        this.suppliers = Object.assign([], this.temp_suppliers);
        console.log("this.suppliers: ", this.suppliers)
        this.load_2thTable_ok=false;
        this.listProducts();
      }
    },

    load_SingleTable_ok(val) {
      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);
        let temp_reagents = this.temp_desserts.map(function(p) {  //
          return p.reag_catalog;
        });
        this.reagents = [...new Set(temp_reagents)];  //去除重複項目
        //let obj= {reag_catalog: '其他',}
        this.reagents.push('其他');

        this.load_SingleTable_ok=false;
        this.listSuppliers();
      }
    }
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    console.log("this.currentUser", this.currentUser)
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();
    this.listReagents();
    //this.initialize()
  },

  methods: {
    initialize() {
      this.load_SingleTable_ok=false;
      this.listReagents();
    },

    listReagents() {
      const path = '/listReagents';
      console.log("listReagents, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length, res.data.outputs);
        this.load_SingleTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_SingleTable_ok=false;
      });
    },

    listSuppliers() {
      const path = '/listSuppliers';
      console.log("listSuppliers, Axios get data...")
      axios.get(path)
      .then((res) => {
        //this.temp_suppliers = res.data.outputs;
        console.log("===GET ok, total records, OBJECTS:", res.data.outputs);
        this.temp_suppliers = res.data.outputs.map(item => Object.values(item)[4]); //從object中copy value至array

        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_2thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_2thTable_ok=false;
      });
    },

    listSuppliersByProc() {
      console.log("listSuppliersByProc, Axios get data...")
      //console.log("this.product_item...", this.product_item)
      //if (this.product_item=="")
      if (this.editedItem.reag_product=="")
        return;
      //console.log("this.product_item...", this.product_item)
      //this.selectProduct=false;

      const path = '/listSuppliersByProc';
      let payload= {
        //prd_name: this.product_item,
        prd_name: this.editedItem.reag_product,
      };
      axios.post(path, payload)
      .then((res) => {
        console.log("===GET ok, total records, OBJECTS:", res.data.outputs.length, res.data.outputs);
        this.temp_suppliers = res.data.outputs;
        //this.temp_suppliers = res.data.outputs.map(item => Object.values(item)[3]); //從object中copy value至array

        this.load_4thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_4thTable_ok=false;
      });
    },

    listProducts() {    //從後端讀取slide-item的主要產品資料
      const path = '/listProducts';
      console.log("listProducts, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_products = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_3thTable_ok=true;   //true: slide-item的主要產品資料ok
      })
      .catch((error) => {
        console.error(error);
        this.load_3thTable_ok=false;
      });
    },

    fieldFocus() {
        this.tosterOK=false;
        this.IDErrMsg='';
        this.nameErrMsg='';
        this.scaleErrMsg='';
        this.stockErrMsg = '';
        this.selectProductErrMsg='';
    },

    fieldCheck() {
      console.log("fieldCheck...")

      if (this.editedItem.reag_product=="") {
        //this.selectProduct=true;
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '請先選擇資材類別!';
        this.snackbar_icon_color= '#adadad';
      }
    },

    editItem (item) {
      //console.log("this.currentUser.perm", this.currentUser.perm)
      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.product_item=this.editedItem.reag_product;
      this.product_item=this.editedItem.reag_product;

      this.selectProduct=false;
      this.dialog = true;
    },

    deleteItem (item) {
      if (this.currentUser.perm >2) {
        this.rightDialog = true;
        return;
      }

      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm () {
      this.removeReagent(this.editedItem.reag_id);

      if (!this.tosterOK) {
        this.desserts.splice(this.editedIndex, 1)
        console.log("deleteItem: ", this.editedItem);

        this.closeDelete()
      }
    },

    close () {
      this.dialog = false
      this.IDErrMsg='';
      this.nameErrMsg='';
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
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

    removeReagent(id) {  //依reagent id來刪除後端table資料
      let path='/removeReagent';
      let payload= {
        ID: id,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("remove reagent status: ", res.data.status);
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem);
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err)
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
    });
    },

    save () {
      console.log("click save button, editedIndex: ", this.editedIndex);

      if (this.editedIndex == -1) {    //add
        this.createReagent(this.editedItem);
        if (!this.tosterOK) {
          this.desserts.push(this.editedItem);
          this.close();
        }
      } else {    //edit
        this.updateReagent(this.editedItem);
        if (!this.tosterOK) {
          Object.assign(this.desserts[this.editedIndex], this.editedItem)
          this.close();
        }
      }
    },

    updateReagent(object) {  //編輯 reagent後端table資料
      console.log("---click update_reagent data---", object);

      const path='/updateReagent';
      //let payload = Object.assign({}, object);
      let payload= {
        block: object,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("update reagent data status: ", res.data.status)
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem)
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        //this.registerOK= false;
      });

      //this.signUp=false;  //註冊OK, 則轉為登入畫面
    },

    createReagent(object) {  //新增 reagent後端table資料
      console.log("createReagent, Axios get data...", object);

      const path='/createReagent';
      let payload= {
        block: object,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("save reagent data status: ", res.data.status)

        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem)
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
          this.snackbar_color='red accent-2';
          this.snackbar=true;
          this.snackbar_info= '錯誤! '+ '試劑編號:'+ res.data.returnID + ' 與歷史資料中 ' +res.data.returnName+' 重複!';
          this.snackbar_icon_color= '#adadad';

        }
      })
      .catch(err => {
        console.error(err);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
      });
    },

    resetQueue() {
      this.reag_catalog.selected_item = this.newItem;
      //this.editedItem.reag_catalog = this.reag_catalog.selected_item
      //let temp=this.reag_catalog.length;
      //this.reagents.splice(temp-2, 0, this.newItem);
      this.reagents.unshift(this.reag_catalog.selected_item);
    },

    resetQueueIn() {
      this.editedItem.reag_In_unit = this.newItemIn;
      //let temp=this.newItemIn.length;
      //this.InUnits.splice(temp-2, 0, this.newItem);
      this.InUnits.unshift(this.editedItem.reag_In_unit);
    },

    resetQueueOut() {
      this.editedItem.reag_Out_unit = this.newItemOut;
      //let temp=this.newItemIn.length;
      //this.InUnits.splice(temp-2, 0, this.newItem);
      this.OutUnits.unshift(this.editedItem.reag_Out_unit);
    },

    setRowStyleForRragent(item) {
      return 'style-for-data-table';
    },

    permCloseFun() {
      this.permDialog = false
      console.log("press permission Close Button...");
      this.$router.push('/navbar');
    },
    rightCloseFun() {
      this.rightDialog = false
      console.log("press permission Close Button...");
      //this.$router.push('/navbar');
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

::v-deep .v-data-table-header th {
  font-size: 0.8em !important;
}

::v-deep .v-data-table td {
  font-size: 12px !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) {
  font-size: 0.8em !important;
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

::v-deep .v-label {
  font-size: 0.8em
}
::v-deep .v-label--active {
  font-size: 1em;
  font-weight: bold;
}

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}

small.msgErr {
  font-size: 80%;
  color: red;
  margin-top: -10px;
}

::v-deep .add_modalbox > .v-card {
    background: rgba(170, 209, 183, 0.37);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(4.8px);
    -webkit-backdrop-filter: blur(4.8px);
    border: 1px solid rgba(170, 209, 183, 1);
}
</style>