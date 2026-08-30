import { describe, expect, it } from "vitest";
import { getThemeColors, getCommonOptions } from "../utils/chartUtils";

describe("chart utilities", () => {
  it("returns correct light and dark theme colors", () => {
    expect(getThemeColors(false)).toEqual({ textColor: "#222222", gridColor: "#ececec", borderColor: "#ffffff" });
    expect(getThemeColors(true)).toEqual({ textColor: "#ffffff", gridColor: "#444444", borderColor: "#1f1f1f" });
  });

  it("builds chart options with title and legend controls", () => {
    const options = getCommonOptions({ title: "Scores", textColor: "#fff", gridColor: "#000", showLegend: false });
    expect(options.responsive).toBe(true);
    expect(options.plugins.title).toMatchObject({ display: true, text: "Scores", color: "#fff" });
    expect(options.plugins.legend.display).toBe(false);
    expect(options.scales.x.grid.color).toBe("#000");
  });
});
