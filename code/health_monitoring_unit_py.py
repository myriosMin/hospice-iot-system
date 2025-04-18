from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
from m5mqtt import M5mqtt
import time
from libs.json_py import *
import unit


setScreenColor(0x000000)
heart_0 = unit.get(unit.HEART, unit.PORTA)
servo_0 = unit.get(unit.SERVO, unit.PORTB)
angle_0 = unit.get(unit.ANGLE, unit.PORTB)
ncir2_1 = unit.get(unit.NCIR2, unit.PORTA)


to_validate = None
temporary = None
hr = None
sp02 = None
body_temp = None
angle = None



label6 = M5TextBox(40, 224, "Measure", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label7 = M5TextBox(197, 224, "Stop Measuring", lcd.FONT_Default, 0xFFFFFF, rotate=0)
header = M5Title(title="Body Monitoring Unit", x=3, fgcolor=0x000000, bgcolor=0x45b1e8)
image0 = M5Img(0, 20, "res/G-BTemp.png", True)
image1 = M5Img(110, 20, "res/G-Heart.png", True)
image2 = M5Img(220, 20, "res/G-SpO2.png", True)
rectangle0 = M5Rect(0, 120, 100, 100, 0x000000, 0x45b1e8)
rectangle1 = M5Rect(110, 120, 100, 100, 0x000000, 0x45b1e8)
rectangle2 = M5Rect(220, 120, 100, 100, 0x000000, 0x45b1e8)
label0 = M5TextBox(7, 129, "Temperature", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label1 = M5TextBox(249, 132, "SP/02", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label2 = M5TextBox(124, 131, "Heart Rate", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label3 = M5TextBox(21, 178, "text", lcd.FONT_Comic, 0xFFFFFF, rotate=0)
label4 = M5TextBox(132, 178, "text", lcd.FONT_Comic, 0xFFFFFF, rotate=0)
label5 = M5TextBox(242, 178, "text", lcd.FONT_Comic, 0xFFFFFF, rotate=0)

import math

#validating body parameters, changing image and fonts based on sensor values
# validating body temperature
def validate_body_temp(to_validate):
  global temporary, hr, sp02, body_temp, angle
  if to_validate == 1:
    label3.setFont(lcd.FONT_Comic)
    if body_temp > 37.2 or body_temp < 35.1: #sick
      image0.changeImg("res/Sick.png")
      wait(0.3)
    else:
      image0.changeImg("res/G-BTemp.png") #normal
      wait(0.3)

# validating sp/o2
def validate_sp_02(to_validate):
  global temporary, hr, sp02, body_temp, angle
  if to_validate == 1:
    hr = float(hr)
    label5.setFont(lcd.FONT_Comic)
    if sp02 <= 90: #low/bad
      image2.changeImg("res/B-SpO2.png")
      wait(0.3)
    else: #normal
      image2.changeImg("res/G-SpO2.png") 
      wait(0.3)
    hr = int(hr)

# validating heart rate
def validate_hr(to_validate):
  global temporary, hr, sp02, body_temp, angle
  if to_validate == 1:
    label4.setFont(lcd.FONT_Comic)
    sp02 = float(sp02)
    if hr > 100 or hr < 50: #normal
      image1.changeImg("res/B-Heart.png")
      wait(0.3)
    else: #bad
      image1.changeImg("res/G-Heart.png")
      wait(0.3)
    sp02 = int(sp02)

#temp variable to turn on/off heart rate sensor and ncir2
def buttonC_wasPressed():
  global temporary, hr, to_validate, sp02, body_temp, angle
  temporary = 0 #off
  heart_0.setLedCurrent(0x00, 0x00)
  pass
btnC.wasPressed(buttonC_wasPressed)

def buttonA_wasPressed():
  global temporary, hr, to_validate, sp02, body_temp, angle
  temporary = 1 #on
  heart_0.setLedCurrent(0x0F, 0x01)
  pass
btnA.wasPressed(buttonA_wasPressed)


wifiCfg.doConnect('Myrios', 'abcdefghi')
if wifiCfg.wlan_sta.isconnected():
  m5mqtt = M5mqtt('body_unit', 'broker.qubitro.com', 1883, '995ca20f-70e3-48aa-b7fe-885d6f14d7b3', 'zWXPS6G$Q6Hj3Mg8aGm-5jLx9fzCiO-IUpDLXeI6', 300)
  m5mqtt.start()
  rgb.setBrightness(100)
  heart_0.setMode(0x03)
  temporary = 0
  body_temp = 36.5
  hr = 0
  sp02 = 0
  while True:
    angle = math.ceil((angle_0.read()) / 17 + 11) #math to adjust angle value to servo angle
    servo_0.write_angle(angle) 
    body_temp = ncir2_1.temperature_measure()
    hr = heart_0.getHeartRate()
    sp02 = heart_0.getSpO2()
    if temporary == 0: #turn off sensors
      label3.setFont(lcd.FONT_DefaultSmall)
      label3.setText('Waiting...')
      label5.setFont(lcd.FONT_DefaultSmall)
      label5.setText('Waiting...')
      label4.setFont(lcd.FONT_DefaultSmall)
      label4.setText('Waiting...')
    else: #turn on sensors
      label3.setText(str(body_temp))
      label4.setText(str(hr))
      label5.setText(str(sp02))
    validate_body_temp(temporary)
    validate_hr(temporary)
    validate_sp_02(temporary)
    if hr > 0 and body_temp > 30: #upload data to qubitro using mqtt for valid valid sensor values
      m5mqtt.publish(str('body_data'), str((py_2_json({'heart_rate':hr,'spo2':sp02,'body_temp':body_temp}))), 0)
    wait_ms(2)
