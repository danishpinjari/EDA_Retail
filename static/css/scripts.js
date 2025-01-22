// Fetch insights from the backend
fetch('/insights')
    .then(response => response.json())
    .then(data => {
        const insightsDiv = document.getElementById('insights');
        insightsDiv.innerHTML = `
            <p>Total Sales: $${data.total_sales}</p>
            <p>Average Age: ${data.average_age}</p>
            <p>Male Customers: ${data.male_count}</p>
            <p>Female Customers: ${data.female_count}</p>
        `;
    });

// Fetch sales by category from the backend
fetch('/sales/category')
    .then(response => response.json())
    .then(data => {
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        new Chart(categoryCtx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Sales by Product Category',
                    data: data.data,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });

// Fetch sales by month from the backend
fetch('/sales/month')
    .then(response => response.json())
    .then(data => {
        const monthCtx = document.getElementById('monthChart').getContext('2d');
        new Chart(monthCtx, {
            type: 'line',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Sales by Month',
                    data: data.data,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    fill: false
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    });

// Fetch transactions from the backend
fetch('/transactions')
    .then(response => response.json())
    .then(transactions => {
        const transactionTable = document.getElementById('transactionTable').querySelector('tbody');
        transactions.forEach(transaction => {
            const row = transactionTable.insertRow();
            Object.values(transaction).forEach(text => {
                const cell = row.insertCell();
                cell.textContent = text;
            });
        });
    });
