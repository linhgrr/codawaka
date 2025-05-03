<template>
  <div class="reset-password-page">
    <div class="polygon-background"></div>
    <div class="reset-glow-1"></div>
    <div class="reset-glow-2"></div>
    
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card reset-card">
            <div class="card-body p-4 p-md-5">
              <h2 class="reset-title text-center mb-4">Đặt lại mật khẩu</h2>
              
              <div v-if="message" class="alert alert-success">{{ message }}</div>
              <div v-if="error" class="alert alert-danger">{{ error }}</div>
              
              <form @submit.prevent="submitNewPassword">
                <div class="form-group mb-4">
                  <label for="password" class="form-label">Mật khẩu mới</label>
                  <input
                    type="password"
                    class="form-control custom-input"
                    id="password"
                    v-model="password"
                    placeholder="Nhập mật khẩu mới"
                    required
                  >
                </div>
                
                <button type="submit" class="btn btn-primary btn-glow w-100 py-3 reset-btn" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  <span>{{ loading ? 'Đang đặt lại...' : 'Đặt lại mật khẩu' }}</span>
                </button>
                
                <p class="text-center mt-4">
                  <router-link to="/login" class="back-link">Quay lại đăng nhập</router-link>
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
import axios from 'axios';
import { API_URL } from '@/utils/apiConfig';

export default {
  name: 'ResetPasswordView',
  data() {
    return {
      password: '',
      loading: false,
      message: '',
      error: ''
    };
  },
  mounted() {
    this.token = this.$route.query.token || '';
    if (!this.token) {
      this.error = 'Token không hợp lệ hoặc đã hết hạn.';
    }
  },
  methods: {
    async submitNewPassword() {
      if (!this.token) return;
      this.loading = true;
      this.message = '';
      this.error = '';
      try {
        await axios.post(`${API_URL}/reset-password`, { token: this.token, new_password: this.password });
        this.message = 'Đặt lại mật khẩu thành công. Bạn có thể đăng nhập với mật khẩu mới.';
      } catch (err) {
        this.error = err.response?.data?.detail || 'Có lỗi xảy ra. Vui lòng thử lại.';
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.reset-password-page {
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

.reset-glow-1, .reset-glow-2 {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: -1;
}

.reset-glow-1 {
  top: -120px;
  right: -100px;
  width: 400px;
  height: 400px;
  background: rgba(123, 63, 228, 0.15);
}

.reset-glow-2 {
  bottom: -150px;
  left: -100px;
  width: 350px;
  height: 350px;
  background: rgba(167, 38, 193, 0.1);
}

.reset-card {
  border: 1px solid var(--dark-border);
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
  background-color: var(--dark-card-bg);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
}

.reset-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border-color: rgba(123, 63, 228, 0.3);
}

.reset-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--primary-gradient);
}

.reset-title {
  color: var(--dark-text);
  font-weight: 700;
  position: relative;
  margin-bottom: 30px;
}

.reset-title:after {
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

.reset-btn {
  background: var(--primary-gradient);
  border: none;
  font-weight: 600;
  border-radius: 10px;
  padding: 12px 0;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px var(--glow-color);
  margin-top: 10px;
}

.reset-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--glow-color);
}

.back-link {
  color: var(--primary-color);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.back-link:hover {
  text-decoration: underline;
}

.alert-danger {
  background-color: rgba(220, 53, 69, 0.15);
  color: #ff8896;
  border-color: rgba(220, 53, 69, 0.3);
  border-radius: 10px;
}

.alert-success {
  background-color: rgba(25, 135, 84, 0.15);
  color: #75e5a0;
  border-color: rgba(25, 135, 84, 0.3);
  border-radius: 10px;
}
</style>
