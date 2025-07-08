# FastAPI OLED & LED Controller

Este proyecto es una API construida con FastAPI para controlar LEDs conectados a una Raspberry Pi y mostrar texto o imágenes en una pantalla OLED

## Requisitos

- Raspberry Pi
- Python 3.7+
- Pantalla OLED
- LEDs conectados a pines GPIO
- Paciencia

## Instalación

1. Clona el repositorio:

2. Instala las dependencias:
   pip install -r requirements.txt

3. Habilita I2C en la Raspberry Pi (si no lo has hecho):
   sudo raspi-config

   Ve a Interfacing Options > I2C > Enable.

## Ejecución

Corre el backend con:

   sudo python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

⚠️ Se usa sudo porque se accede a GPIO.  

Esto iniciará un servidor en tu red local. Para saber la IP a la que debes acceder desde otro dispositivo (como tu navegador o Postman), ejecuta:

   hostname -I

y el resultado será algo como:

   192.168.1.42 172.17.0.1

En este ejemplo la IP local es **192.168.1.42**, por lo que puedes acceder a la API en:  

   http://192.168.1.42:8000

## Probar la API

Puedes abrir en tu navegador la documentación interactiva que genera FastAPI:  

   http://<IP_LOCAL>:8000/docs

O usando la otra interfaz de FastAPI:

   http://<IP_LOCAL>:8000/redoc


## Endpoints principales

- POST /oled/text
  Muestra texto en la pantalla OLED.
  JSON body:
  {
    "message": "Hola Mundo"
  }

- POST /oled/image
  Envía una imagen para mostrarla en la pantalla OLED.
  Form-data:
    - file: archivo de imagen
    - rotation (opcional): rotación (0, 90, 180, 270)

- POST /led/{color}/on
  Enciende un LED (y apaga los otros).

- POST /led/{color}/off
  Apaga un LED.

## Nota

Los LEDs están configurados en los pines GPIO:
- GPIOZero: rojo (17), amarillo (27), verde (22)
- RPi.GPIO: azul (5), blanco (6)

Modifica los pines en main.py si es necesario.

## Hardware

- Raspberry Pi (probado en Raspberry Pi 3)
- OLED Display (I2C)
- LEDs conectados a GPIO 
