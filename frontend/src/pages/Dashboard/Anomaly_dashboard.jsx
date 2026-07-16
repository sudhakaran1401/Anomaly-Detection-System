import { useMemo, useState } from "react";

import AnomalyService from "../../services/AnomalyService";

import MetricCards from "../../components/dashboard/MetricCards";
import ChartSection from "../../components/dashboard/ChartSection";
import DataTable from "../../components/dashboard/DataTable";
import Message from "../../components/Message";
import useMessage from "../../hooks/useMessage";

export default function AnomalyDashboard() {
    const [tableFilter, setTableFilter] = useState("all");
    const [search, setSearch] = useState("");
    const [downloading, setDownloading] = useState(false);

    const {
        message,
        clearMessage,
        showError,
        showSuccess,
    } = useMessage();

    const storedResult = JSON.parse(
        sessionStorage.getItem("anomalyResult") || "{}"
    );

    const dashboard = {
        filename: storedResult.filename || "",
        total: storedResult.total || 0,
        normal: storedResult.normal || 0,
        anomalies: storedResult.anomalies || 0,
    };

    const rows = storedResult.data || [];

    const handleDownload = async (type) => {

    clearMessage();

    try {

        setDownloading(true);

        if (type === "pdf") {

            await AnomalyService.downloadPDF({
                filename: dashboard.filename,
                model_name: storedResult.model_name,
                scaler_type: storedResult.scaler_type,
                contamination: storedResult.contamination,
            });

        } else {

            await AnomalyService.downloadCSV();

        }

        showSuccess(
            `${type.toUpperCase()} downloaded successfully.`
        );

    } catch (error) {

        showError(
            error.response?.data?.message ||
            `Failed to download ${type.toUpperCase()}.`
        );

    } finally {

        setDownloading(false);

    }
    };

    const handleDeleteDataset = () => {
    
    sessionStorage.removeItem("anomalyResult");

    showSuccess("Dataset deleted successfully.");

    setTimeout(() => {
        window.location.href = "/upload";
    }, 800);
    };

    const tableRows = useMemo(() => {
        return rows.filter((row) => {
            const matchesSearch = Object.values(row)
                .join(" ")
                .toLowerCase()
                .includes(search.toLowerCase());

            const matchesFilter =
                tableFilter === "all" ||
                (tableFilter === "normal" &&
                    row.result === "Normal") ||
                (tableFilter === "anomaly" &&
                    row.result === "Anomaly");

            return matchesSearch && matchesFilter;
        });
    }, [rows, search, tableFilter]);

    return (
        <div className="container py-5">
            <div className="text-center mb-4">
                <h3 className="fw-bold">
                    Analytics Dashboard
                </h3>
            </div>

            <Message
                type={message.type}
                message={message.text}
                onClose={clearMessage}
            />

            {/* Dataset */}

            <div className="card shadow-sm mb-4">
                <div className="card-body">
                    <div className="row align-items-center">
                        <div className="col-md-8">
                            <strong>Dataset :</strong>{" "}
                            {dashboard.filename}
                        </div>

                        <div className="col-md-4 text-end">
                            <button 
                            className="btn btn-outline-danger"
                            onClick={handleDeleteDataset}
                            >
                                Delete Dataset
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            {/* Filter */}

            <div className="container mb-3">
                <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
                    <div className="d-flex align-items-center gap-2 flex-wrap">
                        <div className="btn-group">
                            <button
                                className={`btn btn-sm btn-secondary ${
                                    tableFilter === "all"
                                        ? "active"
                                        : ""
                                }`}
                                onClick={() =>
                                    setTableFilter("all")
                                }
                            >
                                All
                            </button>

                            <button
                                className={`btn btn-sm btn-danger ${
                                    tableFilter === "anomaly"
                                        ? "active"
                                        : ""
                                }`}
                                onClick={() =>
                                    setTableFilter("anomaly")
                                }
                            >
                                Anomalies
                            </button>

                            <button
                                className={`btn btn-sm btn-success ${
                                    tableFilter === "normal"
                                        ? "active"
                                        : ""
                                }`}
                                onClick={() =>
                                    setTableFilter("normal")
                                }
                            >
                                Normal
                            </button>
                        </div>

                        <div className="btn-group">
                            <button
                                className="btn btn-success btn-sm"
                                disabled={downloading}
                                onClick={() =>
                                    handleDownload("csv")
                                }
                            >
                                CSV
                            </button>

                            <span className="btn btn-light btn-sm d-flex align-items-center justify-content-center">
                                <i className="bi bi-download"></i>
                            </span>

                            <button
                                className="btn btn-danger btn-sm"
                                disabled={downloading}
                                onClick={() =>
                                    handleDownload("pdf")
                                }
                            >
                                PDF
                            </button>
                        </div>
                    </div>

                    <div>
                        <input
                            type="text"
                            className="form-control search-box"
                            placeholder="Search..."
                            value={search}
                            onChange={(e) =>
                                setSearch(e.target.value)
                            }
                        />
                    </div>
                </div>
            </div>

            <MetricCards
                total={dashboard.total}
                normal={dashboard.normal}
                anomalies={dashboard.anomalies}
            />

            <ChartSection rows={rows} />

            <DataTable rows={tableRows} />
        </div>
    );
}