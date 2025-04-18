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
├── /docs/         # Infographics, flowcharts, presentation slides
├── /code/         # MicroPython scripts per unit
├── README.md
├── LICENSE
└── .gitignore

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