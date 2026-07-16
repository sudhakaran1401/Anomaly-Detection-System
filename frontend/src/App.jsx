import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Main/Home";
import Login from "./pages/Main/Login";
import Navbar from "./components/Navbar";
import AnomalyDashboard from "./pages/Dashboard/Anomaly_dashboard";
import ClassificationDashboard from "./pages/Dashboard/Classification_dashboard";
import History from "./pages/List/History";

export default function AppRoutes() {
    return (
        <BrowserRouter>
            <Navbar />

            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/upload" element={<Home />} />
                <Route path="/dashboard" element={<AnomalyDashboard />} />
                <Route path="/history" element={<History />} />
                <Route
                    path="/classification"
                    element={<ClassificationDashboard />}
                />
            </Routes>

        </BrowserRouter>
    );
}