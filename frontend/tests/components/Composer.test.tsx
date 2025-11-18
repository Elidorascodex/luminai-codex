import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { act } from "react";
import Composer from "../../components/Composer";

describe("Composer", () => {
  it("calls onSend with draft contents", async () => {
    const handleSend = vi.fn();
    const handleNotebook = vi.fn();
    const user = userEvent.setup();

    render(<Composer onSend={handleSend} onOpenNotebook={handleNotebook} />);

    const textarea = screen.getByPlaceholderText(/Attune to the witness/i);
    await act(async () => {
      await user.type(textarea, "Hello Airth");
      await user.click(screen.getByRole("button", { name: /send/i }));
    });

    expect(handleSend).toHaveBeenCalledWith("Hello Airth");
  });

  it("opens notebook when shortcut clicked", async () => {
    const handleNotebook = vi.fn();
    const user = userEvent.setup();

    render(<Composer onSend={vi.fn()} onOpenNotebook={handleNotebook} />);

    await act(async () => {
      await user.click(screen.getByRole("button", { name: /Notebook/i }));
    });
    expect(handleNotebook).toHaveBeenCalled();
  });
});
