// filepath: c:\Users\Tuan Linh\Downloads\óc nhân tạo\prj\ttud\frontend\src\utils\toast.js
import { useToast } from "vue-toastification";

// Initialize toast
const toast = useToast();

/**
 * Display a success toast notification
 * @param {string} message - Message to display
 */
export const showSuccess = (message) => {
  toast.success(message);
};

/**
 * Display an error toast notification
 * @param {string} message - Error message to display
 */
export const showError = (message) => {
  toast.error(message);
};

/**
 * Display an info toast notification
 * @param {string} message - Info message to display
 */
export const showInfo = (message) => {
  toast.info(message);
};

/**
 * Display a warning toast notification
 * @param {string} message - Warning message to display
 */
export const showWarning = (message) => {
  toast.warning(message);
};

/**
 * Generic toast function
 * @param {string} message - Message to display
 * @param {string} type - Type of notification: 'success', 'error', 'info', 'warning'
 */
export const showToast = (message, type = "default") => {
  switch (type.toLowerCase()) {
    case "success":
      toast.success(message);
      break;
    case "error":
      toast.error(message);
      break;
    case "info":
      toast.info(message);
      break;
    case "warning":
      toast.warning(message);
      break;
    default:
      toast(message);
  }
};

export default {
  showSuccess,
  showError,
  showInfo,
  showWarning,
  showToast
};