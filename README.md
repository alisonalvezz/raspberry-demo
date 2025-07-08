# Control OLED y LEDs con Raspberry Pi

Este proyecto permite controlar LEDs conectados a una Raspberry Pi y mostrar texto o imágenes en una pantalla OLED mediante un backend en **FastAPI** y una interfaz web sencilla (para que todo entrara en la memoria de la Raspberry :D)

---

## 📖 Descripción del proyecto

La aplicación tiene dos componentes principales:

1. **Backend (FastAPI)**: API REST que gestiona los LEDs y la pantalla OLED a través de los pines GPIO de la Raspberry Pi.
2. **Frontend (Web UI)**: interfaz web que permite interactuar con el backend desde cualquier dispositivo en la misma red.

Se utiliza una Raspberry Pi como centro de control, con una pantalla OLED conectada vía I2C y varios LEDs conectados a pines GPIO con sus respectivas resistencias.

---

## 🐍 Librerías de Python usadas en el Backend

* **fastapi**: para crear la API REST.
* **uvicorn**: servidor ASGI para correr la app FastAPI.
* **gpiozero**: control sencillo de LEDs.
* **RPi.GPIO**: manejo de pines GPIO a nivel bajo.
* **adafruit-blinka**: soporte de CircuitPython en Raspberry Pi.
* **adafruit-circuitpython-ssd1306**: manejo de la pantalla OLED SSD1306.
* **Pillow**: procesamiento de imágenes antes de enviarlas al OLED.
* **busio**: para la comunicación I2C.
* **threading**: manejo de hilos para sincronizar acceso a la pantalla OLED.
* **io.BytesIO**: para la lectura de imágenes subidas.
* **ImageDraw, ImageFont, ImageOps** (de Pillow): para dibujar texto y ajustar imágenes.

---

## 🚀 Cómo usar

### Backend

1. Instala las dependencias:

   ```bash
   pip3 install -r requirements.txt
   ```
2. Corre el backend:

   ```bash
   sudo python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
3. Obtén la IP local:

   ```bash
   hostname -I
   ```

### Frontend

1. Sirve la carpeta web:

   ```bash
   python3 -m http.server 8080
   ```
2. Accede desde un navegador:

   ```
   http://<IP_DE_TU_RASPBERRY>:8080
   ```

---

## 🌱 Futuras mejoras

* 🌡️ **Agregar sensores** de temperatura y humedad como DHT11 (lo intenté y salió mal).
* 🔊 **Integrar bocinas** para notificaciones sonoras.
* 📝 **Persistencia** para guardar logs de acciones realizadas.
