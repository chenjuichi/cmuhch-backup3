#include <stdint.h>
#include <FastLED.h>
//#include <Arduino.h>
#include <ESP8266TrueRandom.h>
#include <ESP8266WiFi.h>
//#include <ESP8266Ping.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

//定義靜態變數
static const uint8_t D0 = 16;
static const uint8_t D1 = 5;
static const uint8_t D2 = 4;
static const uint8_t D3 = 0;
static const uint8_t D4 = 2;
static const uint8_t D5 = 14;
// ----------

//定義常數
#define NUM_LEDS 30     //總數量
#define LED_TYPE WS2812 // 型號
#define COLOR_ORDER GRB // RGB LED 燈珠排列順序

// MQTT
#define MQTT_MAX_PACKET_SIZE 512
#define MQTT_KEEPALIVE 10800
// ----------

//wifi的設定資料(global var)
//const char* ssid = "ZH";
//const char* password = "-pmc4394";
//const char* mqttServer = "192.168.32.178";

const char* ssid = "staff-Dev";
const char* password = "cmuhch1357";
const char* mqttServer = "10.108.249.100";

//const char* ssid = "HITRON-CD80";
//const char* password = "jchen8241";
//const char* mqttServer = "192.168.0.12";

//const char* ssid = "AndroidAPEFA6";
//const char* password = "ajgp6664";
//const char* mqttServer = "192.168.43.117";

//const char* ssid = "HACD7797";
//const char* password = "77974590pmc";
//const char* mqttServer = "192.168.50.203";

// Set your Static IP address
IPAddress local_IP(10,108,249,103);
// Set your Gateway IP address
IPAddress gateway(10,108,249,254);

IPAddress subnet(255,255,255,0);
IPAddress primaryDNS(10,108,6,238);

unsigned long previousMillis = 0;
unsigned long previousMillis_LED = 0;
unsigned long previousMillis_MQTT = 0;

//unsigned long interval = 30000;
unsigned long interval = 5000;
unsigned long intervalLED = 500;
unsigned long intervalMQTT = 2000;

//UUIDs in binary form are 16 bytes long
byte uuidNumber[16];

boolean ledState = false;
// ----------

//Led燈條的設定資料(global var)
const uint8_t pin[] = {D0, D1, D2, D3, D4, D5};
//const String r = "r";
//const String g = "g";
//const String b = "b";

//Led燈條的變數(global var)
CRGB leds1[NUM_LEDS]; // 建立光帶leds
CRGB leds2[NUM_LEDS]; //
CRGB leds3[NUM_LEDS]; //
CRGB leds4[NUM_LEDS]; //
CRGB leds5[NUM_LEDS]; //

CRGB RGBcolor(0, 0, 0); // RGBcolor（红色数值，绿色数值，蓝色数值）
CRGB RGBcolor_000(0, 0, 0);

// global var
unsigned long tymNow;
int num2nds;

boolean ledFlash = false;

int stripArray1[NUM_LEDS];
int stripArray2[NUM_LEDS];
int stripArray3[NUM_LEDS];
int stripArray4[NUM_LEDS];
int stripArray5[NUM_LEDS];

int stripIndex=0;
int myLayout, myBegin, myEnd, mySegments;
//String temp_color[] = {"r", "g", "b", "off"};
String str_msg= String("off");

