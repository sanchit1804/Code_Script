# 🪞 Webcam Mirror — JavaScript Demo

A lightweight web app that uses your device’s **webcam** and flips the video feed **horizontally**, so it behaves just like a real mirror.  
Built with plain **HTML**, **CSS**, and **JavaScript** — no frameworks required.

---

## 📸 Features

- 🔁 **Real mirror effect** — flips the camera preview horizontally.
- 🎥 **Camera selection** — choose between multiple cameras (front/back on mobile).
- 🖼️ **Snapshot capture** — take photos that respect the mirror orientation.
- 💾 **Instant download** — download your mirrored photo as a `.png` file.
- ⚙️ **Toggle mirroring** — turn the mirror effect on or off anytime.
- 🌗 **Dark UI** — modern, clean, and responsive design.

---

## 🚀 Live Demo

You can run this app locally by opening the HTML file directly in a browser that supports **`getUserMedia()`** (most modern browsers).

---

## 🧠 How It Works

The app uses the **WebRTC API** (`navigator.mediaDevices.getUserMedia`) to access your webcam stream and display it in a `<video>` element.  
CSS is used to flip the live preview horizontally using:

```css
video {
  transform: scaleX(-1);
}
