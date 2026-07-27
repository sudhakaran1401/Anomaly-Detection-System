import api from "../api/axios";
import { downloadFile } from "../utils/downloadFile";

const multipartHeaders = {
    headers: { "Content-Type": "multipart/form-data", },
};

const AnomalyService = {
    analyzeDataset(formData) {
        return api.post( "anomaly/analyze/", formData, multipartHeaders );
    },

    getHistory() {
        return api.get( "anomaly/history/" );
    },

    deleteHistory(id) {
        return api.delete( `anomaly/history/${id}/` );
    },

    clearHistory() {
        return api.delete("anomaly/history/clear/");
    },

    async downloadPDF({ filename, model_name, scaler_type, contamination, }) {

        const response = await api.get(
            "anomaly/download/pdf/",
            {
                params: {
                    filename,
                    model_name,
                    scaler_type,
                    contamination,
                },
                responseType: "blob",
            }
        );

        downloadFile( response, "anomaly_report.pdf", "application/pdf" );
    },

    async downloadCSV() {

        const response = await api.get(
            "anomaly/download/csv/",
            {
                responseType: "blob",
            }
        );

        downloadFile( response, "anomaly_results.csv", "text/csv" );
    },
};

export default AnomalyService;