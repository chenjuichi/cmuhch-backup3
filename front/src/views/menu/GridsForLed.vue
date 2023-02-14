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

    <v-row align="center" justify="center" v-if="currentUser.perm == 1 || currentUser.perm == 2">
      <v-card width="93vw" class="pa-md-4 mx-lg-auto">
        <v-toolbar flat>
          <v-toolbar-title>儲位燈條資料設定</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <!-- -->
          <v-dialog v-model="dialog" max-width="600px" :content-class='temp_css'>
            <v-card>
              <v-card-title>
                <span class="text-h5">儲位燈條編號</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" md="1">
                      <div style="color: #007bff; font-weight: 800;">第{{  tab_index+1 }}站</div>
                    </v-col>
                    <v-col cols="12" md="4">
                      <div style="color: #007bff; font-weight: 800;">層別</div>
                      <vue-numeric-input  v-model="editedItem.grid_layout" :min="1" :max="5" :step="1"></vue-numeric-input>
                    </v-col>
                    <v-col cols="12" md="4">
                      <div style="color: #007bff; font-weight: 800;">格位編號</div>
                      <vue-numeric-input  v-model="editedItem.grid_pos" :min="1" :max="10" :step="1"></vue-numeric-input>
                    </v-col>
                    <v-col cols="12" md="3">
                      <v-switch
                        v-model="switchOnOff"
                        inset
                        @click="confirmCard">
                        <template v-slot:label>
                          <span class="input__label">{{swString}}</span>
                        </template>
                      </v-switch>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeCard">取消</v-btn>
                <v-btn color="blue darken-1" text @click="confirmCard">確定</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
          <!-- -->
          <v-btn color="primary" class="mt-n1 mr-15 mx-auto" style="position: relative; left: 40px;" elevation="5"  @click="connectMQTT">
            <v-icon>mdi-lan-connect</v-icon>
            連線測試
          </v-btn>

          <v-btn color="primary" class="mt-n1 mr-15 mx-auto" elevation="5" @click="saveData">
            <v-icon>mdi-content-save-check</v-icon>
            儲存資料
          </v-btn>
        </v-toolbar>
        <v-tabs vertical>
          <v-tab
            style="font-size:16px; font-weight:600; width: 140px;"
            v-for="(item, index) in items" :key="item.tab"
            @click="nextTabContent(index)">
            <v-icon left>mdi-library-shelves</v-icon>
            {{ item.tab }} ({{ tab_totals[index] }})
          </v-tab>
        </v-tabs>
        <v-card outlined class="mt-1 mx-auto"
          style="width: 75vw; height:40vw; left: 60px; top: -150px;">
          <LedStrip :my_object="items[tab_index].content" :my_key="tab_index" @closeLedStrip="getGridData"></LedStrip>
        </v-card>
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
              <div class="text-h4 pa-12">權限不足...</div>
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
</div>
</template>

<script>
import axios from 'axios';
import VueNumericInput from 'vue-numeric-input';

import Common from '../../mixin/common.js'
import LedStrip from '../../components/LedStrip.vue'

