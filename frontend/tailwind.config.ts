import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "primary-1": "#FBFEF9",
        "primary-2": "#191923",
        "primary-3": "#0E79B2",
        "secondary-1": "#f8fafc",
        "secondary-2": "#427AA1"
      },
      fontFamily: {
        "montserrat": ['var(--font-montserrat)'],
        "karla": ['var(--font-karla)']
      },
      fontSize: {
        "m-32": "32px",
        "m-24": "24px",
        "m-18": "18px",
        "m-16": "16px",
        "k-20": "20px",
        "k-16": "16px"
      }
    },
  },
  plugins: [],
};
export default config;
