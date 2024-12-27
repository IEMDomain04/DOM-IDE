/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
 
    // Or if using `src` directory:
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
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
}

