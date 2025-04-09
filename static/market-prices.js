// Market Prices API Handler
class MarketPricesAPI {
    constructor(apiKey) {
        this.apiKey = apiKey;
        this.baseUrl = 'https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24';
    }

    async getPrices(commodity, state = '', date = '', limit = 15) {
        try {
            // If no date is provided, use 2 days ago as default
            let targetDate;
            if (!date) {
                const today = new Date();
                const twoDaysAgo = new Date(today);
                twoDaysAgo.setDate(today.getDate() - 2);
                targetDate = twoDaysAgo;
            } else {
                targetDate = new Date(date);
            }
            
            const formattedDate = targetDate.toLocaleDateString('en-IN', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            }).split('/').join('/');
            
            // Fetch data for the specific date
            let url = `${this.baseUrl}?api-key=${this.apiKey}&format=json&limit=${limit}`;
            if (commodity) {
                url += `&filters[Commodity.keyword]=${encodeURIComponent(commodity)}`;
            }
            if (state) {
                url += `&filters[State.keyword]=${encodeURIComponent(state)}`;
            }
            url += `&filters[Arrival_Date]=${formattedDate}`;
            
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`API request failed: ${response.status}`);
            }
            
            const data = await response.json();
            return this.processData(data, formattedDate);
        } catch (error) {
            console.error('Error fetching market prices:', error);
            return null;
        }
    }

    processData(data, date) {
        if (!data || !data.records) return null;

        return {
            date: date,
            records: data.records.map(record => ({
                commodity: record.Commodity,
                variety: record.Variety,
                state: record.State,
                district: record.District,
                market: record.Market,
                date: record.Arrival_Date,
                minPrice: record.Min_Price,
                maxPrice: record.Max_Price,
                modalPrice: record.Modal_Price,
                grade: record.Grade
            }))
        };
    }
}

// Chart Manager
class PriceChart {
    constructor(canvasId) {
        this.ctx = document.getElementById(canvasId).getContext('2d');
        this.chart = null;
    }

    initialize() {
        this.chart = new Chart(this.ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Modal Price',
                    data: [],
                    borderColor: '#4caf50',
                    backgroundColor: 'rgba(76, 175, 80, 0.1)',
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: '#1a2e1d',
                        titleColor: '#ffffff',
                        bodyColor: '#e2e8f0',
                        borderColor: '#4caf50',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                return '₹' + context.parsed.y;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)',
                        },
                        ticks: {
                            color: '#9ca3af',
                            maxRotation: 45,
                            minRotation: 45
                        }
                    },
                    y: {
                        beginAtZero: false,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.05)',
                        },
                        ticks: {
                            color: '#9ca3af',
                            callback: function(value) {
                                return '₹' + value;
                            }
                        }
                    }
                }
            }
        });
    }

    updateData(data) {
        if (!data || !data.records || data.records.length === 0) return;

        // Sort prices by market name for consistent display
        const sortedRecords = [...data.records].sort((a, b) => a.market.localeCompare(b.market));

        // Update chart data
        this.chart.data.labels = sortedRecords.map(p => p.market);
        this.chart.data.datasets[0].data = sortedRecords.map(p => p.modalPrice);
        this.chart.update();
    }
}

// UI Manager
class MarketPricesUI {
    constructor() {
        this.api = null;
        this.chart = new PriceChart('priceChart');
        this.initializeEventListeners();
        this.setDefaultDate();
    }

    setDefaultDate() {
        // Set default date to 2 days ago
        const today = new Date();
        const twoDaysAgo = new Date(today);
        twoDaysAgo.setDate(today.getDate() - 2);
        
        // Format date for input (YYYY-MM-DD)
        const formattedDate = twoDaysAgo.toISOString().split('T')[0];
        document.getElementById('date-select').value = formattedDate;
    }

    initializeEventListeners() {
        document.getElementById('crop-select').addEventListener('change', () => this.updateData());
        document.getElementById('state-select').addEventListener('change', () => this.updateData());
        document.getElementById('date-select').addEventListener('change', () => this.updateData());
    }

    async updateData() {
        const crop = document.getElementById('crop-select').value;
        const state = document.getElementById('state-select').value;
        const date = document.getElementById('date-select').value;

        // Show loading state
        document.getElementById('priceChart').style.opacity = 0.5;

        try {
            const response = await this.api.getPrices(crop, state, date);
            if (response) {
                // Update the date display
                document.getElementById('data-date').textContent = `Data as of ${response.date}`;
                
                this.chart.updateData(response);
                this.updatePriceTable(response.records);
            }
        } catch (error) {
            console.error('Error updating data:', error);
        } finally {
            document.getElementById('priceChart').style.opacity = 1;
        }
    }

    updatePriceTable(prices) {
        const tbody = document.querySelector('#price-table tbody');
        tbody.innerHTML = '';

        prices.forEach(price => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="py-3 px-4 text-sm text-white">${price.market}</td>
                <td class="py-3 px-4 text-sm text-gray-300">${price.district}, ${price.state}</td>
                <td class="py-3 px-4 text-sm text-white font-medium">₹${price.modalPrice}</td>
                <td class="py-3 px-4 text-sm text-gray-300">${price.date}</td>
            `;
            tbody.appendChild(row);
        });
    }

    setApiKey(apiKey) {
        this.api = new MarketPricesAPI(apiKey);
        this.chart.initialize();
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.marketPricesUI = new MarketPricesUI();
});