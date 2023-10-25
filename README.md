# CharlieBrite
CharlieBrite is an ESP32 based interface module for an older BetaBrite LED sign.

In addition to serial control of the sign, the ESP32 also provides network connectivity to update the sign.

The Serial connection (9600 baud) to the ESP32 can be used to update the sign in 3 ways.

* Serial Basic: Any basic text sent to the ESP32 will be applied to the sign with basic sign functions.
* Serial JSON: A JSON API can be used to send more precise instructions to the sign, including message, mode, and color.
  * {"msg":"Hello World"}
  * {"msg":"Hello World", "mode":1}
  * {"msg":"Hello World", "mode":1, "color":7}
    
* Serial Legacy: The ESP will detect when a legacy application is trying to update the sign, and will simply shuttle the data directly to the sign as is.

When connected to WiFi the ESP will serve a simple web application that can be used to update the sign.


--------

### Colors and Modes for use with JSON API

Colors

1. RED
2. GREEN
3. AMBER
4. DIMRED
5. DIMGREEN
6. BROWN
7. ORANGE
8. YELLOW
9. RAINBOW1
10. RAINBOW2
11. MIXED
12. AUTO




Modes
1. ROTATE
2. HOLD
3. FLASH
4. ROLL_UP
5. ROLL_DOWN
6. ROLL_LEFT
7. ROLL_RIGHT
8. WIPE_UP
9. WIPE_DOWN
10. WIPE_LEFT
11. WIPE_RIGHT
12. SCROLL
