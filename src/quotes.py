import time
import random
from machine import Pin
import st7789py as st7789
import tft_config
import vga1_8x8 as font

# display y botón locales a la app
tft = tft_config.config(tft_config.WIDE)
button = Pin(9, Pin.IN, Pin.PULL_UP)

QUOTES = [
    "Cafe listo, bugs listos.",
    "Compilo, luego existo.",
    "Mi otro microcontrolador es un 6502.",
    "Funciona en mi placa™.",
    "Wi-Fi es mi superpoder.",
    "El LED parpadea, luego hay vida.",
    "RTFM: Realmente Tremendo Firmware Manual.",
    "El bug era un feature... hasta que no.",
    "GPIO: Grandes Ideas, Pocas Opciones.",
    "Dormir? Prefiero flashear.",
]

COLORS = [
    st7789.RED,
    st7789.BLACK,
    st7789.CYAN,
    st7789.color565(100, 100, 100),
    st7789.color565(0, 0, 100),
]


def center(text, fg=st7789.WHITE, bg=st7789.BLACK):
    length = len(text)
    tft.text(
        font,
        text,
        tft.width // 2 - length // 2 * font.WIDTH,
        tft.height // 2 - font.HEIGHT,
        fg,
        bg,
    )


def show_quote():
    color = random.choice(COLORS)
    quote = random.choice(QUOTES)
    tft.fill(color)
    tft.rect(0, 0, tft.width, tft.height, st7789.WHITE)
    center(quote, st7789.WHITE, color)


def run():
    """
    Loop principal de la app.
    Se queda acá hasta que el usuario haga 'long press' para volver al menú.
    """
    hold_time_to_exit = 1500  # ms para volver al menú
    tft.fill(st7789.BLACK)
    tft.rect(0, 0, tft.width, tft.height, st7789.WHITE)
    center("Quotes App", st7789.WHITE, st7789.BLACK)
    time.sleep(0.5)

    show_quote()
    
    while True:
        # salir si mantienen apretado el botón
        if _button_held_ms(button) >= hold_time_to_exit:
            return  # volvemos al launcher

        # si tocan corto -> nueva frase
        if not button.value():
            show_quote()
            time.sleep(0.2)  # debouncing básico


def _button_held_ms(btn):
    """
    Devuelve cuántos ms viene estando apretado el botón.
    Si no está apretado, devuelve 0.
    """
    if btn.value():  # pull-up => HIGH = suelto
        return 0
    start = time.ticks_ms()
    while not btn.value():
        time.sleep_ms(10)
    end = time.ticks_ms()
    return time.ticks_diff(end, start)