/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/templates/**/*.html",
    "./staticfiles/js/**/*.js",
    "./js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          gold: '#c8a66e',
          blue: '#245d81',
        },
        secondary: {
          'gold-light': '#d4b886',
          'gold-dark': '#b39456',
          'blue-light': '#2e7aa8',
          'blue-dark': '#1a4660',
        }
      },
      fontFamily: {
        'heading': ['Montserrat', 'sans-serif'],
        'body': ['Lato', 'sans-serif'],
        'arabic': ['JF-Flat', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.6s ease-in-out',
        'slide-up': 'slideUp 0.8s ease-out',
        'scale-in': 'scaleIn 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(30px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}

