let currentUnit = 'celsius';
let currentWeatherData = null;
let currentForecastData = null;
const API_KEY = 'bd5e378503939ddaee76f12ad7a97608';
const WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather';
const FORECAST_API_URL = 'https://api.openweathermap.org/data/2.5/forecast';

// Weather condition to icon mapping
const weatherIcons = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Drizzle': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '🌨️',
    'Mist': '🌫️',
    'Fog': '🌫️',
    'Haze': '🌫️'
};

// Gradient colors for different weather conditions
const weatherGradients = {
    'Clear': 'linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #ea580c 100%)',
    'Clouds': 'linear-gradient(135deg, #6b7280 0%, #4b5563 50%, #374151 100%)',
    'Rain': 'linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1e40af 100%)',
    'Drizzle': 'linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1e40af 100%)',
    'Thunderstorm': 'linear-gradient(135deg, #1f2937 0%, #374151 50%, #4b5563 100%)',
    'Snow': 'linear-gradient(135deg, #e5e7eb 0%, #d1d5db 50%, #9ca3af 100%)',
    'default': 'linear-gradient(135deg, #1e3a8a 0%, #7c3aed 50%, #ec4899 100%)'
};

// DOM elements
const elements = {
    loading: document.getElementById('loading'),
    errorMessage: document.getElementById('errorMessage'),
    cityInput: document.getElementById('cityInput'),
    searchBtn: document.getElementById('searchBtn'),
    cityName: document.getElementById('cityName'),
    dateTime: document.getElementById('dateTime'),
    weatherIcon: document.getElementById('weatherIcon'),
    temperature: document.getElementById('temperature'),
    tempToggle: document.getElementById('tempToggle'),
    weatherDescription: document.getElementById('weatherDescription'),
    feelsLike: document.getElementById('feelsLike'),
    humidity: document.getElementById('humidity'),
    windSpeed: document.getElementById('windSpeed'),
    pressure: document.getElementById('pressure'),
    visibility: document.getElementById('visibility'),
    uvIndex: document.getElementById('uvIndex'),
    forecastContainer: document.getElementById('forecastContainer')
};

// Utility functions
function showLoading() {
    elements.loading.style.display = 'flex';
}

function hideLoading() {
    elements.loading.style.display = 'none';
}

function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorMessage.style.display = 'block';
    setTimeout(() => {
        elements.errorMessage.style.display = 'none';
    }, 5000);
}

function getWeatherIcon(condition) {
    return weatherIcons[condition] || '🌤️';
}

function convertTemp(temp, unit) {
    if (unit === 'fahrenheit') {
        return Math.round((temp * 9/5) + 32);
    }
    return Math.round(temp);
}

function formatDate() {
    const now = new Date();
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return now.toLocaleDateString('en-US', options);
}

function updateBackground(weatherCondition) {
    const gradient = weatherGradients[weatherCondition] || weatherGradients.default;
    document.body.style.background = gradient;
    document.body.style.backgroundSize = '400% 400%';
}

