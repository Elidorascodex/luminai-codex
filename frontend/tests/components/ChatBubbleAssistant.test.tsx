import { render, screen } from "@testing-library/react";
import ChatBubbleAssistant from "../../components/ChatBubbleAssistant";

describe("ChatBubbleAssistant", () => {
  it("renders citations as pills", () => {
    render(
      <ChatBubbleAssistant
        text="Reference [ConsentOS](https://example.org)"
        citations={[{ label: "ConsentOS", url: "https://example.org" }]}
        r={0.91}
      />
    );

    const links = screen.getAllByRole("link", { name: /ConsentOS/ });
    // The first link is rendered inside the markdown, second is the citation pill.
    expect(links).toHaveLength(2);
    expect(links[1]).toHaveAttribute("href", "https://example.org");
  });
});
