<template>
<v-app>
  <v-sheet class="overflow-hidden" style="position: relative;">
    <v-container fluid>
      <v-row align="center" justify="center" v-if="currentUser.perm >= 1">
        <v-card width="90vw">
          <v-data-table
            v-model="selected"
            :headers="headers"
            :items="desserts"

            :single-select="singleSelect"
            item-key="id"
            show-select

            :options.sync="pagination"
            :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
          >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title style="height: 40px;">入庫標籤列印作業</v-toolbar-title>
              <v-divider class="mx-4" inset vertical></v-divider>
              <v-spacer></v-spacer>
              <v-btn color="primary" class="mb-2" @click="printSection" depressed :disabled="!check_selected">
                <v-icon left dark>mdi-printer</v-icon>
                預覽標籤
              </v-btn>
            </v-toolbar>
            <!--bug, 待解決
            <v-switch
              v-model="singleSelect"
              label="個別選項"
              style="height: 40px; margin-top:0px; padding-top:0px;"
            ></v-switch>
            -->
          </template>
          <template v-slot:[`item.stockInTag_cnt`]="{ item }">
            <v-text-field
              v-model="item.stockInTag_cnt"

              type="number"
              min=1
              max=20
              oninput="if(Number(this.value) > Number(this.max)) this.value = this.max;"

              @input="getdata(item)"
            ></v-text-field>
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

import SideBar from '../../components/RenderBarCode.vue';
//import print from 'vue-print-nb';

