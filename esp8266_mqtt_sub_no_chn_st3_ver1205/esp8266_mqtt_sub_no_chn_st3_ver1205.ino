// ----------
// com: port 3, driver cp210x
// Additional Boards Manager URLs: http://arduino.esp8266.com/stable/package_esp8266com_index.json
// Board: NodeMCU 1.0(ESP-12E Module)
// Builtin Led: 2
// Up Speed: 115200
// Searial Monitor: Newline, 9600baud
// ----------

#include <string>       //for std::string
#include <vector>       //for vector

#include <stdint.h>
#include <FastLED.h>
#include <ESP8266TrueRandom.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ----------, 修改

// 定義顏色常數
const CRGB RED_COLOR = CRGB::Red;
const CRGB YELLOW_COLOR = CRGB::Yellow;
const CRGB GREEN_COLOR = CRGB::Green;
const CRGB BLACK_COLOR = CRGB::Black;
const CRGB CURRENT_STATION_COLOR = GREEN_COLOR;     // 定義station的led燈條顏色

// 定義時間延遲常數
const int interval_1000 = 1000;
const int interval_2000 = 2 * interval_1000;
const int interval_5000 = 5 * interval_1000;
const unsigned long interval_10000 = 10 * interval_1000;

const int interval_100 = 100;
const int interval_500 = 5 * interval_100;
const int interval_200 = 2 * interval_100;

const int interval_10 = 10;

// ----------

// 定義pin接腳的GPIO編號
static const uint8_t my_D0 = 16;
static const uint8_t my_D1 = 5;
static const uint8_t my_D2 = 4;
static const uint8_t my_D3 = 0;
static const uint8_t my_D4 = 2;
static const uint8_t my_D5 = 14;

#define NUM_LEDS_PER_STRIP 30   // 每1米led燈條有30顆燈珠
#define LED_TYPE WS2812B        // led燈條 driver型號
#define max_bright 128          // led燈條亮度, 0至255
#define NUM_STRIPS 5            // led燈條總數
#define COLOR_ORDER GRB         // led燈珠排列順序

// ----------不同station, 修改

// 定義wifi熱點及主機ip的的資料
const char* ssid = "staff-Dev";
const char* password = "cmuhch1357";
const char* mqttServer = "10.108.249.100";
//
//const char* ssid = "ZH";
//const char* password = "-pmc4394";
//const char* mqttServer = "192.168.32.178";
//
//const char* ssid = "AndroidAPEFA6";
//const char* password = "ajgp6664";
//const char* mqttServer = "192.168.43.117";

const int mqttPort = 1883;              //預設mqtt port編號
const int num_led_init_flash = 3;       //預設初始閃爍次數

// 定義esp8266板子的無線網路的ip資料, 修改
//IPAddress local_IP(10,108,249,101);   //station1, for 熱點 staff-Dev
//IPAddress local_IP(10,108,249,102);   //station2, for 熱點 staff-Dev
IPAddress local_IP(10,108,249,103);   //station3, for 熱點 staff-Dev
//IPAddress local_IP(192,168,43,101);     //station1, for 熱點 AndroidAPEFA6

// 定義gateway的ip資料, 修改
IPAddress gateway(10,108,249,254);    //for 熱點 staff-Dev
//IPAddress gateway(192,168,43,1);        //for 熱點 AndroidAPEFA6

// 定義dns的ip資料, 修改
IPAddress primaryDNS(10,108,6,238);   //for 熱點 staff-Dev
//IPAddress primaryDNS(192,168,43,1);     //for 熱點 AndroidAPEFA6  

// 定義subnet的資料
IPAddress subnet(255,255,255,0);

// ----------

CRGB leds[NUM_STRIPS][NUM_LEDS_PER_STRIP];

int g_int_myLayout;   //led燈條編號(層架)
int g_int_myBegin;    //led燈條的某區段開始編號
int g_int_myEnd;      //led燈條的某區段結束編號 

int g_int_num_ret_seg;

// ----------