char* led_status =" LedOff";
// ----------

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// 收到信息後的CallBack函數
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message Received from [");
  Serial.print(topic);                //顯示MQTT的topic
  Serial.print("] , value: ");

  char message[10]={0x00};
  for (int i = 0; i < length; i++) {
    message[i]=(char)payload[i];
    Serial.print((char)payload[i]);   //顯示MQTT的topic value(json資料形式)
  }
  message[length]=0x00;
  Serial.println("");
  Serial.print("Message Length(Bytes) ");
  Serial.println(length);

  StaticJsonDocument <256> doc;
  deserializeJson(doc, payload);
  const char* ledStrip_layout = doc["Layout"];  //解Layout的JSON序列化(Serialize)資料
  const char* ledStrip_begin = doc["Begin"];    //解Begin的JSON序列化(Serialize)資料
  const char* ledStrip_end = doc["End"];        //解End的JSON序列化(Serialize)資料
  const char* ledStrip_msg = doc["Msg"];        //解Msg的JSON序列化(Serialize)資料
  //顯示json資料
  Serial.print("ledStrip_Layout: ");
  Serial.print(ledStrip_layout);

  Serial.print("  ledStrip_Begin: ");
  Serial.print(ledStrip_begin);

  Serial.print("  ledStrip_End: ");
  Serial.print(ledStrip_end);

  Serial.print("  ledStrip_Msg: ");
  Serial.print(ledStrip_msg);
  Serial.print("  ");

  myLayout = atoi(ledStrip_layout);
  myBegin = atoi(ledStrip_begin);
  myEnd = atoi(ledStrip_end);
  mySegments = myEnd - myBegin + 1;
  switch(myLayout){
    case 1:
      Serial.print("ledStrip_Layout 1: ");
      Serial.print(ledStrip_layout);
      Serial.print(" Begin: ");
      Serial.print(myBegin);
      Serial.print(" Segments: ");
      Serial.print(mySegments);      
      break;
    case 2:
      Serial.print("ledStrip_Layout 2: ");
      Serial.print(ledStrip_layout);
      Serial.print(" Begin: ");
      Serial.print(myBegin);
      Serial.print(" Segments: ");
      Serial.print(mySegments);       
      break;
    case 3:
      Serial.print("ledStrip_Layout 3: ");
      Serial.print(ledStrip_layout);
      Serial.print(" Begin: ");
      Serial.print(myBegin);
      Serial.print(" Segments: ");
      Serial.print(mySegments);       
      break;
    case 4:
      Serial.print("ledStrip_Layout 4: ");
      Serial.print(ledStrip_layout);
      Serial.print(" Begin: ");
      Serial.print(myBegin);
      Serial.print(" Segments: ");
      Serial.print(mySegments);       
      break; 
    case 5:
      Serial.print("ledStrip_Layout 5: ");
      Serial.print(ledStrip_layout);
      Serial.print(" Begin: ");
      Serial.print(myBegin);
      Serial.print(" Segments: ");
      Serial.print(mySegments);
    default:  //0
      Serial.print("ledStrip_Layout All ");
      Serial.print(ledStrip_layout);
      Serial.print(" Begin: ");
      Serial.print(myBegin);
      Serial.print(" Segments: ");
      Serial.print(mySegments);                                     
  }
  
  str_msg= String(ledStrip_msg);
  if (str_msg.equals("on")) {           // 如果收到的訊息為"on"
    //digitalWrite(LED, LOW);           // 點亮LED
    //Serial.println("station3/Layout1/Led5 LED ON");
    ledFlash = false;
    String strLed(" station3/");        // 初始化字串
    strLed = strLed + ledStrip_layout+"/" + ledStrip_begin + "/" + ledStrip_end + " LED_ON";
    
    Serial.println(strLed);
    led_status =" LedOn";
    
    strip_color_on(); //power on指定燈條位置    
  } else if (str_msg.equals("off")){    // 如果收到的訊息為"off"                            
    //digitalWrite(LED, HIGH);          // 點滅LED
    //Serial.println("station3/Layout1/Led5 LED OFF");
    ledFlash = false;
    String strLed(" station3/");        // 初始化字串
    strLed = strLed + ledStrip_layout + "/" + ledStrip_begin + "/" + ledStrip_end + " LED_OFF";
    Serial.println(strLed);
    led_status =" LedOff";

    strip_color_off();  //power off指定燈條位置 
  } else if  (str_msg.equals("flash")){
    String strLed(" station3/");        // 初始化字串
    strLed = strLed + ledStrip_layout + "/" + ledStrip_begin + "/" + ledStrip_end + " LED_FLASH";
    Serial.println(strLed);
    led_status =" LedFlash";
    ledFlash = true;
  }
}

void setup() { 
  pinMode(D0, OUTPUT);     // 設定LED port為輸出模式
  digitalWrite(D0, LOW);   // 設定LED on
  
  init_led_output();          // 初始化燈條
  delay (500);
  //leds_all_off();             //關閉全部leds
  //delay (500);
  Long_2Short_Test("b");  
    
  Serial.begin(9600);         // 設定serial monitor 通訊速率
 
  //WiFi.mode(WIFI_STA);        // 設定ESP8266工作模式為無線終端模式
  // Configures static IP address
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS)) {
    Serial.println("STA Failed to configure");
  }  
    
  connectWifi();              // 連線WiFi
  
  mqttClient.setServer(mqttServer, 1883);   // 設定MQTT服務和port  
  mqttClient.setCallback(mqttCallback);     // 設定MQTT訂閱callback
  
  connectMQTTserver();                      // 連線MQTT服務
}

