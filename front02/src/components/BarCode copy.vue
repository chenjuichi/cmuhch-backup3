<template>
  <v-app>
    <v-container class="scroll-y">
        <v-layout align-center justify-center>
          <v-flex xs12>
            <!--<v-col class="text-right">-->
              <!--
              <v-btn color="primary" dark class="mb-2" @click="printBarcode">
                <v-icon left dark>mdi-keyboard-return</v-icon>返回
              </v-btn>
              &nbsp;&nbsp;
              -->
              <v-btn color="primary" dark class="mb-2" @click="printBarcode">
                <v-icon left dark>mdi-printer</v-icon>列印
              </v-btn>
            <!--</v-col>-->
            <v-btn v-scroll="onScroll" v-show="fab" fab dark fixed bottom right color="primary"
              @click="toTop"  
            >            
              <v-icon>keyboard_arrow_up</v-icon>
            </v-btn>

                    <!--<v-card>-->
            <!--<v-row align="center" justify="center">-->
           
              <v-card align="center" justify="center" width="50vw">
                <div v-for="(field, index) in barcode_data" :key="index">
                  <div>中國醫藥大學新竹附設醫院</div>
                  <barcode :value="field.stockInTag_reagID">
                  Show this if the rendering fails.
                  </barcode>
                  <span>入庫人員: {{ field.stockInTag_Employer }}</span>
                  <v-spacer></v-spacer>
                </div>  
                <!--
                <div>中國醫藥大學新竹附設醫院</div>
                <barcode :value="1234567890" lineColor="#007bff"></barcode>
                <span>入庫人員: {{}}</span>
                -->
              </v-card>
            
            <!--</v-row>-->
                    <!--</v-card>-->
          </v-flex>
        </v-layout>
    </v-container>
  </v-app>
</template>  

<script>
import VueBarcode from 'vue-barcode';

export default {
  //el: "#app",
  name: 'BarCode',

  components: {
    'barcode': VueBarcode,
  },

  props: ['barcode_data'],

  mounted() {
    console.log("BarCode, mounted()...");
    //this.navDrawerContent = 
    //this.$refs['myNavDrawer'].$el.querySelector('div.v-navigation-drawer__content');
  },

  created() {
    console.log("BarCode, created()...");
    
  },

  computed: {

  },

  data() {
    return {
      fab: false,
      //barcodeValue: 'A12345',
      //barCode_ReagID: '',
      //barCode_Employer: '',
      navDrawerContent: null,


    };
  },

  methods: {
    printBarcode() {
      console.log("click, printBarcode()...");      
      
    },

    onScroll (e) {
      console.log("onScroll 1....", e, typeof window);      
      if (typeof window === 'undefined') return
      const top = window.pageYOffset || e.target.scrollTop || 0
      this.fab = top > 20
    },

    toTop () {
      //this.$vuetify.goTo(0)
      this.$vuetify.goTo(0)
      //this.$vuetify.goTo(this.$refs.actions, { container: this.$refs.card });
    }
  },
}
</script>

<style scoped>

</style>