unsigned long previousMillis_WIFI = 0;
unsigned long previousMillis_LED  = 0;
unsigned long previousMillis_MQTT = 0;

unsigned long lastReconnectAttempt = 0;

// ----------

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// 定義結構表示每個段的資訊
struct Segment {
  int start;                // 1~30
  int end;                  // 1~30
  CRGB color;               // 顏色 
  uint8_t brightness;       // 亮度
  unsigned long duration;   // 持續時間（毫秒）for flash status
  unsigned long startTime;  // 開始時間（毫秒）for flash status  
};

std::vector<std::vector<Segment>> segmentsByStrip;  // 使用 std::vector 來管理每條燈的分段資料

// ----------

byte uuidNumber[16];        // 定義MQTT連接裝置的 clientID(UUID編號, 共16 bytes)
boolean ledState = false;   // 定義 system led flash flag
boolean ledFlash = false;         // 預設led燈條不閃爍   
boolean showMqttOnline = false;   // 預設不顯示mqtt online 

// ----------不同station, 修改

// 定義MQTT連接裝置的 topic及client ID
//String string_mqttTopic = "station1";
//String string_mqttTopic = "station2";
String string_mqttTopic = "station3";

String string_mqttTopic_for_reconnect = "reconnect";
String string_mqttTopic_for_online = "online";
String string_clientId = "CLIENT-esp8266-" + string_mqttTopic;

// ----------

