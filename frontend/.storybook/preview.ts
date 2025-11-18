import type { Preview } from "@storybook/react";
import "../styles/globals.css";
import "../styles/components.css";

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
    backgrounds: {
      default: "cosmic",
      values: [
        { name: "cosmic", value: "#050510" },
        { name: "white", value: "#ffffff" },
      ],
    },
  },
};

export default preview;
