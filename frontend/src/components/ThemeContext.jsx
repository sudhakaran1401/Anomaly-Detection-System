import {
    createContext,
    useContext,
    useEffect,
    useState,
} from "react";

const ThemeContext = createContext();

// eslint-disable-next-line react-refresh/only-export-components
export const useTheme = () => useContext(ThemeContext);

export default function ThemeProvider({ children }) {

    const [darkMode, setDarkMode] = useState(
        localStorage.getItem("darkMode") === "enabled"
    );

    useEffect(() => {

        document.body.classList.toggle(
            "dark-mode",
            darkMode
        );

        localStorage.setItem(
            "darkMode",
            darkMode ? "enabled" : "disabled"
        );

    }, [darkMode]);

    const toggleDarkMode = () => {

        setDarkMode(prev => !prev);

    };

    return (

        <ThemeContext.Provider
            value={{
                darkMode,
                toggleDarkMode,
            }}
        >

            {children}

        </ThemeContext.Provider>

    );

}