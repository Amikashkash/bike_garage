module.exports = {
  content: [
    "../templates/**/*.html",
    "../../workshop/templates/**/*.html",
    "../../**/templates/**/*.html",
    "../static/**/*.js",
    "../../static/**/*.js",
  ],
  safelist: [
    'bg-gradient-to-br',
    'bg-gradient-to-r', 
    'bg-gradient-to-tr',
    'from-slate-950',
    'via-blue-950',
    'to-slate-900',
    'backdrop-blur-2xl',
    'backdrop-blur-xl',
    'animate-float-slow',
    'animate-float-medium',
    'animate-float-fast',
    {
      pattern: /(bg|text|border)-(slate|blue|cyan|green|red|yellow|purple|indigo)-(50|100|200|300|400|500|600|700|800|900)/,
    },
    {
      pattern: /(from|via|to)-(slate|blue|cyan|green|red|yellow|purple|indigo)-(50|100|200|300|400|500|600|700|800|900)/,
    },
    {
      pattern: /hover:(from|via|to)-(slate|blue|cyan|green|red|yellow|purple|indigo)-(50|100|200|300|400|500|600|700|800|900)/,
    },
    {
      pattern: /animate-(pulse|bounce|ping|spin)/,
    }
  ],
  theme: { 
    extend: {
      animation: {
        'float-slow': 'float-slow 20s ease-in-out infinite',
        'float-medium': 'float-medium 15s ease-in-out infinite', 
        'float-fast': 'float-fast 12s ease-in-out infinite',
      }
    } 
  },
  plugins: [],
}