void setup() {
  pinMode(my_D0, OUTPUT);       //設定system led port為輸出模式
  digitalWrite(my_D0, LOW);     //設定led on

  Serial.begin(9600);           //設定serial monitor 通訊速率
  
  //初始化led燈條
  FastLED.addLeds<LED_TYPE, my_D1, COLOR_ORDER>(leds[0], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, my_D2, COLOR_ORDER>(leds[1], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, my_D3, COLOR_ORDER>(leds[2], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, my_D4, COLOR_ORDER>(leds[3], NUM_LEDS_PER_STRIP);
  FastLED.addLeds<LED_TYPE, my_D5, COLOR_ORDER>(leds[4], NUM_LEDS_PER_STRIP);

  initializeSegments();         //初始化led燈條分段資料struct

  // 初始步驟 1: 所有led燈條全熄滅0.5秒
  clearAllLEDs();               
  FastLED.show();
  delay(interval_500);

  // 初始步驟 2: 所有led燈條全亮2秒
  applyAllSegments(CURRENT_STATION_COLOR);    
  FastLED.show();
  delay(interval_2000);

  // 初始步驟 3: 所有led燈條全熄滅0.5秒
  clearAllLEDs(); 
  FastLED.show();
  delay(interval_500);

  // 初始步驟 4: 所有led燈條全閃爍0.5秒3次
  for (int i = 0; i < num_led_init_flash; ++i) {    
    applyAllSegments(CURRENT_STATION_COLOR);    //led燈條全亮    
    FastLED.show();
    delay(interval_500);

    clearAllLEDs();   //led燈條全熄滅
    FastLED.show();
    delay(interval_500);
  }

  // 初始步驟 5: 所有led燈條全熄滅且清除分段資料
  clearAllLEDsAndclearAllSegments();
  FastLED.show();  

  // 設定ESP8266工作模式為無線終端模式
  //WiFi.mode(WIFI_STA);        
  // Configures static IP address
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS)) {
    Serial.println("STA Failed to configure");
  }    
  
  // 連接WiFi
  connectWIFI();

  // 連接MQTT伺服器        
  connectMQTTServer();    
}

// ----------

void loop() {
  boolean LoopReturn;
  unsigned long currentMillis = millis();       //print the Wi-Fi status every 5 seconds
  unsigned long currentMillis_LED =  millis();
  unsigned long currentMillis_MQTT =  millis();
  unsigned long currentMillis_RESET =  millis();

  //system led 閃爍
  if (currentMillis_LED - previousMillis_LED >= interval_500) {
    ledState=!ledState;
    if (ledState) {
     digitalWrite(my_D0, LOW); 
    } else {
      digitalWrite(my_D0, HIGH);
    }
    previousMillis_LED = currentMillis_LED;    
  }
  
  //偵測斷線, 重新連線
  if ((WiFi.status() != WL_CONNECTED) && (currentMillis - previousMillis_WIFI >= interval_5000)) {
    
   digitalWrite(my_D0, HIGH);  // 設定led off
   delay (2000);
   
   Serial.println("Reconnecting to WIFI...");
   previousMillis_WIFI = currentMillis;
   ESP.restart();             //Alternatively, restart your board
   //WiFi.disconnect();
   //WiFi.reconnect();   
  }
  
  //偵測是否顯示 MQTT topic online(每2秒)
  if (showMqttOnline) {
    if (currentMillis_MQTT - previousMillis_MQTT >= interval_2000) {
     ESP8266TrueRandom.uuid(uuidNumber); // Generate a new UUID
     String uuidStr = ESP8266TrueRandom.uuidToString(uuidNumber); 
     String myStr = string_mqttTopic + ", the UUID number is " + uuidStr;
     
     mqttClient.publish(string_mqttTopic_for_online.c_str(), myStr.c_str());
     //Serial.println("MQTT station1 on line...");
      
     previousMillis_MQTT = currentMillis_MQTT;
    }
  }  

  //led燈條閃爍(試劑入庫/出庫 狀況)
  fillSegments(currentMillis, g_int_myLayout-1, g_int_myBegin, g_int_myEnd, g_int_num_ret_seg);
  FastLED.show();
  delay (interval_10);   
  
  // 偵測 MQTT 連線
  if (!mqttClient.connected()) {
    if (currentMillis_RESET - lastReconnectAttempt >= interval_10000) {
      lastReconnectAttempt = currentMillis_RESET;     
  
      if (!reconnect()) {  
        if (currentMillis_RESET > interval_10000) {
          // If it's been more than 10 seconds and still can't connect, restart
          Serial.println("Restarting ESP32...");
          ESP.restart();
        }    
      }
    }
  }
    
  LoopReturn=mqttClient.loop();

  if (LoopReturn) {
    //Serial.println("the client is still connected...");  
  } else {
    Serial.println("the client is no longer connected..."); 
  }
}

// ----------

// ESP8266連線wifi
void connectWIFI(){ 
  WiFi.begin(ssid, password);
 
  //等待WiFi連線,成功連線後輸出成功訊息
  Serial.println(); 
  Serial.print("Waitting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(interval_1000);
    Serial.print(".");
  }   //end while
  Serial.println("");
  Serial.println();
  Serial.println("WiFi Connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());   
}

// 連線MQTT服務, 同時訂閱信息
void connectMQTTServer(){  
  int stateCode;  

  mqttClient.setServer(mqttServer, mqttPort);     // 設定MQTT服務和port  
  mqttClient.setCallback(mqttCallback);           // 設定MQTT訂閱callback  
 
  // 連線MQTT服務
  if (mqttClient.connect(string_clientId.c_str(), NULL, NULL)) {
    Serial.println("MQTT Server Connected!");
    Serial.print("Server Address: ");
    Serial.println(mqttServer);
    Serial.print("ClientId: "); 
    Serial.println(string_clientId);
    subscribeTopic();                   // 訂閱指定主题
  } else {
    Serial.print("MQTT Server Connect Failed. Client State: ");
    stateCode = mqttClient.state();
    Serial.print(stateCode);
    Serial.println(", Retry in 1 seconds");    
    delay(1000);
  }   
}

// 訂閱指定主题
void subscribeTopic(){ 
  char subTopic[string_mqttTopic.length() + 1];  
  strcpy(subTopic, string_mqttTopic.c_str());  
   
  if (mqttClient.subscribe(subTopic)) {     // 訂閱主题成功
    Serial.print("Subscrib Topic: ");
    Serial.println(subTopic);
  } else {
    Serial.println("Subscribe Topic Fail..."); 
  }  
}

// MQTT重新連線
//void reconnect() {
bool reconnect() {    
  //while (!mqttClient.connected()) {   // 重新連接MQTT   
    Serial.println("Attempting MQTT reconnection...");    
    
    string_clientId += String(random(0xffff), HEX);                   // 以random亂數重新設立 client ID
    
    if (mqttClient.connect(string_clientId.c_str(), NULL, NULL)) {    // 重新連線    
      Serial.println("Reconnected to MQTT");
      
      sendJsonData(g_int_myLayout, g_int_myBegin, g_int_myEnd, string_clientId + " reconnect OK...",  "string_mqttTopic_for_reconnect");
      char subTopic[string_mqttTopic.length() + 1];  
      strcpy(subTopic, string_mqttTopic.c_str());
      mqttClient.subscribe(subTopic);
      
      return true;
    } else {
      Serial.print("Failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" Retry in 5 seconds");
      delay(5000);
      
      return false;
    }
  //}     //end while
}

// ----------

// MQTT CallBack function(收到MQTT訊息的處理函數)
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  // 顯示MQTT的topic
  Serial.println("Message Received from topic: " + String(topic));
  //Serial.println();

  // 顯示MQTT的payload
  Serial.print("Message body: ");
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // 解析JSON格式的資料
  DynamicJsonDocument doc(256);
  deserializeJson(doc, message);
  String ledStrip_layout = doc["Layout"];  //解Layout的JSON序列化(Serialize)資料(1~5)
  String ledStrip_begin = doc["Begin"];    //解Begin的JSON序列化(Serialize)資料(1~30)
  String ledStrip_end = doc["End"];        //解End的JSON序列化(Serialize)資料(1~30)
  String ledStrip_msg = doc["Msg"];        //解Msg的JSON序列化(Serialize)資料
  
  g_int_myLayout = ledStrip_layout.toInt();
  g_int_myBegin = ledStrip_begin.toInt();
  g_int_myEnd = ledStrip_end.toInt();

  ledStrip_msg.toLowerCase();  
  
  if (ledStrip_msg.equals("on")) {                              
  //*狀況1: 收到的訊息為"on", led燈條指定區段點亮但其他區段不變 
    ledFlash = false;
    //Serial.println(string_strLed + " LED_ON");
    Serial.println("收到的訊息為 on");
    Serial.println("狀況1: led燈條指定區段 點亮 但其他區段不變");
    
    addSegment(g_int_myLayout-1, g_int_myBegin, g_int_myEnd, CURRENT_STATION_COLOR, interval_500);  // 新增一個分段資料
    applySegment(g_int_myLayout-1, g_int_myBegin, g_int_myEnd, CURRENT_STATION_COLOR);              // 將分段資料對應到led燈條    
    serial_print_leds();
    FastLED.show(); 

  } else if (ledStrip_msg.equals("off") || g_int_myLayout == 0) {                             
    // 收到的訊息為"off", led燈條全部熄滅或指定區段熄滅  
    ledFlash = false;
    //Serial.println(string_strLed + " LED_OFF");
    String string_temp = "收到的訊息為 off, 層數: " + String(g_int_myLayout);    
    Serial.println(string_temp);
   
    if (ledStrip_msg.equals("off") && g_int_myLayout == 0) {
  //*狀況2: led燈條全部熄滅
      Serial.println("狀況2: led燈條全部熄滅");
      clearAllLEDsAndclearAllSegments();    // led燈條全部熄滅及清除分段資料
      serial_print_leds();
      FastLED.show();
    } else {
  //*狀況3: led燈條指定區段熄滅但其他區段不變
      Serial.println("狀況3: led燈條指定區段 熄滅 但其他區段不變");
      updateSegment(g_int_myLayout-1, g_int_myBegin, g_int_myEnd, CRGB::Black, interval_500);   // 更新一個分段資料
      applySegment(g_int_myLayout-1, g_int_myBegin, g_int_myEnd, CRGB::Black);                  // 將分段資料對應到led燈條      
      serial_print_leds();
      FastLED.show(); 
    }
    
  } else if  (ledStrip_msg.equals("flash")){
  //*狀況4: 收到的訊息為"flash", 出庫及入庫頁面, led燈條唯一區段閃爍  
    ledFlash = true; 
    //Serial.println(string_strLed + " LED_FLASH");
    Serial.println("收到的訊息為 flash");
    Serial.println("狀況4: led燈條指定區段 閃爍 但其他區段不變");       
    clearAllLEDsAndclearAllSegments();    // led燈條全部熄滅及清除分段資料
    FastLED.show();
    
    g_int_num_ret_seg = addSegment(g_int_myLayout-1, g_int_myBegin, g_int_myEnd, CURRENT_STATION_COLOR, interval_500);  // 新增一個分段資料
    applySegment(g_int_myLayout-1, g_int_myBegin, g_int_myEnd, CURRENT_STATION_COLOR);              // 將分段資料對應到led燈條
    serial_print_leds();      
  } 
}   

// 檢查led燈條的分段資料是否有效 (stripIndex: 0~4, start/end: 1~30)
bool isSegmentValid(int stripIndex, int start, int end) {
  // 檢查是否超出led燈條範圍
  if (start < 0 || end >= NUM_LEDS_PER_STRIP)
    return false;  

  // 檢查是否與現有分段資料重疊
  for (const auto& segment : segmentsByStrip[stripIndex]) {
    if (!(end < segment.start || start > segment.end)) {      
      return false; // 分段資料和現有分段資料有重疊
    }
  }
  return true;      // 分段資料有效
}

//列印led燈條輸出值
void serial_print_leds() {
  for (int strip = 0; strip < NUM_STRIPS; ++strip) {
    Serial.print("strip");
    Serial.print(strip + 1);    
    for (int led = 0; led < NUM_LEDS_PER_STRIP; ++led) {
      if(!(leds[strip][led].r==0 && leds[strip][led].g==0 && leds[strip][led].b==0)) {     
        Serial.print("[");
        Serial.print(led+1);
        Serial.print("] = ");
        
        Serial.print("(");
        Serial.print(leds[strip][led].r);
        Serial.print(",");
        Serial.print(leds[strip][led].g);
        Serial.print(",");
        Serial.print(leds[strip][led].b);
        Serial.print(")");     
        Serial.print(", ");
      }
    }
    Serial.println();
  }
}

// 建立 JSON 物件
void sendJsonData(int int_layout, int int_begin, int int_end, String char_msg, String string_mqttTopic) {  
  DynamicJsonDocument jsonDoc(256);

  String string_layout = String(int_layout);
  String string_begin = String(int_begin);
  String string_end = String(int_end);

  // 添加屬性到 JSON 物件
  jsonDoc["layout"] = string_layout.c_str();
  jsonDoc["begin"]  = string_begin.c_str();
  jsonDoc["end"]    = string_end.c_str();
  jsonDoc["msg"]    = char_msg.c_str();

  // 將 JSON 物件轉換為字串
  String string_jsonString;
  serializeJson(jsonDoc, string_jsonString);

  // 將 JSON 字串發送到 MQTT Topic
  mqttClient.publish(string_mqttTopic.c_str(), string_jsonString.c_str());
}

//初始化led燈條的分段資料
void initializeSegments() {  
  segmentsByStrip.resize(NUM_STRIPS);
  
  for (int i = 0; i < NUM_STRIPS; ++i) {
    segmentsByStrip[i].push_back({0, NUM_LEDS_PER_STRIP-1, CURRENT_STATION_COLOR, max_bright, interval_500}); 
  }
}

void applyAllSegments(CRGB color) {
  for (int i = 0; i < NUM_STRIPS; ++i) {
    // 檢查該led條燈是否有分段資料
    //if (!segmentsByStrip[i].empty()) { 
    //  FastLED.setBrightness(max_bright); 
    //  for (const Segment& segment : segmentsByStrip[i]) {
    //    fill_solid(&leds[i][segment.start-1], segment.end - segment.start + 1, color);
    //  }
    //}
    FastLED.setBrightness(max_bright); 
    fill_solid(&leds[i][0], NUM_LEDS_PER_STRIP, color);
  }
}

// 將分段資料對應到led燈條(stripIndex: 0~4, start/end: 1~30)
void applySegment(int stripIndex, int start, int end, CRGB color) {
  // 檢查該led條燈是否有分段資料
  if (!segmentsByStrip[stripIndex].empty()) { 
    FastLED.setBrightness(max_bright);     
    fill_solid(&leds[stripIndex][start-1], end - start + 1, color);
  }
}

// 將所有led燈條熄滅
void clearAllLEDs() {
  for (int i = 0; i < NUM_STRIPS; ++i) {
    //fill_solid(leds[i], NUM_LEDS_PER_STRIP, CRGB::Black);
    fill_solid(&leds[i][0], NUM_LEDS_PER_STRIP, CRGB::Black);    
  }         
}

// 清空led燈條的分段資料及將所有led燈條熄滅
void clearAllLEDsAndclearAllSegments() {
  for (int i = 0; i < NUM_STRIPS; ++i) {
    // 檢查led燈條是否有分段資料
    if (!segmentsByStrip[i].empty()) {
      segmentsByStrip[i].clear();     // 清空led燈條的分段資料
    }
    fill_solid(&leds[i][0], NUM_LEDS_PER_STRIP, CRGB::Black);    
  }
}

// 新增1個分段資料 (stripIndex: 0~4)
int addSegment(int stripIndex, int start, int end, CRGB color, unsigned long duration) {
  Segment newSegment = {start, end, color, max_bright, duration};
  // 檢查該led條燈的分段資料是否重複或交錯, stripIndex=0~4
  if (isSegmentValid(stripIndex, start, end)) {
    segmentsByStrip[stripIndex].push_back(newSegment);
    Serial.println("Segment added successfully.");
    // 回傳新增的區段索引
    return segmentsByStrip[stripIndex].size() - 1;
  } else {
    Serial.println("Invalid segment. Ignoring.");
    // 如果無效的話回傳 -1 或其他適當的錯誤碼
    return -1;
  }    
}

// 反轉led條燈的分段資料(stripIndex: 0~4)
void fillSegments(unsigned long currentMillis, int stripIndex, int start, int end, int g_int_num_ret_seg) {
  if (ledFlash) {    
    // 檢查該led條燈是否有分段資料, stripIndex=0~4
    if (g_int_num_ret_seg >= 0 && g_int_num_ret_seg < segmentsByStrip[stripIndex].size()) {    
      Segment& segment = segmentsByStrip[stripIndex][g_int_num_ret_seg];      
             
        if (currentMillis - segment.startTime >= segment.duration) {          
          segment.startTime = currentMillis;  // 重新設定開始時間
          // 反轉分段資料的顏色
          FastLED.setBrightness(max_bright);          
          CRGB TEMP_COLOR = (leds[stripIndex][segment.start-1] == CRGB(CRGB::Black)) ? CRGB(CURRENT_STATION_COLOR) : CRGB(CRGB::Black);
          fill_solid(&leds[stripIndex][segment.start-1], segment.end - segment.start + 1, TEMP_COLOR); 
          
          String TEMP_FLASH = (leds[stripIndex][segment.start-1] == CRGB(CRGB::Black)) ? " flash on..." : " flash off...";
          TEMP_FLASH = string_mqttTopic + String(", led:") + String(stripIndex+1) + String("start:") + String(start)+ String(", end:") + String(end) + TEMP_FLASH;
          Serial.println(TEMP_FLASH);
        }
      
    }
  }
}

void updateSegment(int stripIndex, int start, int end, CRGB color, unsigned long duration) {
  // 搜尋指定的分段資料
  for (auto& segment : segmentsByStrip[stripIndex]) {
    if (segment.start == start && segment.end == end) {
      // 更新 color 和 duration
      segment.color = color;
      segment.duration = duration;
      Serial.println("Segment updated successfully.");
      return;  // 找到並更新分段後結束函式
    }
  }

  // 如果沒找到指定的分段
  Serial.println("Segment not found. Unable to update.");
}
