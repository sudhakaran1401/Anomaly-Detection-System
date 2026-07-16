import { useEffect, useMemo, useState } from "react";

import AnomalyService from "../../services/AnomalyService";

import Pagination from "../../components/dashboard/Pagination";
import Message from "../../components/Message";
import LoadingSpinner from "../../components/Spinner";
import { useTheme } from "../../components/ThemeContext";

export default function History() {

    const { darkMode } = useTheme();

    const [history, setHistory] = useState([]);
    const [loading, setLoading] = useState(true);

    const [currentPage, setCurrentPage] = useState(1);
    const [rowsPerPage, setRowsPerPage] = useState(5);

    const [message, setMessage] = useState({
        type: "",
        text: "",
    });

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {

        try {

            setLoading(true);

            const response =
                await AnomalyService.getHistory();

            const data =
                response.data.results ??
                response.data;

            setHistory(data);

        } catch {

            setMessage({
                type: "danger",
                text: "Failed to load history.",
            });

        } finally {

            setLoading(false);

        }

    };

    const handleDelete = async (id) => {

        if (
            !window.confirm(
                "Delete this history record?"
            )
        ) {
            return;
        }

        try {

            await AnomalyService.deleteHistory(id);

            setHistory((prev) =>
                prev.filter(
                    (item) => item.id !== id
                )
            );

            setMessage({
                type: "success",
                text: "History deleted successfully.",
            });

        } catch {

            setMessage({
                type: "danger",
                text: "Failed to delete history.",
            });

        }

    };

    const handleClearAll = async () => {

        try {

            await AnomalyService.clearHistory();

            setHistory([]);

            setMessage({
                type: "success",
                text: "History cleared successfully.",
            });

        } catch {

            setMessage({
                type: "danger",
                text: "Failed to clear history.",
            });

        }

    };

    const currentRows = useMemo(() => {

        const start =
            (currentPage - 1) * rowsPerPage;

        return history.slice(
            start,
            start + rowsPerPage
        );

    }, [
        history,
        currentPage,
        rowsPerPage,
    ]);

    return (

        <div className="container mt-5">

            <div className="d-flex justify-content-between align-items-center mb-4">

                <h2 className="fw-bold mb-0">

                    Detection History

                </h2>

                <button
                    className="btn btn-danger btn-sm"
                    onClick={handleClearAll}
                >

                    <i className="bi bi-trash"></i>{" "}

                    Clear All

                </button>

            </div>

            <Message
                type={message.type}
                message={message.text}
                onClose={() =>
                    setMessage({
                        type: "",
                        text: "",
                    })
                }
            />

            <div
                className={`card shadow-lg ${
                    darkMode
                        ? "theme-dark-card"
                        : "theme-light-card"
                }`}
            >

                <div className="table-responsive">

                    <table className="table table-bordered table-striped table-hover align-middle text-center mb-0">

                        <thead>

                            <tr>

                                <th>#</th>
                                <th>File</th>
                                <th>Model</th>
                                <th>Scaler</th>
                                <th>Contamination</th>
                                <th>Anomalies</th>
                                <th>Date</th>
                                <th>Action</th>

                            </tr>

                        </thead>

                        <tbody>

                            {loading ? (

                                <tr>

                                    <td colSpan="8">

                                        <LoadingSpinner
                                            message="Loading history..."
                                        />

                                    </td>

                                </tr>

                            ) : currentRows.length === 0 ? (

                                <tr>

                                    <td colSpan="8">

                                        No history found.

                                    </td>

                                </tr>

                            ) : (
                                                            currentRows.map((item) => (

                                    <tr key={item.id}>

                                        <td>{item.id}</td>

                                        <td>
                                            {item.filename}
                                        </td>

                                        <td>

                                            <span className="badge bg-primary">

                                                {item.model_name}

                                            </span>

                                        </td>

                                        <td>

                                            <span className="badge bg-secondary">

                                                {item.scaler_type}

                                            </span>

                                        </td>

                                        <td>

                                            {item.contamination ?? "-"}

                                        </td>

                                        <td>

                                            <span className="badge bg-danger">

                                                {item.anomaly_count}

                                            </span>

                                        </td>

                                        <td>

                                            {new Date(
                                                item.created_at
                                            ).toLocaleString()}

                                        </td>

                                        <td>

                                            <button
                                                className="btn btn-danger btn-sm"
                                                onClick={() =>
                                                    handleDelete(
                                                        item.id
                                                    )
                                                }
                                            >

                                                Delete

                                            </button>

                                        </td>

                                    </tr>

                                ))

                            )}

                        </tbody>

                    </table>

                </div>

                <div className="card-body">

                    <Pagination
                        totalRows={history.length}
                        rowsPerPage={rowsPerPage}
                        currentPage={currentPage}
                        setCurrentPage={setCurrentPage}
                        setRowsPerPage={setRowsPerPage}
                    />

                </div>

            </div>

        </div>

    );

}