import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../../api/axios";
import Message from "../../components/Message";
import { useTheme } from "../../components/ThemeContext";

export default function Login() {
    const navigate = useNavigate();
    const { darkMode } = useTheme();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);

    const [message, setMessage] = useState({
        type: "",
        text: "",
    });

    const handleSubmit = async (e) => {
        e.preventDefault();

        setLoading(true);

        setMessage({
            type: "",
            text: "",
        });

        try {
            const response = await api.post("token/", {
                username,
                password,
            });

            localStorage.setItem(
                "access",
                response.data.access
            );

            localStorage.setItem(
                "refresh",
                response.data.refresh
            );

            localStorage.setItem(
                "username",
                username
            );

            setMessage({
                type: "success",
                text: "Login successful.",
            });

            setTimeout(() => {
                navigate("/upload");
            }, 800);

        } catch {

            setMessage({
                type: "danger",
                text: "Invalid username or password.",
            });

        } finally {

            setLoading(false);

        }
    };

    return (
        <div className="container vh-100 d-flex align-items-center justify-content-center">

            <div
                className={`card upload-card shadow p-4 col-md-4 ${
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
                            : "text-muted"
                    }`}
                >
                    Login to continue
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

                    <div className="mb-3">

                        <label className="form-label">
                            Username
                        </label>

                        <input
                            type="text"
                            className="form-control"
                            placeholder="Enter username"
                            value={username}
                            onChange={(e) =>
                                setUsername(e.target.value)
                            }
                        />

                    </div>

                    <div className="mb-3">

                        <label className="form-label">
                            Password
                        </label>

                        <input
                            type="password"
                            className="form-control"
                            placeholder="Enter password"
                            value={password}
                            onChange={(e) =>
                                setPassword(e.target.value)
                            }
                        />

                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary w-100 mt-4"
                        disabled={loading}
                    >
                        {loading
                            ? "Logging in..."
                            : "Login"}
                    </button>

                </form>

            </div>

        </div>
    );
}