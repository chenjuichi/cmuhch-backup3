<template>
<v-app>
  <v-container fluid>
    <v-row align="center" justify="center" v-if="currentUser.perm == 1">
      <v-card width="92vw" class="pa-md-4 mx-lg-auto">
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
<!-- 5 -->
                <div class="container_tab" style="width: 900px; padding: 10px; border-radius: 10px;">
                  <div style="color: white; font-size: 14px; text-align: center;">
                    <p v-for="(n, index) in 30" style="width: 25px; height: 25px; margin: 0px 2px 0px 2px; display:inline; float:left;">
                      {{ index+1 }}
                    </p>
                  </div>
                  <div
                    class="dot"
                    :id="`light_${index}`"
                    style="width: 25px; height: 25px; margin: 0px 2px 0px 2px;"
                    v-for="(n, index) in 30"
                  ></div>
                </div>
                <!--
                <div v-show="isShow"
                  class="temp_text"
                  v-for="field in segments" :key="field.id"
                  :style="styleObject"
                  @mouseover="hover = true"
                  @mouseleave="hover = false"

                >
                  <span v-show="hover">
                    LED{{ field.range0 }} 至 LED{{ field.range1 }}
                  </span>
                  <div class="v22">
                  <TempText
                    :myText="field"
                    @closeTempText="getComp"

                    ></TempText>
                  <div class="vl" :style="styleLeft"></div>
                  </div>
                </div>
                -->

                <v-row>
                  <v-col class="px-4" cols="12" md="1"></v-col>
                  <v-col class="pl-6 pr-2" cols="12" md="5">
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
                  <v-col class="mt-1 pr-2 pl-0" cols="12" md="6">
                    <!--
                    <v-btn

                      small
                      class="ml-0 mr-2 mt-2"

                      color="primary"
                      @click.native="toggleLed($event)">
                      <v-icon>mdi-gesture-tap</v-icon>
                    </v-btn>
                    -->
                <!-- test temp
                      <v-sheet class="mx-0" max-width="300">
                        <v-slide-group
                          multiple
                          show-arrows
                          active-class="success"
                          v-model="model"

                          >
                          <v-slide-item
                            v-for="(n, index) in 15"
                            :key="index"
                            v-slot:default="{ active, toggle }"
                          >
                            <v-btn
                              :id="`btnGroup_${index}`"

                              :input-value="active"
                              :class="{'dnrSelected' : selectedChips[index]}"

                              depressed
                              rounded
                              x-small
                              @click="toggleLed(index)">
                              格位 {{ n }}
                            </v-btn>
                          </v-slide-item>
                        </v-slide-group>
                      </v-sheet>
                -->

                  <template>
                        <v-sheet
                          elevation="10"
                          class="py-1 px-1 rounded-md"
                          style="height: 90%; width: 85%; border-radius: 10px"
                        >
                          <v-chip-group
                            multiple
                            show-arrows
                            v-model="model"
                            active-class="primary--text"
                          >
                            <v-chip
                              style="font-size: 12px; height: 20px;"
                              v-for="(tag, index) in tags"
                              :key="tag"
                              @click="toggleLed(index)"

                            >
                              格位 {{ index+1 }}
                            </v-chip>
                          </v-chip-group>
                        </v-sheet>
                  </template>

                  </v-col>

                </v-row>
                <span style="position:relative; z-index:31; background: red; top: -50px; left: 540px; border-radius: 2px">Add to cart</span>
<!-- end -->
                <!--
                <template>
                  <v-stepper
                    v-model="e6"
                    vertical
                  >
                    <v-stepper-step
                      :complete="e6 > 1"
                      step="1"
                    >
                      Select an app
                    </v-stepper-step>

                    <v-stepper-content step="1">
                      <v-btn
                        color="primary"
                        @click="e6 = 2"
                      >
                        Continue
                      </v-btn>
                    </v-stepper-content>

                    <v-stepper-step
                      :complete="e6 > 2"
                      step="2"
                    >
                      Configure analytics for this app
                    </v-stepper-step>

                    <v-stepper-content step="2">
                      <v-btn
                        color="primary"
                        @click="e6 = 3"
                      >
                        Continue
                      </v-btn>
                    </v-stepper-content>

                    <v-stepper-step
                      :complete="e6 > 3"
                      step="3"
                    >
                      Select an ad format and name ad unit
                    </v-stepper-step>

                    <v-stepper-content step="3">
                      <v-btn
                        color="primary"
                        @click="e6 = 4"
                      >
                        Continue
                      </v-btn>
                    </v-stepper-content>

                    <v-stepper-step step="4">
                      View setup instructions
                    </v-stepper-step>
                    <v-stepper-content step="4">
                      <v-btn
                        color="primary"
                        @click="e6 = 1"
                      >
                        Continue
                      </v-btn>
                    </v-stepper-content>
                  </v-stepper>
                </template>
                -->
