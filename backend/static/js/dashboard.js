let chartType = "line";
let currentChartFilter = "all";
let chart = null;

const normal = JSON.parse(document.getElementById("normal-data").textContent);
const anomalies = JSON.parse(document.getElementById("anomaly-data").textContent);

const scatterElement = document.getElementById("scatter-data");

const scoreData = JSON.parse(
    document.getElementById("score-data").textContent
);

const normalScoreData = JSON.parse(
    document.getElementById("normal-score-data").textContent
);

const anomalyScoreData = JSON.parse(
    document.getElementById("anomaly-score-data").textContent
);

let scatterData = [];

if (scatterElement) {
    scatterData = JSON.parse(scatterElement.textContent);
}

function renderChart() {

    if (chart) {
        chart.destroy();
    }

    let config = {};

    // =====================
    // LINE
    // =====================

    if (chartType === "line") {

        config = {

            type: "line",

            data: {

                labels: ["Normal", "Anomalies"],

                datasets: [

                    {

                        label: "Records",

                        data: [
                            normal,
                            anomalies
                        ],

                        borderColor: "#007bff",

                        backgroundColor: "rgba(0,123,255,0.20)",

                        fill: true,

                        tension: 0.4,

                        pointRadius: 6,

                        pointBackgroundColor: [
                            "#28a745",
                            "#dc3545"
                        ]

                    }

                ]

            }

        };

    }

    // =====================
    // PIE
    // =====================

    else if (chartType === "pie") {

        config = {

            type: "pie",

            data: {

                labels: [

                    "Normal",
                    "Anomalies"

                ],

                datasets: [

                    {

                        data: [

                            normal,
                            anomalies

                        ],

                        backgroundColor: [

                            "#28a745",
                            "#dc3545"

                        ]

                    }

                ]

            }

        };

    }

    // =====================
    // SCATTER
    // =====================

    else if (chartType === "scatter") {

        const normalPoints = scatterData

            .filter(d => d.result === "Normal")

            .map(d => ({

                x: d.pca_x,

                y: d.pca_y

            }));

        const anomalyPoints = scatterData

            .filter(d => d.result === "Anomaly")

            .map(d => ({

                x: d.pca_x,

                y: d.pca_y

            }));

        config = {

            type: "scatter",

            data: {

                datasets: [

                    {

                        label: "Normal",

                        data: normalPoints,

                        backgroundColor: "#28a745",

                        borderColor: "#ffffff"

                    },

                    {

                        label: "Anomalies",

                        data: anomalyPoints,

                        backgroundColor: "#dc3545",

                        borderColor: "#ffffff"

                    }

                ]

            }

        };

    }

    // =====================
    // HISTOGRAM
    // =====================

    else {

        config = {

            type: "bar",

            data: {

                labels: scoreData.map((_, i) => i + 1),

                datasets: [

                    {

                        label: "Anomaly Scores",

                        data: scoreData,

                        backgroundColor: scoreData.map(score =>
                            score < 0
                                ? "#dc3545"
                                : "#28a745"
                        )

                    }

                ]

            }

        };

    }

    chart = new Chart(

        document.getElementById("chartCanvas"),

        {

            ...config,

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    title: {

                        display: true,

                        text:
                            `Anomaly Visualization (${chartType.toUpperCase()})`

                    },

                    tooltip: {

                        callbacks: {

                            label(context) {

                                if (chartType === "scatter") {

                                    return `X: ${context.raw.x}, Y: ${context.raw.y}`;

                                }

                                return context.raw;

                            }

                        }

                    }

                }

            }

        }

    );

}

renderChart();

function toggleChart() {

    if (chartType === "line") {

        chartType = "pie";

    }

    else if (chartType === "pie") {

        chartType = "scatter";

    }

    else if (chartType === "scatter") {

        chartType = "histogram";

    }

    else {

        chartType = "line";

    }

    renderChart();

    setFilter(currentChartFilter);

}


function showAllChart() {

    setFilter("all");

}

function showNormalChart() {

    setFilter("normal");

}

function showAnomaliesChart() {

    setFilter("anomaly");

}


