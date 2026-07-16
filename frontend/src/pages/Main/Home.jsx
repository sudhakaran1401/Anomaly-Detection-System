import { useState } from "react";
import { useNavigate } from "react-router-dom";

import ClassificationService from "../../services/ClassificationService";
import AnomalyService from "../../services/AnomalyService";

import {
    ANOMALY_MODELS,
    CLASSIFICATION_MODELS,
} from "../../constants/models";

import LoadingSpinner from "../../components/Spinner";
import Message from "../../components/Message";
import { useTheme } from "../../components/ThemeContext";

export default function Home() {
    const navigate = useNavigate();
    const { darkMode } = useTheme();

    const [selectedFile, setSelectedFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const [algorithm, setAlgorithm] = useState("isolation_forest");
    const [contamination, setContamination] = useState(0.01);
    const [scaler, setScaler] = useState("standard");

    const [message, setMessage] = useState({
        type: "",
        text: "",
    });

    const handleFileChange = (e) => {
        if (e.target.files.length > 0) {
            setSelectedFile(e.target.files[0]);
        } else {
            setSelectedFile(null);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        setMessage({
            type: "",
            text: "",
        });

        if (!selectedFile) {
            setMessage({
                type: "warning",
                text: "Please select a CSV file.",
            });
            return;
        }

        setLoading(true);

        try {
            const formData = new FormData();

            formData.append("file", selectedFile);

            formData.append("model_name", algorithm);
            formData.append("contamination", contamination);
            formData.append("scaler_type", scaler);

            console.log("Selected Model:", algorithm);
            console.log("Scaler:", scaler);
            console.log("Contamination:", contamination);

            const classification =
                CLASSIFICATION_MODELS.some(
                    (m) => m.value === algorithm
                );

            const response = classification
                ? await ClassificationService.classifyDataset(formData)
                : await AnomalyService.analyzeDataset(formData);

            if (classification) {

                sessionStorage.setItem(
                    "classificationResult",
                    JSON.stringify(response.data.result)
                );

                navigate("/classification");

            } else {

                const anomalyResult = {
                    ...response.data.data,

                    model_name: algorithm,

                    scaler_type: scaler,

                    contamination: contamination,
                };

                sessionStorage.setItem(
                    "anomalyResult",
                    JSON.stringify(anomalyResult)
                );

                navigate("/dashboard");

            }

        } catch (error) {

            console.error(error);

            setMessage({
                type: "danger",
                text:
                    error?.response?.data?.message ||
                    error?.response?.data?.detail ||
                    "Failed to process dataset.",
            });

        } finally {

            setLoading(false);

        }
    };

    return (
        <div className="container vh-100 d-flex align-items-center justify-content-center">

            <div
                className={`card upload-card shadow p-4 col-md-5 ${
                    darkMode
                        ? "theme-dark-card"
                        : "theme-light-card"
                }`}
            >

                <h3 className="text-center mb-2">
                    Smart Anomaly Detection
                </h3>

                <p
                    className={`text-center mb-4 ${
                        darkMode
                            ? "upload-subtitle-dark"
                            : "upload-subtitle-light"
                    }`}
                >
                    Upload your dataset to detect anomalies instantly
                </p>

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

                <form onSubmit={handleSubmit}>

                    <label className="upload-area w-100 mb-3">

                        <input
                            type="file"
                            className="form-control d-none"
                            accept=".csv"
                            onChange={handleFileChange}
                        />

                        <div className="text-center">

                            <h6 className="mb-1">
                                Click or drag file here
                            </h6>

                            <small
                                className={
                                    darkMode
                                        ? "upload-subtitle-dark"
                                        : "upload-subtitle-light"
                                }
                            >
                                Supports CSV files
                            </small>

                        </div>

                    </label>

                    {selectedFile && (

                        <div className="selected-file">

                            {selectedFile.name}

                        </div>

                    )}

                    <select
                        className="form-select mb-3"
                        value={algorithm}
                        onChange={(e) =>
                            setAlgorithm(e.target.value)
                        }
                    >

                        <optgroup label="Anomaly Detection">

                            {ANOMALY_MODELS.map((model) => (
                                <option
                                    key={model.value}
                                    value={model.value}
                                >
                                    {model.label}
                                </option>
                            ))}

                        </optgroup>

                        <optgroup label="Classification">

                            {CLASSIFICATION_MODELS.map((model) => (
                                <option
                                    key={model.value}
                                    value={model.value}
                                >
                                    {model.label}
                                </option>
                            ))}

                        </optgroup>

                    </select>

                    <div className="mb-3">

                        <label className="form-label">
                            Contamination
                        </label>

                        <input
                            type="range"
                            className="form-range"
                            min="0.01"
                            max="0.20"
                            step="0.01"
                            value={contamination}
                            onChange={(e) =>
                                setContamination(e.target.value)
                            }
                        />

                    </div>

                    <select
                        className="form-select mb-4"
                        value={scaler}
                        onChange={(e) =>
                            setScaler(e.target.value)
                        }
                    >

                        <option value="standard">
                            StandardScaler
                        </option>

                        <option value="minmax">
                            MinMaxScaler
                        </option>

                        <option value="robust">
                            RobustScaler
                        </option>

                    </select>

                    <button
                        className="btn btn-primary w-100"
                        disabled={loading}
                    >
                        {loading
                            ? "Processing..."
                            : "Upload & Analyze"}
                    </button>

                </form>

                {loading && (
                    <div className="mt-3">
                        <LoadingSpinner message="Processing file... Please wait" />
                    </div>
                )}

            </div>

        </div>
    );
}