void loop() {
  boolean LoopReturn;
  unsigned long currentMillis = millis();       //print the Wi-Fi status every 5 seconds
  unsigned long currentMillis_LED =  millis();
  unsigned long currentMillis_MQTT =  millis();

  //LED 閃爍
  if (currentMillis_LED - previousMillis_LED >= intervalLED) {
    ledState=!ledState;
    if (ledState) {
     digitalWrite(D0, LOW); 
    } else {
      digitalWrite(D0, HIGH);
    }
    previousMillis_LED = currentMillis_LED;    
  }
  
  //偵測斷線, 重新連線
  if ((WiFi.status() != WL_CONNECTED) && (currentMillis - previousMillis >= interval)) {
    
   digitalWrite(D0, HIGH);  // 設定LED off
   delay (2000);
   
   Serial.println("Reconnecting to WIFI...");
   previousMillis = currentMillis;
   ESP.restart();       //Alternatively, restart your board
   //WiFi.disconnect();
   //WiFi.reconnect();   
  }
  
  //偵測MQTT
  if (currentMillis_MQTT - previousMillis_MQTT >= intervalMQTT) {
   ESP8266TrueRandom.uuid(uuidNumber); // Generate a new UUID
   String uuidStr = ESP8266TrueRandom.uuidToString(uuidNumber); 
   String myStr="hello station3, The UUID number is " + uuidStr;
   
   mqttClient.publish("on_line", myStr.c_str());
   //Serial.println("MQTT station3 on line...");
    
   previousMillis_MQTT = currentMillis_MQTT;
   //ESP.restart();       //Alternatively, restart your board    
  }  

  //偵測入庫/出庫按鍵   
  if (ledFlash) {
    tymNow = millis();
    num2nds = (tymNow/1000);
    
    String strLedFlash("Station3 led flash ");        // 初始化字串
    
    if(num2nds % 2 == 0) {  
      strLedFlash = strLedFlash + "on, layout: " + myLayout + " (begin: " + myBegin + " , end: " + myEnd;
      Serial.println(strLedFlash);      
      for (int j = myBegin-1; j < myBegin-1 + mySegments; j++){
        switch(myLayout){
          case 1:
            leds1[j] = CRGB::Blue;
            FastLED.show();
            delay (10);
            break;
          case 2:
            leds2[j] = CRGB::Blue;
            FastLED.show();
            delay (10);
            break;
          case 3:
            leds3[j] = CRGB::Blue;
            FastLED.show();
            delay (10);
            break;
          case 4:
            leds4[j] = CRGB::Blue;
            FastLED.show();
            delay (10);
            break;
          default: //layout 5
            leds5[j] = CRGB::Blue;
            FastLED.show();
            delay (10);
            break;
        } //end switch check                
      } //end for loop  
    } //end check num2nds
    
    if(num2nds % 2 > 0) {
      strLedFlash = strLedFlash + "off, layout: " + myLayout + " (begin: " + myBegin + " , end: " + myEnd;
      Serial.println(strLedFlash);      
      for (int j = myBegin-1; j < myBegin-1 + mySegments; j++){
        switch(myLayout){
          case 1:
            leds1[j] = CRGB::Black;
            FastLED.show();
            delay (10);       
            break;
          case 2:
            leds2[j] = CRGB::Black;
            FastLED.show();
            delay (10);       
            break;
          case 3:
            leds3[j] = CRGB::Black;
            FastLED.show();
            delay (10);       
            break;    
          case 4:
            leds4[j] = CRGB::Black;
            FastLED.show();
            delay (10);       
            break;    
          default: //layout 5 
            leds5[j] = CRGB::Black;
            FastLED.show();
            delay (10);       
            break;   
        } //end switch check          
      } //end for loop          
    } //end check num2nds 
  } //end check ledFlash
  
  delay(200);

  if (!mqttClient.connected()) {
    reconnect();
  } 
  LoopReturn=mqttClient.loop();

  if (LoopReturn) {
    //Serial.println("the client is still connected...");  
  } else {
    Serial.println("the client is no longer connected..."); 
  }  
}

