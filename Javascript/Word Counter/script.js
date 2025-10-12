const textInput = document.getElementById('textInput');
const wordCount = document.getElementById('wordCount');
const charCount = document.getElementById('charCount');
const sentenceCount = document.getElementById('sentenceCount');
const themeToggle = document.getElementById('themeToggle');

// 🔢 Count words, characters, and sentences
textInput.addEventListener('input', () => {
  const text = textInput.value.trim();

  const words = text.length ? text.split(/\s+/).filter(Boolean).length : 0;
  const chars = text.length;
  const sentences = text.length ? text.split(/[.!?]+/).filter(s => s.trim().length > 0).length : 0;

  wordCount.textContent = words;
  charCount.textContent = chars;
  sentenceCount.textContent = sentences;
});

// 🌙 Toggle between dark and light mode
themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('dark-mode');

  if (document.body.classList.contains('dark-mode')) {
    themeToggle.textContent = '☀️ Light Mode';
  } else {
    themeToggle.textContent = '🌙 Night Mode';
  }
});
