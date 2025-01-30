# Project:

## Waste Management Optimization:

Problem: Static bin collection routes can leave many bins overflowing
Solution: Create a smart waste management system with fill-level so the council can optimes bin collection
Sensors: Ultrasonic distance sensors measure bin fill levels; Weight Sensor to approximate waste density; Air Monitoring for potential pollution cause by waste


## Work split:

Kuno:
- Hardware:
  - PCB
  - mounting + assembly
- Firmware:
  - Reading sensors
  - Sending data to cloud
- Creating Fake Data

Mark & Andrea:
- Cloud:
  - Server
- Application:
  - Collecting data from MQTT
  - displaying the data
  - Figure out which bin needs to be collected next

## The data:

- Current Data:
  - Temp
  - humidity
  - Fill Level
  - Weight
  - Density
- Daily Data:
  - Day high Temp
  - Day Low Temp
  - Day Fill delta
- Counters:
  - Time Since Emptied
  - Time Since Full
  - Number of fills
- Server Data
  - trends ect.


URL:
8c0f88a85b5045dd80b56a73fb589735.s1.eu.hivemq.cloud
Port:
8883
Websocket Port:
8884
TLS MQTT URL:
8c0f88a85b5045dd80b56a73fb589735.s1.eu.hivemq.cloud:8883
TLS Websocket URL:
8c0f88a85b5045dd80b56a73fb589735.s1.eu.hivemq.cloud:8884/mqtt



