<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-body">
            <h3 class="mb-4 text-center">Đặt lại mật khẩu</h3>
            <form @submit.prevent="submitNewPassword">
              <div class="mb-3">
                <label for="password" class="form-label">Mật khẩu mới</label>
                <input type="password" v-model="password" class="form-control" id="password" required>
              </div>
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? 'Đang đặt lại...' : 'Đặt lại mật khẩu' }}
              </button>
            </form>
            <div v-if="message" class="alert alert-success mt-3">{{ message }}</div>
            <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
            <router-link to="/login" class="d-block mt-4 text-center">Quay lại đăng nhập</router-link>
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
.container { min-height: 60vh; }
</style>
