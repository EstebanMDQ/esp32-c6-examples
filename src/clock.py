import network, ntptime, time
from machine import Pin
import st7789py as st7789
import tft_config
import vga1_16x16 as font

tft = tft_config.config(tft_config.WIDE)
button = Pin(9, Pin.IN, Pin.PULL_UP)
TZ_OFFSET = -3  # Argentina (UTC−3)


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(0.5)
    print("WiFi connected:", wlan.ifconfig())


def sync_time():
    try:
        ntptime.host = "pool.ntp.org"
        ntptime.settime()
        print("Time synced!")
    except Exception as e:
        print("NTP sync failed:", e)


def local_time():
    # Ajusta hora UTC con el offset en horas
    return time.localtime(time.time() + TZ_OFFSET * 3600)


def formatted_time():
    t = local_time()
    return "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])


def run():
    connect_wifi("SSID", "Password")
    sync_time()
    hold_time_to_exit = 1500  # ms
    while True:
        # dibujar "hora"
        tft.fill(st7789.BLACK)
        now_txt = formatted_time()
        tft.text(font, "Reloj", 15, 70, st7789.CYAN, st7789.BLACK)
        tft.text(font, now_txt, 10, 100, st7789.WHITE, st7789.BLACK)

        # salir al launcher con long press
        if _button_held_ms(button) >= hold_time_to_exit:
            return

        time.sleep(1)


def _button_held_ms(btn):
    if btn.value():
        return 0
    start = time.ticks_ms()
    while not btn.value():
        time.sleep_ms(10)
    end = time.ticks_ms()
    return time.ticks_diff(end, start)