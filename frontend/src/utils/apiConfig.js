/**
 * API configuration that works with environment variables
 * Uses Vue's environment variables (VUE_APP_* prefix)
 * The webpack configuration in vue.config.js ensures these are available
 */

// This will use the value from .env or the value set during deployment
const API_URL = process.env.VUE_APP_API_URL;

// For debugging - you can remove this in production
console.log('API URL:', API_URL);

export default {
  baseURL: API_URL,
  getFullURL: (path) => `${API_URL}${path}`
};