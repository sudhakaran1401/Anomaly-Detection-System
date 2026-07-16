import { useTheme } from "../../components/ThemeContext";
import StatCard from "./StatCard";

export default function DatasetSummary({ dataset }) {
    const { darkMode } = useTheme();

    const items = [
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
        <div className="card shadow-sm mb-4">
            <div className="card-body">
                <div className="row text-center">
                    {items.map((item) => (
                        <div
                            key={item.title}
                            className="col-md-4"
                        >
                            <StatCard
                                title={item.title}
                                value={item.value}
                                color={item.color}
                                darkMode={darkMode}
                            />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}