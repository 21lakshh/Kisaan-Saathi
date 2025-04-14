const API_KEY = "10bd86a5f317fbbc9b8ee6c3e5a87536";
const BASE_URL = "https://api.openweathermap.org/data/2.5";

// Weather icons mapping
const weatherIcons = {
    '01d': 'fa-sun',           // clear sky (day)
    '01n': 'fa-moon',          // clear sky (night)
    '02d': 'fa-cloud-sun',     // few clouds (day)
    '02n': 'fa-cloud-moon',    // few clouds (night)
    '03d': 'fa-cloud',         // scattered clouds
    '03n': 'fa-cloud',
    '04d': 'fa-cloud',         // broken clouds
    '04n': 'fa-cloud',
    '09d': 'fa-cloud-rain',    // shower rain
    '09n': 'fa-cloud-rain',
    '10d': 'fa-cloud-sun-rain',// rain (day)
    '10n': 'fa-cloud-moon-rain',// rain (night)
    '11d': 'fa-bolt',          // thunderstorm
    '11n': 'fa-bolt',
    '13d': 'fa-snowflake',     // snow
    '13n': 'fa-snowflake',
    '50d': 'fa-smog',          // mist
    '50n': 'fa-smog'
};

// Get current weather
async function getCurrentWeather(city) {
    try {
        const response = await fetch(`${BASE_URL}/weather?q=${city}&appid=${API_KEY}&units=metric`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching current weather:', error);
        return null;
    }
}

// Get 7-day forecast
async function getForecast(city) {
    try {
        const response = await fetch(`${BASE_URL}/forecast?q=${city}&appid=${API_KEY}&units=metric`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching forecast:', error);
        return null;
    }
}

// Update current weather UI
function updateCurrentWeather(data) {
    if (!data) return;

    const icon = weatherIcons[data.weather[0].icon] || 'fa-cloud';
    const temp = Math.round(data.main.temp);
    const description = data.weather[0].description;
    const humidity = data.main.humidity;
    const windSpeed = data.wind.speed;

    try {
        // Update city name
        const cityNameElement = document.querySelector('.text-3xl.md\\:text-4xl.font-bold');
        if (cityNameElement) {
            cityNameElement.textContent = `Weather in ${data.name}`;
        }

        // Update current weather card
        const tempElement = document.querySelector('.text-4xl.font-bold');
        const descElement = document.querySelector('.text-gray-400');
        const iconElement = document.querySelector('.text-6xl');

        if (tempElement) tempElement.textContent = `${temp}°C`;
        if (descElement) descElement.textContent = description;
        if (iconElement) iconElement.className = `fas ${icon} text-yellow-400 text-6xl`;

        // Update weather details
        const windElement = document.querySelector('.fa-wind').parentElement.nextElementSibling;
        const humidityElement = document.querySelector('.fa-tint').parentElement.nextElementSibling;

        if (windElement) windElement.textContent = `${windSpeed} m/s`;
        if (humidityElement) humidityElement.textContent = `${humidity}%`;
    } catch (error) {
        console.error('Error updating current weather UI:', error);
    }
}

// Update forecast UI
function updateForecast(data) {
    if (!data) return;

    try {
        const forecastContainer = document.querySelector('.space-y-4');
        if (!forecastContainer) return;

        const dailyForecasts = {};

        // Group forecasts by day
        data.list.forEach(item => {
            const date = new Date(item.dt * 1000);
            const day = date.toLocaleDateString('en-US', { weekday: 'long' });
            
            if (!dailyForecasts[day]) {
                dailyForecasts[day] = {
                    high: item.main.temp_max,
                    low: item.main.temp_min,
                    icon: item.weather[0].icon,
                    description: item.weather[0].description,
                    date: date
                };
            } else {
                dailyForecasts[day].high = Math.max(dailyForecasts[day].high, item.main.temp_max);
                dailyForecasts[day].low = Math.min(dailyForecasts[day].low, item.main.temp_min);
            }
        });

        // Get the next 7 days starting from today
        const today = new Date();
        const next7Days = Array.from({ length: 7 }, (_, i) => {
            const date = new Date(today);
            date.setDate(today.getDate() + i);
            return date.toLocaleDateString('en-US', { weekday: 'long' });
        });

        // Update forecast cards
        const forecastCards = forecastContainer.querySelectorAll('div.flex.items-center.justify-between');
        
        next7Days.forEach((day, index) => {
            if (forecastCards[index]) {
                const forecast = dailyForecasts[day];
                if (forecast) {
                    const icon = weatherIcons[forecast.icon] || 'fa-cloud';
                    const dateStr = forecast.date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                    
                    const dayElement = forecastCards[index].querySelector('.text-white.font-semibold');
                    const dateElement = forecastCards[index].querySelector('.text-gray-400.text-sm');
                    const iconElement = forecastCards[index].querySelector('.text-2xl');
                    const highTempElement = forecastCards[index].querySelector('.text-right .text-white.font-bold');
                    const lowTempElement = forecastCards[index].querySelector('.text-right .text-gray-400.text-sm');

                    if (dayElement) dayElement.textContent = day;
                    if (dateElement) dateElement.textContent = dateStr;
                    if (iconElement) iconElement.className = `fas ${icon} text-yellow-400 text-2xl`;
                    if (highTempElement) highTempElement.textContent = `${Math.round(forecast.high)}°C`;
                    if (lowTempElement) lowTempElement.textContent = `${Math.round(forecast.low)}°C`;
                }
            }
        });
    } catch (error) {
        console.error('Error updating forecast UI:', error);
    }
}

// Initialize weather data
async function initializeWeather(city = 'Jaipur') {
    try {
        const currentWeather = await getCurrentWeather(city);
        const forecast = await getForecast(city);

        if (currentWeather && forecast) {
            updateCurrentWeather(currentWeather);
            updateForecast(forecast);
        } else {
            console.error('Failed to fetch weather data');
            const errorMessage = document.createElement('div');
            errorMessage.className = 'text-red-500 text-center p-4';
            errorMessage.textContent = 'Failed to fetch weather data. Please try again.';
            document.querySelector('.container').prepend(errorMessage);
        }
    } catch (error) {
        console.error('Error initializing weather:', error);
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Initialize with default city
    initializeWeather();

    // Refresh weather data
    document.getElementById('refresh-weather').addEventListener('click', () => {
        const city = document.getElementById('location-input').value || 'Chennai';
        initializeWeather(city);
    });

    // Search location
    document.getElementById('location-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const city = e.target.value;
            initializeWeather(city);
        }
    });
}); 