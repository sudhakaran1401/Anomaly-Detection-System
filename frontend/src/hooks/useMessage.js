import { useRef, useState } from "react";

export default function useMessage() {
    const [message, setMessage] = useState({
        type: "",
        text: "",
    });

    const timerRef = useRef(null);

    const clearMessage = () => {
        if (timerRef.current) {
            clearTimeout(timerRef.current);
        }

        setMessage({
            type: "",
            text: "",
        });
    };

    const showMessage = (type, text) => {
        if (timerRef.current) {
            clearTimeout(timerRef.current);
        }

        setMessage({
            type,
            text,
        });

        timerRef.current = setTimeout(() => {
            setMessage({
                type: "",
                text: "",
            });
        }, 2000);
    };

    const showSuccess = (text) =>
        showMessage("success", text);

    const showError = (text) =>
        showMessage("danger", text);

    return {
        message,
        clearMessage,
        showSuccess,
        showError,
    };
}