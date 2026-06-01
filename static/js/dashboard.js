let chartType = 'line';

const normal = JSON.parse(document.getElementById('normal-data').textContent);
const anomalies = JSON.parse(document.getElementById('anomaly-data').textContent);

const scatterElement = document.getElementById('scatter-data');
const scoreData = JSON.parse( document.getElementById( 'score-data' ).textContent );

let scatterData = [];

if (scatterElement) {
    scatterData = JSON.parse(scatterElement.textContent);
}

let chart;

function renderChart() {
    if (chart) chart.destroy();

    let config;

    // BAR & PIE
        if (chartType === 'line') {

            config = {
                type: 'line',
                data: {
                    labels: ['Normal', 'Anomalies'],
                    datasets: [{
                        label: "Records",
                        data: [normal, anomalies],
                        borderColor: '#007bff',
                        backgroundColor: 'rgba(0,123,255,0.2)',
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: ['#28a745', '#dc3545'],
                        pointRadius: 6
                    }]
                }
            };
        }
    
    else if (chartType === 'pie') {

        config = {
            type: 'pie',
            data: {
                labels: ['Normal', 'Anomalies'],
                datasets: [
                    {
                        data: [normal, anomalies],
                        backgroundColor: ['#28a745', '#dc3545'],  // 🔥 IMPORTANT
                        tension: 0.4
                    }
                ]
            }
        };

    } 
    // SCATTER
    else if (chartType === 'scatter') {

       const normalPoints = scatterData .filter(d => d.result === 'Normal') .map(d => ({ x: d.pca_x, y: d.pca_y }));

       const anomalyPoints = scatterData .filter(d => d.result === 'Anomaly') .map(d => ({ x: d.pca_x, y: d.pca_y }));

        config = {
            type: 'scatter',
            data: {
                datasets: [
                    {
                        label: 'Normal',
                        data: normalPoints,
                        borderColor:'#ffffff',
                        backgroundColor: '#28a745',
                        tension: 0.4
                    },
                    {
                        label: 'Anomalies',
                        data: anomalyPoints,
                        borderColor:'#ffffff',
                        backgroundColor: '#dc3545',
                        tension: 0.4
                    }
                ]
            }
        };
    }

    else if (chartType === 'histogram') {

    config = {

        type: 'bar',

        data: {

            labels: scoreData.map(
                (_, i) => i + 1
            ),

            datasets: [

                {

                    label: 'Anomaly Scores',

                    data: scoreData,

                    backgroundColor: scoreData.map(
                        score =>
                            score < 0
                            ? '#dc3545'
                            : '#28a745'
                    )
                }
            ]
        }
    };
    }

    chart = new Chart(document.getElementById('chartCanvas'), {
        ...config,
        options: {
            responsive: true,
            maintainAspectRatio: false, // 🔥 FIX SIZE ISSUE
            plugins: {
                title: {
                    display: true,
                    text: `Anomaly Visualization (${chartType.toUpperCase()})`
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            if (chartType === 'scatter') {
                                return `X: ${context.raw.x}, Y: ${context.raw.y}`;
                            }
                            return `${context.label}: ${context.raw} records`;
                        }
                    }
                }
            }
        }
    });
}

// INITIAL LOAD
renderChart();


// 🔁 TOGGLE BETWEEN TYPES
function toggleChart() {
    if (chartType === 'line') {
        chartType = 'pie';
    } else if (chartType === 'pie') {
        chartType = 'scatter';
    } else if (chartType === 'scatter') {
        chartType = 'histogram';
    } else {
        chartType = 'line';
    }
    renderChart();
}


// 🎯 FILTER FUNCTIONS
function showAnomaliesChart() {

    if (
        chartType === 'scatter' ||
        chartType === 'histogram'
    ) {

        if (chartType === 'scatter') {

            chart.data.datasets[0].hidden = true;

            chart.data.datasets[1].hidden = false;
        }

        chart.update();

        return;
    }

    chart.data.datasets[0].data = [
        0,
        anomalies
    ];

    chart.update();
}

