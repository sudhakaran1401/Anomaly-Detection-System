import { describe, expect, it, beforeEach, vi } from "vitest";

vi.mock("axios", () => {
  const apiInstance = { interceptors: { request: { use: vi.fn() }, response: { use: vi.fn() } } };
  return {
    default: { create: vi.fn(() => apiInstance), post: vi.fn() },
  };
});

describe("API client configuration", () => {
  beforeEach(() => {
    vi.resetModules();
    localStorage.clear();
  });

  it("creates the API client with the configured base URL and credentials", async () => {
    const axios = (await import("axios")).default;
    await import("../api/axios");
    expect(axios.create).toHaveBeenCalledWith(
      expect.objectContaining({ withCredentials: true, baseURL: expect.stringContaining("/api/") }),
    );
  });

  it("exports a configured client instance", async () => {
    const api = (await import("../api/axios")).default;
    expect(api).toBeDefined();
    expect(api.interceptors).toBeDefined();
  });
});
