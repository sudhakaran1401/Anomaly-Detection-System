import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler,
} from "chart.js";

import { Line } from "react-chartjs-2";
import BaseChart from "./BaseChart";
import { useTheme } from "../../components/ThemeContext";

import { getThemeColors, getCommonOptions, } from "../../utils/chartUtils";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
);

export default function LineChart({ rows = [] }) {
    const { darkMode } = useTheme();

    const { textColor, gridColor } = getThemeColors(darkMode);

    const normal = rows.filter(
        (row) => row.result === "Normal"
    ).length;

    const anomalies = rows.filter(
        (row) => row.result === "Anomaly"
    ).length;

    const data = {
        labels: ["Normal", "Anomalies"],

        datasets: [
            {
                label: "Records",
                data: [normal, anomalies],

                borderColor: "#0d6efd",
                backgroundColor: "rgba(13,110,253,0.18)",

                fill: true,
                tension: 0.35,
                borderWidth: 3,

                pointRadius: 6,
                pointHoverRadius: 8,

                pointBackgroundColor: [
                    "#22c55e",
                    "#ef4444",
                ],

                pointBorderColor: "#ffffff",
                pointBorderWidth: 2,
            },
        ],
    };

    const options = {
        ...getCommonOptions({
            title: "Anomaly Visualization (LINE)",
            textColor,
            gridColor,
        }),

        scales: {
            x: {
                ticks: {
                    color: textColor,
                },

                grid: {
                    color: gridColor,
                },
            },

            y: {
                beginAtZero: true,

                ticks: {
                    precision: 0,
                    color: textColor,
                },

                grid: {
                    color: gridColor,
                },
            },
        },
    };

    return (
        <BaseChart
            ChartComponent={Line}
            data={data}
            options={options}
        />
    );
}