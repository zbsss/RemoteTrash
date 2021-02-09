# Remote Trash

### A project prepared for IoT laboratories at AGH University of Science and Technology.


The subject of the project was to create a system that implements smart monitoring.
We chose to design system that would monitor the level of filling the trash bins in the city.  

Based on articles ([first](https://www.ijert.org/research/iot-based-smart-garbage-and-waste-monitoring-system-using-mqtt-protocol-IJERTCONV6IS13133.pdf), [second](https://www.researchgate.net/publication/282738798_Smart_Waste_Collection_System_Based_on_Location_Intelligence)) we have designed what should contain the device, which will measure level of garbage in a bin. The digital twin of this device and software for it was prepared by us. 
To run simulations we have made mocked libraries and functions, which could be replaced by real ones in actual device.  

Our device sends information about its battery condition and trash level to Google Cloud cyclicaly. It uses MQTT to connect with cloud.  
   
   #

Our digital device is a twin of actual device, which should contain :</br>
- microcontroller ESP32 (eg. FireBeetle ESP32)
- HCSR04 ultrasonic sensor
- two lithium batteries 3.7V each (eg. li-ion 18650 - capacity: 2600mAh each)

The device will be programmed using micro python.

Because HCSR04 requires 5V and ESP32 only 3.3V we will add a resistor to the circuit. (like [here](https://sheldondwill.wordpress.com/2014/02/04/using-an-ultrasonic-sensor-hc-sr04-with-a-3-3v-micro-controller-tiva-c-series/))

**FireBeetle ESP32 parameters**: (sources: [first](https://diyi0t.com/reduce-the-esp32-power-consumption/), [second](https://eu.mouser.com/new/dfrobot/dfrobot-firebeetle/))<br>
parameter | value
--- | ---
Power Supply | 3.3V DC 
Deepspeed Current: | 0.011mA
Working Current: | 80mA
Transmission Current | 190mA
<br>


**HCSR04 parameters**: ([source](https://datasheet4u.com/datasheet-pdf/ETC/HC-SR04/pdf.php?id=1380136))<br>
parameter | value
--- | ---
Power Supply | +5V DC 
Quiescent Current: | <2mA
Working Current: | 15mA
<br>

**Battery usage**   
Assumptions:
1. ESP32 and HCSR04 sensor are being awaken for 30 s twice a day. For the rest of day the are in a deep sleep (ESP32) or turned off (sensor). Alternatively, ESP32 and HCSR04 sensor are turned on for equivalent of 30 s twice a day, e.g. 1 min once a day.
2. Communication with server is using WiFi. We assume there is a constant access to WiFi network.
3. To get 5V and 3.3V power supply we assumed that these regulators would be used: [first](https://pl.mouser.com/ProductDetail/Microchip-Technology/TC1262-33VDB?qs=Jw2w9zrI6w%252BwE14QJIhJFA%3D%3D&mgh=1&vip=1&gclid=CjwKCAiAi_D_BRApEiwASslbJ7H0cJQEGvKTFvMWM9Xh1R2UAsh5fmZcAWQEGv_KjgUsXIbnqQwQMRoCIS4QAvD_BwE), [second](https://pl.farnell.com/microchip/mcp1703-5002e-db/ic-ldo-reg-250ma-5v-sot223/dp/1627178?gclid=CjwKCAiAxeX_BRASEiwAc1Qdkcw7YHGdpOyY8fNJVOAq-gmqQjOPL75oksJOoKkmFiZcXzzSWzI_ghoCSPIQAvD_BwE&gross_price=true&mckv=sCMYRj03j_dc|pcrid|459816541173|plid||kword||match||slid||product|1627178|pgrid|114468574784|ptaid|pla-303417735835|&CMP=KNC-GPL-SHOPPING-Whoop-HI-31-Aug-20).

With these assumptions our device's working time would be about 19 days 9 h and 30 min.
