import type { Config } from "tailwindcss";

export default {
  darkMode: "class", // Enable class-based dark mode
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "light-background": "#c3c6d4",  // Light mode background
        "light-foreground": "#242a47",  // Light mode text color
        "dark-background": "#181819",   // Dark mode background
        "dark-foreground": "#391d1d",   // Dark mode text color
      },
    },
  },
  plugins: [],
} satisfies Config;
