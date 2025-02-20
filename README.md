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

## MQTT:

URL:
c79e2ea5e65e40f6b79ba3a3aad7c19f.s1.eu.hivemq.cloud
Port:
8883
Websocket Port:
8884

User:admin
Password:Password1  

## MQTT Data:

![Alt text](<Screenshot 2025-02-13 at 11.49.15.png>)
### Data Organisation:
{Postcode area code}/{Street Name}/{House Number}

TS16/FORMBY_WALK/01/

### Sensor Data
./Sensors/Current
{
  "fillLevel": 75,
  "weight": 15.4,
  "density": 1.2
} 

### Environment Data
./Environment/Current
{
  "temp": 22.5,
  "humidity": 60
}

./Environment/Daily
{
  "low": 5.5,
  "high" 22
}