<!-- test 1-->
              <!--
              <template>
                <v-sheet
                  class="mx-auto"
                  max-width="300"
                >
                  <v-slide-group
                    multiple
                    show-arrows
                  >
                    <v-slide-item
                      v-for="n in 15"
                      :key="n"
                      v-slot="{ active, toggle }"
                    >
                      <v-btn
                        class="mx-0"
                        :input-value="active"
                        active-class="purple white--text"
                        depressed
                        rounded
                        x-small
                        @click="toggleLed($event)">
                      >
                        格位 {{ n }}
                      </v-btn>
                    </v-slide-item>
                  </v-slide-group>
                </v-sheet>
              </template>
              -->
<!-- test 2-->
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

  data() {
    return {
      currentUser: {},
      permDialog: false,

      pagination: {
        //itemsPerPage: 10,   //預設值, rows/per page
        //page: 1,
      },

      rounded: [
        '0',
        'sm',
        'md',
        'lg',
        'xl',
        'pill',
        'circle',
      ],
      action: false,
      uniqueRef: 'button2',
      tags: [
        'Work',
        'Home Improvement',
        'Vacation',
        'Food',
        'Drawers',
        'Shopping',
        'Art',
        'Tech',
        'Creative Writing',
      ],

      model: [],
      //myColor: 'dnrSelected',
      //selectedIndex: -1,
      //selected: false,

      tab: null,
      items: ['  第1個料架  ', '  第2個料架  ', '  第3個料架  '],
      text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',

      rangErrMsg: '',
      min: 1,
      max: 30,
      range: [1, 3],
      Leds: [],

      selectedChips: [],

      isShow: false,
      selectedCatalogs: [],
      segments: [],
      segment_width: 44,
      light_width: 29,
      init_id: 1,
      hover: false,

      styleObject: {
        marginRight: 56 + 'px', //init margin-right value
        marginLeft: 56 + 'px',  //init margin-left value
      },
      styleLeft: {
        left: 29 + 'px',
      },
      ledoff: false,
    }
  },

  computed: {
      radius () {
        let rounded = 'rounded'
        const value = this.rounded[this.model]

        if (value !== 'md') {
          rounded += `-${value}`
        }

        return rounded
      },
  },

  watch: {
    model(val) {
        console.log("model: ", val);
    },

/*
    range: {
      handler: function(newValue) {
        console.log("Person: ", newValue);
        this.segments = this.segments.filter(function( obj ) {
          return (newValue[0] != obj.range0 && newValue[1] != obj.range1);
        });
      },

      deep: true
    }
*/
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

    this.selectedChips=[];
    for (let i=0; i<15; i++) {
      this.selectedChips.push(false)
    }
  },

  methods: {
    getComp() {
      let el = document.getElementsByClassName('temp_text').length;

      for (let i=0; i< el; i++) {
        document.getElementsByClassName('temp_text')[i].style['margin-left'] = (this.light_width * this.segments[i].size - this.segment_width) / 2  + 'px';
        document.getElementsByClassName('temp_text')[i].style['margin-right'] = (this.light_width * this.segments[i].size - this.segment_width) / 2  + 'px';
        document.getElementsByClassName('temp_text')[i].style['left'] = (10+29) - 20 * (this.segments[i].id - 1)+ 'px';
        document.getElementsByClassName('temp_text')[i]
        .getElementsByClassName('v22')[0].childNodes[1].style['left']= (29 * this.segments[i].range0 -39) / 2 + 'px';
        //.getElementsByClassName('v22')[0].childNodes[1].style['left']= (29 * this.segments[i].size -39) / 2 + 'px';
      }
    },

    toggleLed(index) {
      this.rangErrMsg='';
      let temp_seg_size=this.segments.length;
      let r0=this.range[0];
      let r1=this.range[1];
      let temp_size=this.range[1] - this.range[0]+1;

      console.log("index: ", index, this.model)
      //for (let i=0; i<15; i++) {
        //let chip = document.getElementById("btnGroup_" + i);
      this.selectedChips[index]= !this.selectedChips[index];
      console.log("index: ", index, this.selectedChips[index])
        //let temp_togg= this.chips[i] ? (chip.className += ' dnrSelected') : (chip.className -= ' dnrSelected');
      //}

      //檢查資料的正確性
      if (this.range[0] > this.range[1]) {
        this.rangErrMsg='格位資料設定錯誤!'
        return;
      }
      for (let i=0; i<temp_seg_size; i++) {
        if ((r0 > this.segments[i].range0 && r0 < this.segments[i].range1) ||
            (r1 > this.segments[i].range0 && r1 < this.segments[i].range1) ||
            (r0 == this.segments[i].range0 && r1 > this.segments[i].range1) ||
            (r1 == this.segments[i].range1 && r0 < this.segments[i].range0)) {
          this.rangErrMsg='格位資料設定錯誤!'
          return;
        }
      }

      //for (let i=0; i<temp_seg_size; i++) {
      //  if (this.segments[i].range0 == r0  && this.segments[i].range1 == r1)
      //    console
//
      //}

      //檢查是否power off Led
      let l1=this.segments.length
      this.segments = this.segments.filter(function( obj ) {
        return (obj.range0 != r0  && obj.range1 != r1);
      });

      if (this.segments.length == l1) {
        console.log("toggle hello");
        let obj= {
          id: this.init_id,
          //text:this.init_id.toString(),
          size: temp_size,
          type: 'station1',
          range0: this.range[0],
          range1: this.range[1],
        }
        this.segments.push(obj);

        this.init_id++;
      } else {
        //this.init_id=0;
        for (var i in this.segments) {
            //this.init_id++;
            this.segments[i].id=i+1;
            //this.segments[i].text=this.segments[i].id.toString();
        }
      }

      this.isShow = true;

      for (let i=this.range[0]-1; i<this.range[1]; i++) {
        let dot = document.getElementById("light_" + i);
        this.Leds[i]= !this.Leds[i];
        let temp_togg= this.Leds[i] ? (dot.className += " on") : (dot.className = "dot");
      }


/*
const newArr = this.segments.map(obj => {
  if (this.range[0] == this.segments[i].range0 && this.range[1] == this.segments[i].range1) {
    return {...obj, name: 'Alfred'};
  }

  return obj;
});

*/

   },

   clickChip(e) {
      console.log("hello click", e);
      this.action=true;
   },
   leaveChip(e) {
      console.log("hello leave", e);
      this.action=false;
   },



    poweroffLed(r0, r1) {
      console.log("hello poweroffLed")
      for (let i=r0-1; i<r1; i++) {
        let dot = document.getElementById("light_" + i);
        this.Leds[i]= !this.Leds[i];
        let temp_togg= this.Leds[i] ? (dot.className += " on") : (dot.className = "dot");
      }

      this.segments = this.segments.filter(function( obj ) {
        return !(obj.range0==r0 && obj.range1==r1);
      });
      let temp_id=1;
      for (const obj of this.segments) {
        obj.id = temp_id;
        //obj.text=temp_id.toString(),
        temp_id++;
      }
      this.init_id=temp_id;
      this.isShow = (this.segments.length !=0) ? true:false;
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
.v22 {
  display: flex;
  height: 22px;
}

.vl {
  border-left: 2px solid green;
  height: 22px;
  position: relative;
  left: 12px
}

.temp_text {
  position: relative;
  //left: 50px;
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

.dnrSelected {
  background: #5FBDEC !important;
  background-color: #5FBDEC !important;
}

small.msgErr {
  font-size: 80%;
  color: red;
  margin-top: -10px;
}

/*  ===  */

span[hover-tooltip] {
  //position: relative;
  cursor: default;
}
span[hover-tooltip]:hover::before {
  content: attr(hover-tooltip);
  font-size: 14px;
  text-align: center;
  position: absolute;
  display: block;
  left: 50%;
  min-width: 150px;
  max-width: 200px;
  bottom: calc(100% + 10px);
  transform: translate(-50%);
  animation: fade-in 300ms ease;
  background: #272727;
  border-radius: 4px;
  padding: 10px;
  color: #ffffff;
  z-index: 1;
}
span[hover-tooltip]:hover::after {
  content: "";
  position: absolute;
  display: block;
  left: 50%;
  width: 0;
  height: 0;
  bottom: calc(100% + 6px);
  margin-left: -3px;
  border: 1px solid black;
  border-color: #272727 transparent transparent transparent;
  border-width: 4px 6px 0;
  animation: fade-in 300ms ease;
  z-index: 1;
}
span[hover-tooltip][tooltip-position=bottom]:hover::before {
  bottom: auto;
  top: calc(100% + 10px);
}
span[hover-tooltip][tooltip-position=bottom]:hover::after {
  bottom: auto;
  top: calc(100% + 6px);
  border-color: transparent transparent #272727;
  border-width: 0 6px 4px;
}

@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

</style>