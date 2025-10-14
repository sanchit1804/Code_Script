# 🎮 Rock Paper Scissors

A simple browser-based Rock-Paper-Scissors game built with **HTML** and **JavaScript**.

---

## 🧩 Overview

This project allows a user to select **Rock**, **Paper**, or **Scissors**, then plays against the computer.  
The computer’s move is chosen randomly, and the result is displayed instantly on the web page.

---

## 💻 How It Works

### 1. HTML Interface
The HTML file (`index.html`) provides:
- A title and instruction header.
- Three radio buttons for selecting your hand.
- A **Submit** button to play.
- A `<div>` element where the result is shown.

```html
<form name="hand">
  <input type="radio" name="RPS" value="rock"> Rock<br>
  <input type="radio" name="RPS" value="paper"> Paper<br>
  <input type="radio" name="RPS" value="scissors"> Scissors<br>
</form>
<input type="button" value="Submit" onclick="game()">
<div id="result"></div>
