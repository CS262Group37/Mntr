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
    },
  },
  plugins: [],
}
