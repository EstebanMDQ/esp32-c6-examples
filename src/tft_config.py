"""Waveshare ESP32-C6-LCD-1.47

https://www.waveshare.com/wiki/ESP32-C6-LCD-1.47

172x320 ST7789 display with ESP32-C6
Note: Using 240x320 mode with offset for 172x320 display
"""

from machine import Pin, SPI
import st7789py as st7789

TFA = 0
BFA = 0
WIDE = 1
TALL = 0
SCROLL = 0      # orientation for scroll.py
FEATHERS = 1    # orientation for feathers.py

def config(rotation=0):
    """
    Configures and returns an instance of the ST7789 display driver.

    Args:
        rotation (int): The rotation of the display (default: 0).

    Returns:
        ST7789: An instance of the ST7789 display driver.
    """

    return st7789.ST7789(
        SPI(1, baudrate=80000000, sck=Pin(7), mosi=Pin(6), miso=Pin(5)),
        240,
        320,
        reset=Pin(21, Pin.OUT),
        cs=Pin(14, Pin.OUT),
        dc=Pin(15, Pin.OUT),
        backlight=Pin(22, Pin.OUT),
        rotation=rotation)