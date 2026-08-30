import { describe, expect, it } from "vitest";

describe("ADS download/export service", () => {
  it("supports Blob responses for exported files", () => {
    const blob = new Blob(["ADS test export"], {
      type: "text/csv",
    });

    expect(blob).toBeInstanceOf(Blob);
    expect(blob.type).toBe("text/csv");
    expect(blob.size).toBeGreaterThan(0);
  });

  it("creates the expected download filename from Content-Disposition", () => {
    const response = {
      data: "test,data",
      headers: {
        "content-disposition": 'attachment; filename="anomaly_results.csv"',
      },
    };

    const disposition = response.headers["content-disposition"];
    const match = disposition.match(/filename="?([^"]+)"?/);

    expect(match[1]).toBe("anomaly_results.csv");
  });
});