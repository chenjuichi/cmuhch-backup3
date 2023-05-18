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
      <v-card width="72vw" class="pa-md-4  mt-5 mx-lg-auto">
        <v-data-table
          :headers="headers"
          :items="desserts"
          class="elevation-1"
          :options.sync="pagination"
          :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title>儲位資料</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-dialog v-model="dialog" max-width="800px" :content-class='temp_css'>
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
                          <v-tooltip v-model="errorShow" top color="error">
                            <template v-slot:activator="{ on, attrs }">

                              <v-text-field
                                v-model="editedItem.grid_reagID"
                                label="資材碼"

                              ></v-text-field>
                              <!--
                              <v-select
                                :items="reagentForSelect"
                                label="資材碼"
                                style="position:relative; top: 10px;"
                                dense
                                outlined
                                v-model="editedItem.grid_reagID"
                              ></v-select>-->
                            </template>
                            <span>資材碼錯誤或放置位置重複!</span>
                          </v-tooltip>
                        </v-col>
                        <v-col cols="12" md="9">
                          <v-text-field
                            v-model="editedItem.grid_reagName"
                            :value="fromReagIdDisp"
                            label="品名"
                            readonly
                          ></v-text-field>
                          <!--
                          <v-autocomplete
                            v-model="editedItem.grid_reagName"
                            :items="autocomplete_items"
                            :value="fromReagIdDisp"
                            :loading="autocomplete_loading"
                            :search-input.sync="autocomplete_search"
                            hide-details
                            hide-selected
                            label="品名"
                            solo
                          >
                          </v-autocomplete>
                          -->
                        </v-col>
                      </v-row>
                      <!-- 第2列-->
                      <v-row>
                        <v-col cols="12" md="4">
                          <div style="color: #007bff; font-weight: 800;">站別</div>
                          <vue-numeric-input  v-model="editedItem.grid_station" :min="1" :max="3" :step="1"></vue-numeric-input>
                        </v-col>
                        <v-col cols="12" md="4">
                          <div style="color: #007bff; font-weight: 800;">層別</div>
                          <vue-numeric-input  v-model="editedItem.grid_layout" :min="1" :max="5" :step="1"></vue-numeric-input>
                        </v-col>
                        <v-col cols="12" md="4">
                          <div style="color: #007bff; font-weight: 800;">格位編號</div>
                          <vue-numeric-input  v-model="editedItem.grid_pos" :min="1" :max="10" :step="1"></vue-numeric-input>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                    <v-btn color="blue darken-1" text @click="save" :disabled='checkDataForSaveButton'>確定</v-btn>
                    <!--
                    <v-tooltip v-model="saveOk" bottom :position-x="toster_pos_x" :position-y="toster_pos_y" color="error">
                      <span>資材碼重複或放置位置重複!</span>
                    </v-tooltip>
                    -->
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
import VueNumericInput from 'vue-numeric-input';

import Common from '../../mixin/common.js'

