import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import LoadingSpinner from '../components/Spinner';

describe("presentational components", () => {
  it("renders loading spinner and custom message", () => {
    render(<LoadingSpinner message="Processing dataset" />);
    expect(screen.getByRole("status")).toBeInTheDocument();
    expect(screen.getByText("Processing dataset")).toBeInTheDocument();
  });
});


