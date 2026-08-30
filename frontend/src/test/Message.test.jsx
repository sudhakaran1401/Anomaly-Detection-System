import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import Message from "../components/Message";

describe("Message component", () => {
  it("renders and closes an alert", () => {
    const onClose = vi.fn();
    render(<Message type="danger" message="Something failed" onClose={onClose} />);
    expect(screen.getByRole("alert")).toHaveClass("alert-danger");
    fireEvent.click(screen.getByRole("button", { name: /close/i }));
    expect(onClose).toHaveBeenCalledOnce();
  });

  it("renders nothing when the message is empty", () => {
    const { container } = render(<Message message="" />);
    expect(container.firstChild).toBeNull();
  });
});
