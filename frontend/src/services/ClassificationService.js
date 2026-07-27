import api from "../api/axios";
import { downloadFile } from "../utils/downloadFile";

const multipartHeaders = {
    headers: {
        "Content-Type": "multipart/form-data",
    },
};

const ClassificationService = {
    classifyDataset(formData) {
        return api.post(
            "classification/classify/",
            formData,
            multipartHeaders
        );
    },

    getResults() {
        return api.get(
            "classification/results/"
        );
    },

    getResult(id) {
        return api.get(
            `classification/results/${id}/`
        );
    },

    deleteResult(id) {
        return api.delete(
            `classification/results/${id}/`
        );
    },

    async downloadPDF(id) {
        const response = await api.get(
            `classification/results/${id}/download/pdf/`,
            {
                responseType: "blob",
            }
        );

        downloadFile(
            response,
            "classification_report.pdf",
            "application/pdf"
        );
    },
};

export default ClassificationService;