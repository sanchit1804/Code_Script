/**
 * Fetch a random joke from JokeAPI (https://v2.jokeapi.dev/)
 * Returns a string with the joke text.
 */
async function getJoke() {
  const url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,racist,sexist";
  const response = await fetch(url);
  const data = await response.json();

  if (data.type === "single") {
    return data.joke;
  } else {
    return `${data.setup}\n\n${data.delivery}`;
  }
}

/**
 * Updates the joke displayed on the page.
 */
async function updateJoke() {
  const jokeElement = document.getElementById("joke");
  const button = document.getElementById("next-btn");

  // Disable button while loading
  button.disabled = true;
  jokeElement.textContent = "Loading a new joke...";

  try {
    const joke = await getJoke();
    jokeElement.textContent = joke;
  } catch (error) {
    jokeElement.textContent = "Oops! Couldn't fetch a joke.";
    console.error(error);
  } finally {
    button.disabled = false;
  }
}

// Load an initial joke when the page opens
document.addEventListener("DOMContentLoaded", () => {
  updateJoke();
  document.getElementById("next-btn").addEventListener("click", updateJoke);
});
