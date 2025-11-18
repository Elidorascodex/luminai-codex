import type { Meta, StoryObj } from "@storybook/react";
import Composer from "../components/Composer";

const meta: Meta<typeof Composer> = {
  title: "Screen A/Composer",
  component: Composer,
  args: {
    onSend: (text: string) => alert(text),
    onOpenNotebook: () => alert("Notebook shortcut"),
  },
};

export default meta;

type Story = StoryObj<typeof Composer>;

export const Default: Story = {};