export default {
  name: 'StockInTagPrint',

  mixins: [Common],

  components: {
    SideBar,
  },

  mounted() {
    console.log("StockInTag, mounted()...");

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
      { text: '資料ID', sortable: true, value: 'id', width: '10%', align: 'start'},
      { text: '資材碼', sortable: true, value: 'stockInTag_reagID', width: '7%' },
      { text: '品名', sortable: true, value: 'stockInTag_reagName', width: '200px' },
      { text: '效期', sortable: true, value: 'stockInTag_reagPeriod', width: '90px' },
      { text: '保存溫度', sortable: false, value: 'stockInTag_reagTemp', width: '10%' },
      { text: '入庫日期', sortable: true, value: 'stockInTag_Date', width: '90px' },
      { text: '入庫人員', sortable: true, value: 'stockInTag_Employer', width: '10%' },
      { text: '批號', sortable: true, value: 'stockInTag_batch', width: '15%' },
      { text: '張數', sortable: false, value: 'stockInTag_cnt', width: '8%' },
    ],




    in_drafTags: 0,

    desserts: [],
    temp_desserts: [],

    editedIndex: -1,

    last_alpha: '',       //2023-01-03 add
    last_status: true,    //2023-01-03 add
    last_date: '',        //2023-01-03 add
    todayForAlpha: '',    //2023-01-03 add

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
        console.log("load_2thTable_ok, get last alpha", " today: ", this.todayForAlpha, " last date: ", this.last_date, " alpha: ", this.last_alpha, this.last_status)
        let ch = 'A'
        if (this.last_status) {
          let ascii = this.last_alpha.charCodeAt(0);
          if (this.todayForAlpha != this.last_date)
            ascii = ascii + 1;
          ch = String.fromCharCode(ascii);
        }
        this.desserts = this.desserts.map((obj) => ({ ...obj, stockInTag_alpha: ch }));
        this.last_alpha=ch;
        console.log("load_2thTable_ok, ", " today: ", this.todayForAlpha, " last date: ", this.last_date, " alpha: ", this.last_alpha);
        this.load_2thTable_ok=false;
      }
    },

    load_SingleTable_ok(val) {
      if (val) {
        //this.desserts = Object.assign([], this.temp_desserts);
        this.desserts =  JSON.parse(JSON.stringify(this.temp_desserts));

        this.load_SingleTable_ok=false;
        this.getLastBatchAlphaForStockIn();
      }
    },

    drawer: {
      handler: function() {
        this.$nextTick(() => {
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
              this.desserts = Object.assign([], temp_arr);
              temp_arr=[];
              temp_arr =  JSON.parse(JSON.stringify(this.temp_selected));
              temp_arr = temp_arr.map((obj) => ({ ...obj, stockInTag_alpha: this.last_alpha }));

              this.selected = Object.assign([], temp_arr);
              //window.location.reload();
              this.reload=false;
            }
          }
        });
      },
      immediate: true,
    },

    selected(val) {
      this.temp_selected =  JSON.parse(JSON.stringify(val));
    },
  },

  created () {
    console.log("StockInTag, created()...");

    //load 員工與權限資料
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }
    this.stockInTag_EmpID = this.currentUser.empID;
    //console.log("empID: ", this.currentUser.empID, this.stockInTag_EmpID)

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    ////load 入庫草案資料
    //this.in_drafTags=0
    //if ("tags_draft" in localStorage) {
    //  let tempDesserts = JSON.parse(localStorage.getItem("tags_draft") || "[]");
    //  console.log("# of desserts: ", tempDesserts.length, tempDesserts);
    //  this.in_drafTags=tempDesserts.length;
    //}

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listStockInTagPrintData();
    //this.initialize()
  },

  methods: {
    initialize() {
      this.load_SingleTable_ok=false;
      this.listStockInTagPrintData();
      /*
      this.desserts = [

        {
          //id: 1,
          stockInTag_reagID: '123456789',
          stockInTag_reagName: 'ABC',
          stockInTag_reagPeriod: '111/10/31',
          stockInTag_reagTemp: '2~8度C',
          stockInTag_Date: '111/06/01',
          stockInTag_EmpID: 'N12345',
          stockInTag_Employer: '陳健南',
          stockInTag_batch: '1110012345B123400066',
          stockInTag_cnt: 4,
        },
        {
          //id: 2,
          stockInTag_reagID: '234567891',
          stockInTag_reagName: 'ABCD',
          stockInTag_reagPeriod: '111/12/31',
          stockInTag_reagTemp: '2~8度C',
          stockInTag_Date: '111/06/01',
          stockInTag_EmpID: 'N12345',
          stockInTag_Employer: '陳健南',
          stockInTag_batch: '1110012345C123400055',
          stockInTag_cnt: 2,
        },
        {
          //id: 3,
          stockInTag_reagID: '234567892',
          stockInTag_reagName: 'A11',
          stockInTag_reagPeriod: '111/12/31',
          stockInTag_reagTemp: '2~8度C',
          stockInTag_Date: '111/06/01',
          stockInTag_EmpID: 'N12345',
          stockInTag_Employer: '陳健南',
          stockInTag_batch: '1110012345B123400033',
          stockInTag_cnt: 10,
        },
        {
          //id: 4,
          stockInTag_reagID: '234567893',
          stockInTag_reagName: 'A12',
          stockInTag_reagPeriod: '112/6/30',
          stockInTag_reagTemp: '2~8度C',
          stockInTag_Date: '111/06/01',
          stockInTag_EmpID: 'N12345',
          stockInTag_Employer: '陳健南',
          stockInTag_batch: '1110012345B123400033',
          stockInTag_cnt: 1,
        },
        {
          //id: 5,
          stockInTag_reagID: '234567894',
          stockInTag_reagName: 'B2233',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '2~8度C',
          stockInTag_Date: '111/06/01',
          stockInTag_EmpID: 'N12345',
          stockInTag_Employer: '陳健南',
          stockInTag_batch: '1110012345B123400022',
          stockInTag_cnt: 10,
        },
        {
          //id: 6,
          stockInTag_reagID: '234567897',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 1,
        },
        {
          //id: 7,
          stockInTag_reagID: '234567898',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 10,
        },
        {
          //id: 8,
          stockInTag_reagID: '234567899',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 5,
        },
        {
          //id: 9,
          stockInTag_reagID: '214567897',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 10,
        },
        {
          //id: 10,
          stockInTag_reagID: '214567898',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/03/10',
          stockInTag_EmpID: 'T12345',
          stockInTag_Employer: '林成興',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 2,
        },
        {
          //id: 11,
          stockInTag_reagID: '214567899',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 10,
        },
        {
          //id: 12,
          stockInTag_reagID: '224567897',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 20,
        },
        {
          //id: 13,
          stockInTag_reagID: '224567898',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 10,
        },
        {
          //id: 14,
          stockInTag_reagID: '224567899',
          stockInTag_reagName: 'B3344',
          stockInTag_reagPeriod: '111/8/31',
          stockInTag_reagTemp: '常溫',
          stockInTag_Date: '111/06/25',
          stockInTag_EmpID: 'T87654',
          stockInTag_Employer: '吳仲偉',
          stockInTag_batch: '1110012345A123400001',
          stockInTag_cnt: 10,
        },

      ];
      */
    },

    listStockInTagPrintData() {
      const path = '/listStockInTagPrintData';
      console.log("listStockInTagPrintData, Axios get data...")
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

    //setRowStyle(item) {
    //  return 'style-for-data-table';
    //},

    getdata(item) {
      this.editedIndex = this.desserts.indexOf(item);
      console.log(this.desserts[this.editedIndex].stockInTag_cnt);
      this.temp_desserts[this.editedIndex].stockInTag_cnt = this.desserts[this.editedIndex].stockInTag_cnt;
      this.updateStockInByCnt(this.desserts[this.editedIndex]);
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

      //if ("totalTags" in localStorage) {
      //  localStorage.removeItem('totalTags');
      //}
      localStorage.setItem("totalTags", this.total_tags);

      console.log("leave onWaitTags()...");

      this.updateStockInByPrintFlag();
      //2022-12-23 mark
      //this.desserts = this.desserts.filter(val => !this.selected.includes(val));
      this.selected=[]; //2022-12-23 add
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
      /*
      this.$router.push({
        name: 'RenderBarCode',
        params: {
          selectDatas: this.selected,
        }
      });
      */
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

//::v-deep .style-for-data-table td {
::v-deep tr td {
  padding-left: 8px !important;
  padding-right: 0px !important;
}

//::v-deep .v-data-table > .v-data-table__wrapper > table > thead > tr > th {
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
  //visibility:hidden;    //bug, 待解決
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
</style>