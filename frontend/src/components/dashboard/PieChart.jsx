import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    Title,
} from "chart.js";

import { Pie } from "react-chartjs-2";
import { useTheme } from "../../components/ThemeContext";
import BaseChart from "./BaseChart";
import { getThemeColors, getCommonOptions, } from "../../utils/chartUtils";

ChartJS.register(
    ArcElement,
    Tooltip,
    Legend,
    Title
);

export default function PieChart({ rows = [] }) {
    const { darkMode } = useTheme();

    const {
        textColor,
        borderColor,
    } = getThemeColors(darkMode);

    const normal = rows.filter(
        (row) => row.result === "Normal"
    ).length;

    const anomalies = rows.filter(
        (row) => row.result === "Anomaly"
    ).length;

    const data = {
        labels: [
            "Normal",
            "Anomalies",
        ],

        datasets: [
            {
                data: [
                    normal,
                    anomalies,
                ],

                backgroundColor: [
                    "#22c55e",
                    "#ef4444",
                ],

                borderColor,
                borderWidth: 2,
                hoverOffset: 12,
            },
        ],
    };

    const commonOptions = getCommonOptions({
        title: "Normal vs Anomalies",
        textColor,
        showLegend: true,
    });

    const options = {
        ...commonOptions,

        plugins: {
            ...commonOptions.plugins,

            tooltip: {
                callbacks: {
                    label(context) {
                        const value = context.raw;
                        const total = normal + anomalies;

                        const percent = total
                            ? ((value / total) * 100).toFixed(2)
                            : 0;

                        return `${context.label}: ${value} (${percent}%)`;
                    },
                },
            },
        },
    };

    return (
        <BaseChart
            ChartComponent={Pie}
            data={data}
            options={options}
        />
    );
}