<template>
  <div id="app" class="dark-theme">
    <nav class="navbar navbar-expand-lg custom-navbar fixed-top">
      <div class="container">
        <router-link to="/" class="navbar-brand">
          <span class="brand-text">Codawaka</span>
          <span class="brand-highlight">AI</span>
        </router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item" v-if="isLoggedIn">
              <router-link to="/generate" class="nav-link">Generate code</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link to="/history" class="nav-link">History</router-link>
            </li>
            <li class="nav-item" v-if="isAdmin">
              <router-link to="/admin" class="nav-link">Admin</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item" v-if="isLoggedIn">
              <span class="nav-link credits-display">
                <span class="credits-icon"><i class="fas fa-coins"></i></span>
                <span class="credits-amount">{{ credits }}</span>
              </span>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link to="/buy-credits" class="nav-link btn-buy-credits">
                <i class="fas fa-plus-circle"></i> Buy Credits
              </router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <router-link to="/profile" class="nav-link">
                <i class="fas fa-user-circle"></i> Profile
              </router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link to="/login" class="nav-link">Login</router-link>
            </li>
            <li class="nav-item" v-if="!isLoggedIn">
              <router-link to="/register" class="nav-link btn-outline">Sign up</router-link>
            </li>
            <li class="nav-item" v-if="isLoggedIn">
              <a @click="logout" class="nav-link cursor-pointer">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="navbar-spacer"></div>
    <router-view />
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'App',
  computed: {
    ...mapGetters(['isLoggedIn', 'isAdmin', 'credits']),
  },
  methods: {
    ...mapActions(['logout']),
    handleScroll() {
      const navbar = document.querySelector('.custom-navbar');
      if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
      } else {
        navbar.classList.remove('scrolled');
      }
    }
  },
  created() {
    // Load FontAwesome if not already loaded
    if (!document.getElementById('font-awesome-css')) {
      const link = document.createElement('link');
      link.id = 'font-awesome-css';
      link.rel = 'stylesheet';
      link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css';
      document.head.appendChild(link);
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  }
};
</script>

<style>
:root {
  /* Main background colors */
  --dark-bg: #0D0D12;
  --dark-card-bg: #101016;
  --dark-card-secondary: #18181F;
  --dark-navbar: #0A0A0F;
  --dark-border: #27272F;
  
  /* Text colors */
  --dark-text: #FFFFFF;
  --dark-text-secondary: #A1A1AA;
  
  /* Brand colors */
  --primary-color: #5E5CE6;
  --primary-color-hover: #7A78FF;
  --primary-gradient: linear-gradient(90deg, #5E5CE6, #8F8CF7);
  --accent-color: #0571FF;
  --glow-color: rgba(94, 92, 230, 0.4);
  
  /* Special colors */
  --success-color: #0CB07A;
  --warning-color: #FFB224;
  --danger-color: #FF4545;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body, html {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: var(--dark-bg);
  color: var(--dark-text);
  overflow-x: hidden;
  scroll-behavior: smooth;
}

.dark-theme {
  background-color: var(--dark-bg);
  color: var(--dark-text);
  min-height: 100vh;
}

.custom-navbar {
  background-color: rgba(8, 8, 22, 0.7);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
  padding: 15px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.navbar-spacer {
  height: 80px; /* Adjust based on your navbar height */
}

.scrolled {
  background-color: rgba(8, 8, 22, 0.9);
  padding: 10px 0;
}

.navbar-brand {
  font-weight: 700;
  font-size: 1.5rem;
  color: var(--dark-text) !important;
  display: flex;
  align-items: center;
}

.brand-text {
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-highlight {
  color: var(--accent-color);
  font-weight: 800;
  margin-left: 4px;
}

.nav-link {
  color: var(--dark-text-secondary) !important;
  margin: 0 5px;
  transition: all 0.3s ease;
  font-weight: 500;
  padding: 8px 15px !important;
  border-radius: 8px;
}

.nav-link:hover, .nav-link.router-link-active {
  color: var(--dark-text) !important;
  background-color: rgba(255, 255, 255, 0.05);
}

.btn-primary {
  background: var(--primary-color);
  border: none;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  border-radius: 6px;
  font-weight: 500;
  transition: all 0.2s ease;
  color: white;
  padding: 10px 16px;
  letter-spacing: -0.01em;
}

.btn-primary:hover:not(:disabled) {
  background: var(--primary-color-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 6px;
  color: var(--dark-text);
  font-weight: 500;
  transition: all 0.2s ease;
  padding: 10px 16px;
  letter-spacing: -0.01em;
}

.btn-secondary:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-1px);
  border-color: rgba(255, 255, 255, 0.2);
}

.btn-outline {
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 6px;
  color: var(--dark-text) !important;
  background: transparent;
}

.btn-outline:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  color: white !important;
}

.credits-display {
  display: flex;
  align-items: center;
  background: rgba(94, 92, 230, 0.12);
  border-radius: 6px;
  padding: 6px 12px !important;
}

.credits-icon {
  color: var(--primary-color);
  margin-right: 8px;
}

.credits-amount {
  font-weight: 600;
  color: var(--dark-text) !important;
}

.cursor-pointer {
  cursor: pointer;
}

.btn-buy-credits {
  background: rgba(94, 92, 230, 0.12);
  color: var(--primary-color) !important;
  border-radius: 6px;
  margin-right: 10px;
  transition: all 0.2s ease;
  font-weight: 500;
}

.btn-buy-credits:hover {
  background: rgba(94, 92, 230, 0.2);
  transform: translateY(-1px);
}

/* Common Components Styling */
.card {
  background-color: var(--dark-card-bg);
  border: 1px solid var(--dark-border);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.form-control, .form-select {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--dark-border);
  color: var(--dark-text);
  border-radius: 8px;
}

.form-control:focus, .form-select:focus {
  background-color: rgba(0, 0, 0, 0.3);
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(94, 92, 230, 0.2);
  color: var(--dark-text);
}

input::placeholder, textarea::placeholder {
  color: var(--dark-text-secondary);
  opacity: 0.7;
}

.modal-content {
  background-color: var(--dark-card-bg);
  border: 1px solid var(--dark-border);
  color: var(--dark-text);
}

.modal-header {
  border-bottom: 1px solid var(--dark-border);
}

.modal-footer {
  border-top: 1px solid var(--dark-border);
}

.alert-primary {
  background-color: rgba(94, 92, 230, 0.15);
  color: #b69fff;
  border-color: rgba(94, 92, 230, 0.3);
}

.alert-danger {
  background-color: rgba(220, 53, 69, 0.15);
  color: #ff8896;
  border-color: rgba(220, 53, 69, 0.3);
}

.alert-success {
  background-color: rgba(40, 167, 69, 0.15);
  color: #75ffa0;
  border-color: rgba(40, 167, 69, 0.3);
}

pre, code {
  background-color: #0a0a1a;
  color: #e0e0ff;
  border-radius: 8px;
}

/* Table Styling */
.table {
  color: var(--dark-text);
}

.table thead th {
  background-color: rgba(0, 0, 0, 0.2);
  color: var(--dark-text-secondary);
  border-bottom: 2px solid var(--dark-border);
}

.table tbody td {
  border-bottom: 1px solid var(--dark-border);
  vertical-align: middle;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: rgba(255, 255, 255, 0.02);
}

.table-hover tbody tr:hover {
  background-color: rgba(123, 63, 228, 0.05);
}

/* Animation for gradient text */
@keyframes gradientFlow {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style>