import StatCard from "./StatCard";

export default function DetectionSummary({ summary }) {
    const cards = [
        {
            title: "Total Records",
            value: summary.total_records,
            color: "primary",
        },
        {
            title: "Normal",
            value: summary.normal_records,
            color: "success",
        },
        {
            title: "Anomalies",
            value: summary.anomaly_records,
            color: "danger",
        },
    ];

    return (
        <div className="row g-3 justify-content-between mb-5">
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
                    />
                </div>
            ))}
        </div>
    );
}