export default function DatasetCard({
    filename,
    modelName,
    actions,
}) {
    return (
        <div className="card shadow-sm mb-4">
            <div className="card-body">
                <div className="row align-items-center">

                    <div className="col-md-8">
                        <p className="mb-1">
                            <strong>Dataset :</strong>{" "}
                            {filename}
                        </p>

                        {modelName && (
                            <p className="mb-0">
                                <strong>Model :</strong>{" "}
                                {modelName}
                            </p>
                        )}
                    </div>

                    {actions && (
                        <div className="col-md-4 text-end">
                            {actions}
                        </div>
                    )}

                </div>
            </div>
        </div>
    );
}