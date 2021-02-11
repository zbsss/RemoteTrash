# Remote Trash

### A project prepared for IoT laboratories at AGH University of Science and Technology.  
  

Developed by:  
 - Michał Kurleto [@zbsss](https://github.com/zbsss)
 - Karol Hamielec [@lewelyn7](https://github.com/lewelyn7)
 - Magdalena Pastuła [@Sharon131](https://github.com/Sharon131)
 - Natalia Brzozowska [@brzozia](https://github.com/brzozia)


The subject of the project was to create a system that implements smart monitoring.
We chose to design system that would monitor the level of filling the trash bins in the city.  

Based on articles ([first<sup>1</sup>](https://www.ijert.org/research/iot-based-smart-garbage-and-waste-monitoring-system-using-mqtt-protocol-IJERTCONV6IS13133.pdf), [second<sup>2</sup>](https://www.researchgate.net/publication/282738798_Smart_Waste_Collection_System_Based_on_Location_Intelligence)) we have designed what should contain the device, which will measure level of garbage in a bin. The digital twin of this device and software for it was prepared by us. 
To run simulations we have made mocked libraries and functions, which could be replaced by real ones in actual device.  

Our device sends information about its battery condition and trash level to Google Cloud cyclicaly. It uses MQTT to connect with cloud.  
   
   #

Our digital device is a twin of actual device, which should contain :  
- microcontroller ESP32 (eg. FireBeetle ESP32)
- HCSR04 ultrasonic sensor
- two lithium batteries 3.7V each (eg. li-ion 18650 - capacity: 2600mAh each)

The device will be programmed using micro python.

Because HCSR04 requires 5V and ESP32 only 3.3V we will add a resistor to the circuit. (like [here<sup>3</sup>](https://sheldondwill.wordpress.com/2014/02/04/using-an-ultrasonic-sensor-hc-sr04-with-a-3-3v-micro-controller-tiva-c-series/))

**FireBeetle ESP32 parameters**: (sources: [first<sup>4</sup>](https://diyi0t.com/reduce-the-esp32-power-consumption/), [second<sup>5</sup>](https://eu.mouser.com/new/dfrobot/dfrobot-firebeetle/))  
parameter | value
--- | ---
Power Supply | 3.3V DC 
Deepspeed Current: | 0.011mA
Working Current: | 80mA
Transmission Current | 190mA
<br>


**HCSR04 parameters**: ([source<sup>6</sup>](https://datasheet4u.com/datasheet-pdf/ETC/HC-SR04/pdf.php?id=1380136))  
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
3. To get 5V and 3.3V power supply we assumed that these regulators would be used: [first<sup>7</sup>](https://pl.mouser.com/ProductDetail/Microchip-Technology/TC1262-33VDB?qs=Jw2w9zrI6w%252BwE14QJIhJFA%3D%3D&mgh=1&vip=1&gclid=CjwKCAiAi_D_BRApEiwASslbJ7H0cJQEGvKTFvMWM9Xh1R2UAsh5fmZcAWQEGv_KjgUsXIbnqQwQMRoCIS4QAvD_BwE), [second<sup>8</sup>](https://pl.farnell.com/microchip/mcp1703-5002e-db/ic-ldo-reg-250ma-5v-sot223/dp/1627178?gclid=CjwKCAiAxeX_BRASEiwAc1Qdkcw7YHGdpOyY8fNJVOAq-gmqQjOPL75oksJOoKkmFiZcXzzSWzI_ghoCSPIQAvD_BwE&gross_price=true&mckv=sCMYRj03j_dc|pcrid|459816541173|plid||kword||match||slid||product|1627178|pgrid|114468574784|ptaid|pla-303417735835|&CMP=KNC-GPL-SHOPPING-Whoop-HI-31-Aug-20).

With these assumptions our device's working time would be about 19 days 9 h and 30 min.

#  

### Code description

The main program of the device is in file *device.py*.  
To create an object of the Device class, the device configuration should be passed as a parameter. The device configuration should contain the information needed to connect using mqtt and information about a bin like: bin id, capacity and time between two sent messages (*message_time*). 

As long as the device's battery is not discharged the device gets the bin filling, updates the battery usage, sends information to the cloud and falls into a *sleep* for a specified period of time (*message time*). The device uses less energy while *sleeping*.   

The actual device should retrieve information about the level of filling the bin from the HCSR04 sensor. We have mocked library used to operate the sensor, so that the bin will be filling up with the given speed.  
We have also mocked some of *machine* library functions used to operate microcontroller.

The simulation is run from the file *simulation.py*, where the devices programs are started in separate threads.

### Cloud Computing

To handle data processing and managing of IOT devices we chose Google Cloud services. *IOT Core* service is responsible for registering devices, receiving data and uploading configuration to devices. Telemetry data gathered from smart bins are passed to *Big Query* via *Dataflow* and then they are ready to be processed with Big Data/AI tools available on Google Cloud. Data are transferred with MQTT protocol secured with TLS and RSA algorithm. Devices are configured to send: battery level, bin fulfillment, device ID and timestamp of a measurement - all packed up into JSON.

We also prepared a simple script to bulk register many devices. We only have to pass device list as an argument and script will do all job for us, this includes key generation and sending proper metadata to IOT Core.

### Visualization

The visualization is run as a seperate script *visualization.py*. Data is queried from *Big Query* every 10 seconds and for each device only the entry with the newest timestamp is displayed.

     
<br>
<br>

#
[<sup>1</sup> first article](https://www.ijert.org/research/iot-based-smart-garbage-and-waste-monitoring-system-using-mqtt-protocol-IJERTCONV6IS13133.pdf): **IoT based Smart Garbage and Waste Monitoring
System using MQTT Protocol**, authors: Harshitha N, Nehashree K Ruthika, Rhea Benny, Varsha S P, Keerthi Kumar M2 2Assitant Professor, Department of TCE, GSSSIETW, Mysuru, Karnataka, India. Students, BE, Department of TCE, GSSSIETW, Mysuru, Karnataka, India; access: 10.02.2021  
[<sup>2</sup> second article](https://www.researchgate.net/publication/282738798_Smart_Waste_Collection_System_Based_on_Location_Intelligence): **Smart Waste Collection System Based on Location Intelligence** authors: Jose M. Gutierrez, Michael Jensenb, Morten Heniusa and Tahir Riaz; access: 10.02.2021  
[<sup>3</sup>](https://sheldondwill.wordpress.com/2014/02/04/using-an-ultrasonic-sensor-hc-sr04-with-a-3-3v-micro-controller-tiva-c-series/) **Using An Ultrasonic Sensor (HC-SR04) with a 3.3v micro-controller (Tiva C Series)** author: sheldondwill; access: 10.02.2021  
[<sup>4</sup>](https://diyi0t.com/reduce-the-esp32-power-consumption/) **Guide to Reduce the ESP32 Power Consumption by 95%** author: Christopher David; access: 10.02.2021  
[<sup>5</sup>](https://eu.mouser.com/new/dfrobot/dfrobot-firebeetle/) **DFRobot FireBeetle ESP32 IOT Microcontroller**; access: 10.02.2021  
[<sup>6</sup>](https://datasheet4u.com/datasheet-pdf/ETC/HC-SR04/pdf.php?id=1380136) **HC-SR04 Datasheet** author: Elijah J. Morgan; access: 10.02.2021  
[<sup>7</sup>](https://pl.mouser.com/ProductDetail/Microchip-Technology/TC1262-33VDB?qs=Jw2w9zrI6w%252BwE14QJIhJFA%3D%3D&mgh=1&vip=1&gclid=CjwKCAiAi_D_BRApEiwASslbJ7H0cJQEGvKTFvMWM9Xh1R2UAsh5fmZcAWQEGv_KjgUsXIbnqQwQMRoCIS4QAvD_BwE) access: 11.01.2021   
[<sup>8</sup>](https://pl.farnell.com/microchip/mcp1703-5002e-db/ic-ldo-reg-250ma-5v-sot223/dp/1627178?gclid=CjwKCAiAxeX_BRASEiwAc1Qdkcw7YHGdpOyY8fNJVOAq-gmqQjOPL75oksJOoKkmFiZcXzzSWzI_ghoCSPIQAvD_BwE&gross_price=true&mckv=sCMYRj03j_dc|pcrid|459816541173|plid||kword||match||slid||product|1627178|pgrid|114468574784|ptaid|pla-303417735835|&CMP=KNC-GPL-SHOPPING-Whoop-HI-31-Aug-20) access: 11.01.2021  
