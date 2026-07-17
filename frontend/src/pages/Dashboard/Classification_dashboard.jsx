import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import ClassificationService from "../../services/ClassificationService";
import { getPerformanceInsight } from "../../utils/performanceInsight";

import LoadingSpinner from "../../components/Spinner";
import Message from "../../components/Message";

import useMessage from "../../hooks/useMessage";
import DatasetCard from "../../components/dashboard/DatasetCard";
import DatasetSummary from "../../components/dashboard/DatasetSummary";
import DetectionSummary from "../../components/dashboard/DetectionSummary";
import MetricGrid from "../../components/dashboard/MetricGrid";
import ConfusionMatrix from "../../components/dashboard/ConfusionMatrix";
import PerformanceInsightCard from "../../components/dashboard/InsightCard";
import DashboardActions from "../../components/dashboard/Actions";

export default function ClassificationDashboard() {
    const navigate = useNavigate();

    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);

    const {
        message,
        clearMessage,
        showError,
        showSuccess,
    } = useMessage();

    useEffect(() => {
        fetchLatestResult();
    }, []);

    const fetchLatestResult = async () => {
        try {
            const response =
                await ClassificationService.getResults();

            if (
                response.data.success &&
                response.data.results.length
            ) {
                const latest =
                    response.data.results[0];

                setReport({
                    id: latest.id,
                    filename: latest.file_name,
                    model_name: latest.model_name,
                    target_column: latest.target_column,

                    metrics: {
                        accuracy: latest.accuracy,
                        precision: latest.precision,
                        recall: latest.recall,
                        f1: latest.f1_score,
                        roc_auc: latest.roc_auc,
                        confusion_matrix:
                            latest.confusion_matrix,
                        summary: latest.summary,
                        dataset_summary:
                            latest.dataset_summary,
                    },

                    confusion_matrix_chart:
                        latest.confusion_matrix_chart,
                });
            }
        } catch (error) {
            showError(
                error.response?.data?.message ||
                "Unable to load classification results."
            );
        } finally {
            setLoading(false);
        }
    };

    const downloadPDF = async () => {

    if (!report) return;

    clearMessage();

    try {

        await ClassificationService.downloadPDF(
            report.id
        );

        showSuccess(
            "PDF downloaded successfully."
        );

    } catch (error) {

        showError(
            error.response?.data?.message ||
            "Failed to download PDF."
        );

    }
    };

    if (loading) {
        return <LoadingSpinner />;
    }

    if (!report) {
        return (
            <div className="container py-5 text-center">
                <h3>No Classification Result Found</h3>

                <Message
                    type={message.type}
                    message={message.text}
                    onClose={clearMessage}
                />
            </div>
        );
    }

    const metrics = report.metrics;
    const summary = metrics.summary;
    const dataset = metrics.dataset_summary || {};

    const insight = getPerformanceInsight(metrics);

    const modelName = report.model_name
        .replaceAll("_", " ")
        .replace(/\b\w/g, (c) =>
            c.toUpperCase()
        );

    return (
        <div className="container py-5">

            <div className="text-center mb-5">
                <h2 className="fw-bold">
                    Classification Analysis Report
                </h2>
            </div>

            <Message
                type={message.type}
                message={message.text}
                onClose={clearMessage}
            />

            <DatasetCard
                filename={report.filename}
                modelName={modelName}
            />

            {/* <DatasetSummary
                dataset={dataset}
            /> */}

            <DetectionSummary
                summary={summary}
            />

            <MetricGrid
                metrics={metrics}
            />

            <ConfusionMatrix
                matrix={metrics.confusion_matrix}
                image={`http://127.0.0.1:8000/media/${report.confusion_matrix_chart}`}
            />

            <PerformanceInsightCard
                insight={insight}
            />

            <DashboardActions
                onUpload={() => navigate("/upload")}
                onDownload={downloadPDF}
            />

        </div>
    );
}