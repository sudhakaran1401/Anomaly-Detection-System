import { describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import AppRoutes from "../App";

vi.mock("../components/Navbar", () => ({ default: () => <nav>Navigation</nav> }));
vi.mock("../pages/Main/Login", () => ({ default: () => <div>Login Page</div> }));
vi.mock("../pages/Main/Home", () => ({ default: () => <div>Upload Page</div> }));
vi.mock("../pages/Dashboard/Anomaly_dashboard", () => ({ default: () => <div>Anomaly Dashboard</div> }));
vi.mock("../pages/Dashboard/Classification_dashboard", () => ({ default: () => <div>Classification Dashboard</div> }));
vi.mock("../pages/List/History", () => ({ default: () => <div>History Page</div> }));

describe("application routing", () => {
  it("renders the login route", () => {
    render(<AppRoutes />);
    expect(screen.getByText("Login Page")).toBeInTheDocument();
    expect(screen.getByText("Navigation")).toBeInTheDocument();
  });
});
