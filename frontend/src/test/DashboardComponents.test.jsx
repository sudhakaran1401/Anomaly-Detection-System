import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";

import StatCard from "../components/dashboard/StatCard";
import Pagination from "../components/dashboard/Pagination";
import DatasetCard from "../components/dashboard/DatasetCard";
import DetectionSummary from "../components/dashboard/DetectionSummary";
import MetricGrid from "../components/dashboard/MetricGrid";
import MetricCards from "../components/dashboard/MetricCards";
import DatasetSummary from "../components/dashboard/DatasetSummary";
import PerformanceInsightCard from "../components/dashboard/InsightCard";
import ConfusionMatrix from "../components/dashboard/ConfusionMatrix";
import BaseChart from "../components/dashboard/BaseChart";

// MetricCards uses useTheme() internally.
// Mock only the hook; no ThemeProvider is required for this unit test.
vi.mock("../components/ThemeContext", () => ({
  useTheme: () => ({
    darkMode: false,
  }),
}));

describe("dashboard components", () => {
  it("formats StatCard values to the requested precision", () => {
    render(
      <StatCard
        title="Accuracy"
        value={0.98765}
        precision={3}
        color="success"
        bordered
      />
    );

    expect(screen.getByText("0.988")).toBeInTheDocument();
    expect(screen.getByText("Accuracy")).toBeInTheDocument();
  });

  it("shows N/A when a StatCard value is missing", () => {
    render(<StatCard title="ROC-AUC" value={null} />);

    expect(screen.getByText("N/A")).toBeInTheDocument();
  });

  it("renders pagination range and disables boundary buttons", () => {
    const setCurrentPage = vi.fn();
    const setRowsPerPage = vi.fn();

    render(
      <Pagination
        totalRows={12}
        rowsPerPage={5}
        currentPage={1}
        setCurrentPage={setCurrentPage}
        setRowsPerPage={setRowsPerPage}
      />
    );

    expect(
      screen.getByText("Showing 1-5 of 12")
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: "Previous" })
    ).toBeDisabled();

    fireEvent.click(
      screen.getByRole("button", { name: "Next" })
    );

    expect(setCurrentPage).toHaveBeenCalledWith(2);
  });

  it("resets pagination to page one when rows per page changes", () => {
    const setCurrentPage = vi.fn();
    const setRowsPerPage = vi.fn();

    render(
      <Pagination
        totalRows={30}
        rowsPerPage={5}
        currentPage={3}
        setCurrentPage={setCurrentPage}
        setRowsPerPage={setRowsPerPage}
      />
    );

    fireEvent.change(
      screen.getByRole("combobox"),
      {
        target: { value: "10" },
      }
    );

    expect(setRowsPerPage).toHaveBeenCalledWith(10);
    expect(setCurrentPage).toHaveBeenCalledWith(1);
  });

  it("renders dataset filename, model and optional actions", () => {
    render(
      <DatasetCard
        filename="customers.csv"
        modelName="Isolation Forest"
        actions={<button>Delete</button>}
      />
    );

    expect(
      screen.getByText("customers.csv")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Isolation Forest")
    ).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: "Delete" })
    ).toBeInTheDocument();
  });

  it("renders detection summary metrics", () => {
    render(
      <DetectionSummary
        summary={{
          total_records: 100,
          normal_records: 92,
          anomaly_records: 8,
        }}
      />
    );

    expect(
      screen.getByText("Total Records")
    ).toBeInTheDocument();

    expect(
      screen.getByText("100")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Normal")
    ).toBeInTheDocument();

    expect(
      screen.getByText("92")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Anomalies")
    ).toBeInTheDocument();

    expect(
      screen.getByText("8")
    ).toBeInTheDocument();
  });

  it("renders all classification metric cards", () => {
    render(
      <MetricGrid
        metrics={{
          accuracy: 0.91,
          precision: 0.9,
          recall: 0.89,
          f1: 0.895,
          roc_auc: 0.93,
        }}
      />
    );

    expect(
      screen.getByText("Accuracy")
    ).toBeInTheDocument();

    expect(
      screen.getByText("0.9100")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Precision")
    ).toBeInTheDocument();

    expect(
      screen.getByText("0.9000")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Recall")
    ).toBeInTheDocument();

    expect(
      screen.getByText("0.8900")
    ).toBeInTheDocument();

    expect(
      screen.getByText("F1 Score")
    ).toBeInTheDocument();

    expect(
      screen.getByText("0.8950")
    ).toBeInTheDocument();

    expect(
      screen.getByText("ROC-AUC")
    ).toBeInTheDocument();

    expect(
      screen.getByText("0.9300")
    ).toBeInTheDocument();
  });

  it("passes chart data and options to the chart component", () => {
    const Chart = ({ data, options }) => (
      <div data-testid="chart">
        {data.label}:{options.title}
      </div>
    );

    render(
      <BaseChart
        ChartComponent={Chart}
        data={{ label: "dataset" }}
        options={{ title: "Anomalies" }}
      />
    );

    expect(
      screen.getByTestId("chart")
    ).toHaveTextContent("dataset:Anomalies");
  });

  it("renders anomaly metric cards", () => {
    render(
      <MetricCards
        total={20}
        normal={17}
        anomalies={3}
      />
    );

    expect(
      screen.getByText("Total Records")
    ).toBeInTheDocument();

    expect(
      screen.getByText("20")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Normal")
    ).toBeInTheDocument();

    expect(
      screen.getByText("17")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Anomalies")
    ).toBeInTheDocument();

    expect(
      screen.getByText("3")
    ).toBeInTheDocument();
  });

  it("renders dataset training and testing summary", () => {
    render(
      <DatasetSummary
        dataset={{
          total_dataset_records: 100,
          training_records: 70,
          testing_records: 30,
        }}
      />
    );

    expect(
      screen.getByText("Total Dataset Records")
    ).toBeInTheDocument();

    expect(
      screen.getByText("100")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Training Records")
    ).toBeInTheDocument();

    expect(
      screen.getByText("70")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Testing Records")
    ).toBeInTheDocument();

    expect(
      screen.getByText("30")
    ).toBeInTheDocument();
  });

  it("renders a performance insight with its severity class", () => {
    render(
      <PerformanceInsightCard
        insight={{
          className: "alert-success",
          title: "Excellent Model Performance",
          message: "Reliable predictions.",
        }}
      />
    );

    expect(
      screen.getByText("Performance Insight")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Excellent Model Performance")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Reliable predictions.")
    ).toBeInTheDocument();
  });

  it("renders confusion matrix values and image", () => {
    render(
      <ConfusionMatrix
        matrix={[
          [8, 1],
          [2, 9],
        ]}
        image="/media/matrix.png"
      />
    );

    expect(
      screen.getByText("Predicted Normal")
    ).toBeInTheDocument();

    expect(
      screen.getByText("Predicted Anomaly")
    ).toBeInTheDocument();

    expect(
      screen.getByText("8")
    ).toBeInTheDocument();

    expect(
      screen.getByText("9")
    ).toBeInTheDocument();

    expect(
      screen.getByRole("img", {
        name: "Confusion Matrix",
      })
    ).toHaveAttribute(
      "src",
      "/media/matrix.png"
    );
  });

  it("uses server-side pagination flags", () => {
    const setCurrentPage = vi.fn();

    render(
      <Pagination
        totalRows={25}
        rowsPerPage={5}
        currentPage={2}
        setCurrentPage={setCurrentPage}
        setRowsPerPage={vi.fn()}
        serverSide
        hasPrevious={true}
        hasNext={false}
      />
    );

    expect(
      screen.getByRole("button", {
        name: "Previous",
      })
    ).not.toBeDisabled();

    expect(
      screen.getByRole("button", {
        name: "Next",
      })
    ).toBeDisabled();
  });
});