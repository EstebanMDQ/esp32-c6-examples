import sys 
import time
from machine import Pin
import st7789py as st7789
import tft_config
import vga1_16x16 as font
import vga1_8x8 as font2

# importá acá las apps que quieras ofrecer en el menú
# import quotes
# import clock
# import apps.clock_app as clock_app
# etc...

# Configuración común de pantalla y botón
tft = tft_config.config(tft_config.WIDE)
button = Pin(9, Pin.IN, Pin.PULL_UP)

# Lista de apps del menú
APPS = [
    {"name": "Frases", "module": "quotes"},
    {"name": "Reloj", "module": "clock"},
    {"name": "Dados", "module": "dices"},
    {"name": "MIDI Seq", "module": "midi_seq"},
]

# ------------------------
# Helpers de UI y botón
# ------------------------


def draw_menu(selected_idx):
    tft.fill(st7789.BLACK)
    # 172
    # tft.rect(0, 35, tft.width, tft.height - 35, st7789.WHITE)
    title = "Launcher"
    tft.text(font, title, 80, 50, st7789.CYAN, st7789.BLACK)
    y = 60 + font.HEIGHT
    for i, app in enumerate(APPS):
        prefix = ">" if i == selected_idx else " "
        line = "{} {}".format(prefix, app["name"])
        color = st7789.WHITE if i == selected_idx else st7789.color565(150, 150, 150)
        tft.text(font, line, 10, y, color, st7789.BLACK)
        y += font.HEIGHT + 4
    tft.text(
        font2,
        "tap=next                     hold=run",
        10,
        tft.height - font.HEIGHT - 35,
        st7789.color565(80, 80, 80),
        st7789.BLACK,
    )


def button_held_ms(btn):
    # si está suelto => 0
    if btn.value():
        return 0
    start = time.ticks_ms()
    while not btn.value():
        time.sleep_ms(10)
    end = time.ticks_ms()
    return time.ticks_diff(end, start)


def wait_for_press_and_measure(btn):
    """
    Bloquea hasta que detecta que el botón fue presionado y soltado.
    Devuelve cuánto tiempo (ms) estuvo presionado.
    """
    # esperar a que lo aprieten
    while btn.value():  # HIGH = suelto
        time.sleep_ms(10)
    # medir mientras está apretado
    start = time.ticks_ms()
    while not btn.value():
        time.sleep_ms(10)
    end = time.ticks_ms()
    return time.ticks_diff(end, start)


def launch_app(module_name):
    """
    Importa dinámicamente el módulo (por ej. "apps.quotes_app"),
    llama module.run(), y luego intenta liberar RAM.
    """
    # importar módulo
    mod = __import__(module_name)
    # __import__("apps.quotes_app") devuelve el top-level "apps",
    # así que tenemos que bajar hasta el submódulo real:
    for part in module_name.split(".")[1:]:
        mod = getattr(mod, part)

    # correr la app
    if hasattr(mod, "run"):
        mod.run()
    else:
        # fallback básico en pantalla si no tiene run()
        tft.fill(st7789.BLACK)
        tft.text(font, "No run()", 10, 10, st7789.RED, st7789.BLACK)
        time.sleep(1)

    # limpieza opcional:
    # sacamos el módulo de sys.modules para que, cuando volvamos
    # a importarlo más tarde, se recargue desde cero.
    if module_name in sys.modules:
        del sys.modules[module_name]


# ------------------------
# Loop principal del launcher
# ------------------------

def main():
    selected = 0
    draw_menu(selected)
    time.sleep_ms(200)

    while True:
        press_time = wait_for_press_and_measure(button)

        if press_time < 600:
            # corto -> siguiente opción
            selected = (selected + 1) % len(APPS)
            draw_menu(selected)
            time.sleep_ms(200)  # debouncing visual
        else:
            # long press: lanzar app dinámica
            tft.fill(st7789.BLACK)
            tft.text(font, "Launching...", 10, 10, st7789.WHITE, st7789.BLACK)

            app_info = APPS[selected]
            module_name = app_info["module"]

            launch_app(module_name)

            # cuando la app vuelve (return), redibujamos menú
            draw_menu(selected)
            time.sleep_ms(200)

main()