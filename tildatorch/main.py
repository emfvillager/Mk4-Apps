"""This app goes with the Torch Tutorial"""

___name___         = "Tilda Torch"
___license___      = "MIT"
___dependencies___ = ["sleep"]
___categories___   = ["EMF"]
___bootstrapped___ = False

import ugfx, os, time, sleep
from tilda import Buttons
from machine import Pin

torch = Pin(Pin.GPIO_FET)

ugfx.init()
Pin(Pin.PWM_LCD_BLIGHT).on()
ugfx.clear()

ugfx.text(5, 5, "TORRRRRRCH!!!!!", ugfx.BLACK)
torch.on()

while (not Buttons.is_pressed(Buttons.BTN_A)) and (not Buttons.is_pressed(Buttons.BTN_B)) and (not Buttons.is_pressed(Buttons.BTN_Menu)):
    sleep.wfi()

torch.off()

ugfx.clear()
