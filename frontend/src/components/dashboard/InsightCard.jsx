export default function PerformanceInsightCard({
    insight,
}) {
    return (
        <div className="card shadow mt-4">
            <div className="card-body">

                <h5>
                    Performance Insight
                </h5>

                <div
                    className={`alert ${insight.className}`}
                >
                    <strong>
                        {insight.title}
                    </strong>

                    <br />

                    {insight.message}

                </div>

            </div>
        </div>
    );
}