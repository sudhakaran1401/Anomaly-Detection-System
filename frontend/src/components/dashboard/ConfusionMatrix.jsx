export default function ConfusionMatrix({
    matrix,
    image,
}) {
    return (
        <>
            <div className="card shadow mt-4">
                <div className="card-header">
                    <h5 className="mb-0">Confusion Matrix</h5>
                </div>

                <div className="card-body">
                    <div className="row align-items-center">

                        {/* Table */}
                        <div className="col-md-6">
                            <table className="table table-bordered text-center">
                                <thead>
                                    <tr>
                                        <th></th>
                                        <th>Predicted Normal</th>
                                        <th>Predicted Anomaly</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    <tr>
                                        <th>Actual Normal</th>
                                        <td>{matrix[0][0]}</td>
                                        <td>{matrix[0][1]}</td>
                                    </tr>

                                    <tr>
                                        <th>Actual Anomaly</th>
                                        <td>{matrix[1][0]}</td>
                                        <td>{matrix[1][1]}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>

                        {/* Image */}
                        <div className="col-md-6 text-center">
                            <img
                                src={image}
                                alt="Confusion Matrix"
                                className="img-fluid rounded confusion-img"
                            />
                        </div>

                    </div>
                </div>
            </div>
        </>
    );
}