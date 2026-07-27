import StatCard from "./StatCard";

export default function MetricGrid({ metrics }) {
    const cards = [
        ["Accuracy", "success", metrics.accuracy],
        ["Precision", "primary", metrics.precision],
        ["Recall", "warning", metrics.recall],
        ["F1 Score", "danger", metrics.f1],
        ["ROC-AUC", "info", metrics.roc_auc],
    ];

    return (
        <div className="row g-3 justify-content-between">
            {cards.map(([title, color, value]) => (
                <div
                    key={title}
                    className="col-md-2"
                >
                    <StatCard
                        title={title}
                        value={value}
                        color={color}
                        precision={4}
                        bordered
                    />
                </div>
            ))}
        </div>
    );
}