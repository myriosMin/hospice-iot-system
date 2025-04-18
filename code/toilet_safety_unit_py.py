from m5stack import *
from m5ui import *
from uiflow import *
import wifiCfg
import time
import unit


setScreenColor(0x45b1e8)
servo_0 = unit.get(unit.SERVO, unit.PORTB)
pahub_0 = unit.get(unit.PAHUB, unit.PORTA, 0x70)
pbhub_0 = unit.get(unit.PBHUB, unit.PAHUB0)
rfid_0 = unit.get(unit.RFID, unit.PAHUB5)
gesture_0 = unit.get(unit.GESTURE, unit.PAHUB2)


get_gesture = None
Lights = None
FloorWetness = None
Fall = None
i = None

"""The earth sensor we used did not work properly when it is connected to PbHub; under normal condition (i.e., when it is not wet) it reads over 600 moisture, and when the sensor is touched with a wet finger, it reads around 400 moisture.
We tried adjusting the sensitivity, but the earth sensor works as expected only when it is connected to Port B directly, and it refuses to work properly though Port B.
"""

image0 = M5Img(110, 70, "res/16.jpg", True)
label0 = M5TextBox(40, 205, "LOCK ", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
label1 = M5TextBox(209, 205, "UNLOCK", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
title0 = M5Title(title="Toilet System", x=115, fgcolor=0x000000, bgcolor=0xc7c7c7)
label2 = M5TextBox(146, 210, "Text", lcd.FONT_Default, 0xFFFFFF, rotate=0)
image1 = M5Img(110, 70, "res/15.jpg", True)
label3 = M5TextBox(96, 40, "Have you fallen?", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label4 = M5TextBox(10, 50, "Click the  ", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label5 = M5TextBox(10, 70, "middle button", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label10 = M5TextBox(134, 195, "Wetness", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label6 = M5TextBox(10, 90, "within", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label7 = M5TextBox(9, 135, "seconds not to", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label8 = M5TextBox(21, 110, "label8", lcd.FONT_Comic, 0xFFFFFF, rotate=0)
label9 = M5TextBox(10, 155, "turn on the", lcd.FONT_Default, 0xFFFFFF, rotate=0)


#turn off toilet light after use
def Turn_Off_Lights():
  global get_gesture, Lights, FloorWetness, Fall, i
  if Lights == 1:
    rgb.setColorAll(0x000000)
    Lights = 0
  else:
    Lights = 0

#defect fall in toilet
def Fall_Detector():
  global get_gesture, Lights, FloorWetness, Fall, i
  get_gesture = gesture_0.get_gesture()
  if get_gesture == (gesture_0.GestureDown):
    #show fall instructions
    label3.show()
    label4.show()
    label5.show()
    label6.show()
    label7.show()
    label9.show()
    #count 5 seconds before turning on the alarm
    for i in range(5, -1, -1):
      label8.show()
      label8.setText(str(i))
      wait(1)
      image1.changeImg("res/16.jpg")
      if not (btnB.isPressed()) and i != 0: #continue with next iteration if the button is not pressed
        continue
      elif btnB.isPressed(): #stop the alarm and change text upon button press
        label3.hide()
        label6.hide()
        label7.hide()
        label8.hide()
        label9.hide()
        image1.changeImg("res/15.jpg")
        label4.setText('Glad that you')
        label5.setText('are safe.')
        rgb.setColorAll(0x33ff33)
        wait(3)
        rgb.setColorAll(0x000000)
        label4.hide()
        label5.hide()
        break
      elif i == 0: #counter becomes zerp; turn on fall alarm
        Fall = 0
        while not ((btnC.isPressed()) or (rfid_0.isCardOn()) == 1):
          wait(0.5)
          pbhub_0.setColor(1, 0, 3, 0xff0000)
          speaker.tone(1800, 200)
          wait(0.5)
          pbhub_0.setColor(1, 0, 3, 0x000000)
          speaker.tone(1800, 200)
          wait(0.5)


def buttonA_wasPressed(): #lock toilet after entering
  global get_gesture, Lights, FloorWetness, Fall, i
  if 600 < FloorWetness: #not wet
    servo_0.write_angle(180)
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonC_wasPressed(): #unlock toilet to go out after use
  global get_gesture, Lights, FloorWetness, Fall, i
  pbhub_0.setColor(1, 0, 3, 0x006600)
  servo_0.write_angle(90)
  wait(5)
  servo_0.write_angle(180)
  Turn_Off_Lights()
  pass
btnC.wasPressed(buttonC_wasPressed)


wifiCfg.doConnect('Myrios', 'abcdefghi')
if wifiCfg.wlan_sta.isconnected():
  gesture_0.begin()
  Fall = 0
  get_gesture = 0
  servo_0.write_angle(180)
  image0.hide()
  image1.hide()
  pbhub_0.setColor(1, 0, 3, 0x006600)
  while True:
    #hide fall texts
    label3.hide()
    label4.hide()
    label5.hide()
    label6.hide()
    label7.hide()
    label8.hide()
    label9.hide()
    label2.setText(str(pbhub_0.analogRead(0)))
    FloorWetness = pbhub_0.analogRead(0)
    #show good/bad image based on floor wetness
    if FloorWetness > 600: #not wet
      image0.hide()
      image1.show()
    if FloorWetness > 600 and (rfid_0.isCardOn()) == 1: #not wet and person comes
      wait(1)
      servo_0.write_angle(90) #unlock door
      rgb.setColorAll(0xffffff) 
      pbhub_0.setColor(1, 0, 3, 0x660000)
      Lights = 1
      wait(3)
      while (rfid_0.isCardOn()) == 0: #detect fall until RFID is read on person exiting
        rgb.setColorAll(0x33ffff)
        Fall_Detector()
      #hide text if there is no actual fall after downward gesture defection
      label3.hide()
      label4.hide()
      label5.hide()
      label6.hide()
      label7.hide()
      label8.hide()
      label9.hide()
    elif FloorWetness < 600: #floor is wet; lock the door 
      label10.setColor(0xff0000)
      label2.setColor(0xff0000)
      image1.hide()
      image0.show()
    wait_ms(2)
