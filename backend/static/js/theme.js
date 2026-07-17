function updateThemeButton() {

    const button = document.getElementById("themeToggle");

    if (!button) return;

    if (document.body.classList.contains("dark-mode")) {

        button.innerHTML = "☀ Light Mode";

    } else {

        button.innerHTML = "🌙 Dark Mode";

    }
}

function applyDarkMode() {

    const body = document.getElementById("body");

    if (!body) return;

    const darkMode = localStorage.getItem("darkMode");

    if (darkMode === "enabled") {

        body.classList.add("dark-mode");

    } else {

        body.classList.remove("dark-mode");

    }

    updateThemeButton();
}

function toggleDark() {

    const body = document.getElementById("body");

    if (!body) return;

    body.classList.toggle("dark-mode");

    if (body.classList.contains("dark-mode")) {

        localStorage.setItem("darkMode", "enabled");

    } else {

        localStorage.setItem("darkMode", "disabled");

    }

    updateThemeButton();
}

document.addEventListener("DOMContentLoaded", applyDarkMode);