function setFilter(type) {

    currentChartFilter = type;

    document
        .querySelectorAll(".btn-group .btn")
        .forEach(btn => btn.classList.remove("active"));

    if (type === "all") {

        document
            .getElementById("chart_all")
            ?.classList.add("active");

    }

    else if (type === "normal") {

        document
            .getElementById("chart_normal")
            ?.classList.add("active");

    }

    else {

        document
            .getElementById("chart_anomaly")
            ?.classList.add("active");

    }

    if (chartType === "scatter") {

        chart.data.datasets[0].hidden =
            (type === "anomaly");

        chart.data.datasets[1].hidden =
            (type === "normal");

        chart.update();

        return;

    }

    if (chartType === "histogram") {

        let data = scoreData;

        let colors =
            scoreData.map(score =>
                score < 0
                    ? "#dc3545"
                    : "#28a745"
            );

        if (type === "normal") {

            data = normalScoreData;

            colors =
                normalScoreData.map(() => "#28a745");

        }

        else if (type === "anomaly") {

            data = anomalyScoreData;

            colors =
                anomalyScoreData.map(() => "#dc3545");

        }

        chart.data.labels =
            data.map((_, i) => i + 1);

        chart.data.datasets[0].data =
            data;

        chart.data.datasets[0].backgroundColor =
            colors;

        chart.update();

        return;

    }

    if (type === "all") {

        chart.data.datasets[0].data = [

            normal,
            anomalies

        ];

    }

    else if (type === "normal") {

        chart.data.datasets[0].data = [

            normal,
            0

        ];

    }

    else {

        chart.data.datasets[0].data = [

            0,
            anomalies

        ];

    }

    chart.update();

}

function searchTable() {

    const input =
        document
            .getElementById("searchInput")
            .value
            .toLowerCase();

    const rows =
        document.querySelectorAll(
            "#dataTable tbody tr"
        );

    rows.forEach(row => {

        row.style.display =
            row.innerText
                .toLowerCase()
                .includes(input)
            ? ""
            : "none";

    });

}

function resetPage() {

    currentFilter = "all";

    const rows =
        document.querySelectorAll(
            "#dataTable tbody tr"
        );

    rows.forEach(row => {

        row.dataset.visible = "true";

    });

    const search =
        document.getElementById(
            "searchInput"
        );

    if (search) {

        search.value = "";

    }

    currentPage = 1;

    if (typeof showPage === "function") {

        showPage(currentPage);

    }

    updatePDFLink();

}

function downloadCSV() {

    const rows =
        document.querySelectorAll(
            "#dataTable tbody tr"
        );

    const csv = [];

    const headers =
        document.querySelectorAll(
            "#dataTable thead th"
        );

    csv.push(
        [...headers]
            .map(h => h.innerText)
            .join(",")
    );

    rows.forEach(row => {

        if (
            row.dataset.visible !== "false"
        ) {

            const cols =
                row.querySelectorAll("td");

            csv.push(

                [...cols]
                    .map(c => c.innerText.trim())
                    .join(",")

            );

        }

    });

    const blob = new Blob(

        [csv.join("\n")],

        {
            type: "text/csv"
        }

    );

    const url =
        URL.createObjectURL(blob);

    const a =
        document.createElement("a");

    a.href = url;

    a.download =
        "filtered_data.csv";

    document.body.appendChild(a);

    a.click();

    document.body.removeChild(a);

    URL.revokeObjectURL(url);

}

function updatePDFLink() {

    const pdfBtn =
        document.getElementById(
            "pdfBtn"
        );

    if (!pdfBtn) return;

    const baseUrl =
        pdfBtn.href.split("?")[0];

    if (currentFilter === "normal") {

        pdfBtn.href =
            baseUrl +
            "?filter=normal";

    }

    else if (
        currentFilter === "anomaly"
    ) {

        pdfBtn.href =
            baseUrl +
            "?filter=anomaly";

    }

    else {

        pdfBtn.href =
            baseUrl;

    }

}


function clearFile() {

    window.location.href = "/upload";

}