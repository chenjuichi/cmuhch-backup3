<template>
<v-app>
  <v-sheet class="overflow-hidden" style="position: relative;">
    <v-container fluid>
      <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
        <v-card width="96vw">
          <v-data-table
            dense
            v-model="selected"
            :headers="headers"
            :items="desserts"

            :single-select="singleSelect"
            item-key="id"
            :show-select="currentUser.perm<=2"
            class="elevation-1"
            :options.sync="pagination"
            :search="search"
            :custom-filter="filterOnlyCapsText"
            @item-selected="itemSelected"
            :footer-props="{'itemsPerPageText': '每頁的資料筆數', 'items-per-page-options': [10, 30, 50]}"
          >
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title style="height: 40px;">補印標籤</v-toolbar-title>
                <v-divider class="mx-4" inset vertical></v-divider>
                <v-spacer></v-spacer>

                <v-text-field
                  v-model="search"
                  placeholder="關鍵字查詢(Caps)"
                  @input="(val) => (search = search.toUpperCase())"
                  class="style-1"
                >
                </v-text-field>
                <v-spacer></v-spacer>

                <v-btn color="primary" class="mb-2" @click="printSection" depressed :disabled="!check_selected">
                  <v-icon left dark>mdi-printer</v-icon>
                  預覽標籤
                </v-btn>
              </v-toolbar>
              <!-- 2023-07-21 add -->
              <v-progress-linear
                v-show="isLoading"
                indeterminate
                color="red"
              />

            </template>
            <!-- 2023-07-20 -->
            <!-- 2023-08-07 mark
            <template v-slot:[`item.stockInTag_alpha`]="{ item }">
              <v-text-field
                v-model="item.stockInTag_alpha"

                class="centered-input pe-0 me-2 py-1 my-0 block_tag_pages"
                style="width:35px; max-width:35px;"

                @input="getAlpha(item)"
                :disabled="currentUser.perm>2"
              ></v-text-field>
            </template>
            -->

            <template v-slot:[`item.stockInTag_cnt`]="{ item }">
              <v-text-field
                v-model="item.stockInTag_cnt"

                class="centered-input pe-0 me-2 py-1 my-0 block_myText_inv_cnt_mdf"
                style="width:35px; max-width:35px;"

                type="number"
                min=1
                max=20
                oninput="if(Number(this.value) > Number(this.max)) this.value = this.max;"
                @input="getdata(item)"
                :disabled="currentUser.perm>2"
              >
              </v-text-field>
            </template>

            <template v-slot:no-data>
              <!--<strong><font color='red'>目前沒有資料</font></strong>  2023-07-21 mark-->
              <strong><font color='blue'>資料下載中...</font></strong>  <!--2023-07-21 add-->
            </template>

          </v-data-table>
        </v-card>
      </v-row>

      <v-row align="center" justify="space-around" v-else>
          <v-dialog
            v-model="permDialog"
            transition="dialog-bottom-transition"
            max-width="500px"
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

    <v-navigation-drawer
      v-model="drawer"
      height="100vh"
      width="25vw"
      temporary
      right
      app
    >

      <SideBar :sidebar="selected" :drawer="drawer" :alpha="last_alpha" @waitTags="onWaitTags"></SideBar>

    </v-navigation-drawer>

  </v-sheet>
</v-app>
</template>

<script>
import axios from 'axios';
import Common from '../../mixin/common.js'

import SideBar from '../../components/RenderBarCodeRePrintTag.vue';

