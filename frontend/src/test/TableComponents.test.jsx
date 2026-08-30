import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import TableHeader from "../components/TableHeader";
import TableBody from "../components/TableBody";

describe("table components", () => {
  it("formats table headers", () => {
    render(<table><TableHeader columns={["file_name", "result"]} /></table>);
    expect(screen.getByText("File Name")).toBeInTheDocument();
    expect(screen.getByText("Result")).toBeInTheDocument();
  });

  it("renders an empty table state", () => {
    render(<table><TableBody rows={[]} columns={["name"]} /></table>);
    expect(screen.getByText("No records found.")).toBeInTheDocument();
  });

  it("formats numeric cells and anomaly/normal badges", () => {
    render(<table><TableBody rows={[{ score: 0.123456, result: "Anomaly" }, { result: "Normal" }]} columns={["score", "result"]} /></table>);
    expect(screen.getByText("0.123")).toBeInTheDocument();
    expect(screen.getByText("Anomaly")).toHaveClass("badge", "bg-danger");
    expect(screen.getByText("Normal")).toHaveClass("badge", "bg-success");
  });
  it("renders record_id as an integer", () => {
  render( <table> <TableBody rows={[{ record_id: 1.0 }]} columns={["record_id"]} /> </table> );
  expect(screen.getByText("1")).toBeInTheDocument();
  });
});
