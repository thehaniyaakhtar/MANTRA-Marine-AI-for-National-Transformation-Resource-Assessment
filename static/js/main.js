document.addEventListener('DOMContentLoaded', loadCharts);

function loadCharts() {
    // Load timeseries
    fetch('/api/visualize/timeseries')
        .then(r => r.json())
        .then(data => {
            Plotly.newPlot('timeseries-chart', JSON.parse(data.plot).data, JSON.parse(data.plot).layout);
        });
    
    // Load correlations
    fetch('/api/visualize/correlations')
        .then(r => r.json())
        .then(data => {
            Plotly.newPlot('correlation-chart', JSON.parse(data.plot).data, JSON.parse(data.plot).layout);
        });
}

function analyzeSpecies() {
    const species = document.getElementById('species-select').value;
    fetch(`/api/trends/${species}`)
        .then(r => r.json())
        .then(data => {
            document.getElementById('species-analysis').style.display = 'block';
            document.getElementById('species-content').innerHTML = `<p>Trend: ${data.trend_percent}%</p><p>Peak Year: ${data.peak_year}</p><p>Latest Catch: ${data.total_catch.toLocaleString()} tonnes</p>`;
        });
}

function searchData() {
    const query = document.getElementById('search-query').value;
    const year = document.getElementById('search-year').value;
    
    fetch(`/api/search?query=${query}&year=${year}`)
        .then(r => r.json())
        .then(data => {
            let html = '<table><tr><th>Year</th><th>Catch</th></tr>';
            data.forEach(row => {
                html += `<tr><td>${row.Year}</td><td>${row.total_catch}</td></tr>`;
            });
            html += '</table>';
            document.getElementById('search-results').innerHTML = html;
        });
}