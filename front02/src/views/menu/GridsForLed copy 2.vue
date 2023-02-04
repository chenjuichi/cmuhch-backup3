<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm == 1">
      <v-card width="92vw" class="pa-md-4  mt-5 mx-lg-auto">
        <v-toolbar flat>
          <v-toolbar-title>儲位Led資料設定</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
        </v-toolbar>

        <v-tabs vertical>
          <v-tab>
            <v-icon left>mdi-account</v-icon>
            第1站料架
          </v-tab>
          <v-tab>
            <v-icon left>mdi-lock</v-icon>
            第2站料架
          </v-tab>
          <v-tab>
            <v-icon left>mdi-access-point</v-icon>
            第3站料架
          </v-tab>

          <v-tab-item>
            <v-card flat>
              <v-card-text id="app_tab_1" ref="card_text">
                <div class="container_tab" style="width: 900px; padding: 10px; border-radius: 10px;">
                  <div
                    class="dot"
                    :id="`lights_5_${index}`"
                    style="width: 25px; height: 25px; margin: 3px 2px 2px 2px;"
                    v-for="(n, index) in 30"
                  ></div>
                </div>
                <div v-show="isShow"
                  :id="`temp_texts_5__${field.id}`"
                  class="temp_text"
                  v-for="(field, index) in segments" :key="index"
                  :style="styleObject">
                  <TempText :myText="field" @closeTempText="getComp"></TempText>
                </div>

                <v-row>
                  <v-col class="px-4" cols="12" md="1">
                  </v-col>
                  <v-col class="pl-6 pr-2" cols="12" md="10">
                    <v-range-slider
                      v-model="range"
                      @click="eraseErrMsg"
                      :max="max"
                      :min="min"
                      hide-details
                      class="align-center"
                    >
                      <template v-slot:prepend>
                        <v-text-field
                          :value="range[0]"
                          :max="max"
                          :min="min"
                          @focus="eraseErrMsg"
                          class="mt-0 pt-0"
                          v-model="range[0]"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          @change="$set(range, 0, $event)"
                        ></v-text-field>
                      </template>
                      <template v-slot:append>
                        <v-text-field
                          :value="range[1]"
                          :max="max"
                          :min="min"
                          class="mt-0 pt-0"
                          v-model="range[1]"
                          hide-details
                          single-line
                          type="number"
                          style="width: 60px"
                          @focus="eraseErrMsg"
                          @change="$set(range, 1, $event)"
                        ></v-text-field>
                      </template>
                    </v-range-slider>
                    <small class="msgErr" v-text= "rangErrMsg"></small>
                  </v-col>
                  <v-col class="pr-4 pl-0" cols="12" md="1">
                    <v-btn

                      small
                      class="ml-0 mr-2 mt-2"

                      color="primary"
                      @click="toggleLed()">
                      <v-icon>mdi-gesture-tap</v-icon>
                    </v-btn>

                  </v-col>
                </v-row>
                <!--
                <p>
                  第1個料架建置中...
                </p>
                -->


              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card flat>
              <v-card-text id="app_tab_2">
                <p>
                  第2個料架建置中...
                </p>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card flat>
              <v-card-text id="app_tab_3">
                <p>
                  第3個料架建置中...
                </p>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs>

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
import Common from '../../mixin/common.js'
import TempText from '../../components/TempText.vue'

export default {
  name: 'GridsForLed',

  components: {
    TempText: TempText,
  },

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
    currentUser: {},
    permDialog: false,

    pagination: {
      //itemsPerPage: 10,   //預設值, rows/per page
      //page: 1,
    },


    tab: null,
    items: ['  第1個料架  ', '  第2個料架  ', '  第3個料架  '],
    text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',

    rangErrMsg: '',
    min: 1,
    max: 30,
    range: [1, 3],
    Leds: [],

    isShow: false,
    segments: [],
    segment_width: 56,
    light_width: 29,
    init_id: 1,

    styleObject: {
      marginRight: 56 + 'px', //init margin-right value
      marginLeft: 56 + 'px',  //init margin-left value
    },
  }),

  computed: {

  },

  watch: {

  },

  created () {
    this.currentUser = JSON.parse(localStorage.getItem("loginedUser"));
    if (this.currentUser.perm == 0 || this.currentUser.perm >1) {
      this.permDialog=true;
      //console.log("router undefine!")
    }

    this.pagination.itemsPerPage=this.currentUser.setting_items_per_page

    this.Leds=[];
    for (let i=0; i<this.max; i++) {
      this.Leds.push(false)
    }
  },

  methods: {
    getComp() {
      let el = document.getElementsByClassName('temp_text').length;
      for (let i=0; i< el; i++) {
        document.getElementsByClassName('temp_text')[i].style['margin-left'] = (this.light_width * this.segments[i].size - this.segment_width) / 2  + 'px';
        document.getElementsByClassName('temp_text')[i].style['margin-right'] = (this.light_width * this.segments[i].size - this.segment_width) / 2  + 'px';
      }
    },

    toggleLed() {
      this.rangErrMsg='';
      if (this.range[0] > this.range[1]) {
        this.rangErrMsg='格位資料設定錯誤!'
        return;
      }
      let temp_seg_size=this.segments.length
      for (let i=0; i<temp_seg_size; i++) {
        if (this.range[0] <= this.segments[i].range[0] || this.range[0] <= this.segments[i].range[1] ||
            this.range[1] <= this.segments[i].range[0] || this.range[1] <= this.segments[i].range[1]) {
          this.rangErrMsg='格位資料設定錯誤!'
          return;
        }
      }

      let temp_size=this.range[1] - this.range[0]+1;
      console.log("temp_size", temp_size)
      let obj= {
        id: this.init_id,
        text:this.init_id.toString(),
        size: temp_size,
        type: 'station1',
        range: this.range,
      }
      this.segments.push(obj);

      this.init_id++;

      this.isShow = true;

      for (let i=this.range[0]-1; i<this.range[1]; i++) {
        let dot = document.getElementById("lights_5_" + i);
        this.Leds[i]= !this.Leds[i];
        let temp_togg= this.Leds[i] ? (dot.className += " on") : (dot.className = "dot");
      }
    },

    eraseErrMsg() {
      console.log("range data error...")
      this.rangErrMsg='';
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

::v-deep .v-data-table >.v-data-table__wrapper > table > tbody > tr:last-child td:nth-child(4) > .v-input--selection-controls__input {
  margin-top: -18px;
}

::v-deep .v-data-table >.v-data-table__wrapper > table > tbody > td:last-child > label {
  margin-bottom: -4px;
}

::v-deep .v-data-table >.v-data-table__wrapper > table > tbody > tr:last-child {
  background: #7DA79D;
}

::v-deep .myLabel label  {
  margin-bottom: 1px;
}

::v-deep .v-data-table-header th:nth-last-child(3) span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(2) span {
  color: #1f4788 !important;
}
::v-deep .v-data-table-header th:nth-last-child(1) span {
  color: #1f4788 !important;
}

//=====
.temp_text {
  position: relative;
  left: 50px;
  top: 5px;
  display: inline-block;
  font-size: 10px;
  border-radius: 20px;
  background: red;

  padding: 0 10px 0 10px;
  //margin: 0 15px 0 15px;
  margin-top: 0;
  //margin-right: (var(--wd) - 56px)/2;
  margin-bottom: 0;
  //margin-left: (var(--wd) - 56px)/2;
}

.led_segment {
  display: inline-block;
}

.container_tab  {
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
  font-size: 80%;
  color: red;
  margin-top: -10px;
}
</style>