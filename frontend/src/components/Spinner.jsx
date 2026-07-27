export default function LoadingSpinner({
    message = "Loading..."
}) {
    return (
        <div className="container py-5 text-center">
            <div
                className="spinner-border text-primary"
                role="status"
            />
            <p className="mt-3">{message}</p>
        </div>
    );
}