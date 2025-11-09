import time
from machine import Pin
import st7789py as st7789
import tft_config
import vga1_16x16 as font

# display y botón locales a la app
tft = tft_config.config(tft_config.WIDE)
button = Pin(9, Pin.IN, Pin.PULL_UP)
SEQUENCE = [0, 40, 80, 120, 70, 30, 10, 90]

def send_midi_control_change(controller, value, channel=0):
    """
    Simula el envío de un mensaje MIDI de Control Change.
    En una implementación real, esto enviaría datos por UART o USB MIDI.
    """
    print(
        "MIDI CC - Channel: {}, Controller: {}, Value: {}".format(
            channel + 1, controller, value
        )
    )


def trigger_step(param_value):
    tft.text(font, f"CC: {param_value}    ", 150, 100, st7789.YELLOW, st7789.BLACK)

def run():
    """
    Loop principal de la app.
    Se queda acá hasta que el usuario haga 'long press' para volver al menú.
    """
    hold_time_to_exit = 1500  # ms para volver al menú
    tft.fill(st7789.BLACK)
    tft.text(font, "MIDI Seq", 50, 50, st7789.CYAN, st7789.BLACK)
    time.sleep(0.5)

    bpm = 120
    interval_ms = 60000 // bpm
    last_tap = None
    next_step = 0
    current_step = 0
    while True:
        tft.text(font, f"bmp: {bpm}    ", 120, 70, st7789.WHITE, st7789.BLACK)
        # salir si mantienen apretado el botón
        button_held_ms = _button_held_ms(button)
        if button_held_ms >= hold_time_to_exit:
            return  # volvemos al launcher
        current = time.ticks_ms()
        if current > next_step:
            next_step = current + interval_ms
            trigger_step(SEQUENCE[current_step])
            current_step += 1
            if current_step == len(SEQUENCE):
                current_step = 0
        if button_held_ms > 10:
            if last_tap is not None:
                time_diff_ms = time.ticks_diff(current, last_tap)
                if time_diff_ms > 0:
                    bpm = 60000 // time_diff_ms
                    interval_ms = 60000 // bpm
                    next_step = current
            last_tap = current
        


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