export default {
  name: 'Grids',

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
  },

  data: () => ({
    currentUser: {},
    permDialog: false,
    rightDialog: false,
    //2023-05-03 add
    autocomplete_loading: false,
    autocomplete_items: [],
    autocomplete_select: null,
    autocomplete_search: null,
    temp_autocomplete_items: [],
    redirectTimeout: null,  //2023-05-04 add
    //
    snackbar: false,
    snackbar_color: 'success',
    snackbar_right: true,
    snackbar_top: true,
    snackbar_info: '',
    snackbar_icon_color: '#adadad',

    errorShow: false,
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

    //資料表頭
    headers: [
      //{ text: 'ID', sortable: false, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'grid_reagID', width: '12%' },
      { text: '品名', sortable: false, value: 'grid_reagName', width: '40%' },
      { text: '站別', sortable: false, value: 'grid_station', width: '10%' },
      { text: '層別', sortable: false, value: 'grid_layout', width: '10%' },
      { text: '格位編號', sortable: false, value: 'grid_pos', width: '18%' },
      { text: 'Actions', sortable: false, value: 'actions', width: '10%' },
    ],

    reagent_Desserts: [
      /*
      {
        //id: 1,
        reag_id: '123456789',
        reag_name: 'ABC',
      },
      {
        //id: 2,
        reag_id: '234567891',
        reag_name: 'ABCD',
      },
      {
        //id: 3,
        reag_id: '234567892',
        reag_name: 'A11',
      },
      {
        //id: 4,
        reag_id: '234567893',
        reag_name: 'A12',
      },
      {
        //id: 5,
        reag_id: '234567894',
        reag_name: 'B2233',
      },
      {
        //id: 6,
        reag_id: '234567897',
        reag_name: 'B3347',
      },
      {
        //id: 7,
        reag_id: '234567898',
        reag_name: 'B3348',
      },
      {
        //id: 8,
        reag_id: '234567899',
        reag_name: 'B3349',
      },
      {
        //id: 9,
        reag_id: '214567897',
        reag_name: 'B3397',
      },
      {
        //id: 10,
        reag_id: '214567898',
        reag_name: 'B3398',
      },
      {
        //id: 11,
        reag_id: '214567899',
        reag_name: 'B3399',
      },
      {
        //id: 12,
        reag_id: '224567897',
        reag_name: 'B3356',
      },
      {
        //id: 13,
        reag_id: '224567898',
        reag_name: 'B3357',
      },
      {
        //id: 14,
        reag_id: '224567899',
        reag_name: 'B3366',
      },
      */
    ],
    temp_reagent_Desserts: [],

    desserts: [],
    temp_desserts: [],

    reagentForSelect: [],

    editedIndex: -1,
    editedItem: {
      grid_reagID: '',
      grid_reagName: '',
      grid_station: 1,
      grid_layout: 1,
      grid_pos: 1,
      grid_id:0,
    },
    defaultItem: {
      grid_reagID: '',
      grid_reagName: '',
      grid_station: 1,
      grid_layout: 1,
      grid_pos: 1,
      grid_id:0,
    },
    saveOk: false,
    deleteOk: false,

    load_SingleTable_ok: false, //for get grids table data
    load_2thTable_ok: false,    //for get reagent table data

    load_4thTable_ok: false,    //2023-05-03 add
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? '新增資料' : '編輯資料'
    },

    fromReagIdDisp() {  //return reagent name
      if (this.editedItem.grid_reagID != '') {
        console.log("fromReagIdDisp, result 1-1...", this.reagent_Desserts, this.editedItem.grid_reagID);
        const result = this.reagent_Desserts.find(x => x.reag_id === this.editedItem.grid_reagID);
        //this.reagent_Desserts.find(x => x.reag_id === this.editedItem.grid_reagID || { value: null }).value;
        //console.log("value: ", value, typeof(value));
        console.log("fromReagIdDisp, result 1-2...", result);

        if (result != 'undefined' && result != null) {
          console.log("fromReagIdDisp, result 2-1...", result);
          let val= Object.values(result);
          this.editedItem.grid_reagName=val[1];
          this.errorShow=false;
          console.log("fromReagIdDisp, result 2-2: ", result, typeof(result), val[1]);
          return val[1];
        } else {
          this.editedItem.grid_reagName='';
          this.errorShow=true;
          return '';
        }
      }
    },
    // 2023-05-03 add
    fromReagNameDisp() {  //show reagent id, by name
      if (this.autocomplete_search !=null)
        this.editedItem.grid_reagName = this.autocomplete_search;

      if (this.editedItem.grid_reagName != '') {

        const result = this.reagent_Desserts.find(x => x.grid_reagName === this.editedItem.grid_reagName);

        console.log("fromReagNameDisp, result 1...", this.reagent_Desserts, result, this.reagent_Desserts);

        if (result != 'undefined' && result != null) {
          console.log("fromReagNameDisp, result 2...", result, this.editedIndex);
          if (this.editedIndex == -1) {
            this.editedItem.grid_reagID = result.reag_id;
          }
          console.log("fromReagNameDisp, result 22...", result, this.editedIndex, this.editedItem);

          this.errorShowForReagName=false;
          return this.editedItem.grid_reagID;
        } else {
          console.log("fromReagNameDisp, result 3...", result);
          this.editedItem.grid_reagID='';

          this.errorShowForReagName=true;
          return '';
        }
      }
    },
    //
    checkDataForSaveButton() {
      if (!!this.editedItem.grid_reagID && !!this.editedItem.grid_reagName) {
        return false;
      } else {
        return true
      }
    },
  },

  watch: {
    dialog (val) {
      val || this.close();
    },

    dialogDelete (val) {
      val || this.closeDelete()
    },

    load_2thTable_ok(val) {
      if (val) {
        this.reagent_Desserts = Object.assign([], this.temp_reagent_Desserts);
        this.load_2thTable_ok=false;
      }
    },

    load_SingleTable_ok(val) {
      if (val) {
        this.temp_desserts.sort(function (a, b) {
            return a.grid_station.localeCompare(b.grid_station) || a.grid_layout.localeCompare(b.grid_layout) || a.grid_pos.localeCompare(b.grid_pos);
        });

        console.log(this.temp_desserts);

        this.desserts = Object.assign([], this.temp_desserts);
        this.load_SingleTable_ok=false;
        this.listReagents();
      }
    },
    // 2023-05-03 add
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
    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listGrids();
    //this.initialize()
  },

  methods: {
    initialize () {
      this.load_SingleTable_ok=false;
      this.listGrids();

    },

    listGrids() {
      const path = '/listGrids';
      console.log("listGrids, Axios get data...")
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
      console.log("grids, listReagents(), Axios get data...")
      axios.get(path)
      .then((res) => {
        let temp_len=res.data.outputs.length
        for (let i=0; i<temp_len; i++) {
          let temp_obj = {
            reag_id: res.data.outputs[i]['reag_id'],
            reag_name: res.data.outputs[i]['reag_name'],
          }
          this.temp_reagent_Desserts.push(temp_obj);
        }

        this.reagentForSelect = this.temp_reagent_Desserts.map(function(p) {  //
          return p.reag_id;
        });
        this.reagentForSelect = [...new Set(this.reagentForSelect)];  //去除重複項目

        this.load_2thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.load_2thTable_ok=false;
      });
    },
    // 2023-05-03 add
    listGridForCheckByReagentName() {
      console.log("listGridForCheckByReagentName, Axios post data...", this.editedItem.grid_reagName)
      const path = '/listGridForCheckByReagentName';

      var payload= {
        reag_name:  this.editedItem.grid_reagName,
      };
      axios.post(path, payload)
      .then((res) => {
        console.log("GET ok, status: ", res.data.status);
          this.temp_autocomplete_items=res.data.outputs;

          this.load_4thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        console.log("通訊錯誤!");

        this.load_4thTable_ok=false;
      });
    },

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
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm () {
      //console.log("reagend id , grid id: ", this.editedItem.grid_reagID, this.editedItem.grid_id)

      this.removeGrid(this.editedItem.grid_reagID, this.editedItem.grid_id);

      if (!this.tosterOK) {
        this.desserts.splice(this.editedIndex, 1)
        console.log("deleteItem: ", this.editedItem);

        this.closeDelete()
      }

    },

    close () {
      this.dialog = false
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

    removeGrid(read_id, grid_id) {  //依grid id來刪除後端table資料
      let path='/removeGrid';
      let payload= {
        ID: read_id,
        GRID: grid_id,
      };
      axios.post(path, payload)
      .then(res => {
        console.log("remove grid LINK status: ", res.data.status);
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          this.editedItem = Object.assign({}, this.defaultItem);
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
          console.error(err)
      });
    },

    save () {
      console.log("click save button, editedIndex: ", this.editedIndex);

      if (this.editedIndex == -1) {    //add
        this.createGrid(this.editedItem);
        if (!this.tosterOK) {
          this.desserts.push(this.editedItem);
        }
      } else {    //edit
        this.updateGrid(this.editedItem);
        if (!this.tosterOK) {
          Object.assign(this.desserts[this.editedIndex], this.editedItem)
        }
      }
      this.close();
    },

    updateGrid(object) {  //編輯 reagent and grid後端table資料
      console.log("---click update_grid data---", object);

      const path='/updateGrid';
      let payload = Object.assign({}, object);
      axios.post(path, payload)
      .then(res => {
        console.log("update reagent and grid data/LINK status: ", res.data.status)
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

    },

    createGrid(object) {  //新增 reagent後端table資料
      console.log("---click create_grid data---", object);

      const path='/createGrid';
      let payload = Object.assign({}, object);
      axios.post(path, payload)
      .then(res => {
        console.log("save grid data/LINK status: ", res.data.status)

        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
          //this.saveOk=true;
          this.editedItem = Object.assign({}, this.defaultItem)
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
          this.snackbar_color='red accent-2';
          this.snackbar=true;
          console.log(res.data.returnID , res.data.returnGrid)
          if (res.data.returnCode==1)
            this.snackbar_info= '錯誤! '+ '試劑編號:'+ res.data.returnID + ' 沒有此試劑資料.';
          if (res.data.returnCode==2)
            this.snackbar_info= '錯誤! '+ '還沒建立 '+ res.data.returnGrid + ' 資料.';
          if (res.data.returnCode==3)
            this.snackbar_info= '錯誤! 該 '+ res.data.returnGrid + ' 已有試劑編號:' + res.data.returnID  + ' 資料.';
          if (res.data.returnCode==4)
            this.snackbar_info= '錯誤! 在其他 '+ res.data.returnGrid + ' 已有該筆試劑資料.';

          this.snackbar_icon_color= '#adadad';
        }
      })
      .catch(err => {
        console.error(err);
      });
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

::v-deep .v-data-table-header {
  background-color: #7DA79D;
}

::v-deep .v-data-table-header th {
  font-size: 1em !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) {
  font-size: 0.8em !important;
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

::v-deep .add_modalbox > .v-card {
    background: rgba(170, 209, 183, 0.37);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(4.8px);
    -webkit-backdrop-filter: blur(4.8px);
    border: 1px solid rgba(170, 209, 183, 1);
}
</style>