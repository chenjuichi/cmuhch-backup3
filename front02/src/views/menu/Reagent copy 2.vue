0000000000000000000000000000000000000000 eae9fb3b2824bd74cfc64ac07d574c6bb7002247 “chenjuichi <chenjuichi@gmail.com> 1665110870 +0800	commit (initial): start git
eae9fb3b2824bd74cfc64ac07d574c6bb7002247 6f4c69e19c9e7fd8422ffccd3132ca57a2eab030 “chenjuichi <chenjuichi@gmail.com> 1665973655 +0800	commit: modify 盤點作業
6f4c69e19c9e7fd8422ffccd3132ca57a2eab030 a731f588d8868cc435925fe047f1cb5c9bf65aa9 “chenjuichi <chenjuichi@gmail.com> 1668574672 +0800	commit: major in led
a731f588d8868cc435925fe047f1cb5c9bf65aa9 3e09544582b705fde4ccbf90fea234657df9e355 “chenjuichi <chenjuichi@gmail.com> 1669120469 +0800	commit: modify for reagent
3e09544582b705fde4ccbf90fea234657df9e355 76bce183851071f3cad9de260c0a6a4224de1763 “chenjuichi <chenjuichi@gmail.com> 1669120668 +0800	commit: modify for reagent 3
                                                                                                                                                                                                                                  </v-btn>
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
                          <v-text-field
                            v-model="editedItem.reag_id"
                            label="資材碼"
                            prepend-icon="mdi-alphabetical"
                            :readonly="formTitle === '編輯資料'"
                            @focus="fieldFocus"
                          ></v-text-field>
                          <small class="msgErr" v-text= "IDErrMsg"></small>
                        </v-col>

                        <v-col cols="12" md="4">
                          <v-text-field
                            v-model="editedItem.reag_name"
                            label="品名"
                            prepend-icon="mdi-hospital-box-outline"
                            @focus="fieldFocus"
                          ></v-text-field>
                          <small class="msgErr" v-text= "nameErrMsg"></small>
                        </v-col>

                        <v-col cols="12" md="4">
                          <!--試劑組別 {{ reag_catalog.selected_item }}-->
                          <div v-if="reag_catalog.selected_item!=='其他'">
                            <v-select class="company-size-dropdown"
                              :items="reagents"
                              attach
                              v-model="reag_catalog.selected_item"
                              label="試劑組別"
                              required>
                            </v-select>
                          </div>
                          <div v-else>
                            <v-text-field
                              autofocus
                              label="試劑組別"
                              v-model="newItem"
                              v-on:keyup.enter="resetQueue">

                            </v-text-field>
                          </div>
                        </v-col>

                      </v-row>

                      <!-- 第2列-->
                      <v-row>
                        <v-col cols="12" md="2">
                          <v-select
                            :items="['盒', '包', '袋', '瓶', '個', '條']"
                            label="入庫單位"
                            prepend-icon="mdi-tray-plus"
                            v-model="editedItem.reag_In_unit"
                            @focus="fieldFocus"
                          ></v-select>
                        </v-col>
                        <v-col cols="12" md="2">
                          <v-select
                            :items="['盒', '包', '袋', '瓶', '個', '條']"
                            label="出庫單位"
                            prepend-icon="mdi-tray-minus"
                            v-model="editedItem.reag_Out_unit"
                            @focus="fieldFocus"
                          ></v-select>
                        </v-col>
                        <v-col cols="12" md="3">
                          <v-text-field
                            v-model="editedItem.reag_scale"
                            label="比例"
                            prepend-icon="mdi-scale"
                            @focus="fieldFocus"
                          ></v-text-field>
                          <small class="msgErr" v-text= "scaleErrMsg"></small>
                        </v-col>

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
                      </v-row>

                      <!-- 第3列-->
                      <v-row>
                        <v-col cols="12" md="2">
                          <v-text-field
                            v-model="editedItem.reag_stock"
                            label="安全存量"
                            prepend-icon="mdi-tray-alert"
                            @focus="fieldFocus"
                          ></v-text-field>
                          <small class="msgErr" v-text= "nameErrMsg"></small>
                        </v-col>
                        <v-col cols="12" md="4">
                          <v-select
                            :items="['室溫','2~8度C','-20度C']"
                            label="保存溫度"
                            prepend-icon="mdi-temperature-celsius"
                            v-model="editedItem.reag_temp"
                            @focus="fieldFocus"
                          ></v-select>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-select
                            :items="suppliers"
                            label="供應商"
                            prepend-icon="mdi-home-city-outline"
                            v-model="editedItem.reag_supplier"
                            @focus="fieldFocus"
                          ></v-select>
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

    fromDateMenu: false,
    fromDateVal: null,

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
      { text: '資材碼', sortable: true, value: 'reag_id', width: '10%' },
      { text: '品名', sortable: false, value: 'reag_name', width: '12%' },
      { text: '資材組別', sortable: true, value: 'reag_catalog', width: '10%' },
      { text: '入庫單位', sortable: false, value: 'reag_In_unit', width: '8%' },
      { text: '出庫單位', sortable: false, value: 'reag_Out_unit', width: '8%' },
      { text: '比例', sortable: false, value: 'reag_scale', width: '5%' },
      { text: '效期', sortable: true, value: 'reag_period', width: '8%' },
      { text: '安全存量', sortable: false, value: 'reag_stock', width: '8%' },
      { text: '保存溫度', sortable: false, value: 'reag_temp', width: '9%' },
      { text: '供應商', sortable: true, value: 'reag_supplier', width: '12%' },
      { text: 'Actions', sortable: false, value: 'actions', width: '10%' },
    ],

    desserts: [],
    temp_desserts: [],

    suppliers: [],
    temp_suppliers: [],

    editedIndex: -1,
    editedItem: {
      //id: 0,
      reag_id: '',
      reag_name: '',
      reag_In_unit: '',
      reag_Out_unit: '',
      reag_scale: '0',
      reag_period: '',
      reag_stock: '0',
      reag_temp: '',
      reag_catalog: '',
      reag_supplier: '',
    },
    defaultItem: {
      reag_id: '',
      reag_name: '',
      reag_In_unit: '',
      reag_Out_unit: '',
      reag_scale: '0',
      reag_period: '',
      reag_stock: '0',
      reag_temp: '',
      reag_catalog: '',
      reag_supplier: '',
    },

    reag_catalog: {
      selected_item: '',
    },
    newItem: '',
    reagents: [],

    load_SingleTable_ok: false,
    load_2thTable_ok: false
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },

    fromDateDisp() {
      if (this.fromDateVal != null) {
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

    checkDataForSaveButton() {
      if (!!this.editedItem.reag_id && !!this.editedItem.reag_name &&
          !!this.editedItem.reag_In_unit && !!this.editedItem.reag_Out_unit &&
          !!this.editedItem.reag_scale && !!this.editedItem.reag_period &&
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
      let isEmpIDRule = /^\w{1,9}$/;

      this.IDErrMsg = '';
      let result = this.editedItem.reag_id.search(isEmpIDRule);
      //let len=this.editedItem.reag_id.length
      console.log("reg: ", result);
      //if (result != -1 || len==0) {
      if (result != -1) {
        this.IDErrMsg = '';
      } else {
        this.IDErrMsg = '資料格式錯誤!';
      }
    },

    'editedItem.reag_name': function () {
      let isNameRule = /^[\u4e00-\u9fa5_a-zA-Z0-9]+$/;

      this.nameErrMsg = '';
      let result = this.editedItem.reag_name.search(isNameRule);
      let len=this.editedItem.reag_name.length
      console.log("reg: ", result, len);
      if (len<=50) {
      //if (result != -1) {
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

    load_2thTable_ok(val) {
      if (val) {
        this.suppliers = Object.assign([], this.temp_suppliers);
        this.load_2thTable_ok=false;
      }
    },

    load_SingleTable_ok(val) {
      if (val) {
        this.desserts = Object.assign([], this.temp_desserts);
        let temp_reagents = this.temp_desserts.map(function(p) {  //
          return p.reag_catalog;
        });
        this.reagents = [...new Set(temp_reagents)];
        //let obj= {reag_catalog: '其他',}
        this.reagents.push('其他');

        this.load_SingleTable_ok=false;
        this.listSuppliers();
      }
    }
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
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
        this.temp_suppliers = res.data.outputs.map(item => Object.values(item)[3]); //從object中copy value至array

        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_2thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_2thTable_ok=false;
      });
    },

    fieldFocus() {
      this.tosterOK=false;
      this.IDErrMsg='';
      this.nameErrMsg='';
      this.scaleErrMsg='';
      this.stockErrMsg = '';
    },

    editItem (item) {
      this.editedIndex = this.desserts.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem (item) {
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
      let payload = Object.assign({}, object);
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
      console.log("---click create_reagent data---");

      //const defaultPassword='a12345678';
      const path='/createReagent';
      let payload = Object.assign({}, object);
      axios.post(path, payload)
      .then(res => {
        console.log("save reagent data status: ", res.data.status)

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
      });
    },

    resetQueue() {
      this.reag_catalog.selected_item = this.newItem;
      let temp=this.reag_catalog.length;
      this.reagents.splice(temp-2, 0, this.newItem);
      //this.reagents.join()
    },

    setRowStyleForRragent(item) {
      return 'style-for-data-table';
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
  font-size: 1em !important;
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
  font-size: 1em
}
::v-deep .v-label--active {
  font-size: 1.2em;
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