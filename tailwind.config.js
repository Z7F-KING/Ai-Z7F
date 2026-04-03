/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        darkBg: "#0d1117",
        panelBg: "#161b22",
        borderClr: "#30363d",
        neonCyan: "#22d3ee"
      }
    },
  },
  plugins: [],
}
