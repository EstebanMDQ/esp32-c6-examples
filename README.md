# esp32-c6-examples

Ejemplos en MicroPython para la **placa ESP32-C6-LCD-1.47** de Waveshare.  
Incluye un **launcher** con menú para elegir entre varias mini-apps:

- 🕒 **Reloj** – muestra la hora local (sin parpadeos)
- 💬 **Frases** – genera frases aleatorias con fondos de colores
- 🎲 **Dados** – simula una tirada de dados animada

---

## 🧠 Descripción general

El proyecto implementa un pequeño "sistema operativo" de demostración para MicroPython, con un **menú principal (launcher)** que permite navegar entre aplicaciones usando el botón **BOOT** de la placa:

- **Presionar** brevemente → pasa al siguiente ítem del menú  
- **Mantener presionado** → ejecuta la app seleccionada  
- Dentro de cada app, mantener presionado el botón vuelve al menú

Cada aplicación está definida como un módulo en el directorio `apps/`, con una función principal `run()`.

---

## 📁 Estructura del proyecto

```
esp32-c6-examples/
│
├── main.py                 # Launcher principal
├── tft_config.py           # Configuración del display ST7789
├── clock.py                # App de reloj
├── quotes.py               # App de frases aleatorias
└── dices.py                # App de dados
```

---

## 🚀 Instalación

1. Flasheá **MicroPython para ESP32-C6** las instrucciones de como hacerlo están aca https://informalthinkers.com/blog/2025-10-17-esp32-c6-micropython.html

2. Copiá todos los archivos del repositorio a la placa:

   ```bash
   mpremote cp -r esp32-c6-examples/src/* :
   ```

3. Reiniciá la placa.  
   El launcher se cargará automáticamente y mostrará el menú en pantalla.

---

## 🧭 Uso

- **BOTÓN BOOT**:
  - *Tap corto:* cambia la app seleccionada
  - *Mantener presionado (>0.6 s):* ejecuta la app seleccionada  
- **Dentro de una app:**
  - *Mantener presionado (>1.5 s):* vuelve al menú

---

## ⚙️ Requisitos

- Placa **Waveshare ESP32-C6-LCD-1.47**
- MicroPython 1.23+ compilado para ESP32-C6
- Librerías:
  - `st7789py`
  - `vga1_8x8`
  - `tft_config` (incluida en el repo)
- Fuente VGA 8x8 integrada en el repo
- Conexión USB-C para subir los scripts o ver el REPL

---

## 🕒 Configurar zona horaria
En clock.py, editar
```python
TZ_OFFSET = -3  # Argentina (UTC−3)
```

Podés modificarlo según tu región.  
Si sincronizás hora por Wi-Fi (con `ntptime`), el reloj mostrará la hora local correcta.

---

## 💡 Ideas para extender

- Agregar más apps al menú
- Mostrar temperatura, sensor de luz, o animaciones
- Usar `shared_ctx` para reutilizar el mismo objeto `tft` entre apps

---

## 🧑‍💻 Autor

Proyecto de **Esteban Soler**, 2025.  
Diseñado para experimentar con la **ESP32-C6-LCD-1.47** y aprender desarrollo con MicroPython.

---

## 📸 Créditos

- [Waveshare ESP32-C6-LCD-1.47](https://www.waveshare.com/esp32-c6-lcd-1.47.htm)
- Librería ST7789 adaptada de [micropython-st7789](https://github.com/russhughes/st7789_mpy)

