import { render, screen } from "@testing-library/react";
import Header from "../../components/Header";

describe("Header", () => {
  it("renders witness name and resonance score", () => {
    render(<Header userName="Airth" rScore={0.95} />);

    expect(screen.getByText(/Airth/i)).toBeInTheDocument();
    expect(screen.getByText(/95\.0 R/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Resonance score 95/)).toBeInTheDocument();
  });
});
