module.exports = {
  mode: 'jit',
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  content: [],
  theme: {
    fontFamily: {
      'display': 'Nunito',
      'body': 'Roboto',
    },
    
    extend: {
      colors: {
        prussianBlue: '#0E2A47',
        brightNavyBlue: '#3379C2',
        firebrick: '#BB0A21',
        imperialRed: '#F02D3A',
        congoPink: '#FF7370',
        cultured: '#F4F5F6',
      },

      backgroundImage: {
        'blueBg': "url('./res/blue-bg.svg')",
        'blueBgWide': "url('./res/blue-bg-wide.svg')",
      },

      keyframes: {
        growDown: {
          '0%': {
            opacity: '0',
            transform: 'scaleY(0)',
          },
          '80%': {
            transform: 'scaleY(1.1)',
          },
          '100%': {
            opacity: '1',
            transform: 'scaleY(1)',
          },
        },
      },

      animation: {
        growDown: 'growDown 300ms ease-in-out forwards',
      }
    },
  },
  plugins: [],
}
