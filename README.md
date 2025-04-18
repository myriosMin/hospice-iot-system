# 🩺 Integrated Hospice Care System

> “How might we design an integrated IoT system to improve hospice care?”

This was a group project for our **Engineering Exploration module (Year 1 Sem 2)** at NYP, created by [Min](https://github.com/myriosMin), [Habib](#), [Alex](#), and [Jin Bin](#).  
The aim: build a responsive IoT system that brings **safety, comfort, and dignity** to elderly hospice patients.

---

## 🌟 Overview

This system is divided into **3 main units**:

1. **Environmental Monitoring** (temp, humidity, TVOC)
2. **Health Monitoring** (SpO₂, pulse, temperature)
3. **Safety Monitoring** (fall detection, toilet access, wet floor)

All three units are powered by **M5Stack Fire**, interconnected with **MQTT**, and upload live data to **Qubitro Cloud** for visualization.

---

## 💡 Key Features

- ⚙️ Smart temperature/humidity/air quality alerts
- 🧠 Real-time vital sign tracking
- 🚨 Fall detection system with countdown + alarm
- 🪪 RFID-based toilet access
- 💬 Gesture-based emergency alert
- 📊 Qubitro-powered dashboards
- 📡 MQTT interconnectivity between units

---

## 🧰 Tech Stack

| Category      | Tools/Components |
|---------------|------------------|
| Microcontroller | M5Stack Fire (x3) |
| Sensors        | ENV III, TVOC/eCO2, Earth sensor, Pulse Oximeter, NCIR 2, Gesture, RFID |
| Actuators      | Micro Servo Motors (x3) |
| Connectivity   | MQTT protocol |
| Cloud Storage  | Qubitro |
| Programming    | MicroPython (via UIFlow) |

---

## 📦 Repository Structure

- `docs/` – Infographics, presentation slides, and flowcharts  
- `code/` – MicroPython scripts for each unit (environment, health, safety)  
- `README.md` – Project overview and setup  
- `LICENSE` – MIT license info  
- `.gitignore` – Git tracking rules

---

## ⚙️ Setup Instructions

### 🧱 Hardware Requirements

To replicate this project, you'll need the following components:

- `3×` M5Stack Fire core units  
- `1×` ENV III Unit (temperature & humidity)  
- `1×` TVOC/eCO2 Unit (air quality)  
- `1×` Earth Unit (wet floor detection)  
- `1×` Mini Heart Rate Unit  
- `1×` NCIR 2 Unit (IR body temperature)  
- `1×` Gesture Sensor  
- `1×` RFID Unit  
- `3×` Micro Servo Motors  
- USB-C cables, breadboard, and jumper wires (for optional testing and prototyping)

**Environmental Fire unit** is connected with ENV III and TVOC/eCO2 sensors, and a servo motor.
**Health Fire unit** is connected with Heart Rate and NCIR 2 sensors, and a servo motor.
**Safety Fire unit** is connected with Gesture sensor, RFID unit and a servo motor.

---

### 💻 Software Setup (MicroPython via UIFlow)

All units were programmed using **M5Stack UIFlow**, which uses **MicroPython**.

#### 📅 Required Imports
The following modules and libraries were used (usually already imported in UIFlow):

```python
from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
from m5mqtt import M5mqtt
from libs.json_py import *
import unit
```

#### 🚀 Getting Started with UIFlow
1. Go to [https://flow.m5stack.com](https://flow.m5stack.com)  
2. Connect your M5Stack Fire device via WiFi
3. Flash the UIFlow firmware onto your device (if not already done)  
4. Use the UI editor to add sensors/units, or switch to code view to write MicroPython manually  
5. Ensure WiFi is configured using `wifiCfg` to enable MQTT connectivity

---

### ☁️ Cloud Dashboard with Qubitro

We used [**Qubitro**](https://qubitro.com) for real-time cloud data visualization and MQTT communication.

#### 🔧 Steps to Set Up:
1. Create an account at [qubitro.com](https://qubitro.com)  
2. Create 3 devices (one per unit: Environment, Health, Safety)  
3. Generate MQTT credentials (server, port, username, password, topic)  
4. Add the credentials in each unit's MicroPython code

#### 🧪 Sample MQTT Setup:
```python
m5mqtt = M5mqtt("unit_1", "mqtt.qubitro.com", 1883, "your_username", "your_password", 300)
m5mqtt.start()
```

Each unit sends data every few seconds to Qubitro, where real-time dashboards and graphs can be built easily.

---

### 🧠 Tips & Troubleshooting

- Use the UIFlow Unit test tool to confirm sensor communication before full integration  
- If a sensor isn’t working, check its **I2C address** and wiring  
- Some sensors may need **sensitivity adjustment** or slight physical tuning  
- MQTT errors? Double-check your **Qubitro credentials** and network connection  
- For multi-unit communication, ensure **unique MQTT topics** are used to prevent message overlap

---

## 📸 Story

[▶ Read the story behind the project and how it works](https://myriosmin.com/2025/04/18/integrated-hospice-care-system-iot-project/)

---

## 📺 Demo Video

[▶ Watch on YouTube](https://www.youtube.com/watch?v=4nAW6GZMmRo)

---

## 📚 Learning Takeaways

- Interfacing multiple sensors with M5Stack hardware
- Writing MicroPython and debugging hardware integration
- Using MQTT for distributed sensor communication
- Deploying cloud dashboards for monitoring
- Designing tech with empathy for real users

---

## 🧑‍🤝‍🧑 Contributors

| Name | Role |
|------|------|
| Min | Environmental Unit / MQTT / Qubitro |
| Habib | Health Unit / Prototype |
| Alex | Safety Unit / Prototype |
| Jin Bin | Documentation / Prototype |

---

## 🌱 SDG Alignment

- **Goal 3**: Good Health and Well-Being  
- **Goal 9**: Industry, Innovation, and Infrastructure  
- **Goal 11**: Sustainable Cities and Communities

---

## 📝 License

MIT License (Feel free to build on this project for **learning** purposes citing proper credits!)

---

## 🔗 External Links

- 💻 [Hackster Project Page](https://www.hackster.io/t2_group5_nyp/integrated-hospice-care-system-d8c2f0)
- 📺 [Demo Video](https://www.youtube.com/watch?v=4nAW6GZMmRo)
- 📖 [Related Blog Post](https://myriosmin.com/2025/04/18/integrated-hospice-care-system-iot-project/) 

---

Thanks for stopping by!  
If you’re building something similar, feel free to fork this repo or reach out. Let's build thoughtful tech, together 💙