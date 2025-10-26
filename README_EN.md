# esp32-c6-examples

MicroPython examples for the **Waveshare ESP32-C6-LCD-1.47** board.  
Includes a **launcher** with a menu to choose between several mini-apps:

- 🕒 **Clock** – displays local time (no flicker)  
- 💬 **Quotes** – generates random phrases with colored backgrounds  
- 🎲 **Dice** – simulates an animated dice roll  

---

## 🧠 Overview

This project implements a small demonstration “operating system” for MicroPython, featuring a **main menu (launcher)** that lets you navigate between apps using the board’s **BOOT** button:

- **Short press** → move to the next menu item  
- **Long press** → launch the selected app  
- Inside each app, a long press returns to the main menu  

Each application is defined as a module inside the `apps/` directory, with a main `run()` function.

---

## 📁 Project structure

```
esp32-c6-examples/
│
├── main.py                 # Main launcher
├── tft_config.py           # ST7789 display configuration
├── clock.py                # Clock app
├── quotes.py               # Random phrases app
└── dices.py                # Dice app
```

---

## 🚀 Installation

1. Flash **MicroPython for ESP32-C6**.  
   Instructions can be found here: https://informalthinkers.com/blog/2025-10-17-esp32-c6-micropython.html

2. Copy all repository files to the board:

   ```bash
   mpremote cp -r esp32-c6-examples/src/* :
   ```

3. Restart the board.  
   The launcher will start automatically and display the menu on the screen.

---

## 🧭 Usage

- **BOOT BUTTON**:
  - *Short tap:* switch to the next app  
  - *Hold (>0.6 s):* launch the selected app  
- **Inside an app:**
  - *Hold (>1.5 s):* return to the menu  

---

## ⚙️ Requirements

- **Waveshare ESP32-C6-LCD-1.47** board  
- MicroPython 1.23+ compiled for ESP32-C6  
- Libraries:
  - `st7789py`
  - `vga1_8x8`
  - `tft_config` (included in the repo)
- Built-in VGA 8x8 font (included)
- USB-C connection to upload scripts or access the REPL  

---

## 🕒 Timezone configuration

In `clock.py`, edit:

```python
TZ_OFFSET = -3  # Argentina (UTC−3)
```

Adjust it for your region.  
If you sync time via Wi-Fi (using `ntptime`), the clock will display the correct local time.

---

## 💡 Ideas for extensions

- Add more apps to the menu  
- Display temperature, light sensor readings, or animations  
- Use `shared_ctx` to reuse the same `tft` object across apps  

---

## 🧑‍💻 Author

Project by **Esteban Soler**, 2025.  
Designed to experiment with the **ESP32-C6-LCD-1.47** and learn MicroPython development.

---

## 📸 Credits

- [Waveshare ESP32-C6-LCD-1.47](https://www.waveshare.com/esp32-c6-lcd-1.47.htm)  
- ST7789 library adapted from [micropython-st7789](https://github.com/russhughes/st7789_mpy)
