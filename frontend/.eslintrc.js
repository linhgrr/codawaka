module.exports = {
  root: true,
  env: {
    node: true
  },
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended'
  ],
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false, // This tells babel-eslint not to require a config file
    babelOptions: {
      plugins: ['@babel/plugin-syntax-jsx']
    }
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    // Tắt một số quy tắc có thể gây phiền nhiễu trong quá trình phát triển
    'vue/no-unused-components': 'warn',
    'no-unused-vars': 'warn'
  }
}