import api from "../api/axios";
import { downloadFile } from "../utils/downloadFile";

const multipartHeaders = {
    headers: {
        "Content-Type": "multipart/form-data",
    },
};

const AnomalyService = {
    analyzeDataset(formData) {
        return api.post(
            "anomaly/analyze/",
            formData,
            multipartHeaders
        );
    },

    getHistory() {
        return api.get("anomaly/history/");
    },

    // Delete ONE history record
    deleteHistory(id) {
        return api.delete(`anomaly/history/${id}/`);
    },

    // Delete ALL history records
    clearHistory() {
        return api.delete("anomaly/history/clear/");
    },

    async downloadPDF({
        filename,
        model_name,
        scaler_type,
        contamination,
        filter = "all",
    }) {
        const response = await api.get(
            "anomaly/download/pdf/",
            {
                params: {
                    filename,
                    model_name,
                    scaler_type,
                    contamination,
                    filter,
                },
                responseType: "blob",
            }
        );

        downloadFile(
            response,
            "anomaly_report.pdf",
            "application/pdf"
        );

        return response;
    },

    async downloadCSV(filter = "all") {
        const response = await api.get(
            "anomaly/download/csv/",
            {
                params: {
                    filter,
                },
                responseType: "blob",
            }
        );

        downloadFile(
            response,
            "anomaly_results.csv",
            "text/csv"
        );

        return response;
    },
};

export default AnomalyService;