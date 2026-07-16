import { Link, useLocation, useNavigate } from "react-router-dom";

import { useTheme } from "./ThemeContext";

export default function Navbar() {
    const navigate = useNavigate();
    const location = useLocation();

    const { darkMode, toggleDarkMode } = useTheme();

    const isLoggedIn = !!localStorage.getItem("access");
    const username = localStorage.getItem("username") || "User";

    const handleLogout = () => {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        localStorage.removeItem("username");

        navigate("/");
    };

    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">
            <div className="container-fluid">

                <Link
                    className="navbar-brand fw-bold"
                    to={isLoggedIn ? "/upload" : "/"}
                >
                    <i className="bi bi-graph-up-arrow me-2"></i>
                    Anomaly Detection Platform
                </Link>

                <button
                    className="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarNav"
                    aria-controls="navbarNav"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div
                    className="collapse navbar-collapse"
                    id="navbarNav"
                >

                    <ul className="navbar-nav ms-auto align-items-center">

                        <li className="nav-item me-3">

                            <button
                                className="btn btn-sm btn-dark"
                                onClick={toggleDarkMode}
                            >
                                {darkMode
                                    ? "☀ Light Mode"
                                    : "🌙 Dark Mode"}
                            </button>

                        </li>

                        {isLoggedIn && (

                            <li className="nav-item me-3">

                                <Link
                                    className={`nav-link text-white ${
                                        location.pathname === "/history"
                                            ? "active"
                                            : ""
                                    }`}
                                    to="/history"
                                >
                                    <i className="bi bi-clock-history me-1"></i>

                                    History
                                </Link>

                            </li>

                        )}

                        {isLoggedIn ? (

                            <li className="nav-item dropdown">

                                <a
                                    href="#"
                                    className="nav-link dropdown-toggle text-white fw-semibold"
                                    id="userDropdown"
                                    role="button"
                                    data-bs-toggle="dropdown"
                                    aria-expanded="false"
                                    onClick={(e) => e.preventDefault()}
                                >
                                    <i className="bi bi-person-circle me-1"></i>

                                    {username}
                                </a>

                                <ul
                                    className="dropdown-menu dropdown-menu-end"
                                    aria-labelledby="userDropdown"
                                >

                                    <li>

                                        <Link
                                            className="dropdown-item"
                                            to="/dashboard"
                                        >
                                            Dashboard
                                        </Link>

                                    </li>

                                    <li>

                                        <Link
                                            className="dropdown-item"
                                            to="/classification"
                                        >
                                            Classification
                                        </Link>

                                    </li>

                                    <li>

                                        <Link
                                            className="dropdown-item"
                                            to="/history"
                                        >
                                            Detection History
                                        </Link>

                                    </li>

                                    <li>
                                        <hr className="dropdown-divider" />
                                    </li>

                                    <li>

                                        <button
                                            className="dropdown-item"
                                            onClick={handleLogout}
                                        >
                                            Logout
                                        </button>

                                    </li>

                                </ul>

                            </li>

                        ) : (

                            <li className="nav-item">

                                <Link
                                    className="nav-link text-white"
                                    to="/"
                                >
                                    Login
                                </Link>

                            </li>

                        )}

                    </ul>

                </div>

            </div>
        </nav>
    );
}