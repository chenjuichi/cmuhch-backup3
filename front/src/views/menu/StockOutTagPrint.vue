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
            show-select
            :show-select="currentUser.perm<=2"
            class="elevation-1"
            :options.sync="pagination"
            :footer-props="{itemsPerPageText: '每頁的資料筆數'}"
          >
            <template v-slot:top>
              <v-toolbar flat>
                <v-toolbar-title style="height: 40px;">出庫標籤列印作業</v-toolbar-title>
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
            <template v-slot:[`item.stockOutTag_cnt`]="{ item }">
              <!-- modify :max in the follow tag -->
              <v-text-field
                v-model="item.stockOutTag_cnt"

                type="number"
                min=1
                :max="item.stockOutTag_cnt_max"

                oninput="if(Number(this.value) > Number(this.max)) this.value = this.max;"
                @input="getdata(item)"
                :disabled="currentUser.perm>2"
              ></v-text-field>
            </template>

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

//import SideBar from '../../components/RenderBarCode.vue';
//import SideBar from '../../components/RenderBarCode.vue';
import SideBar from '../../components/RenderBarCodeRePrintTag.vue';

//import print from 'vue-print-nb';

export default {
  name: 'stockOutTagPrint',

  mixins: [Common],

  components: {
    SideBar,
  },

  mounted() {
    console.log("stockOutTagPrint, mounted()...");

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
    stockOutTag_EmpID: '',   //入庫人員之員工編號

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
    barCode_select: [],

    pagination: {},

    //資料表頭
    headers: [
      { text: '資料ID', sortable: false, value: 'id', width: '5%', align: 'start'},  //2023-06-26 modify
      { text: '資材碼', sortable: true, value: 'stockOutTag_reagID', width: '6%' },
      { text: '品名', sortable: true, value: 'stockOutTag_reagName', width: '270px' },
      { text: '效期', sortable: true, value: 'stockOutTag_reagPeriod', width: '70px' },
      { text: '保存溫度', sortable: false, value: 'stockOutTag_reagTemp', width: '6%' },
      { text: '入庫日期', sortable: true, value: 'stockOutTag_In_Date', width: '75px' },
      { text: '領料日期', sortable: true, value: 'stockOutTag_Out_Date', width: '75px' },
      { text: '領料人員', sortable: true, value: 'stockOutTag_Employer', width: '75px' },
     //{ text: '入庫人員', sortable: false, value: 'stockOutTag_Employer', width: '15%' },
      { text: '批號', sortable: true, value: 'stockOutTag_batch', width: '8%' },

      { text: '字母', sortable: true, value: 'stockOutTag_alpha', width: '5%' },    // 2023-07-14 add

      { text: '領料單位', sortable: false, value: 'stockOutTag_unit', width: '8%', align: 'center' },
      { text: '張數', sortable: false, value: 'stockOutTag_cnt', width: '5%' },
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
        let ch = 'a'
        if (this.last_status) {
          let ascii = this.last_alpha.charCodeAt(0);
          if (this.todayForAlpha != this.last_date)
            ascii = ascii + 1;
          ch = String.fromCharCode(ascii);
        }
        this.desserts = this.desserts.map((obj) => ({ ...obj, stockOutTag_alpha: ch }));
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
        //this.getLastBatchAlphaForStockOut();    // 2023-07-14 mark
      }
    },

    drawer: {
      handler: function() {
        this.$nextTick(() => {
          if (this.drawer) {
            console.log("disable scrollbar...");
            this.root.style.setProperty('--bar','hidden');
            /*
            let temp_arr=[];
            temp_arr =  JSON.parse(JSON.stringify(this.temp_desserts));
            this.desserts = Object.assign([], temp_arr);
            temp_arr=[];
            console.log("disable scrollbar, this.temp_selected", this.temp_selected);
            temp_arr =  JSON.parse(JSON.stringify(this.temp_selected));
            //temp_arr = temp_arr.map((obj) => ({ ...obj, stockOutTag_alpha: this.last_alpha }));

            this.selected = Object.assign([], temp_arr);
            console.log("disable scrollbar, this.selected", this.selected);
            */

            this.reload=true;
          } else {
            console.log("enable scrollbar...");
            this.root.style.setProperty('--bar','scroll');
            if (this.reload) {
              let temp_arr=[];
              console.log("enable scrollbar, this.temp_selected", this.temp_selected);
              temp_arr =  JSON.parse(JSON.stringify(this.temp_desserts));
              this.desserts = Object.assign([], temp_arr);
              //temp_arr=[];                                                                        //2023-08-08 mark
              //temp_arr =  JSON.parse(JSON.stringify(this.temp_selected));                         //2023-08-08 mark
              //temp_arr = temp_arr.map((obj) => ({ ...obj, stockOutTag_alpha: this.last_alpha })); //2023-08-08 mark

              //this.selected = Object.assign([], temp_arr);                                        //2023-08-08 mark
              //console.log("enable scrollbar, this.selected", this.selected);

              //window.location.reload();
              this.reload=false;
            }
          }
          // 2023-08-08 add
          console.log("b, this.selected => ", this.selected)
          //新增 key:value
          this.selected = this.temp_selected.map(object => {
            return {...object, stockInTag_rePrint: '出庫' };
          });
          console.log("a, this.selected => ", this.selected)
          //
        });
      },
      immediate: true,
    },

    selected(val) {
      //if (val) {
      //  console.log("see see, ", val, val[0]['id'], val[0]['stockOutTag_alpha'])
      //  let index = this.temp_desserts.findIndex(p => p.id == val[0]['id']);
      //  //this.temp_selected =  JSON.parse(JSON.stringify(this.temp_desserts[index]));
      //}
      this.temp_selected =  JSON.parse(JSON.stringify(val));
    },
  },

  created () {
    console.log("stockOutTagPrint, created()...");

    //load 員工與權限資料
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm < 1) {
      this.permDialog=true;
    }
    this.stockOutTag_EmpID = this.currentUser.empID;
    //console.log("empID: ", this.currentUser.empID, this.stockOutTag_EmpID)

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

    this.liststockOutTagPrintData();
    //this.initialize()
  },

  methods: {
    initialize() {
      this.load_SingleTable_ok=false;
      this.liststockOutTagPrintData();
      /*
      this.desserts = [

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
        },
        {
          //id: 2,
          stockOutTag_reagID: '234567891',
          stockOutTag_reagName: 'ABCD',
          stockOutTag_reagPeriod: '111/12/31',
          stockOutTag_reagTemp: '2~8度C',
          stockOutTag_Date: '111/06/01',
          stockOutTag_EmpID: 'N12345',
          stockOutTag_Employer: '陳健南',
          stockOutTag_batch: '1110012345C123400055',
          stockOutTag_cnt: 2,
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
        },
        {
          //id: 7,
          stockOutTag_reagID: '234567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_cnt: 10,
        },
        {
          //id: 8,
          stockOutTag_reagID: '234567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_cnt: 5,
        },
        {
          //id: 9,
          stockOutTag_reagID: '214567897',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_cnt: 10,
        },
        {
          //id: 10,
          stockOutTag_reagID: '214567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_Date: '111/03/10',
          stockOutTag_EmpID: 'T12345',
          stockOutTag_Employer: '林成興',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_cnt: 2,
        },
        {
          //id: 11,
          stockOutTag_reagID: '214567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_cnt: 10,
        },
        {
          //id: 12,
          stockOutTag_reagID: '224567897',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_cnt: 20,
        },
        {
          //id: 13,
          stockOutTag_reagID: '224567898',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_cnt: 10,
        },
        {
          //id: 14,
          stockOutTag_reagID: '224567899',
          stockOutTag_reagName: 'B3344',
          stockOutTag_reagPeriod: '111/8/31',
          stockOutTag_reagTemp: '常溫',
          stockOutTag_Date: '111/06/25',
          stockOutTag_EmpID: 'T87654',
          stockOutTag_Employer: '吳仲偉',
          stockOutTag_batch: '1110012345A123400001',
          stockOutTag_cnt: 10,
        },

      ];
      */
    },

    liststockOutTagPrintData() {
      const path = '/liststockOutTagPrintData';
      console.log("liststockOutTagPrintData, Axios get data...")
      axios.get(path)
      .then((res) => {
        this.temp_desserts = res.data.outputs;
        console.log("GET ok, total records:", res.data.outputs);
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

    getLastBatchAlphaForStockOut() {
      const path = '/getLastBatchAlphaForStockOut';
      console.log("getLastBatchAlphaForStockOut, Axios get data...")
      axios.get(path)
      .then((res) => {
        //console.log("GET ok, total records:", res.data.outputs.length);
        console.log("getLastBatchAlphaForStockOut, GET ok...");

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

    setRowStyle(item) {
      return 'style-1';
    },

    getdata(item) {
      this.editedIndex = this.desserts.indexOf(item);
      console.log(this.desserts[this.editedIndex].stockOutTag_cnt);
      this.temp_desserts[this.editedIndex].stockOutTag_cnt = this.desserts[this.editedIndex].stockOutTag_cnt;
      this.updateStockInByCnt(this.desserts[this.editedIndex]);
    },

    updateStockInByCnt(object) {  //編輯 後端table資料
      console.log("---click update_stockOutTagPrint_by_cnt data---", object);

      const path='/updateStockOutByCnt';
      let payload = Object.assign({}, object);

      axios.post(path, payload)
      .then(res => {
        console.log("update stockOutTagPrint data, status: ", res.data.status);
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

      this.updateStockOutByPrintFlag();
      //2022-12-24 mark
      //this.desserts = this.desserts.filter(val => !this.selected.includes(val));
      this.selected=[]; //2022-12-24 add
      this.drawer=false;  //2023-01-31 add
    },

    updateStockOutByPrintFlag() {
      console.log("---click update_stockOut_by_printFlag---", this.selected);

      const path='/updateStockOutByPrintFlag';
      let payload= {
        blocks: this.selected,
        count: this.selected.length,
      };

      axios.post(path, payload)
      .then(res => {
        console.log("update stockOutTagPrint data, status: ", res.data.status);
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

      //this.selected.forEach(item=>{
      //
      //  item.stockOutTag_alpha=this.temp_desserts array1[item.key]
      //})

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

::v-deep .v-data-table-header th:nth-child(1) > div.v-data-table__checkbox.v-simple-checkbox {
//::v-deep tr th:nth-child(1) {
  width: 40px !important;
  max-width: 40px !important;
}
::v-deep tr td:nth-child(1) {
  width: 40px !important;
  max-width: 40px !important;
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

::v-deep .v-data-table__wrapper td:nth-last-child(1) .v-text-field {
  width: 40px !important;
  max-width: 40px !important;
}
// modify font size, 2023-07-14 add
::v-deep .v-data-table td {
  font-size: 12px !important;
}
// modify table header font size, 2023-07-14 add
::v-deep .v-data-table-header th {
  font-size: 0.9em !important;
}
</style>