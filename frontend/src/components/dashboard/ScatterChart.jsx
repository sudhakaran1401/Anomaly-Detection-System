import {
    Chart as ChartJS,
    LinearScale,
    PointElement,
    Tooltip,
    Legend,
    Title,
} from "chart.js";

import { Scatter } from "react-chartjs-2";
import { useTheme } from "../../components/ThemeContext";
import BaseChart from "./BaseChart";
import { getThemeColors, getCommonOptions, } from "../../utils/chartUtils";

ChartJS.register(
    LinearScale,
    PointElement,
    Tooltip,
    Legend,
    Title
);

export default function ScatterChart({ rows = [] }) {
    const { darkMode } = useTheme();

    if (!rows.length) {
        return <div className="chart-wrapper" />;
    }

    const { textColor, gridColor } = getThemeColors(darkMode);

    const numericColumns = Object.keys(rows[0]).filter(
        (key) => typeof rows[0][key] === "number"
    );

    const xKey = rows[0].hasOwnProperty("pca_x")
        ? "pca_x"
        : numericColumns[0];

    const yKey = rows[0].hasOwnProperty("pca_y")
        ? "pca_y"
        : numericColumns[1];

    const normal = rows
        .filter((row) => row.result === "Normal")
        .map((row) => ({
            x: row[xKey],
            y: row[yKey],
        }));

    const anomaly = rows
        .filter((row) => row.result === "Anomaly")
        .map((row) => ({
            x: row[xKey],
            y: row[yKey],
        }));

    const data = {
        datasets: [
            {
                label: "Normal",
                data: normal,
                backgroundColor: "#22c55e",
                pointRadius: 4,
                pointHoverRadius: 6,
            },
            {
                label: "Anomalies",
                data: anomaly,
                backgroundColor: "#ef4444",
                pointRadius: 5,
                pointHoverRadius: 7,
            },
        ],
    };

    const options = {
        ...getCommonOptions({
            title: "Anomaly Visualization (SCATTER)",
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

                title: {
                    display: true,
                    text: xKey,
                    color: textColor,
                },
            },

            y: {
                ticks: {
                    color: textColor,
                },

                grid: {
                    color: gridColor,
                },

                title: {
                    display: true,
                    text: yKey,
                    color: textColor,
                },
            },
        },
    };

    return (
        <BaseChart
            ChartComponent={Scatter}
            data={data}
            options={options}
        />
    );
}