// API functions
async function fetchWeather(city) {
    try {
        const response = await fetch(`${WEATHER_API_URL}?q=${city}&appid=${API_KEY}&units=metric`);
        if (!response.ok) {
            throw new Error(`Weather data not found for "${city}". Please check the city name and try again.`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        throw new Error(error.message || 'Failed to fetch weather data. Please try again.');
    }
}

async function fetchForecast(city) {
    try {
        const response = await fetch(`${FORECAST_API_URL}?q=${city}&appid=${API_KEY}&units=metric`);
        if (!response.ok) {
            throw new Error('Failed to fetch forecast data');
        }
        const data = await response.json();
        return data;
    } catch (error) {
        throw new Error('Failed to fetch forecast data. Please try again.');
    }
}

// Display functions
function displayWeather(data) {
    currentWeatherData = data;
    
    elements.cityName.textContent = `${data.name}, ${data.sys.country}`;
    elements.dateTime.textContent = formatDate();
    
    const condition = data.weather[0].main;
    elements.weatherIcon.textContent = getWeatherIcon(condition);
    
    const temp = convertTemp(data.main.temp, currentUnit);
    const unit = currentUnit === 'celsius' ? '°C' : '°F';
    elements.temperature.textContent = `${temp}${unit}`;
    
    elements.weatherDescription.textContent = data.weather[0].description;
    
    // Update details
    const feelsLikeTemp = convertTemp(data.main.feels_like, currentUnit);
    elements.feelsLike.textContent = `${feelsLikeTemp}${unit}`;
    elements.humidity.textContent = `${data.main.humidity}%`;
    elements.windSpeed.textContent = `${Math.round(data.wind.speed * 10) / 10} m/s`;
    elements.pressure.textContent = `${data.main.pressure} hPa`;
    elements.visibility.textContent = data.visibility ? `${Math.round(data.visibility / 1000)} km` : 'N/A';
    
    // UV Index is not available in the free API, so we'll show N/A
    elements.uvIndex.textContent = 'N/A';
    
    // Update background based on weather
    updateBackground(condition);
}

function displayForecast(data) {
    currentForecastData = data;
    elements.forecastContainer.innerHTML = '';
    
    // Group forecast data by day (every 8th item represents a new day as data is every 3 hours)
    const dailyForecasts = [];
    for (let i = 0; i < data.list.length; i += 8) {
        if (dailyForecasts.length >= 5) break;
        dailyForecasts.push(data.list[i]);
    }
    
    dailyForecasts.forEach((forecast, index) => {
        const forecastCard = document.createElement('div');
        forecastCard.className = 'glass-card forecast-card';
        
        const date = new Date(forecast.dt * 1000);
        const dayName = index === 0 ? 'Today' : date.toLocaleDateString('en-US', { weekday: 'long' });
        
        const condition = forecast.weather[0].main;
        const icon = getWeatherIcon(condition);
        const highTemp = convertTemp(forecast.main.temp_max, currentUnit);
        const lowTemp = convertTemp(forecast.main.temp_min, currentUnit);
        const unit = currentUnit === 'celsius' ? '°C' : '°F';
        
        forecastCard.innerHTML = `
            <div class="forecast-day">${dayName}</div>
            <div class="forecast-icon">${icon}</div>
            <div class="forecast-description">${forecast.weather[0].description}</div>
            <div class="forecast-temps">
                <span class="high-temp">${highTemp}${unit}</span>
                <span class="low-temp">${lowTemp}${unit}</span>
            </div>
        `;
        
        elements.forecastContainer.appendChild(forecastCard);
    });
}

function updateTemperatureDisplay() {
    if (currentWeatherData) {
        displayWeather(currentWeatherData);
    }
    if (currentForecastData) {
        displayForecast(currentForecastData);
    }
}

// Main functions
async function loadWeatherData(city) {
    showLoading();
    elements.errorMessage.style.display = 'none';
    
    try {
        const [weatherData, forecastData] = await Promise.all([
            fetchWeather(city),
            fetchForecast(city)
        ]);
        
        displayWeather(weatherData);
        displayForecast(forecastData);
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
}

function handleSearch() {
    const city = elements.cityInput.value.trim();
    if (city) {
        loadWeatherData(city);
        elements.cityInput.value = '';
    }
}

function toggleTemperatureUnit() {
    currentUnit = currentUnit === 'celsius' ? 'fahrenheit' : 'celsius';
    elements.tempToggle.textContent = currentUnit === 'celsius' ? '°F' : '°C';
    updateTemperatureDisplay();
}

// Update time every minute
function updateTime() {
    elements.dateTime.textContent = formatDate();
}

// Event listeners
elements.searchBtn.addEventListener('click', handleSearch);
elements.cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});
elements.tempToggle.addEventListener('click', toggleTemperatureUnit);

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    // Load default city (London)
    loadWeatherData('London');
    
    // Update time every minute
    setInterval(updateTime, 60000);
    updateTime();
});
