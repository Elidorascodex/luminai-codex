import type { Meta, StoryObj } from "@storybook/react";
import NotebookStub from "../components/NotebookStub";
import { notebookEntries } from "../lib/mockData";

const meta: Meta<typeof NotebookStub> = {
  title: "Screen A/NotebookStub",
  component: NotebookStub,
  args: {
    open: true,
    entries: notebookEntries,
    onClose: () => undefined,
    onOpen: () => undefined,
  },
};

export default meta;

type Story = StoryObj<typeof NotebookStub>;

export const Default: Story = {};
