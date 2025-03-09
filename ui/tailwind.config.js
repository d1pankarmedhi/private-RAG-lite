/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}", // Correctly includes JSX/TSX files
    ],
    theme: {
        extend: {},
    },
    plugins: [require('@tailwindcss/typography')],
}