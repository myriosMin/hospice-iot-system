from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
from m5mqtt import M5mqtt
from libs.json_py import *
import unit


setScreenColor(0x000000)
pahub_0 = unit.get(unit.PAHUB, unit.PORTA, 0x70)
env2_0 = unit.get(unit.ENV2, unit.PAHUB0)
tvoc_0 = unit.get(unit.TVOC, unit.PAHUB1)
servo_0 = unit.get(unit.SERVO, unit.PORTB)


var1 = None
var2 = None
min_humidity = None
max_humidity = None
min_temp = None
max_temp = None
humid_condition = None
temp_condition = None
tvoc_condition = None
condition = None #overall condition used to control RGB bar
tvoc_limit = None
body_temp_condition = None
ac_status = None
ventilation = None



title0 = M5Title(title="Indoor Environment Control Unit", x=3, fgcolor=0x000000, bgcolor=0x45b1e8)
image0 = M5Img(5, 25, "res/default.jpg", True)
image1 = M5Img(110, 25, "res/default.jpg", True)
image2 = M5Img(215, 25, "res/default.jpg", True)
rectangle0 = M5Rect(5, 130, 100, 85, 0x000000, 0x45b1e8)
label0 = M5TextBox(60, 220, "-1", lcd.FONT_Default, 0xFFFFFF, rotate=0)
rectangle1 = M5Rect(110, 130, 100, 85, 0x000000, 0x45b1e8)
rectangle2 = M5Rect(215, 130, 100, 50, 0x000000, 0x45b1e8)
label1 = M5TextBox(240, 220, "+1", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label2 = M5TextBox(140, 220, "Toggle", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label3 = M5TextBox(25, 135, "Humidity", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label4 = M5TextBox(120, 135, "Room Temp", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label5 = M5TextBox(245, 135, "TVOC", lcd.FONT_Default, 0xFFFFFF, rotate=0)
rectangle3 = M5Rect(215, 180, 100, 35, 0x000000, 0x45b1e8)
label6 = M5TextBox(247, 182, "A/C:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label7 = M5TextBox(238, 198, "Venti:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label8 = M5TextBox(40, 155, "08", lcd.FONT_Comic, 0xFFFFFF, rotate=0)
label9 = M5TextBox(145, 155, "09", lcd.FONT_Comic, 0xFFFFFF, rotate=0)
label10 = M5TextBox(250, 155, "10", lcd.FONT_Comic, 0xFFFFFF, rotate=0)
label11 = M5TextBox(20, 190, "11", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label12 = M5TextBox(73, 190, "12", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label13 = M5TextBox(125, 190, "13", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label14 = M5TextBox(177, 190, "14", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label15 = M5TextBox(280, 182, "15", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label16 = M5TextBox(280, 198, "16", lcd.FONT_Default, 0xFFFFFF, rotate=0)
line0 = M5Line(M5Line.PLINE, 20, 205, 45, 205, 0xFFFFFF)
line1 = M5Line(M5Line.PLINE, 125, 205, 150, 205, 0xFFFFFF)
line2 = M5Line(M5Line.PLINE, 73, 190, 98, 190, 0xFFFFFF)
line3 = M5Line(M5Line.PLINE, 177, 190, 202, 190, 0xFFFFFF)
line4 = M5Line(M5Line.PLINE, 40, 190, 40, 205, 0xFFFFFF)
line5 = M5Line(M5Line.PLINE, 95, 190, 95, 205, 0xFFFFFF)
line6 = M5Line(M5Line.PLINE, 147, 190, 147, 205, 0xFFFFFF)
line7 = M5Line(M5Line.PLINE, 200, 190, 200, 205, 0xFFFFFF)
triangle0 = M5Triangle(95, 190, 92, 195, 98, 195, 0xFFFFFF, 0xFFFFFF)
triangle1 = M5Triangle(200, 190, 197, 195, 203, 195, 0xFFFFFF, 0xFFFFFF)
triangle2 = M5Triangle(40, 205, 37, 200, 43, 200, 0xFFFFFF, 0xFFFFFF)
triangle3 = M5Triangle(147, 205, 144, 200, 150, 200, 0xFFFFFF, 0xFFFFFF)

from numbers import Number


#var1 and var2 are used to toggle four variables (odd/even - four combinations for 2 var)
#change text color of the selected variable
def toggle_limits():
  global var1, var2, min_humidity, max_humidity, min_temp, max_temp, humid_condition, temp_condition, tvoc_condition, condition, tvoc_limit, body_temp_condition, ac_status, ventilation
  if var1 % 2 == 0 and var2 % 2 == 0:
    label14.setColor(0xffffff)
    label11.setColor(0x3366ff)
  elif var1 % 2 == 1 and var2 % 2 == 0:
    label11.setColor(0xffffff)
    label12.setColor(0x3366ff)
  elif var1 % 2 == 1 and var2 % 2 == 1:
    label12.setColor(0xffffff)
    label13.setColor(0x3366ff)
  else:
    label13.setColor(0xffffff)
    label14.setColor(0x3366ff)

#determine himudity, change image accordingly and change the overall conditon
def determine_humidity():
  global var1, var2, min_humidity, max_humidity, min_temp, max_temp, humid_condition, temp_condition, tvoc_condition, condition, tvoc_limit, body_temp_condition, ac_status, ventilation
  if (env2_0.humidity) < min_humidity:
    humid_condition = 'low'
    condition = False
    image0.changeImg("res/L-Humidity.png")
  elif (env2_0.humidity) > max_humidity:
    humid_condition = 'high'
    condition = False
    image0.changeImg("res/H-Humidity.png")
  else:
    humid_condition = 'normal'
    condition = True
    image0.changeImg("res/G-Humidity.png")

#determine room temperature, change image accordingly and change the overall conditon
def determine_room_temp():
  global var1, var2, min_humidity, max_humidity, min_temp, max_temp, humid_condition, temp_condition, tvoc_condition, condition, tvoc_limit, body_temp_condition, ac_status, ventilation
  if (env2_0.temperature) < min_temp:
    temp_condition = 'low'
    condition = False
    image1.changeImg("res/L-Temp.png")
  elif (env2_0.temperature) > max_temp:
    temp_condition = 'high'
    condition = False
    image1.changeImg("res/H-Temp.png")
  else:
    temp_condition = 'normal'
    condition = True
    image1.changeImg("res/G-Temp.png")

#determine air quality (tvoc) (co2 and other sensor values can be used as well), change image accordingly and change the overall conditon
def determine_tvoc():
  global var1, var2, min_humidity, max_humidity, min_temp, max_temp, humid_condition, temp_condition, tvoc_condition, condition, tvoc_limit, body_temp_condition, ac_status, ventilation
  if (tvoc_0.TVOC) > tvoc_limit:
    tvoc_condition = False
    condition = False
    image2.changeImg("res/B-TVOC.png")
  else:
    tvoc_condition = True
    condition = True
    image2.changeImg("res/G-TVOC.png")


#increase var1 and var2 accordingly to get desired format (4 odd/even combinations)
def buttonB_wasPressed():
  global var1, var2, min_humidity, max_humidity, min_temp, max_temp, humid_condition, temp_condition, tvoc_condition, condition, tvoc_limit, body_temp_condition, ac_status, ventilation
  if var1 == var2 and var1 % 2 == 0:
    var1 = (var1 if isinstance(var1, Number) else 0) + 1
  elif var1 == var2 and var1 % 2 == 1:
    var1 = (var1 if isinstance(var1, Number) else 0) + 1
  else:
    var2 = (var2 if isinstance(var2, Number) else 0) + 1
  pass
btnB.wasPressed(buttonB_wasPressed)

#decrease the selected limit by 1 
def buttonA_wasPressed():
  global var1, var2, min_humidity, max_humidity, min_temp, max_temp, humid_condition, temp_condition, tvoc_condition, condition, tvoc_limit, body_temp_condition, ac_status, ventilation
  if var1 % 2 == 0 and var2 % 2 == 0:
    min_humidity = (min_humidity if isinstance(min_humidity, Number) else 0) + -1
  elif var1 % 2 == 1 and var2 % 2 == 0:
    max_humidity = (max_humidity if isinstance(max_humidity, Number) else 0) + -1
  elif var1 % 2 == 1 and var2 % 2 == 1:
    min_temp = (min_temp if isinstance(min_temp, Number) else 0) + -1
  else:
    max_temp = (max_temp if isinstance(max_temp, Number) else 0) + -1
  pass
btnA.wasPressed(buttonA_wasPressed)

#increase the selected limit by 1
def buttonC_wasPressed():
  global var1, var2, min_humidity, max_humidity, min_temp, max_temp, humid_condition, temp_condition, tvoc_condition, condition, tvoc_limit, body_temp_condition, ac_status, ventilation
  if var1 % 2 == 0 and var2 % 2 == 0:
    min_humidity = (min_humidity if isinstance(min_humidity, Number) else 0) + 1
  elif var1 % 2 == 1 and var2 % 2 == 0:
    max_humidity = (max_humidity if isinstance(max_humidity, Number) else 0) + 1
  elif var1 % 2 == 1 and var2 % 2 == 1:
    min_temp = (min_temp if isinstance(min_temp, Number) else 0) + 1
  else:
    max_temp = (max_temp if isinstance(max_temp, Number) else 0) + 1
  pass
btnC.wasPressed(buttonC_wasPressed)


wifiCfg.doConnect('Myrios', 'abcdefghi')
if wifiCfg.wlan_sta.isconnected():
  m5mqtt = M5mqtt('env_unit', 'broker.qubitro.com', 1883, '5ad1ffd6-d9a8-4e01-9a2b-de9a0f053163', 'w2YLdJEgCOSk2mUHX5BiQjar6DD2Rr3JbEFmr5RP', 300)
  m5mqtt.start()
  min_humidity = 40
  max_humidity = 65
  min_temp = 23
  max_temp = 30
  tvoc_limit = 220
  condition = True
  tvoc_condition = True
  body_temp_condition = 'normal'
  humid_condition = 'normal'
  temp_condition = 'normal'
  ac_status = 0
  ventilation = 0
  var1 = 0
  var2 = 0
  servo_0.write_angle(0)
  while True:
    label8.setText(str(env2_0.humidity))
    label9.setText(str(env2_0.temperature))
    label10.setText(str(tvoc_0.TVOC))
    label15.setText(str(ac_status))
    label16.setText(str(ventilation))
    label11.setText(str(min_humidity))
    label12.setText(str(max_humidity))
    label13.setText(str(min_temp))
    label14.setText(str(max_temp))
    #pre-set good-condition images
    image0.changeImg("res/G-Humidity.png")
    image1.changeImg("res/G-Temp.png")
    image2.changeImg("res/G-TVOC.png")
    toggle_limits()
    determine_humidity()
    determine_room_temp()
    determine_tvoc()
    #set RGB bar to red except for normal conditions of all sensors
    if condition == False:
      rgb.setColorAll(0xff0000)
    elif humid_condition != 'normal':
      rgb.setColorAll(0xff0000)
    elif temp_condition != 'normal':
      rgb.setColorAll(0xff0000)
    elif tvoc_condition == False:
      rgb.setColorAll(0xff0000)
    else:
      rgb.setColorAll(0x33ff33)
    #turn on/off air conditioner based on humidity and room temp values
    if humid_condition == 'normal' and temp_condition == 'normal':
      ac_status = 0
    else:
      ac_status = 1
      #turn on/off air purifier and window based on air quality
    if tvoc_condition == True:
      ventilation = 0
      servo_0.write_angle(0)
    else:
      ventilation = 1
      servo_0.write_angle(90)
    #upload sensor data to qubitro using mqtt for further analysis
    m5mqtt.publish(str('env_data'), str((py_2_json({'humidity':(env2_0.humidity),'room_temp':(env2_0.temperature),'tvoc':(tvoc_0.TVOC)}))), 0)
    wait_ms(2)