// ESP8266連線wifi
void connectWifi(){ 
  WiFi.begin(ssid, password);
  //WiFi.begin(ssid);     //if no password  
 
  //等待WiFi連線,成功連線後輸出成功訊息
  Serial.print("Waitting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi Connected!");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());   // You can get IP address assigned to ESP8266    
}

// 連線MQTT服務并訂閱信息
void connectMQTTserver(){
  // 客户端ID
  int stateCode;
  String clientId = "CLIENT-esp8266-3";
 
  // 連線MQTT服務
  if (mqttClient.connect(clientId.c_str(), NULL, NULL)) { 
    Serial.println("MQTT Server Connected.");
    Serial.println("Server Address: ");
    Serial.println(mqttServer);
    Serial.println("ClientId: ");
    Serial.println(clientId);
    subscribeTopic(); // 訂閱指定主题
  } else {
    Serial.print("MQTT Server Connect Failed. Client State:");
    stateCode=mqttClient.state();
    Serial.println(stateCode);
    delay(1000);
  }   
}

// 訂閱指定主题
void subscribeTopic(){ 
  String topicString = "station3";
  char subTopic[topicString.length() + 1];  
  strcpy(subTopic, topicString.c_str());
  
  // 確認訂閱主题是否訂閱成功
  if(mqttClient.subscribe(subTopic)){
    Serial.println("Subscrib Topic: ");
    Serial.println(subTopic);
  } else {
    Serial.print("Subscribe Fail...");
  }  
}

// MQTT重新連線
void reconnect() {
  // Loop until we're reconnected
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "CLIENT-esp8266-3-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (mqttClient.connect(clientId.c_str(), NULL, NULL)) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      mqttClient.publish("reconnect", "hello, station3...");
      // ... and resubscribe
      mqttClient.subscribe("reconnect");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    } //end if
  } //end while
}

//初始化燈條,輸出腳位 D1~D5 對應 leds1~leds5
void init_led_output(){
  LEDS.addLeds<LED_TYPE, D1, COLOR_ORDER>(leds1, NUM_LEDS);
  LEDS.addLeds<LED_TYPE, D2, COLOR_ORDER>(leds2, NUM_LEDS);
  LEDS.addLeds<LED_TYPE, D3, COLOR_ORDER>(leds3, NUM_LEDS);
  LEDS.addLeds<LED_TYPE, D4, COLOR_ORDER>(leds4, NUM_LEDS);
  LEDS.addLeds<LED_TYPE, D5, COLOR_ORDER>(leds5, NUM_LEDS);
  delay(10);
}

void strip_color_on(){
  switch(myLayout){
    case 1:
       strip_section_on(leds1, stripArray1);
       break;
    case 2:
       strip_section_on(leds2, stripArray2);
       break;
    case 3:
       strip_section_on(leds3, stripArray3);
       break;
    case 4:
       strip_section_on(leds4, stripArray4);
       break;       
    case 5:
       strip_section_on(leds5, stripArray5);
       break;
    default:  //0
       leds_all_on("b", 128);             //開啟全部leds
       delay (500);  
       break;          
  }  
}

void strip_color_off(){
  switch(myLayout){
    case 1:
       strip_section_off(leds1, stripArray1);
       break;
    case 2:
       strip_section_off(leds2, stripArray2);
       break;
    case 3:
       strip_section_off(leds3, stripArray3);
       break;
    case 4:
       strip_section_off(leds4, stripArray4);
       break;       
    case 5:
       strip_section_off(leds5, stripArray5);
       break;
    default:  //0
       leds_all_off();             //關閉全部leds
       delay (500);  
       break;         
  }  
}
/*
void copy(int* src, int* dst, int len) {
  memcpy(dst, src, sizeof(src[0])*len);
}
*/

/*
bool pingTest(){
  Serial.print("Pinging host : "); Serial.println(Remote_Host);
  if(Ping.ping(Remote_Host, 2)) { // Ping the remote host with two ping requests
    Serial.println("Success!!");
    return true;
  } else {
    Serial.println("Error :(");
    return false;
  };
};
*/

