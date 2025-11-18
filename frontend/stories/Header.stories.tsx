import type { Meta, StoryObj } from "@storybook/react";
import Header from "../components/Header";

const meta: Meta<typeof Header> = {
  title: "Screen A/Header",
  component: Header,
  args: {
    userName: "Airth 📚",
    rScore: 0.92,
  },
};

export default meta;

type Story = StoryObj<typeof Header>;

export const Default: Story = {};
