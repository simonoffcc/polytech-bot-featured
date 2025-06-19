document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('puffinsChart').getContext('2d');
    let puffinChart;

    function processData(data) {
        const labels = data.map(item => item.date);
        const availability = data.map(item => item.is_available ? 1 : 0);
        
        const availableDays = availability.filter(val => val === 1).length;
        const totalDays = data.length;
        
        document.getElementById('stats').innerHTML = 
            `<p>Пышки были в наличии ${availableDays} из последних ${totalDays} дней, по которым есть данные.</p>`;

        return { labels, availability };
    }

    function renderChart(data) {
        const { labels, availability } = processData(data);
        
        if (puffinChart) {
            puffinChart.destroy();
        }

        puffinChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Наличие пышек (1 = да, 0 = нет)',
                    data: availability,
                    backgroundColor: availability.map(val => val === 1 ? 'rgba(75, 192, 192, 0.7)' : 'rgba(255, 99, 132, 0.7)'),
                    borderColor: availability.map(val => val === 1 ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)'),
                    borderWidth: 1,
                    barThickness: 20,
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        ticks: {
                            stepSize: 1,
                            callback: function(value) {
                                return value === 1 ? 'Да' : 'Нет';
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    async function fetchInitialData() {
        try {
            const response = await fetch('/api/puffins-data');
            const data = await response.json();
            renderChart(data);
        } catch (error) {
            console.error('Error fetching initial data:', error);
            document.getElementById('stats').innerHTML = `<p>Не удалось загрузить данные.</p>`;
        }
    }

    function setupWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const ws = new WebSocket(`${protocol}//${window.location.host}/ws`);

        ws.onmessage = function(event) {
            console.log("WebSocket message received:", event.data);
            const newData = JSON.parse(event.data);
            fetchInitialData(); // Просто перезапрашиваем все данные для простоты
        };

        ws.onclose = function() {
            console.log('WebSocket connection closed. Trying to reconnect...');
            setTimeout(setupWebSocket, 3000); // Попытка переподключения через 3 сек
        };

        ws.onerror = function(error) {
            console.error('WebSocket error:', error);
        };
    }

    const tg = window.Telegram.WebApp;
    tg.ready();
    
    fetchInitialData();
    setupWebSocket();
}); 