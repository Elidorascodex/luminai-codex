import type { Meta, StoryObj } from "@storybook/react";
import ChatBubbleAssistant from "../components/ChatBubbleAssistant";

const meta: Meta<typeof ChatBubbleAssistant> = {
  title: "Screen A/ChatBubbleAssistant",
  component: ChatBubbleAssistant,
  args: {
    persona: "LuminAI 🧠",
    text: "Notebook anchor loaded.\nRefer to [ConsentOS](https://example.org) for emoji cadence.",
    citations: [{ label: "ConsentOS v1.1", url: "https://example.org" }],
    r: 0.86,
  },
};

export default meta;

type Story = StoryObj<typeof ChatBubbleAssistant>;

export const Primary: Story = {};
