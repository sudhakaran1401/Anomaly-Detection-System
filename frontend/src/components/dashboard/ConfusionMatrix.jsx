export default function ConfusionMatrix({
    matrix,
    image,
}) {
    return (
        <>
            <div className="card shadow mt-4">
                <div className="card-header">
                    <h5 className="mb-0">
                        Confusion Matrix
                    </h5>
                </div>

                <div className="card-body">

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
            </div>

            <div className="card shadow mt-4">

                <div className="card-header">
                    <h5 className="mb-0">
                        Confusion Matrix Visualization
                    </h5>
                </div>

                <div className="card-body text-center">

                    <img
                        src={image}
                        alt="Confusion Matrix"
                        className="img-fluid"
                    />

                </div>

            </div>
        </>
    );
}