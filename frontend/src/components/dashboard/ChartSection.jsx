import { useState } from "react";

import LineChart from "./LineChart";
import PieChart from "./PieChart";
import ScatterChart from "./ScatterChart";
import HistogramChart from "./HistogramChart";

import { useTheme } from "../../components/ThemeContext";

const charts = [
    {
        key: "line",
        component: LineChart,
    },
    {
        key: "pie",
        component: PieChart,
    },
    {
        key: "scatter",
        component: ScatterChart,
    },
    {
        key: "histogram",
        component: HistogramChart,
    },
];

export default function ChartSection({ rows = [] }) {
    const { darkMode } = useTheme();

    const [chartIndex, setChartIndex] = useState(0);
    const [view, setView] = useState("all");

    const filteredRows =
        view === "normal"
            ? rows.filter((row) => row.result === "Normal")
            : view === "anomaly"
            ? rows.filter((row) => row.result === "Anomaly")
            : rows;

    const SelectedChart =
        charts[chartIndex].component;

    return (
        <div className="container mt-4">
            <div
                className={`card shadow-sm ${
                    darkMode
                        ? "theme-dark-card"
                        : "theme-light-card"
                }`}
            >
                <div className="card-body">
                    <div className="row align-items-center">

                        <div className="col-md-2 d-flex flex-column gap-2">

                            <button
                                className="btn btn-primary btn-sm"
                                onClick={() =>
                                    setChartIndex(
                                        (prev) =>
                                            (prev + 1) %
                                            charts.length
                                    )
                                }
                            >
                                📊 Toggle Chart
                            </button>

                            <div
                                className="btn-group"
                                role="group"
                            >
                                <button
                                    className={`btn btn-danger btn-sm ${
                                        view === "anomaly"
                                            ? "active"
                                            : ""
                                    }`}
                                    onClick={() =>
                                        setView("anomaly")
                                    }
                                >
                                    Anomalies
                                </button>

                                <button
                                    className={`btn btn-success btn-sm ${
                                        view === "normal"
                                            ? "active"
                                            : ""
                                    }`}
                                    onClick={() =>
                                        setView("normal")
                                    }
                                >
                                    Normal
                                </button>
                            </div>

                            <button
                                className="btn btn-secondary btn-sm"
                                onClick={() =>
                                    setView("all")
                                }
                            >
                                🔄 Reset
                            </button>

                        </div>

                        <div className="col-md-10">
                            <div className="chart-container">
                                <SelectedChart
                                    rows={filteredRows}
                                />
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    );
}