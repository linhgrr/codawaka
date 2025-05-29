<template>
  <div id="app" class="dark-theme">
    <nav class="navbar navbar-expand-lg custom-navbar">
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
  }
};
</script>

<style>
:root {
  --dark-bg: #0c0c1d;
  --dark-card-bg: #12122a;
  --dark-navbar: #080816;
  --dark-border: #212145;
  --dark-text: #e0e0ff;
  --dark-text-secondary: #9999cc;
  --primary-color: #7b3fe4;
  --primary-gradient: linear-gradient(90deg, #7b3fe4, #a726c1);
  --accent-color: #a726c1;
  --glow-color: rgba(123, 63, 228, 0.5);
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
  background-color: var(--dark-navbar);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
  padding: 15px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
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

.btn-outline {
  border: 1px solid var(--primary-color);
  border-radius: 8px;
  color: var(--primary-color) !important;
}

.btn-outline:hover {
  background: var(--primary-color);
  color: white !important;
}

.credits-display {
  display: flex;
  align-items: center;
  background: rgba(123, 63, 228, 0.1);
  border-radius: 20px;
  padding: 6px 15px !important;
}

.credits-icon {
  color: gold;
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
  background: rgba(123, 63, 228, 0.15);
  color: #b69fff !important;
  border-radius: 8px;
  margin-right: 10px;
  transition: all 0.3s ease;
}

.btn-buy-credits:hover {
  background: rgba(123, 63, 228, 0.25);
  transform: translateY(-2px);
}

/* Common Components Styling */
.card {
  background-color: var(--dark-card-bg);
  border: 1px solid var(--dark-border);
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.btn-primary {
  background: var(--primary-gradient);
  border: none;
  box-shadow: 0 4px 15px var(--glow-color);
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--glow-color);
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
  box-shadow: 0 0 0 3px rgba(123, 63, 228, 0.2);
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
  background-color: rgba(123, 63, 228, 0.15);
  color: #b69fff;
  border-color: rgba(123, 63, 228, 0.3);
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