function showNormalChart() {

    if (
        chartType === 'scatter' ||
        chartType === 'histogram'
    ) {

        if (chartType === 'scatter') {

            chart.data.datasets[0].hidden = false;

            chart.data.datasets[1].hidden = true;
        }

        chart.update();

        return;
    }

    chart.data.datasets[0].data = [
        normal,
        0
    ];

    chart.update();
}

function showAllChart() {

    if (
        chartType === 'scatter' ||
        chartType === 'histogram'
    ) {

        if (chartType === 'scatter') {

            chart.data.datasets[0].hidden = false;

            chart.data.datasets[1].hidden = false;
        }

        chart.update();

        return;
    }

    chart.data.datasets[0].data = [
        normal,
        anomalies
    ];

    chart.update();
}


function setFilter(type) {

    document
        .querySelectorAll('.btn-group .btn')
        .forEach(btn =>
            btn.classList.remove('active')
        );

    if (type === 'all') {

        document
            .getElementById('chart_all')
            .classList.add('active');

    } else if (type === 'anomaly') {

        document
            .getElementById('chart_anomaly')
            .classList.add('active');

    } else {

        document
            .getElementById('chart_normal')
            .classList.add('active');
    }

    if (chartType === 'scatter') {

        if (type === 'all') {

            chart.data.datasets[0].hidden = false;

            chart.data.datasets[1].hidden = false;

        } else if (type === 'anomaly') {

            chart.data.datasets[0].hidden = true;

            chart.data.datasets[1].hidden = false;

        } else {

            chart.data.datasets[0].hidden = false;

            chart.data.datasets[1].hidden = true;
        }

        chart.update();

        return;
    }

    if (chartType === 'histogram') {
        return;
    }

    if (type === 'all') {

        chart.data.datasets[0].data = [
            normal,
            anomalies
        ];

    } else if (type === 'anomaly') {

        chart.data.datasets[0].data = [
            0,
            anomalies
        ];

    } else {

        chart.data.datasets[0].data = [
            normal,
            0
        ];
    }

    chart.update();
}


// 🔍 SEARCH
function searchTable() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let rows = document.querySelectorAll("#dataTable tbody tr");

    rows.forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(input) ? "" : "none";
    });
}


function resetPage() {

    currentFilter = "all";

    let rows = document.querySelectorAll(
        "#dataTable tbody tr"
    );

    rows.forEach(row => {
        row.dataset.visible = "true";
    });

    document.getElementById(
        "searchInput"
    ).value = "";

    currentPage = 1;

    showPage(currentPage);

    updatePDFLink();
}


// 📥 CSV DOWNLOAD
function downloadCSV() {
    let rows = document.querySelectorAll("#dataTable tbody tr");
    let csv = [];

    // Header
    let headers = document.querySelectorAll("#dataTable thead th");
    csv.push([...headers].map(h => h.innerText).join(","));

    rows.forEach(row => {
        // ✅ Only rows that are actually visible (pagination + filter)
        if (row.dataset.visible !== "false") {
            let cols = row.querySelectorAll("td");
            csv.push([...cols].map(c => c.innerText.trim()).join(","));
        }
    });

    let blob = new Blob([csv.join("\n")], { type: "text/csv" });
    let url = URL.createObjectURL(blob);

    let a = document.createElement("a");
    a.href = url;
    a.download = "filtered_data.csv";
    a.click();
}

function updatePDFLink() {
    let baseUrl = document.getElementById("pdfBtn").getAttribute("href").split('?')[0];

    if (currentFilter === "normal") {
        document.getElementById("pdfBtn").href = baseUrl + "?filter=normal";
    } else if (currentFilter === "anomaly") {
        document.getElementById("pdfBtn").href = baseUrl + "?filter=anomaly";
    } else {
        document.getElementById("pdfBtn").href = baseUrl;
    }
}

function clearFile() {
    // Redirect to home page (upload screen)
    window.location.href = "";
}