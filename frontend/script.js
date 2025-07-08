const API_URL = "http://192.168.1.22:8000";

let ledStates = {
  red: false,
  yellow: false,
  green: false,
  blue: false,
  white: false,
};

function toggleLED(color) {
  const newState = !ledStates[color];

  if (newState) {
    Object.keys(ledStates).forEach((otherColor) => {
      if (otherColor !== color && ledStates[otherColor]) {
        fetch(`${API_URL}/led/${otherColor}/off`, { method: "POST" })
          .then(() => {
            ledStates[otherColor] = false;
            updateButtonUI(otherColor);
          })
          .catch((err) => console.error(err));
      }
    });
  }

  fetch(`${API_URL}/led/${color}/${newState ? "on" : "off"}`, {
    method: "POST",
  })
    .then((res) => {
      if (!res.ok) throw new Error(`Error al cambiar LED ${color}`);
      ledStates[color] = newState;
      updateButtonUI(color);
    })
    .catch((err) => {
      console.error(err);
      alert(`No se pudo cambiar el LED ${color}`);
    });
}


function updateButtonUI(color) {
  const btn = document.getElementById(`led-${color}`);
  if (ledStates[color]) {
    btn.classList.remove("off");
    btn.classList.add("on");
    btn.textContent = `${emojiForColor(color)} ${capitalize(color)} ON`;
  } else {
    btn.classList.remove("on");
    btn.classList.add("off");
    btn.textContent = `${emojiForColor(color)} ${capitalize(color)} OFF`;
  }
}

function emojiForColor(color) {
  switch (color) {
    case "red": return "🔴";
    case "yellow": return "🟡";
    case "green": return "🟢";
    case "blue": return "🟦";
    case "white": return "⚫";
    default: return "";
  }
}

function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function sendText() {
  const message = document.getElementById("oledMessage").value.trim();
  if (!message) {
    alert("Escribe un mensaje para enviar.");
    return;
  }

  fetch(`${API_URL}/oled/text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  })
    .then((res) => res.json())
    .then((data) => console.log(data.message))
    .catch((err) => console.error(err));
}

function chooseAndSendImage() {
  const fileInput = document.getElementById("imageFile");
  const file = fileInput.files[0];
  if (!file) {
    alert("Selecciona una imagen para enviar.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  fetch(`${API_URL}/oled/image`, {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      console.log(data.message);
      fileInput.value = "";
    })
    .catch((err) => console.error(err));
}

document.addEventListener("DOMContentLoaded", () => {
  Object.keys(ledStates).forEach(color => updateButtonUI(color));
});