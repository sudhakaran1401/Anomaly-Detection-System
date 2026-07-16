export default function DashboardActions({
    onUpload,
    onDownload,
}) {
    return (
        <div className="text-center mt-5">

            <button
                className="btn btn-primary me-3"
                onClick={onUpload}
            >
                Upload Another Dataset
            </button>

            <button
                className="btn btn-danger"
                onClick={onDownload}
            >
                Download PDF Report
            </button>

        </div>
    );
}