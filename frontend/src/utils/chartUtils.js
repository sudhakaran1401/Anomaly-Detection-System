export const getThemeColors = (darkMode) => ({
    textColor: darkMode ? "#ffffff" : "#222222",
    gridColor: darkMode ? "#444444" : "#ececec",
    borderColor: darkMode ? "#1f1f1f" : "#ffffff",
});

export const getCommonOptions = ({
    title,
    textColor,
    gridColor,
    showLegend = true,
}) => ({
    responsive: true,
    maintainAspectRatio: false,
    animation: {
        duration: 1000,
        easing: "easeInOutQuart",
    },

    transitions: {
        active: {
            animation: {
                duration: 1000,
            },
        },
    },

    plugins: {
        title: {
            display: !!title,
            text: title,
            color: textColor,
            font: {
                size: 18,
                weight: "bold",
            },
        },

        legend: {
            display: showLegend,
            position: "top",

            labels: {
                color: textColor,           
            },
        },
    },

    scales: {
        x: {
            ticks: {
                color: textColor,
            },

            grid: {
                color: gridColor,
            },
        },

        y: {
            ticks: {
                color: textColor,
            },

            grid: {
                color: gridColor,
            },
        },
    },
});