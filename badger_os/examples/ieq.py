import time
import badger2040
import badger_os
from breakout_bme68x import BreakoutBME68X
import pimoroni_i2c

# Display Setup
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(2)

WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

PINS_PICO_EXPLORER = {"sda": 4, "scl": 5}

i2c = pimoroni_i2c.PimoroniI2C(**PINS_PICO_EXPLORER)
#bme = BreakoutBME68X(i2c,0x77)
bme = BreakoutBME68X(i2c)

def draw_values(t,h,p):

    # Clear the display
    display.set_pen(15)
    display.clear()
    display.set_pen(0)
    display.set_font("sans")

    # Draw the page header
    display.set_pen(15)
    display.rectangle(0, 0, WIDTH, 20)
    display.set_pen(0)
    y=10
    display.text("IEQ", 0, 10, y, 0.5)
    scale=100
    n=1
    offset=30
    display.text("T="+t+" C", 0 , y+offset, scale, n)
    display.text("h="+h+" %", 0 , y+offset*2, scale, n)
    display.text("p="+p+" hPa", 0 , y+offset*3, scale, n)
    display.update()


    
while True:
    temperature, pressure, humidity, gas, status, _, _ = bme.read()
    heater = "Stable" if status else "Unstable" # & STATUS_HEATER_STABLE 
    #print("{:0.2f}c, {:0.2f}Pa, {:0.2f}%, {:0.2f} Ohms, Heater: {}".format(
    #    temperature, pressure, humidity, gas, heater))
    temp = str(round(temperature,1))
    press = str(round(pressure/100,1))
    humid = str(round(humidity,1))
    draw_values(temp, humid, press)
    time.sleep(10.0)
