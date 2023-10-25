#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>

AsyncWebServer server(80);

#include <WiFi.h>
const char* wifi_ssid="";
const char* wifi_pass="";

#include <ArduinoJson.h>
StaticJsonDocument<300> doc;

#define START_HEADER         0x01
#define START_TEXT           0x02
#define START_MODE           0x1b
#define SIGN_TYPE_ALL_VERIFY 0x21
#define SIGN_TYPE_ALL        0x3f
#define END_TRANSMISSION     0x04
#define COMMAND_WRITE_TEXT   0x41
#define FILE_PRIORITY        0x30
#define TEXT_POSITION_MIDDLE 0x20

#define MODE_ROTATE          0x61
#define MODE_HOLD            0x62
#define MODE_FLASH           0x63
#define MODE_ROLL_UP         0x65
#define MODE_ROLL_DOWN       0x66
#define MODE_ROLL_LEFT       0x67
#define MODE_ROLL_RIGHT      0x68
#define MODE_WIPE_UP         0x69
#define MODE_WIPE_DOWN       0x6a
#define MODE_WIPE_LEFT       0x6b
#define MODE_WIPE_RIGHT      0x6c
#define MODE_SCROLL          0x6d

#define START_TEXT_COLOR     0x1c
#define TEXT_COLOR_RED       0x31
#define TEXT_COLOR_GREEN     0x32
#define TEXT_COLOR_AMBER     0x33
#define TEXT_COLOR_DIMRED    0x34
#define TEXT_COLOR_DIMGREEN  0x35
#define TEXT_COLOR_BROWN     0x36
#define TEXT_COLOR_ORANGE    0x37
#define TEXT_COLOR_YELLOW    0x38
#define TEXT_COLOR_RAINBOW1  0x39
#define TEXT_COLOR_RAINBOW2  0x41
#define TEXT_COLOR_MIX       0x42
#define TEXT_COLOR_AUTO      0x43

byte WAKEUP[]                 = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
byte SIGN_ADDRESS_BROADCAST[] = {0x30, 0x30};

byte colors[] = {TEXT_COLOR_RED,TEXT_COLOR_GREEN,TEXT_COLOR_AMBER,TEXT_COLOR_DIMRED,TEXT_COLOR_DIMGREEN,TEXT_COLOR_BROWN,TEXT_COLOR_ORANGE,TEXT_COLOR_YELLOW,TEXT_COLOR_RAINBOW1,TEXT_COLOR_RAINBOW2,TEXT_COLOR_MIX,TEXT_COLOR_AUTO};
byte modes[]  = {MODE_ROTATE,MODE_HOLD,MODE_FLASH,MODE_ROLL_UP,MODE_ROLL_DOWN,MODE_ROLL_LEFT,MODE_ROLL_RIGHT,MODE_WIPE_UP,MODE_WIPE_DOWN,MODE_WIPE_LEFT,MODE_WIPE_RIGHT,MODE_SCROLL};

String serial_message;

const char* PARAM_MESSAGE = "message";





void notFound(AsyncWebServerRequest *request) {
    request->send(404, "text/plain", "Not found");
}





void update_sign(String msg, int color=0, int modee=0){
  Serial2.write(WAKEUP,6);
  Serial2.write(START_HEADER);
  Serial2.write(SIGN_TYPE_ALL);
  Serial2.write(SIGN_ADDRESS_BROADCAST,2);
  Serial2.write(START_TEXT);
  Serial2.write(COMMAND_WRITE_TEXT);
  Serial2.write(FILE_PRIORITY);
  Serial2.write(START_MODE);
  Serial2.write(TEXT_POSITION_MIDDLE);
  Serial2.write(modes[modee]);
  Serial2.write(START_TEXT_COLOR);
  Serial2.write(colors[color]);
  Serial2.print(msg);
  Serial2.write(END_TRANSMISSION);
}





void setup() {
    Serial.begin(9600);
    Serial2.begin(9600, SERIAL_8N1, 17, 16);

    WiFi.begin(wifi_ssid, wifi_pass);

    server.on("/", HTTP_GET, [] (AsyncWebServerRequest *request) {
        String message;
        if (request->hasParam(PARAM_MESSAGE)) {
          update_sign(request->getParam(PARAM_MESSAGE)->value());
        }
        request->send(200, "text/html", "<form><input type=\"text\" name=\"message\" required><input type=\"submit\" value=\"Update\"></form>");
    });

    server.onNotFound(notFound);
    server.begin();
}





// Handle incoming Serial JSON commands
void handle_serial_json(){
  DeserializationError err = deserializeJson(doc, Serial);
  if (err == DeserializationError::Ok){        
    update_sign(doc["msg"], doc["color"], doc["mode"]);
    }
}





// This function shuttles data from the incoming serial connection to the outgoing rs232 serial connection
// It allows any legacy systems/software to still use the serial connection
void handle_serial_mitm(){
  delay(100); // Give time for the serial buffer to fill with incoming message, may not be best way
  while(Serial.available() > 0){
    Serial2.write(Serial.read());
  }  
}





// In the event that incoming Serial data is neither a legacy protocol or a JSON command.
// Assume it is text and send it to the sign
void handle_serial_basic(){
  
  while (Serial.available() > 0){
    char recieved = Serial.read();
    if (recieved == '\n'){
      serial_message.trim();
      if(serial_message != ""){
        update_sign(serial_message);
        serial_message = "";
      }
    }
    else{
      serial_message += recieved;
    }
  }
}





void handle_serial(){
  while (Serial.available() > 0){
    
    byte next = Serial.peek(); // Check first byte of incoming message
    
    if     (next == '{')  handle_serial_json();
    else if(next == 0x00) handle_serial_mitm();
    else                  handle_serial_basic();
    
    if(Serial.available()>0){
      Serial.read(); // Discard the byte if it has not been consumed
    }
    
  }
}
 



void loop() {
  handle_serial();
  
}
