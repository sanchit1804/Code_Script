# Random Joke Generator

A simple web app that fetches and displays random jokes using the JokeAPI.  

---

## Features
- Fetches random jokes from the [JokeAPI](https://sv443.net/jokeapi/v2/).
- Error handling for failed requests.
- Responsive layout for desktop and mobile.

---

## File Structure

project/
│
├── index.html # Main HTML file
├── style.css # CSS for styling the app
└── script.js # JavaScript to fetch and display jokes

## How It Works
1. When the page loads, a random joke is fetched and displayed.
2. Clicking **“Next!”** fetches another joke from JokeAPI.
3. The button temporarily disables while loading to prevent spam.

## How to Run It
1. Clone the repository.
2. Open `index.html` in your web browser.