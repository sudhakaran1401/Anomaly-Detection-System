import { useTheme } from "../../components/ThemeContext";
import StatCard from "./StatCard";

export default function MetricCards({
    total = 0,
    normal = 0,
    anomalies = 0,
}) {
    const { darkMode } = useTheme();

    const cards = [
        {
            title: "Total Records",
            value: total,
            color: "primary",
        },
        {
            title: "Normal",
            value: normal,
            color: "success",
        },
        {
            title: "Anomalies",
            value: anomalies,
            color: "danger",
        },
    ];

    return (
        <div className="container">
            <div className="row g-3 justify-content-between">

                {cards.map((card) => (
                    <div
                        key={card.title}
                        className="col-md-4"
                    >
                        <StatCard
                            title={card.title}
                            value={card.value}
                            color={card.color}
                            bordered
                            darkMode={darkMode}
                        />
                    </div>
                ))}

            </div>
        </div>
    );
}