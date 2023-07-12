<template>
<v-app>
  <MyBarcode :barcode_data="regFields" @pressPrint="onPressPrint"></MyBarcode>
</v-app>
</template>

<script>
import axios from 'axios';

import Common from '../mixin/common.js'

import MyBarcode from './BarCodeRePrintTag.vue';

export default {
  name: 'RenderBarCodeRePrintTag',

  mixins: [Common],

  components: {
    MyBarcode,
  },

  //props: [
  //  'sidebar', 'drawer'
  //],
  props: {
    sidebar: {
      type: Array,
      required: true,
    },
    drawer: {
      type: Boolean,
      required: true,
    },
    alpha: {
      type: String,
      required: true,
    }
  },

  data () {
    return {
      fields: [],
      show_barcode: false,
      regFields: [],
      waiting_in_total_tags: 0,

      last_alpha_records: [],
      load_SingleTable_ok: false,
    };
  },

  watch: {
    sidebar(val) {
      this.fields.push(val);
      console.log("sidebar:", val);
      console.log("fields:", this.fields);
    },

    drawer(val) {
      if (val) {
        this.show_barcode=val;
        console.log("drawer ok!");
        this.formField();
      }
      console.log("drawer:", val);
    },

    //codeInfo(val) {
    //  this.fields.push(val);
    //  console.log("codeInfo:", val);
    //},
    load_SingleTable_ok(val) {
      console.log("load_SingleTable_ok: ", val);

      if (val) {
        //this.desserts = Object.assign([], this.temp_desserts);

        this.load_SingleTable_ok=false;
        console.log("b this.regFields: ", this.regFields);
        this.assignLastAlphaForStockIn();
        console.log("a this.regFields: ", this.regFields);
      }
    },


  },

  created () {
    console.log("RenderBarCodeRePrintTag, created()...");
  },

  mounted() {
    console.log("RenderBarCodeRePrintTag, mounted()...");
  },

  computed: {

  },

  methods: {
    formField() {
      console.log("RenderBarCodeRePrintTag, formField()...");

      this.regFields=[];
      let temp_len=this.fields.length;
      console.log("temp_len: ", temp_len);
      for (let i=0; i < temp_len; i++) {
        console.log("temp_len, type: ", typeof(this.fields[temp_len-1][i]), this.fields[temp_len-1][i]);
        if (typeof(this.fields[temp_len-1][i]) !="undefined") {
          //console.log("RenderRePrintTag, tag obj: ", 'stockInTag_cnt' in this.fields[temp_len-1][i]);
          if ('stockInTag_cnt' in this.fields[temp_len-1][i]) {   //入庫
            let temp_tags=this.fields[temp_len-1][i].stockInTag_cnt;
            for (let j=0; j < temp_tags; j++) {
              this.fields[temp_len-1][i]['stockInTag_cnt']=1;
              //this.fields[temp_len-1][i]['stockInTag_alpha']=this.alpha;  //2023-01-03 add
              this.regFields.push(this.fields[temp_len-1][i]);
            }
          } else {   //出庫
            let temp_tags=this.fields[temp_len-1][i].stockOutTag_cnt;
            for (let j=0; j < temp_tags; j++) {
              this.fields[temp_len-1][i]['stockOutTag_cnt']=1;
              //this.fields[temp_len-1][i]['stockOutTag_alpha']=this.alpha;  //2023-01-03 add
              this.regFields.push(this.fields[temp_len-1][i]);
            }
          }
          //console.log("RenderBarCodeRePrintTag, this.alpha: ", this.alpha)
        }
      }
      console.log("this.regFields: ", this.regFields);


      this.waiting_in_total_tags=this.regFields.length;

      console.log("this.regFields: ", this.regFields);
      /*
      let uniqueRegFields = [...new Set(this.regFields)];
      console.log("uniqueRegFields: ", uniqueRegFields);
      this.load_SingleTable_ok=false;
      this.getLastAlphaForUniqueStockIn(uniqueRegFields);
      */
      //this.$emit('waitTags', this.waiting_in_total_tags);
    },
    /*
    getLastAlphaForUniqueStockIn(uniqueArray) {
      console.log("getLastBatchAlphaForStockIn, Axios post data...", uniqueArray);

      const path = '/getLastAlphaForUniqueStockIn';
      let payload = Object.assign([], uniqueArray);
      axios.post(path, payload)
      .then(res => {
        console.log("getLastBatchAlphaForStockIn, GET ok.....", res.data.outputs);
        //this.last_status=res.data.status;
        this.last_alpha_records=res.data.outputs;
        this.tosterOK = false;  //false: 關閉錯誤訊息畫面
        this.load_SingleTable_ok=true;
      })
      .catch((error) => {
        console.error(error);
        this.tosterOK = true;   //true: 顯示錯誤訊息畫面
        this.load_SingleTable_ok=false;
      });
    },

    assignLastAlphaForStockIn() {
      let temp1_len=this.last_alpha_records.length;
      let temp2_len=this.regFields.length;
      for (let i=0; i<temp1_len; i++) {
        for (let j=0; j<temp2_len; j++) {
          if (this.regFields[j].stockInTag_reagID==this.last_alpha_records[i].reagent_id)
            this.regFields[j].stockInTag_alpha=this.last_alpha_records[i].lastAlpha;
        }
      }
    },
    */
    onPressPrint(value) {
      this.is_print_OK=value;
      if (this.is_print_OK)
        this.$emit('waitTags', this.waiting_in_total_tags);
    },

    /*
    addFormElement(type) {
      this.isShow = true;
      if (this.isShow) {
        this.fields.push({
          'type': type,
          id: this.count++
        });
        this.isPrint = true;
      }
    },
    */
  },
}
</script>

<style scoped>

</style>