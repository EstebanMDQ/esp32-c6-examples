import time
import random
from machine import Pin
import st7789py as st7789
import tft_config
import vga1_16x16 as font

# display y botón locales a la app
tft = tft_config.config(tft_config.WIDE)
button = Pin(9, Pin.IN, Pin.PULL_UP)


def show_dices(d1, d2):
    tft.fill(st7789.BLACK)
    tft.rect(0, 0, tft.width, tft.height, st7789.WHITE)
    tft.text(font, "Dados", 80, 50, st7789.CYAN, st7789.BLACK)
    if d1 is None and d2 is None:
        tft.text(font, "Presiona el boton", 40, 20, st7789.YELLOW, st7789.BLACK)
    else:
        tft.text(font, "{:02d}".format(d1), 40, 120, st7789.YELLOW, st7789.BLACK)
        tft.text(font, "{:02d}".format(d2), 200, 120, st7789.YELLOW, st7789.BLACK)


def run():
    """
    Loop principal de la app.
    Se queda acá hasta que el usuario haga 'long press' para volver al menú.
    """
    hold_time_to_exit = 1500  # ms para volver al menú
    show_dices(None, None)
    while True:
        # salir al launcher con long press
        press_time = _button_held_ms(button)
        if press_time >= hold_time_to_exit:
            return
        elif press_time > 20:
            show_dices(random.randint(1, 6), random.randint(1, 6))
        time.sleep_ms(10)


def _button_held_ms(btn):
    if btn.value():
        return 0
    start = time.ticks_ms()
    while not btn.value():
        time.sleep_ms(10)
    end = time.ticks_ms()
    return time.ticks_diff(end, start)        