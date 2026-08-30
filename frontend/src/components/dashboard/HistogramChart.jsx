import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend,
    Title,
} from "chart.js";

import { Bar } from "react-chartjs-2";
import { useTheme } from "../../components/ThemeContext";
import BaseChart from "./BaseChart";

import { getThemeColors, getCommonOptions, } from "../../utils/chartUtils";

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Tooltip,
    Legend,
    Title
);

export default function HistogramChart({ rows = [] }) {
    const { darkMode } = useTheme();

    const { textColor, gridColor } = getThemeColors(darkMode);

    const labels = rows.map((_, index) => index + 1);

    const data = {
        labels,
        datasets: [
            {
                label: "Anomaly Scores",
                data: rows.map((row) => row.anomaly_score ?? 0),

                backgroundColor: rows.map((row) =>
                    row.result === "Anomaly"
                        ? "#ef4444"
                        : "#22c55e"
                ),

                borderRadius: 4,
                borderSkipped: false,
                borderWidth: 0,
                barPercentage: 1,
                categoryPercentage: 1,
            },
        ],
    };

    const options = {
        ...getCommonOptions({
            title: "Anomaly Visualization (HISTOGRAM)",
            textColor,
            gridColor,
        }),

        scales: {
            x: {
                ticks: {
                    color: textColor,
                    maxTicksLimit: 25,
                },

                grid: {
                    color: gridColor,
                },

                title: {
                    display: true,
                    text: "Records",
                    color: textColor,
                },
            },

            y: {
                min: -0.1,
                max: 0.2,

                ticks: {
                    color: textColor,
                },

                grid: {
                    color: gridColor,
                },

                title: {
                    display: true,
                    text: "Anomaly Score",
                    color: textColor,
                },
            },
        },
    };

    return (
        <BaseChart
            ChartComponent={Bar}
            data={data}
            options={options}
        />
    );
}