void strip_section_on(CRGB* tempLeds, int* tempArray){
  boolean myTest=false;
  
  //檢查array內是否有值, true: 有
  for (int i=0; i<NUM_LEDS; i=i+2) {
    if (myBegin-1 == stripArray1[i] && mySegments == stripArray1[i+1]) {
      myTest=true;
      //Serial.println("on STRIP1: " +String(i)+" "+ String(stripArray1[i])+" "+String(tempArray[i+1]));        
      break;
    }
  }
  
  //Serial.println("on STRIP2: "+String(myTest));
  
  //新值加入
  if (myTest==false) {
    //Serial.println("on STRIP3: "+String(stripIndex));
    tempArray[stripIndex]=myBegin-1;
    stripIndex++;
    tempArray[stripIndex]=mySegments;
    stripIndex++;
    //Serial.println("on STRIP4: "+String(tempArray[stripIndex-2])+" "+String(tempArray[stripIndex-1]));
  }
 
  for (int i = 0; i < NUM_LEDS; i=i+2) {
    if (tempArray[i] !=0 || tempArray[i+1] !=0) {      
      for (int j = tempArray[i]; j < tempArray[i]+tempArray[i+1]; j++){
        tempLeds[j] = CRGB::Green;
        FastLED.show();
        delay (10);
      }
    }
  }
}

void strip_section_off(CRGB* tempLeds, int* tempArray){
  
  //檢查array內是否有值, true: 有
  for (int i=0; i<NUM_LEDS; i=i+2) {
     if (myBegin-1 == tempArray[i] && mySegments == tempArray[i+1]) {
       //Serial.println("off STRIP11: " +String(i)+" "+ String(tempArray[i])+" "+String(tempArray[i+1]));  
       for (int j = tempArray[i]; j < tempArray[i]+tempArray[i+1]; j++){
         tempLeds[j] = CRGB::Black;
         FastLED.show();
         delay (10);
       }
       tempArray[i]=0;   
       tempArray[i+1]=0;
       //Serial.println("off STRIP22: " +String(i)+" "+ String(tempArray[i])+" "+String(tempArray[i+1]));          
       break;
     }
  }
}

void Long_2Short_Test(String led_color) {
  leds_all_off();                   //關閉全部leds
  delay (100);
    
  leds_all_on(led_color, 128);      //開啟全部leds
  delay (2000);
  leds_all_off();                   //關閉全部leds
  delay (500);  

  leds_all_on(led_color, 128);      //開啟全部leds
  delay (500);
  leds_all_off();                   //關閉全部leds
  delay (500);
  leds_all_on(led_color, 128);      //開啟全部leds
  delay (500);
  leds_all_off();                   //關閉全部leds
  delay (500);     
}

//關閉全部leds
void leds_all_off() {
  Serial.println("leds_all_off...");
   
  fill_solid(leds1 + 0, NUM_LEDS, RGBcolor_000);
  fill_solid(leds2 + 0, NUM_LEDS, RGBcolor_000);
  fill_solid(leds3 + 0, NUM_LEDS, RGBcolor_000);
  fill_solid(leds4 + 0, NUM_LEDS, RGBcolor_000);
  fill_solid(leds5 + 0, NUM_LEDS, RGBcolor_000);
  FastLED.show();
}

//開啟全部leds
void leds_all_on(String color_val, uint8_t max_bright) {
  Serial.println("leds_all_on...");
  
  leds_color_set(color_val);                    //顏色：r,g,b  
  FastLED.setBrightness(max_bright);            //亮度:0~255  
  fill_solid(leds1 + 0, NUM_LEDS, RGBcolor);
  fill_solid(leds2 + 0, NUM_LEDS, RGBcolor);
  fill_solid(leds3 + 0, NUM_LEDS, RGBcolor);
  fill_solid(leds4 + 0, NUM_LEDS, RGBcolor);
  fill_solid(leds5 + 0, NUM_LEDS, RGBcolor);    
  FastLED.show();
}

//設定Leds顏色
void leds_color_set(String color_val) {
  RGBcolor.r = 0;
  RGBcolor.g = 0;
  RGBcolor.b = 0;

  if (color_val == "r"){
    RGBcolor.r = 255;
  } else if (color_val == "g"){
    RGBcolor.g = 255;
  } else if (color_val == "b"){
    RGBcolor.b = 255;
  }
}
