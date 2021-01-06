# Remote Trash

Digital twin of our device should contain:</br>
- microcontroller ESP32 (eg. FireBeetle ESP32)
- HCSR04 ultrasonic sensor
- lithium battery 3.7V

The device will be programmed using micro python.

Because HCSR04 requires 5V and ESP32 only 3.3V we will add a resistor to the circuit. (like here: https://sheldondwill.wordpress.com/2014/02/04/using-an-ultrasonic-sensor-hc-sr04-with-a-3-3v-micro-controller-tiva-c-series/)

**FireBeetle ESP32 parameters**: (source: https://diyi0t.com/reduce-the-esp32-power-consumption/ and https://eu.mouser.com/new/dfrobot/dfrobot-firebeetle/)<br>
parameter | value
--- | ---
Power Supply | 3.3V DC 
Lightspeel Current: | ~2mA
Working current: | 80mA
Transmission Current | 190mA
<br>


**HCSR04 parameters**: (source: https://datasheet4u.com/datasheet-pdf/ETC/HC-SR04/pdf.php?id=1380136)<br>
parameter | value
--- | ---
Power Supply | +5V DC 
Quiescent Current: | <2mA
Working current: | 15mA
<br>

_TODO: trzeba jeszcze dodać realistycze spadki energii baterii - jak dużo prądu zużywa ESP32 z tym sensorem w czasie lightsleep i w czasie działania i wysyłania wiadomości. I trzeba jakoś pobierać info o aktualnym stanie rozładowania baterii (w tym rzeczywistym urządzeniu)._


https://datasheet4u.com/datasheet-pdf/ETC/HC-SR04/pdf.php?id=1380136