<template>
<v-app>   
  <v-container fluid class="pa-1">
    
    <div id="printMe" v-if="isShow" class="barcode-layout">
      <!--
      <div v-for="field in qrTags" :key="field.work_id">
        <PrintQRCode :stack="field"></PrintQRCode>
      </div>
      -->                    
    </div>
    <v-row align="center" justify="space-around">
      <v-col cols="12" md="6">
        <v-btn v-on:click="addFormElement('BarCode')" v-show="!isPrint">
          <v-icon left>mdi-qrcode</v-icon>
          {{ $t('FORKIN.ShowQRCode') }}
        </v-btn>
        
        <v-btn v-print="printObj" :class="{'disable-events': !isPrint}">

          <v-icon left>mdi-printer</v-icon>
          {{ $t('FORKIN.PrintQRCode') }}
        </v-btn>        
      </v-col>
    </v-row>
  </v-container>
</v-app>
</template>

<script>
import MyBarcode from '../components/BarCode.vue';
//import print from 'vue-print-nb';

export default {
  name: 'RenderBarCode',

  components: {
    MyBarcode, 
    //print,
  },

  created () {
    console.log("RenderBarCode, created()...");
  },

  mounted() {
    console.log("RenderBarCode, mounted()...");    
  },

  data: () => ({
    isShow: false,    
    isPrint: false,
    printObj: {
      id: "printMe",
      preview: true,
      previewTitle: "列 印 預 覽",
      popTitle: "cmu-hch print",
      extraCss: "",
      previewPrintBtnLabel: "列 印",
      previewBeforeOpenCallback (vue) {
        console.log('正在下載預覽窗口')
      },
      previewOpenCallback (vue) {
        console.log('已經完成下載預覽窗口')
      },
      beforeOpenCallback (vue) {
        console.log('打開之前')
      },
      openCallback (vue) {
        console.log('执行了打印')
      },
      closeCallback (vue) {
        console.log('關閉了列印工具')
      },
    },
    fields: [],
  }),
  methods: {
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
  },
}
</script>