export default {
  name: 'GridsForLed',

  components: {
    LedStrip, VueNumericInput,
  },

  mixins: [Common],

  mounted() {
    // if back button is pressed
    window.onpopstate = () => {
      console.log("press back button, good bye...");

      //const userData = JSON.parse(localStorage.getItem('loginedUser'));
      //userData.setting_items_per_page = this.pagination.itemsPerPage;
      //localStorage.setItem('loginedUser', JSON.stringify(userData));
    };
  },

  data() {
    return {
      currentUser: {},
      permDialog: false,

      snackbar: false,
      snackbar_color: 'success',
      snackbar_right: true,
      snackbar_top: true,
      snackbar_info: '',
      snackbar_icon_color: '#adadad',

      //pagination: {
        //itemsPerPage: 10,   //預設值, rows/per page
        //page: 1,
      //},

      dialog: false,

      items: [
        { tab: '第1站料架', content: {} },
        { tab: '第2站料架', content: {} },
        { tab: '第3站料架', content: {} },
      ],
      tab_index: 0,

      rangErrMsg: '',
      errorMessages: {  //for 錯誤訊息
        message1: '',
        message2: '',
        message3: '',
        message4: '',
        message5: '',
      },
      min: 1,
      max: 30,

      ranges: {     //for slider輸入範圍
        range1: [],
        range2: [],
        range3: [],
        range4: [],
        range5: [],
      },
      tab1_rans: {
        range1: [],
        range2: [],
        range3: [],
        range4: [],
        range5: [],
      },
      tab2_rans: {
        range1: [],
        range2: [],
        range3: [],
        range4: [],
        range5: [],
      },
      tab3_rans: {
        range1: [],
        range2: [],
        range3: [],
        range4: [],
        range5: [],
      },

      segment_values: [], //for輸入segment代號

      selectedLeds: {   //for顯示數字或'.' , 共30組
        led1: [
        //  value:
        ],
        led2: [],
        led3: [],
        led4: [],
        led5: [],
      },
      selectedLamps: {  //for顯示Led燈號
        led1: [
        //  value:
        ],
        led2: [],
        led3: [],
        led4: [],
        led5: [],
      },

      segments: {     //for在各segment內的值
        segment1: [
      //  seg_id:,
      //  range0:,
      //  range1:,
        ],
        segment2: [],
        segment3: [],
        segment4: [],
        segment5: [],
      },
      tab1_segs: {
        segments1: [],
        segments2: [],
        segments3: [],
        segments4: [],
        segments5: [],
      },
      tab2_segs: {
        segments1: [],
        segments2: [],
        segments3: [],
        segments4: [],
        segments5: [],
      },
      tab3_segs: {
        segments1: [],
        segments2: [],
        segments3: [],
        segments4: [],
        segments5: [],
      },

      myObject1: {
        segs: {},
        rans: {},
      },
      myObject2: {
        segs: {},
        rans: {},
      },
      myObject3: {
        segs: {},
        rans: {},
      },
      tab_totals: [],

      temp_desserts: [],

      editedItem: {
        grid_station: 1,
        grid_layout: 1,
        //grid_seg_id: 1,
        grid_pos: 1,
      },
      defaultItem: {
        grid_station: 1,
        grid_layout: 1,
        //grid_seg_id: 1,
        grid_pos: 1,
      },

      pre_topic: 0,

      switchOnOff: false,
      sw_on_str: '亮燈',
      sw_off_str: '熄燈',
      mqtt_topic:['station1','station2','station3',],
      load_SingleTable_ok: false, //for get grids table data
    }
  },

  computed: {
    swString() {
      return this.switchOnOff ? this.sw_on_str : this.sw_off_str;
    },
  },

  watch: {
    load_SingleTable_ok(val) {
      if (val) {
        this.load_SingleTable_ok=false;

        this.getTabsData();
      } //end if condition
    },  //end load_SingleTable_ok()

    tab_index(newValue, oldValue) {
      console.log("newValue, oldValue, tab_index: ",newValue, oldValue, this.tab_index);
      this.pre_topic=oldValue;
    },
  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm == 0 || this.currentUser.perm >1) {
      this.permDialog=true;
      //console.log("router undefine!")
    }

    //this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    // init燈號數字資料
    let obj= {value: '.',}
    for (let i=0; i<this.max; i++) {
      let obj= {value: '.',}
      this.selectedLeds.led1.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: '.',}
      this.selectedLeds.led2.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: '.',}
      this.selectedLeds.led3.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: '.',}
      this.selectedLeds.led4.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: '.',}
      this.selectedLeds.led5.push(obj);
    }

    // init燈號led資料
    for (let i=0; i<this.max; i++) {
      let obj= {value: false,}
      this.selectedLamps.led1.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: false,}
      this.selectedLamps.led2.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: false,}
      this.selectedLamps.led3.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: false,}
      this.selectedLamps.led4.push(obj);
    }
    for (let i=0; i<this.max; i++) {
      let obj= {value: false,}
      this.selectedLamps.led5.push(obj);
    }

    this.load_SingleTable_ok=false;
    this.initAxios();

    this.listGrids();
  },

  methods: {
    listGrids() {
      const path = '/listGridsForLed';
      console.log("listGridsForLed, Axios get data...")
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

    getTabsData() {
      let max_stations=3;
      let max_layouts=5;
      let grid_count=this.temp_desserts.length;

      //get data from database into tab1_segs, tab2_segs and tab3_segs
      for (let i=0; i<grid_count; i++) {
        let sw = parseInt(this.temp_desserts[i].grid_station);
        switch (sw) {
          case 1:   //第1個料站
            for (let i=0; i<max_layouts; i++) {
              this.tab1_segs[Object.keys(this.tab1_segs)[i]] = this.temp_desserts.filter(function( obj ) {
                return (parseInt(obj.grid_station) == 1  && parseInt(obj.grid_layout) == i+1);
              });
            }

            for (let i=0; i<max_layouts; i++) {
              let segs= this.tab1_segs[Object.keys(this.tab1_segs)[i]].length;
              /*
              if (segs != 0) {
                let j=0
                do {
                  delete this.tab1_segs[Object.keys(this.tab1_segs)[i]][j].grid_reagName;
                  delete this.tab1_segs[Object.keys(this.tab1_segs)[i]][j].grid_reagID;
                  j++
                } while  (j < segs);
              }
              */
            }

            break;
          case 2:   //第2個料站
            for (let i=0; i<max_layouts; i++) {
              this.tab2_segs[Object.keys(this.tab2_segs)[i]] = this.temp_desserts.filter(function( obj ) {
                return (parseInt(obj.grid_station) == 2  && parseInt(obj.grid_layout) == i+1);
              });
            }

            for (let i=0; i<max_layouts; i++) {
              let segs= this.tab2_segs[Object.keys(this.tab2_segs)[i]].length;
              /*
              if (segs != 0) {
                let j=0
                do {
                  delete this.tab2_segs[Object.keys(this.tab2_segs)[i]][j].grid_reagName;
                  delete this.tab2_segs[Object.keys(this.tab2_segs)[i]][j].grid_reagID;
                  j++
                } while  (j < segs);
              }
              */
            }

            break;
          default:     //第3個料站
            for (let i=0; i<max_layouts; i++) {
              this.tab3_segs[Object.keys(this.tab3_segs)[i]] = this.temp_desserts.filter(function( obj ) {
                return (parseInt(obj.grid_station) == 3  && parseInt(obj.grid_layout) == i+1);
              });
            }

            for (let i=0; i<max_layouts; i++) {
              let segs= this.tab3_segs[Object.keys(this.tab3_segs)[i]].length;
              /*
              if (segs != 0) {
                let j=0
                do {
                  delete this.tab3_segs[Object.keys(this.tab3_segs)[i]][j].grid_reagName;
                  delete this.tab3_segs[Object.keys(this.tab3_segs)[i]][j].grid_reagID;
                  j++
                } while  (j < segs);
              }
              */
            }

            break;
        } //end switch loop
      } //end for loop

      this.tab_totals[0]=0;
      for (let index=0; index<5; index++) {
        let t1=Object.keys(this.tab1_segs[Object.keys(this.tab1_segs)[index]]).length
        this.tab_totals[0] = this.tab_totals[0] + t1;
      }
      console.log("tab1 :", this.tab_totals[0]);

      this.tab_totals[1]=0;
      for (let index=0; index<5; index++) {
        let t2=Object.keys(this.tab2_segs[Object.keys(this.tab2_segs)[index]]).length
        this.tab_totals[1] = this.tab_totals[1] + t2;
      }
      console.log("tab2 :", this.tab_totals[1]);

      this.tab_totals[2]=0;
      for (let index=0; index<5; index++) {
        let t3=Object.keys(this.tab3_segs[Object.keys(this.tab3_segs)[index]]).length
        this.tab_totals[2] = this.tab_totals[2] + t3;
      }
      console.log("tab3 :", this.tab_totals[2]);

      this.myObject1.segs = Object.assign({}, this.tab1_segs);
      this.myObject2.segs = Object.assign({}, this.tab2_segs);
      this.myObject3.segs = Object.assign({}, this.tab3_segs);

      //get (tab1_rans, tab2_rans, tab3_rans) data from (tab1_segs, tab2_segs, tab3_segs)
      for (let i=0; i<max_layouts; i++) {
        //console.log("station 1...")
        if (this.tab1_segs[Object.keys(this.tab1_segs)[i]].length!=0) {
          this.tab1_rans[Object.keys(this.tab1_rans)[i]][0]=parseInt(this.tab1_segs[Object.keys(this.tab1_segs)[i]][0].range0);
          this.tab1_rans[Object.keys(this.tab1_rans)[i]][1]=parseInt(this.tab1_segs[Object.keys(this.tab1_segs)[i]][0].range1);
        } else {
          this.tab1_rans[Object.keys(this.tab1_rans)[i]][0]=1;  //init range slider min default value
          this.tab1_rans[Object.keys(this.tab1_rans)[i]][1]=3;  //init range slider max default value
        }

        //console.log("station 2...")
        if (this.tab2_segs[Object.keys(this.tab2_segs)[i]].length!=0) {
          this.tab2_rans[Object.keys(this.tab2_rans)[i]][0]=parseInt(this.tab2_segs[Object.keys(this.tab2_segs)[i]][0].range0);
          this.tab2_rans[Object.keys(this.tab2_rans)[i]][1]=parseInt(this.tab2_segs[Object.keys(this.tab2_segs)[i]][0].range1);
        } else {
          this.tab2_rans[Object.keys(this.tab2_rans)[i]][0]=1;  //init range slider min default value
          this.tab2_rans[Object.keys(this.tab2_rans)[i]][1]=3;  //init range slider max default value
        }

        //console.log("station 3...")
        if (this.tab3_segs[Object.keys(this.tab3_segs)[i]].length!=0) {
          this.tab3_rans[Object.keys(this.tab3_rans)[i]][0]=parseInt(this.tab3_segs[Object.keys(this.tab3_segs)[i]][0].range0);
          this.tab3_rans[Object.keys(this.tab3_rans)[i]][1]=parseInt(this.tab3_segs[Object.keys(this.tab3_segs)[i]][0].range1);
        } else {
          this.tab3_rans[Object.keys(this.tab3_rans)[i]][0]=1;  //init range slider min default value
          this.tab3_rans[Object.keys(this.tab3_rans)[i]][1]=3;  //init range slider max default value
        }
      }
      this.myObject1.rans = Object.assign({}, this.tab1_rans);
      this.myObject2.rans = Object.assign({}, this.tab2_rans);
      this.myObject3.rans = Object.assign({}, this.tab3_rans);

      this.items[0].content = Object.assign({}, this.myObject1);
      this.items[1].content = Object.assign({}, this.myObject2);
      this.items[2].content = Object.assign({}, this.myObject3);

      //this.slider_data_ok=true;
    },

    getGridData(value, index, obj) {
      console.log("hello return from child component ...", value, index, obj)
      if (value==0) {
        //console.log("return from station1 ...", obj[Object.keys(obj)[index]], this.tab1_segs[Object.keys(this.tab1_segs)[index]]);
        this.tab1_segs[Object.keys(this.tab1_segs)[index]]= Object.assign([], obj[Object.keys(obj)[index]]);
        console.log("station1 new obj: ", this.tab1_segs[Object.keys(this.tab1_segs)[index]]);

        //this.myObject1.segs[Object.keys(this.myObject1.segs)[index]] = Object.assign({}, this.tab1_segs[Object.keys(this.tab1_segs)[index]]);
        this.myObject1.segs = Object.assign({}, this.tab1_segs);

        //this.myObject1.segs[Object.keys(this.myObject1.segs)[index]] = this.tab1_segs[Object.keys(this.tab1_segs)[index]];
        console.log("station1 new myObject1.segs: ", this.myObject1.segs)
        this.items[0].content = Object.assign({}, this.myObject1);

        this.tab_totals[0]=0;
        for (let index=0; index<5; index++) {
          let t1=Object.keys(this.tab1_segs[Object.keys(this.tab1_segs)[index]]).length
          this.tab_totals[0] = this.tab_totals[0] + t1;
        }
      }

      if (value==1) {
        //console.log("return from station2 ...", obj[Object.keys(obj)[index]], this.tab2_segs[Object.keys(this.tab1_segs)[index]])
        this.tab2_segs[Object.keys(this.tab2_segs)[index]]= Object.assign([], obj[Object.keys(obj)[index]]);
        console.log("station2 new obj: ", this.tab2_segs[Object.keys(this.tab2_segs)[index]])

        this.myObject2.segs = Object.assign({}, this.tab2_segs);

        //this.myObject2.segs = Object.assign({}, this.tab2_segs);
        //this.myObject2.segs[Object.keys(this.myObject2.segs)[index]] = Object.assign({}, this.tab2_segs[Object.keys(this.tab2_segs)[index]]);
        //this.myObject2.segs[Object.keys(this.myObject2.segs)[index]] = this.tab2_segs[Object.keys(this.tab2_segs)[index]];
        console.log("station2 new myObject1.segs: ", this.myObject2.segs)
        this.items[1].content = Object.assign({}, this.myObject2);

        this.tab_totals[1]=0;
        for (let index=0; index<5; index++) {
          let t2=Object.keys(this.tab2_segs[Object.keys(this.tab2_segs)[index]]).length
          this.tab_totals[1] = this.tab_totals[1] + t2;
        }
      }

      if (value==2) {
        console.log("return from station3 ...", obj[Object.keys(obj)[index]], this.tab3_segs[Object.keys(this.tab1_segs)[index]])

        this.tab3_segs[Object.keys(this.tab3_segs)[index]]= Object.assign([], obj[Object.keys(obj)[index]]);
        console.log("station3 new obj: ", this.tab3_segs[Object.keys(this.tab3_segs)[index]])
        this.myObject3.segs = Object.assign({}, this.tab3_segs);

        //this.myObject3.segs = Object.assign({}, this.tab3_segs);
        //this.myObject3.segs[Object.keys(this.myObject3.segs)[index]] = Object.assign({}, this.tab3_segs[Object.keys(this.tab3_segs)[index]]);
        //this.myObject3.segs[Object.keys(this.myObject3.segs)[index]] = this.tab3_segs[Object.keys(this.tab3_segs)[index]];
        console.log("station3 new myObject1.segs: ", this.myObject3.segs)
        this.items[2].content = Object.assign({}, this.myObject3);

        this.tab_totals[2]=0;
        for (let index=0; index<5; index++) {
          let t3=Object.keys(this.tab3_segs[Object.keys(this.tab3_segs)[index]]).length
          this.tab_totals[2] = this.tab_totals[2] + t3;
        }
      }
    },

    nextTabContent(index) {
      console.log("hello, tab index:", index);
      this.tab_index=index;
    },

    closeCard () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    confirmCard () {
      let temp_segs= {};
      if (this.tab_index==0) {
        temp_segs = Object.assign({}, this.tab1_segs);
        console.log("segment compare", temp_segs, this.tab1_segs)
      }
      if (this.tab_index==1) {
        temp_segs = Object.assign({}, this.tab2_segs);
        console.log("segment compare", temp_segs, this.tab2_segs)
      }
      if (this.tab_index==2) {
        temp_segs = Object.assign({}, this.tab3_segs);
        console.log("segment compare", temp_segs, this.tab3_segs)
      }

      let temp_len=temp_segs[Object.keys(temp_segs)[this.editedItem.grid_layout-1]].length;
      console.log("tab1_segs", this.editedItem.grid_layout, this.editedItem.grid_pos, temp_segs, "temp_len: ", temp_len);
      let loop_ok = true;   //true,層與格位編號資料正確
      let range_begin = 0;
      let range_end = 0;
      for (let i=0; i<temp_len; i++) {
        let temp_seg=parseInt(temp_segs[Object.keys(temp_segs)[this.editedItem.grid_layout-1]][i].seg_id);
        console.log("tab1_segs, layout", i+1, "  ", temp_segs[Object.keys(temp_segs)[this.editedItem.grid_layout-1]][i]);
        console.log("tab1_segs, layout, seg_id: ", temp_seg, this.editedItem.grid_pos);

        if (temp_seg == this.editedItem.grid_pos) {
          range_begin = temp_segs[Object.keys(temp_segs)[this.editedItem.grid_layout-1]][i].range0;
          range_end = temp_segs[Object.keys(temp_segs)[this.editedItem.grid_layout-1]][i].range1;
          loop_ok = false;
          break;
        }
      }
      console.log("tab1_segs step1", loop_ok, "  ", range_begin, "  ", range_end)
      if (!loop_ok) {
        let layout=this.editedItem.grid_layout;
        this.mqttForStation(layout, range_begin, range_end);
      } else {
        console.log("格位編號錯誤!");
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '格位編號錯誤!';
        this.snackbar_icon_color= '#adadad';
      }
    },

    async mqttForStation(layout, range_begin, range_end) {
        //let path='/mqtt/station1';
        let path='/mqtt/station';
        //let temp_layout=this.currentLedLayout.toString();
        let temp_layout=layout.toString();
        //let temp_pos=this.currentLedPos.toString();
        console.log("station: " + this.currentIndex + this.mqtt_topic[this.tab_index] + this.tab_index)
        console.log("station: " + this.mqtt_topic[this.tab_index] + "layout: " + temp_layout + " pos: " + range_begin + " , " + range_end)
        let temp_sw= this.switchOnOff ? 'on' : 'off';
        //let temp_sw= 'flash';
        let payload= {
          topic: this.mqtt_topic[this.tab_index],
          layout: temp_layout,
          pos_begin: range_begin,
          pos_end: range_end,
          msg: temp_sw,
        };

        try {
          let res = await axios.post(path, payload);
          console.log("mqtt ok", res.data.status);
        } catch (err) {
          console.error(err)
          console.log("通訊錯誤!");
          this.snackbar_color='red accent-2';
          this.snackbar=true;
          this.snackbar_info= '通訊錯誤!';
          this.snackbar_icon_color= '#adadad';
        }
    },

    async mqttForStationOff() {
      console.log("mqttForStationOff, tab index: ", this.tab_index)

      let path='/mqtt/station';
      let temp_layout='0';
      let range_begin='0';
      let range_end='0';
      let temp_sw= 'off';
      //let myTopic=this.mqtt_topic[this.tab_index]
      let myTopic=this.mqtt_topic[this.pre_topic]
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
      } catch (err) {
        console.error(err)
        console.log("通訊錯誤!");
        this.snackbar_color='red accent-2';
        this.snackbar=true;
        this.snackbar_info= '通訊錯誤!';
        this.snackbar_icon_color= '#adadad';
      }
    },

    connectMQTT() {
      console.log("connectMQTT, tab index: ", this.tab_index);

      this.switchOnOff= false;
      this.dialog = true;

      this.mqttForStationOff();
    },

    saveData() {  //update grid後端table資料
      console.log("---GridsForLed, click saveData---");

      const path='/updateGridsForLed';
      let payload= {
        tab1_segs: this.tab1_segs,
        tab2_segs: this.tab2_segs,
        tab3_segs: this.tab3_segs,
      };

      axios.post(path, payload)
      .then(res => {
        console.log("update grid data, return status: ", res.data.status)
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

::v-deep .centered-input input {
  text-align: center !important;
}
.container_tab1  {
  background: #666;
  overflow: hidden;
  margin: auto;
  font-size: 0;
}

.dot {
  display: inline-block;
  font-size: 0px;
  line-height: 0;
  border-radius: 50%;
  background: #444;
  box-shadow: inset 0px 0px 10px 5px #303030;
  position:relative;
}

.dot::after{
  content:' ';
  position:absolute;
  background-color:rgba(255,255,255,1);
  border-radius:50%;
  width:15px;
  height:15px;
  right:4px;
  bottom:4px;
  background-image: radial-gradient(center, circle closest-side, #777, #333);
  background-image: -o-radial-gradient(center, circle closest-side, #777, #333);
  background-image: -ms-radial-gradient(center, circle closest-side, #777, #333);
  background-image: -moz-radial-gradient(center, circle closest-side, #777, #333);
  background-image: -webkit-radial-gradient(center, circle closest-side, #777, #333);
}

.on {
  background: #fff;
  box-shadow: 0px 0px 20px 3px #fcfcaa, inset 0px 0px 13px #777;
}

.on::after{
  display:none;
}

small.msgErr {
  font-size: 85%;
  color: red;
  margin-top: -10px;
  position: relative;
  right: -120px;
  top: -17px;
}

.input__label {
  color: #007bff;
  font-weight: 800;
}
</style>