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
    },
    //2024-03-27 add
    flag: {
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
      console.log("watch...")
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
    console.log("RenderBarCodeRePrintTag, created()..., sidebar: ", this.sidebar);
  },

  mounted() {
    console.log("RenderBarCodeRePrintTag, mounted()...");
  },

  computed: {

  },

  methods: {
    formField() {
      console.log("RenderBarCodeRePrintTag, formField()...", this.fields);

      this.regFields=[];

      let temp_len=this.fields.length;
      let temp_len2=this.fields[temp_len-1].length;
      let temp_len3=temp_len-1;
      let temp_len4=temp_len2-1;  //2024-03-27 add
      console.log("formField(), temp_len, temp_len2, flag: ", temp_len, temp_len2, this.flag);
      for (let ttt=0; ttt < temp_len; ttt++)
        console.log("for loop: ", this.fields[ttt]);

      console.log("this.fields, this.fields[temp_len3]: ", this.fields, this.fields[temp_len3]);
      // 2024-01-11 modify this for statement
      //for (let i=0; i < temp_len; i++) {
      for (let i=0; i < temp_len2; i++) {
      // end
        // 2024-01-11 modify this if statement
        //if (typeof(this.fields[temp_len-1][i]) !="undefined") {

        console.log("temp_len2, i, this.fields[temp_len3][i]: ", temp_len2,  i, this.fields[temp_len3][i]);

        if (typeof(this.fields[temp_len3][i]) !="undefined") {
        // end
          // 2024-01-11 modify this if statement
          //if (this.fields[temp_len-1][i].stockInTag_rePrint=='入庫') {  //2023-08-08 modify
          if (this.flag=='stockin' || (this.flag=='' && this.fields[temp_len3][i].stockInTag_rePrint=='入庫')) {
          // end
            // 2024-01-11 modify the following line
            //let temp_tags=this.fields[temp_len-1][i].stockInTag_cnt;
            let temp_tags=this.fields[temp_len3][i].stockInTag_cnt;
            // end
            console.log("入庫, temp_tags: ", temp_tags)
            for (let j=0; j < temp_tags; j++) {
              // 2024-01-11 modify the following block
              /*
              this.fields[temp_len-1][i]['stockInTag_cnt']=1;
              this.fields[temp_len-1][i]['stockInTag_rePrint']='入庫';  //2023-08-08 add
              //this.fields[temp_len-1][i]['stockInTag_alpha']=this.alpha;  //2023-01-03 add
              this.regFields.push(this.fields[temp_len-1][i]);
              */
              this.fields[temp_len3][i]['stockInTag_cnt']=1;
              this.fields[temp_len3][i]['stockInTag_rePrint']='入庫';
              this.regFields.push(this.fields[temp_len3][i]);
              // end
            }
          } else {   //出庫
            // 2024-01-11 modify the following block
            /*
            let temp_tags=this.fields[temp_len-1][i].stockOutTag_cnt;
            if (typeof(temp_tags) == "undefined") {
              temp_tags=this.fields[temp_len-1][i].stockInTag_cnt;
            }
            console.log("出庫, temp_tags: ", temp_tags)
            for (let j=0; j < temp_tags; j++) {
              this.fields[temp_len-1][i]['stockOutTag_cnt']=1;
              this.fields[temp_len-1][i]['stockInTag_rePrint']='出庫';  //2023-08-08 add
              //this.fields[temp_len-1][i]['stockOutTag_alpha']=this.alpha;  //2023-01-03 add
              this.regFields.push(this.fields[temp_len-1][i]);
            }
            */
            let temp_tags=this.fields[temp_len3][i].stockOutTag_cnt;
            if (typeof(temp_tags) == "undefined") {
              temp_tags=this.fields[temp_len3][i].stockInTag_cnt;
            }
            console.log("出庫, temp_tags: ", temp_tags)
            for (let j=0; j < temp_tags; j++) {
              this.fields[temp_len3][i]['stockOutTag_cnt']=1;
              this.fields[temp_len3][i]['stockInTag_rePrint']='出庫';
              this.regFields.push(this.fields[temp_len3][i]);
            }
            // end
          }
        }
      }
      console.log("this.regFields: ", this.regFields);

      this.waiting_in_total_tags=this.regFields.length;
      console.log("this.regFields: ", this.regFields);
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