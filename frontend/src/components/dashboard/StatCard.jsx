export default function StatCard({
    title,
    value,
    color = "primary",
    bordered = false,
    precision = null,
}) {
    const displayValue =
        value == null
            ? "N/A"
            : precision != null
            ? Number(value).toFixed(precision)
            : value;

    return (
        <div
            className={`card shadow-sm h-100 ${
                bordered ? `border-${color}` : ""
            }`}
        >
            <div className="card-body text-center">
                <h6>{title}</h6>

                <h3 className={`text-${color} fw-bold`}>
                    {displayValue}
                </h3>
            </div>
        </div>
    );
}