<template>
  <div class="login-page">
    <div class="polygon-background"></div>
    <div class="login-glow-1"></div>
    <div class="login-glow-2"></div>
    
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card login-card">
            <div class="card-body p-4 p-md-5">
              <h2 class="login-title text-center mb-4">Login</h2>
              
              <div v-if="error" class="alert alert-danger">{{ error }}</div>
              
              <form @submit.prevent="onSubmit">
                <div class="form-group mb-4">
                  <label for="username" class="form-label">Username</label>
                  <input
                    type="text"
                    class="form-control custom-input"
                    id="username"
                    v-model="username"
                    placeholder="Enter username"
                    required
                  >
                </div>
                
                <div class="form-group mb-4">
                  <label for="password" class="form-label">Password</label>
                  <input
                    type="password"
                    class="form-control custom-input"
                    id="password"
                    v-model="password"
                    placeholder="Enter password"
                    required
                  >
                </div>
                
                <button type="submit" class="btn btn-primary btn-glow w-100 py-3 login-btn" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  {{ loading ? 'Logging in...' : 'Login' }}
                </button>
                
                <p class="text-center mt-4 register-prompt">
                  Don't have an account?
                  <router-link to="/register" class="register-link">Register now</router-link>
                </p>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { showError } from '@/utils/toast';

export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
      error: null,
      loading: false
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.error = null
      
      const user = {
        username: this.username,
        password: this.password
      }
      
      this.$store.dispatch('login', user)
        .then(() => {
          this.$router.push('/')
        })
        .catch(err => {
          console.error(err)
          this.error = err.response?.data?.detail || 'Login failed. Please check your username and password.'
          showError(this.error)
        })
        .finally(() => {
          this.loading = false
        })
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 76px);
  display: flex;
  align-items: center;
  position: relative;
  padding: 60px 0;
  overflow: hidden;
}

.polygon-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><polygon points="10,1 19,10 10,19 1,10" stroke="rgba(123,63,228,0.08)" stroke-width="1" fill="none" /></svg>');
  background-size: 50px 50px;
  opacity: 0.5;
  z-index: -1;
}

.login-glow-1, .login-glow-2 {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: -1;
}

.login-glow-1 {
  top: -120px;
  right: -100px;
  width: 400px;
  height: 400px;
  background: rgba(123, 63, 228, 0.15);
}

.login-glow-2 {
  bottom: -150px;
  left: -100px;
  width: 350px;
  height: 350px;
  background: rgba(167, 38, 193, 0.1);
}

.login-card {
  border: 1px solid var(--dark-border);
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  background-color: var(--dark-card-bg);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border-color: rgba(123, 63, 228, 0.3);
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--primary-gradient);
}

.login-title {
  color: var(--dark-text);
  font-weight: 700;
  position: relative;
  margin-bottom: 30px;
}

.login-title:after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 3px;
  background: var(--primary-gradient);
  border-radius: 3px;
}

.form-label {
  color: var(--dark-text-secondary);
  font-weight: 500;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.custom-input {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--dark-border);
  color: var(--dark-text);
  border-radius: 10px;
  padding: 12px 15px;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.custom-input:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(123, 63, 228, 0.2);
}

.login-btn {
  background: var(--primary-gradient);
  border: none;
  font-weight: 600;
  border-radius: 10px;
  padding: 12px 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px var(--glow-color);
  margin-top: 10px;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--glow-color);
}

.register-prompt {
  color: var(--dark-text-secondary);
  font-size: 0.95rem;
  margin-top: 20px;
}

.register-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-left: 5px;
}

.register-link:hover {
  text-decoration: underline;
}

.alert-danger {
  background-color: rgba(220, 53, 69, 0.15);
  color: #ff8896;
  border-color: rgba(220, 53, 69, 0.3);
  border-radius: 10px;
}
</style>