export default {
  name: 'RePrintTag',

  mixins: [Common],

  components: {
    SideBar,
  },

  mounted() {
    console.log("RePrintTag, mounted()...");

    //document.addEventListener('click', this.onClick);

    this.root = document.documentElement;

    // if back button is pressed
    window.onpopstate = () => {
    //window.onpopstate = function(event) {
      console.log("press back button, good bye...");

      this.total_tags = 0;
      localStorage.setItem("totalTags", 0);

      const userData = JSON.parse(localStorage.getItem('loginedUser'));
      userData.setting_items_per_page = this.pagination.itemsPerPage;
      localStorage.setItem('loginedUser', JSON.stringify(userData));
    };
  },

  data: () => ({
    currentUser: {},

    total_tags: 0,
    showS: false,
    permDialog: false,
    stockInTag_EmpID: '',   //入庫人員之員工編號

    errorShowForEmployer: false,
    errorShowForReagName: false,

    tosterOK: false,

    dialog: false,

    drawer: false,
    root: null,
    reload: false,

    singleSelect: false,
    //singleSelect: true,
    selected: [],
    temp_selected: [],

    pagination: {},

    //資料表頭
    headers: [
      { text: '資料ID', sortable: false, value: 'id', width: '6%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'stockInTag_reagID', width: '7%' },
      { text: '品名', sortable: true, value: 'stockInTag_reagName', width: '215px' },
      { text: '入庫/出庫', sortable: true, value: 'stockInTag_rePrint', width: '90px' },
      { text: '保存溫度', sortable: false, value: 'stockInTag_reagTemp', width: '10%' },
      { text: '入(出)庫日期', sortable: true, value: 'stockInTag_Date', width: '90px' },
      { text: '入(出)庫人員', sortable: true, value: 'stockInTag_Employer', width: '10%' },
      { text: '批號', sortable: true, value: 'stockInTag_batch', width: '9%' },
      { text: '字母', sortable: false, value: 'stockInTag_alpha', width: '5%' },
      { text: '張數', sortable: false, value: 'stockInTag_cnt', width: '6%' },
    ],

    in_drafTags: 0,

    isLoading: false,   // 2023-07-21 add

    desserts: [],
    temp_desserts: [],

    editedIndex: -1,

    last_alpha: '',       //2023-01-03 add
    last_status: true,    //2023-01-03 add
    last_date: '',        //2023-01-03 add
    todayForAlpha: '',    //2023-01-03 add

    search: '',

    load_SingleTable_ok: false, //for get employer table data
    load_2thTable_ok: false,    //for get reagent table data
  }),

  computed: {
    check_selected() {
      if (Array.isArray(this.selected) && this.selected.length) {
        console.log("array exists and is not empty: ", this.selected);
        return true;
      } else {
        return false;
      }
    },
  },

  watch: {
    dialog (val) {
      val || this.close()
    },

    load_2thTable_ok(val) {
      if (val) {
        //console.log("b, alpha: ", this.desserts, this.last_alpha);
        this.todayDisp();
        /*
        //console.log("load_2thTable_ok, get last alpha", " today: ", this.todayForAlpha, " last date: ", this.last_date, " alpha: ", this.last_alpha, this.last_status)
        console.log("load_2thTable_ok, get last alpha")
        let ch = 'A'
        if (this.last_status) {
          let ascii = this.last_alpha.charCodeAt(0);
          if (this.todayForAlpha != this.last_date)
            ascii = ascii + 1;
          ch = String.fromCharCode(ascii);
        }
        this.desserts = this.desserts.map((obj) => ({ ...obj, stockInTag_alpha: ch }));
        this.last_alpha=ch;
        //console.log("load_2thTable_ok, ", " today: ", this.todayForAlpha, " last date: ", this.last_date, " alpha: ", this.last_alpha);
        */
        this.load_2thTable_ok=false;
      }
    },

    load_SingleTable_ok(val) {
      if (val) {
        //this.desserts = Object.assign([], this.temp_desserts);
        this.desserts =  JSON.parse(JSON.stringify(this.temp_desserts));

        this.isLoading = false;   //2023-07-21 add

        this.load_SingleTable_ok=false;
        //console.log("this.desserts: ", this.desserts)
        //this.getAlphaForRePrintTag();
      }
    },

    drawer: {
      handler: function() {
        this.$nextTick(() => {
          console.log("this.selected: ", this.selected)
          if (this.drawer) {
            console.log("disable scrollbar...");
            this.root.style.setProperty('--bar','hidden');
            this.reload=true;
          } else {
            console.log("enable scrollbar...");
            this.root.style.setProperty('--bar','scroll');
            if (this.reload) {
              let temp_arr=[];
              temp_arr =  JSON.parse(JSON.stringify(this.temp_desserts));
              console.log("step1 temp_arr: ", temp_arr)
              this.desserts = Object.assign([], temp_arr);
              //temp_arr=[];                                                                        // 2023-08-08 mark
              //temp_arr =  JSON.parse(JSON.stringify(this.temp_selected));                         // 2023-08-08 mark
              //temp_arr =  JSON.parse(JSON.stringify(this.selected));
              //console.log("step2 temp_arr: ", temp_arr)
              //temp_arr = temp_arr.map((obj) => ({ ...obj, stockInTag_alpha: this.last_alpha }));  // 2023-08-08 mark
              //console.log("step3 temp_arr: ", temp_arr)

              //this.selected = Object.assign([], temp_arr);                                        // 2023-08-08 mark
              //console.log("step4 this.selected: ", this.selected)
              //window.location.reload();
              this.reload=false;
            }
          }
          // 2023-08-08 add
          console.log("b, this.selected => ", this.selected)
          this.selected = Object.assign([], this.temp_selected);
          console.log("a, this.selected => ", this.selected)
          //
        });
      },
      immediate: true,
    },

    selected(val) {
      console.log("val: ", val)
      this.temp_selected =  JSON.parse(JSON.stringify(val));
    },
  },

  created () {
    console.log("RePrintTag, created()...");

    //load 員工與權限資料
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }
    this.stockInTag_EmpID = this.currentUser.empID;
    //console.log("empID: ", this.currentUser.empID, this.stockInTag_EmpID)

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listRePrintTagData();
  },

  methods: {
    initialize() {
      this.load_SingleTable_ok=false;
      this.listRePrintTagData();
    },

    listRePrintTagData() {
      console.log("listRePrintTagData, Axios get data...")

      this.isLoading = true;     //2023-07-21 add
      const path = '/listRePrintTagData';
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs.length);
        this.load_SingleTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.isLoading = true;     //2023-07-21 add
        this.load_SingleTable_ok=false;
      });
    },

    todayDisp() {
      let todayVal=(new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10);

      let yy_value=todayVal.substring(0, 4);
      let mmdd_value=todayVal.substring(5, todayVal.length);
      mmdd_value=mmdd_value.replace('-','/');
      let b = parseInt(yy_value);
      b = b - 1911;
      yy_value = b.toString()
      this.todayForAlpha = yy_value + '/' + mmdd_value;
    },

    getLastBatchAlphaForStockIn() {
      const path = '/getLastBatchAlphaForStockIn';
      console.log("getLastBatchAlphaForStockIn, Axios get data...")
      axios.get(path)
      .then((res) => {
        console.log("getLastBatchAlphaForStockIn, GET ok.....");

        this.last_status=res.data.status
        //if (res.data.status) {
        this.last_alpha = res.data.outputs;
        this.last_date = res.data.output_date
        this.tosterOK = false;  //false: 關閉錯誤訊息畫面
        this.load_2thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        this.load_2thTable_ok=false;
      });
    },

    getAlphaForRePrintTag() {
      console.log("RePrintTag, getAlphaForRePrintTag()...")

      const path = '/getAlphaForRePrintTag';
      axios.get(path)
      .then((res) => {
        console.log("getAlphaForRePrintTag, GET ok.....");

        this.last_status=res.data.status
        //if (res.data.status) {
        this.last_alpha = res.data.outputs;
        console.log("getAlphaForRePrintTag(), this.last_alpha: ", this.last_alpha)
        this.last_date = res.data.output_date
        this.tosterOK = false;  //false: 關閉錯誤訊息畫面
        this.load_2thTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        this.load_2thTable_ok=false;
      });
    },

    filterOnlyCapsText (value, search, item) {
      return value != null &&
        search != null &&
        typeof value === 'string' &&
        value.toString().toLocaleUpperCase().indexOf(search) !== -1
    },

    itemSelected(items){
      console.log("itemSelected: ", items)
      let item=items.item
      let value=items.value
      console.log("hello...", item, value)
    },

    getAlpha(item) {
      console.log("getAlpha: ",item);

      this.editedIndex = this.desserts.indexOf(item);
      //this.editedIndex = this.desserts.map(object => object.id).indexOf(item.id); //for dessertsDisplay
      this.desserts[this.editedIndex].stockInTag_alpha=this.desserts[this.editedIndex].stockInTag_alpha.trim()
      this.temp_desserts[this.editedIndex].stockInTag_alpha = this.desserts[this.editedIndex].stockInTag_alpha;

      console.log("getAlpha, index: ", this.editedIndex, this.desserts[this.editedIndex].stockInTag_alpha);
      let inputLetter=this.desserts[this.editedIndex].stockInTag_alpha
      //console.log("STEP1...")
      let letterLength=inputLetter.length
      //console.log("comment: ", this.commentForInventory, this.commentForInventory.length)
      if (letterLength == 1 && inputLetter.toUpperCase() === inputLetter) {
        let objIndex = this.selected.findIndex(o => o.id == this.desserts[this.editedIndex].id);
        //console.log("STEP2..., objIndex", objIndex)
        if (objIndex != -1) {
          this.selected[objIndex]['stockInTag_alpha'] = inputLetter;
          //console.log("STEP3...")
        }
      }
    },

    getdata(item) {
      this.editedIndex = this.desserts.indexOf(item);
      console.log(this.desserts[this.editedIndex].stockInTag_cnt);
      this.temp_desserts[this.editedIndex].stockInTag_cnt = this.desserts[this.editedIndex].stockInTag_cnt;
      let objIndex = this.selected.findIndex(o => o.id == this.desserts[this.editedIndex].id);
      console.log("objIndex: ", objIndex)
      if (objIndex != -1) {
        this.selected[objIndex].stockInTag_cnt=this.desserts[this.editedIndex].stockInTag_cnt;
      }
      //this.updateStockInByCnt(this.desserts[this.editedIndex]);
    },

    updateStockInByCnt(object) {  //編輯 後端table資料
      console.log("---click update_stockInTagPrint_by_cnt data---", object);

      const path='/updateStockInByCnt';
      let payload = Object.assign({}, object);

      axios.post(path, payload)
      .then(res => {
        console.log("update StockInTagPrint data, status: ", res.data.status);
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

    onWaitTags(value) {
      console.log("total count for tags: ", value);
      this.total_tags=value;

      localStorage.setItem("totalTags", this.total_tags);

      console.log("leave onWaitTags()...");

      //this.updateStockInByPrintFlag();
      this.selected=[];   //2022-12-23 add
      this.drawer=false;  //2023-01-31 add
    },

    updateStockInByPrintFlag() {
      console.log("---click update_stockIn_by_printFlag---, selected data: ", this.selected);

      const path='/updateStockInByPrintFlag';
      let payload= {
        blocks: this.selected,
        count: this.selected.length,
      };

      axios.post(path, payload)
      .then(res => {
        console.log("update StockInTagPrint data, status: ", res.data.status);
        if (res.data.status) {
          this.tosterOK = false;  //false: 關閉錯誤訊息畫面
        } else {
          this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        }
      })
      .catch(err => {
        console.error(err);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
      });
    },

    printSection() {
      console.log("click, printSection()...");

      this.drawer=true;
    },

    permCloseFun () {
      this.permDialog = false
      console.log("press permission Close Button...");
      this.$router.push('/navbar');
    },
  },
}
</script>

<style>
:root {
  --bar: scroll;
}

html {
  overflow-y: var(--bar) !important;
}
</style>

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

::v-deep tr td {
  padding-left: 8px !important;
  padding-right: 0px !important;
}

::v-deep tr > th {
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

::v-deep .v-data-table-header th:nth-child(1) i {
  color: blue;
  display:none;
}

::v-deep header {
  height: 48px !important;
  margin-top: 10px !important;
}

::v-deep .v-toolbar__content {
  height: 42px !important;
}

::v-deep .v-toolbar__title {
  height: 40px !important;
}

::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}

::v-deep .v-data-footer {
  margin-top: 0px;
  margin-bottom: 2px;
}

::v-deep .block_myText_inv_cnt_mdf {
  width: 24px;
  font-size: 14px;
}
::v-deep div.v-input.style-1 > .v-input__control > .v-input__slot > .v-text-field__slot > input {
  max-width: 350px !important;
  width: 350px !important;
}
::v-deep div.v-input.style-1 > .v-input__control > .v-input__slot {
  max-width: 350px !important;
  width: 350px !important;
}
// modify data table header text color, 2023-0707-14 add
::v-deep .v-data-table-header th:last-child span {
  color: #1f4788 !important;
}

::v-deep .block_tag_pages {
  width: 24px;
  font-size: 14px;
}
</style>