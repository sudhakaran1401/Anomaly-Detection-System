import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";

import ThemeProvider from "./components/ThemeContext";

import "./index.css";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

ReactDOM.createRoot(document.getElementById("root")).render(

    <React.StrictMode>

        <ThemeProvider>

            <App />

        </ThemeProvider>

    </React.StrictMode>

);