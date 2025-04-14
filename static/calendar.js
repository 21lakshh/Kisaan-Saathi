class CropCalendar {
    constructor() {
        this.currentDate = new Date();
        this.months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        
        this.initializeCalendar();
        this.setupEventListeners();
    }

    initializeCalendar() {
        this.updateCalendar();
        this.updateCropAdvice();
    }

    updateCalendar() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        // Update month and year display
        document.getElementById('current-month').textContent = 
            `${this.months[month]} ${year}`;
        
        // Get first day of month and total days
        const firstDay = new Date(year, month, 1).getDay();
        const totalDays = new Date(year, month + 1, 0).getDate();
        
        // Clear previous calendar
        const calendarDays = document.getElementById('calendar-days');
        calendarDays.innerHTML = '';
        
        // Add empty cells for days before first day of month
        for (let i = 0; i < firstDay; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.className = 'h-12 bg-[#1a2e1d] rounded-lg';
            calendarDays.appendChild(emptyCell);
        }
        
        // Add days of the month
        for (let day = 1; day <= totalDays; day++) {
            const dayCell = document.createElement('div');
            dayCell.className = 'h-12 bg-[#1a2e1d] rounded-lg flex items-center justify-center cursor-pointer hover:bg-[#2a3e2d] transition-colors text-white font-medium';
            dayCell.textContent = day;
            
            // Highlight today
            if (day === new Date().getDate() && 
                month === new Date().getMonth() && 
                year === new Date().getFullYear()) {
                dayCell.classList.add('bg-[#4caf50]', 'text-white', 'font-bold');
            }
            
            // Add click event for each day
            dayCell.addEventListener('click', () => {
                this.handleDayClick(day, month, year);
            });
            
            calendarDays.appendChild(dayCell);
        }
    }

    setupEventListeners() {
        document.getElementById('prev-month').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this.updateCalendar();
        });
        
        document.getElementById('next-month').addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this.updateCalendar();
        });
    }

    handleDayClick(day, month, year) {
        const selectedDate = new Date(year, month, day);
        this.updateCropAdvice(selectedDate);
    }

    updateCropAdvice(date = new Date()) {
        const month = date.getMonth();
        const day = date.getDate();
        
        // Get weather data for the selected date
        const weatherData = this.getWeatherData();
        
        // Update advice based on season and weather
        const advice = this.generateCropAdvice(month, weatherData);
        document.getElementById('crop-advice').textContent = advice;
        
        // Update recommended activities
        const activities = this.generateRecommendedActivities(month, weatherData);
        const activitiesList = document.getElementById('recommended-activities');
        activitiesList.innerHTML = activities.map(activity => 
            `<li>${activity}</li>`
        ).join('');
    }

    getWeatherData() {
        // This would typically fetch real weather data
        // For now, return mock data
        return {
            temperature: 25,
            humidity: 60,
            rainfall: 0
        };
    }

    generateCropAdvice(month, weatherData) {
        const season = this.getSeason(month);
        const { temperature, humidity, rainfall } = weatherData;
        
        if (season === 'Summer') {
            if (temperature > 30) {
                return 'High temperatures detected. Ensure proper irrigation and consider using shade nets for sensitive crops.';
            }
            return 'Summer season is ideal for growing heat-tolerant crops like okra, brinjal, and cucumber.';
        } else if (season === 'Monsoon') {
            if (rainfall > 0) {
                return 'Rainfall expected. Ensure proper drainage and protect crops from waterlogging.';
            }
            return 'Monsoon season is perfect for rice cultivation and other water-intensive crops.';
        } else if (season === 'Winter') {
            if (temperature < 15) {
                return 'Low temperatures detected. Protect sensitive crops with frost covers.';
            }
            return 'Winter season is suitable for growing wheat, mustard, and various vegetables.';
        }
        
        return 'Regular monitoring and maintenance recommended for current weather conditions.';
    }

    generateRecommendedActivities(month, weatherData) {
        const season = this.getSeason(month);
        const { temperature, humidity } = weatherData;
        
        const activities = [];
        
        // General activities
        activities.push('Regular soil moisture monitoring');
        activities.push('Pest and disease inspection');
        
        // Season-specific activities
        if (season === 'Summer') {
            activities.push('Early morning irrigation');
            activities.push('Mulching to retain soil moisture');
            if (temperature > 30) {
                activities.push('Extra watering in the evening');
            }
        } else if (season === 'Monsoon') {
            activities.push('Drainage system check');
            activities.push('Fungicide application if needed');
        } else if (season === 'Winter') {
            activities.push('Frost protection measures');
            activities.push('Greenhouse maintenance');
        }
        
        return activities;
    }

    getSeason(month) {
        if (month >= 2 && month <= 5) return 'Summer';
        if (month >= 6 && month <= 9) return 'Monsoon';
        return 'Winter';
    }
}

// Initialize calendar when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CropCalendar();
}); 