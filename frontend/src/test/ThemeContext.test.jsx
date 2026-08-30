import { describe, expect, it } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import ThemeProvider, { useTheme } from "../components/ThemeContext";

function ThemeConsumer() {
  const { darkMode, toggleDarkMode } = useTheme();
  return <button onClick={toggleDarkMode}>{darkMode ? "dark" : "light"}</button>;
}

describe("ThemeProvider", () => {
  it("loads, toggles and persists dark mode", () => {
    localStorage.setItem("darkMode", "enabled");
    render(<ThemeProvider><ThemeConsumer /></ThemeProvider>);
    expect(screen.getByRole("button")).toHaveTextContent("dark");
    expect(document.body).toHaveClass("dark-mode");
    fireEvent.click(screen.getByRole("button"));
    expect(screen.getByRole("button")).toHaveTextContent("light");
    expect(document.body).not.toHaveClass("dark-mode");
    expect(localStorage.getItem("darkMode")).toBe("disabled");
  });
});
