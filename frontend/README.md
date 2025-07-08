# Web UI para Control de OLED y LEDs

Esta es una interfaz web para controlar LEDs conectados a una Raspberry Pi y enviar texto o imágenes a una pantalla OLED. La web se comunica con un backend en con FastAPI.

---

## 📦 Requisitos

* Backend FastAPI corriendo en la Raspberry Pi.
* Raspberry Pi con los LEDs y la pantalla OLED conectados.
* Paciencia

---

## 📂 Estructura del proyecto

```
.
├── index.html       # Interfaz web principal
├── style.css        # Estilos para la UI
├── script.js        # JavaScript para enviar peticiones al backend
```

---

## 🚀 Cómo usar

1. **Clonar este repositorio en la Raspberry Pi**:

   ```bash
   git clone <URL_DEL_REPO>
   cd <REPO>
   ```

2. **Asegurate de que el backend esté corriendo** en la Raspberry Pi:

   ```bash
   sudo python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Edita `script.js`** y cambia la variable `API_URL` para que apunte a la IP del backend:

   ```js
   const API_URL = "http://<IP_DE_TU_RASPBERRY>:8000";
   ```

   Podes encontrar la IP de la Raspberry ejecutando:

   ```bash
   hostname -I
   ```

4. **Sirve la web en la Raspberry Pi con un servidor simple**:

   ```bash
   python3 -m http.server 8080
   ```

   Esto iniciará un servidor web accesible desde otros dispositivos en:

   ```
   http://<IP_DE_TU_RASPBERRY>:8080
   ```

5. **Abre el navegador en cualquier dispositivo** conectado a la misma red e ingresa la dirección anterior.

---

## 🖥️ Funcionalidades

* ✅ Encender y apagar LEDs individuales:

  * Rojo 🔴
  * Amarillo 🟡
  * Verde 🟢
  * Azul 🟦
  * Blanco ⚫

* ✅ Enviar texto para mostrarlo en la pantalla OLED.

* ✅ Subir imágenes para mostrarlas en la pantalla OLED.

---

## 🌐 Endpoints usados

* `POST /led/<color>/on`: enciende un LED y apaga los demás.
* `POST /led/<color>/off`: apaga un LED.
* `POST /oled/text`: muestra un mensaje en el OLED.
* `POST /oled/image`: sube una imagen al OLED.

---

## 📌 Nota

Si accedes desde otro dispositivo, asegúrate de que la Raspberry Pi y el dispositivo estén en la **misma red local** y que no haya firewalls bloqueando el puerto 8000.
