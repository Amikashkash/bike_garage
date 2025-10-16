module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:react/jsx-runtime',
    'plugin:react-hooks/recommended',
    'prettier',
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  settings: {
    react: {
      version: 'detect',
    },
  },
  plugins: ['react', 'react-hooks'],
  rules: {
    // Console warnings allowed for debugging
    'no-console': ['warn', { allow: ['warn', 'error'] }],

    // Unused vars should warn, not error
    'no-unused-vars': 'warn',

    // React specific rules
    'react/prop-types': 'off', // We'll add TypeScript later
    'react/react-in-jsx-scope': 'off', // Not needed with React 18
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',

    // Code style (let Prettier handle most)
    'prefer-const': 'warn',
    'no-var': 'error',
  },
};
