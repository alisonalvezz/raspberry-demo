from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gpiozero import LED as GPIOZeroLED
import RPi.GPIO as GPIO
from io import BytesIO
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont, ImageOps
from threading import Lock
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LED_PINS_GPIOZERO = {}
LED_PINS_RPIO = {}

i2c = busio.I2C(3, 2)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.show()

width = oled.width
height = oled.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

oled_lock = Lock()

def display_message(text: str, delay: float = 2.5):
    with oled_lock:
        oled.fill(0)
        oled.show()
        bbox = font.getbbox("A")
        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]
        max_lines = height // char_height
        max_chars_per_line = width // char_width

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if len(test_line) <= max_chars_per_line:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                while len(word) > max_chars_per_line:
                    lines.append(word[:max_chars_per_line])
                    word = word[max_chars_per_line:]
                current_line = word

        if current_line:
            lines.append(current_line)

        pages = [lines[i:i + max_lines] for i in range(0, len(lines), max_lines)]

        for page_lines in pages:
            oled.fill(0)
            draw.rectangle((0, 0, width, height), outline=0, fill=0)
            for idx, line in enumerate(page_lines):
                y = idx * char_height
                draw.text((0, y), line, font=font, fill=255)
            oled.image(image)
            oled.show()
            time.sleep(delay)


@app.post("/oled/image")
async def upload_and_display_image(file: UploadFile, rotation: int = 0):
    try:
        contents = await file.read()
        img = Image.open(BytesIO(contents))
        img = ImageOps.exif_transpose(img)
        img = img.resize((width, height), Image.LANCZOS).convert("1")

        if rotation in [90, 180, 270]:
            img = img.rotate(rotation, expand=True)

        with oled_lock:
            oled.fill(0)
            oled.image(img)
            oled.show()

        return {"status": "success", "message": f"Imagen mostrada con rotación {rotation}°"}
    except Exception as e:
        return {"status": "error", "message": f"Error al procesar imagen: {str(e)}"}

class TextInput(BaseModel):
    message: str

@app.post("/oled/text")
def show_text(input_data: TextInput):
    display_message(input_data.message)
    return {"status": "success", "message": "Texto mostrado correctamente"}

@app.on_event("startup")
def setup_leds():
    global LED_PINS_GPIOZERO, LED_PINS_RPIO

    LED_PINS_GPIOZERO = {
        "red": GPIOZeroLED(17),
        "yellow": GPIOZeroLED(27),
        "green": GPIOZeroLED(22),
    }

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    LED_PINS_RPIO = {
        "blue": 5,
        "white": 6,
    }


@app.on_event("shutdown")
def cleanup():
    print("\nCerrando LEDs y OLED...")
    for led in LED_PINS_GPIOZERO.values():
        led.off()
        led.close()

    for pin in LED_PINS_RPIO.values():
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

    with oled_lock:
        oled.fill(0)
        oled.show()


@app.post("/led/{color}/on")
def turn_on_led(color: str):
    for other_color, led in LED_PINS_GPIOZERO.items():
        if other_color != color:
            led.off()
    for other_color, pin in LED_PINS_RPIO.items():
        if other_color != color:
            GPIO.output(pin, GPIO.LOW)

    if color in LED_PINS_GPIOZERO:
        LED_PINS_GPIOZERO[color].on()
        return {"status": "success", "message": f"LED {color} encendida y otras apagadas"}
    elif color in LED_PINS_RPIO:
        GPIO.output(LED_PINS_RPIO[color], GPIO.HIGH)
        return {"status": "success", "message": f"LED {color} encendida y otras apagadas"}
    else:
        return {"status": "error", "message": "Color inválido"}

@app.post("/led/{color}/off")
def turn_off_led(color: str):
    if color in LED_PINS_GPIOZERO:
        LED_PINS_GPIOZERO[color].off()
        return {"status": "success", "message": f"LED {color} apagado"}
    elif color in LED_PINS_RPIO:
        GPIO.output(LED_PINS_RPIO[color], GPIO.LOW)
        return {"status": "success", "message": f"LED {color} apagado"}
    else:
        return {"status": "error", "message": "Color inválido"}