<template>
  <div class="register-page">
    <div class="polygon-background"></div>
    <div class="register-glow-1"></div>
    <div class="register-glow-2"></div>
    
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card register-card">
            <div class="card-body p-4 p-md-5">
              <h2 class="register-title text-center mb-4">Register Account</h2>
              
              <div v-if="error" class="alert alert-danger mb-4">{{ error }}</div>
              <div v-if="success" class="alert alert-success mb-4">{{ success }}</div>
              
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
                  <label for="email" class="form-label">Email</label>
                  <input
                    type="email"
                    class="form-control custom-input"
                    id="email"
                    v-model="email"
                    placeholder="Enter your email"
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
                
                <div class="form-group mb-4">
                  <label for="referralCode" class="form-label">
                    Referral Code <span class="text-muted">(Optional)</span>
                  </label>
                  <input
                    type="text"
                    class="form-control custom-input"
                    id="referralCode"
                    v-model="referralCode"
                    placeholder="Enter referral code if you have one"
                  >
                  <small class="form-text text-muted">
                    Have a friend's code? Enter it here and get started with more credits!
                  </small>
                </div>
                
                <div class="referral-info alert alert-info mb-4">
                  <div class="d-flex align-items-start">
                    <i class="fas fa-info-circle me-2 mt-1"></i>
                    <div>
                      <p class="mb-1"><strong>Referral Benefits:</strong></p>
                      <ul class="mb-0 ps-3">
                        <li>New users start with <strong>2 credits</strong></li>
                        <li>Use a referral code to support your friend</li>
                        <li>When someone uses your code, you get <strong>+3 credits</strong></li>
                        <li>After registration, share your own code to earn more!</li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <button type="submit" class="btn btn-primary btn-glow w-100 py-3 register-btn" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  {{ loading ? 'Registering...' : 'Register' }}
                </button>
                
                <p class="text-center mt-4 login-prompt">
                  Already have an account?
                  <router-link to="/login" class="login-link">Login</router-link>
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
import { showSuccess, showError } from '@/utils/toast';

export default {
  name: 'RegisterView',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      referralCode: '',
      error: null,
      success: null,
      loading: false
    }
  },
  created() {
    // Check if there's a referral code in the URL query params
    const urlParams = new URLSearchParams(window.location.search);
    const codeFromUrl = urlParams.get('ref');
    if (codeFromUrl) {
      this.referralCode = codeFromUrl;
    }
  },
  methods: {
    onSubmit() {
      this.loading = true
      this.error = null
      this.success = null
      
      const user = {
        username: this.username,
        email: this.email,
        password: this.password
      }
      
      // Add referral code if provided
      if (this.referralCode && this.referralCode.trim() !== '') {
        user.referral_code = this.referralCode.trim();
      }
      
      this.$store.dispatch('register', user)
        .then(() => {
          this.success = 'Registration successful! You can login now.'
          showSuccess(this.success)
          this.username = ''
          this.email = ''
          this.password = ''
          this.referralCode = ''
        })
        .catch(err => {
          console.error(err)
          this.error = err.response?.data?.detail || 'Registration failed. Please try again.'
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
.register-page {
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

.register-glow-1, .register-glow-2 {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: -1;
}

.register-glow-1 {
  top: -120px;
  left: -100px;
  width: 400px;
  height: 400px;
  background: rgba(123, 63, 228, 0.15);
}

.register-glow-2 {
  bottom: -150px;
  right: -100px;
  width: 350px;
  height: 350px;
  background: rgba(167, 38, 193, 0.1);
}

.register-card {
  border: 1px solid var(--dark-border);
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  background-color: var(--dark-card-bg);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
}

.register-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border-color: rgba(123, 63, 228, 0.3);
}

.register-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--primary-gradient);
}

.register-title {
  color: var(--dark-text);
  font-weight: 700;
  position: relative;
  margin-bottom: 30px;
}

.register-title:after {
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

.register-btn {
  background: var(--primary-gradient);
  border: none;
  font-weight: 600;
  border-radius: 10px;
  padding: 12px 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px var(--glow-color);
  margin-top: 10px;
}

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--glow-color);
}

.login-prompt {
  color: var(--dark-text-secondary);
  font-size: 0.95rem;
  margin-top: 20px;
}

.login-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  margin-left: 5px;
}

.login-link:hover {
  text-decoration: underline;
}

.alert-danger {
  background-color: rgba(220, 53, 69, 0.15);
  color: #ff8896;
  border-color: rgba(220, 53, 69, 0.3);
  border-radius: 10px;
}

.alert-success {
  background-color: rgba(40, 167, 69, 0.15);
  color: #75e58f;
  border-color: rgba(40, 167, 69, 0.3);
  border-radius: 10px;
}
</style>