import StatCard from "./StatCard";

export default function DatasetSummary({ dataset }) {
    const cards = [
        {
            title: "Total Dataset Records",
            value: dataset.total_dataset_records,
            color: "primary",
        },
        {
            title: "Training Records",
            value: dataset.training_records,
            color: "success",
        },
        {
            title: "Testing Records",
            value: dataset.testing_records,
            color: "danger",
        },
    ];

    return (
        <div className="row g-3 justify-content-between mb-4">
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