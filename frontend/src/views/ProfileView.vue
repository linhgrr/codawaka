<template>
  <div class="profile-page">
    <div class="blockchain-grid"></div>
    <div class="container py-4">
      <h2 class="page-title mb-4">My Profile</h2>
      
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading profile...</p>
      </div>
      
      <div class="row" v-else>
        <div class="col-md-4 mb-4">
          <div class="card dark-card">
            <div class="card-header">
              <h5 class="mb-0">Account Information</h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <label class="form-label text-muted">Username</label>
                <p class="form-control-static">{{ user.username }}</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted">Email</label>
                <p class="form-control-static">{{ user.email }}</p>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted">Account Status</label>
                <span class="badge" :class="user.is_active ? 'bg-success' : 'bg-danger'">
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted">Role</label>
                <span class="badge" :class="user.is_admin ? 'bg-primary' : 'bg-secondary'">
                  {{ user.is_admin ? 'Admin' : 'User' }}
                </span>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted">Current Credits</label>
                <p class="form-control-static credits-display">
                  <i class="fas fa-coins me-2 text-warning"></i>
                  <span class="fw-bold">{{ user.credits }}</span>
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-md-8">
          <div class="card dark-card mb-4">
            <div class="card-header">
              <h5 class="mb-0">My Referral Program</h5>
            </div>
            <div class="card-body">
              <div class="referral-info mb-4">
                <div class="d-flex align-items-center mb-3">
                  <i class="fas fa-gift text-primary fs-4 me-3"></i>
                  <div>
                    <h5 class="mb-1">Invite Friends & Earn Credits</h5>
                    <p class="mb-0 text-muted">Share your referral code with friends and earn 3 credits for each new user who signs up using your code.</p>
                  </div>
                </div>
                
                <!-- Thống kê người dùng đã giới thiệu -->
                <div class="referral-stats mb-4">
                  <div class="row">
                    <div class="col-md-6">
                      <div class="stat-card p-3 text-center">
                        <div class="stat-icon mx-auto mb-2">
                          <i class="fas fa-users"></i>
                        </div>
                        <h3 class="mb-1">{{ referralStats.total_referrals }}</h3>
                        <p class="mb-0 text-muted small">Total Referrals</p>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="stat-card p-3 text-center">
                        <div class="stat-icon mx-auto mb-2">
                          <i class="fas fa-coins"></i>
                        </div>
                        <h3 class="mb-1">{{ referralStats.total_referrals * 3 }}</h3>
                        <p class="mb-0 text-muted small">Credits Earned from Referrals</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div class="referral-code-box p-3 mb-4">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <small class="text-muted d-block mb-1">Your Referral Code</small>
                      <h3 class="mb-0 referral-code">{{ user.referral_code }}</h3>
                    </div>
                    <button class="btn btn-primary" @click="copyReferralCode">
                      <i class="fas fa-copy me-2"></i> Copy Code
                    </button>
                  </div>
                </div>
                
                <div class="referral-link-box p-3 mb-4">
                  <div class="d-flex justify-content-between align-items-center">
                    <div>
                      <small class="text-muted d-block mb-1">Referral Link</small>
                      <div class="referral-link">{{ referralLink }}</div>
                    </div>
                    <button class="btn btn-primary" @click="copyReferralLink">
                      <i class="fas fa-copy me-2"></i> Copy Link
                    </button>
                  </div>
                </div>
                
                <div class="share-options">
                  <div class="mb-2">Share directly:</div>
                  <div class="d-flex gap-2">
                    <a :href="'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(referralLink)" target="_blank" class="btn btn-outline-primary">
                      <i class="fab fa-facebook"></i>
                    </a>
                    <a :href="'https://twitter.com/intent/tweet?text=' + encodeURIComponent('Join me on Codawaka AI and get free credits! Use my referral code:') + '&url=' + encodeURIComponent(referralLink)" target="_blank" class="btn btn-outline-primary">
                      <i class="fab fa-twitter"></i>
                    </a>
                    <a :href="'mailto:?subject=' + encodeURIComponent('Join me on Codawaka AI') + '&body=' + encodeURIComponent('Hey!\n\nI\'m using Codawaka AI for code generation and thought you might like it too.\n\nSign up using my referral code: ' + user.referral_code + ' or use this link: ' + referralLink + '\n\nThanks!')" class="btn btn-outline-primary">
                      <i class="fas fa-envelope"></i>
                    </a>
                  </div>
                </div>
              </div>
              
              <div class="referral-benefits mt-4">
                <h6 class="mb-3">How It Works</h6>
                <div class="row">
                  <div class="col-md-4 mb-3">
                    <div class="benefit-card p-3">
                      <div class="benefit-icon mb-2">
                        <i class="fas fa-share-alt"></i>
                      </div>
                      <h6>1. Share Your Code</h6>
                      <p class="small mb-0">Share your unique referral code with friends.</p>
                    </div>
                  </div>
                  <div class="col-md-4 mb-3">
                    <div class="benefit-card p-3">
                      <div class="benefit-icon mb-2">
                        <i class="fas fa-user-plus"></i>
                      </div>
                      <h6>2. Friend Signs Up</h6>
                      <p class="small mb-0">They register using your referral code.</p>
                    </div>
                  </div>
                  <div class="col-md-4 mb-3">
                    <div class="benefit-card p-3">
                      <div class="benefit-icon mb-2">
                        <i class="fas fa-coins"></i>
                      </div>
                      <h6>3. Get Rewarded</h6>
                      <p class="small mb-0">You earn 3 credits for each successful referral.</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { showSuccess, showError } from '@/utils/toast';

export default {
  name: 'ProfileView',
  data() {
    return {
      loading: true,
      user: {
        username: '',
        email: '',
        is_active: true,
        is_admin: false,
        credits: 0,
        referral_code: ''
      },
      referralStats: {
        total_referrals: 0
      }
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn']),
    referralLink() {
      return `${window.location.origin}/register?ref=${this.user.referral_code}`;
    }
  },
  mounted() {
    this.fetchUserProfile();
  },
  methods: {
    fetchUserProfile() {
      this.loading = true;
      const token = localStorage.getItem('token');
      const headers = { 'Authorization': `Bearer ${token}` };
      const API_URL = process.env.VUE_APP_API_URL || 'http://47.129.30.28:8000';
      
      // Sử dụng Promise.all để gọi đồng thời hai API endpoints
      Promise.all([
        // Get current user data from API
        fetch(`${API_URL}/users/me`, { headers })
          .then(response => {
            if (!response.ok) throw new Error('Failed to fetch profile data');
            return response.json();
          }),
        
        // Get referral statistics
        fetch(`${API_URL}/users/me/referrals`, { headers })
          .then(response => {
            if (!response.ok) throw new Error('Failed to fetch referral statistics');
            return response.json();
          })
      ])
        .then(([userData, referralData]) => {
          this.user = userData;
          this.referralStats = referralData;
        })
        .catch(error => {
          console.error('Error fetching profile data:', error);
          showError('Failed to load profile data. Please try again.');
        })
        .finally(() => {
          this.loading = false;
        });
    },
    copyReferralCode() {
      navigator.clipboard.writeText(this.user.referral_code)
        .then(() => {
          showSuccess('Referral code copied to clipboard!');
        })
        .catch(() => {
          showError('Failed to copy referral code. Please try again.');
        });
    },
    copyReferralLink() {
      navigator.clipboard.writeText(this.referralLink)
        .then(() => {
          showSuccess('Referral link copied to clipboard!');
        })
        .catch(() => {
          showError('Failed to copy referral link. Please try again.');
        });
    }
  }
}
</script>

<style scoped>
.profile-page {
  position: relative;
  min-height: calc(100vh - 56px);
  padding: 20px 0;
  background-color: var(--dark-bg);
  color: var(--dark-text);
}

.blockchain-grid {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: linear-gradient(rgba(65, 88, 208, 0.05) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(65, 88, 208, 0.05) 1px, transparent 1px);
  background-size: 30px 30px;
  z-index: 0;
  pointer-events: none;
}

.page-title {
  color: var(--dark-text);
  font-weight: 600;
  font-size: 2.2rem;
  margin-bottom: 2rem;
  position: relative;
  display: inline-block;
}

.page-title:after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 50px;
  height: 3px;
  background: linear-gradient(90deg, #0070f3, #00c9ff);
  border-radius: 3px;
}

.dark-card {
  background-color: var(--dark-card-bg);
  border: 1px solid var(--dark-border);
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
}

.dark-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}

.dark-card .card-header {
  background-color: var(--dark-card-secondary);
  border-bottom: 1px solid var(--dark-border);
  padding: 15px 20px;
}

.form-control-static {
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  margin-bottom: 0;
  color: var(--dark-text); /* Thêm màu chữ sáng hơn */
}

.credits-display {
  font-size: 1.2rem;
  color: var(--dark-text); /* Thêm màu chữ sáng hơn */
}

.referral-code-box, .referral-link-box {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  border: 1px solid var(--dark-border);
  color: var(--dark-text); /* Thêm màu chữ sáng hơn */
}

.referral-code {
  font-family: 'Consolas', 'Monaco', monospace;
  font-weight: 700;
  letter-spacing: 1px;
  color: var(--primary-color);
}

.referral-link {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 0.9rem;
  word-break: break-all;
  color: #e0e0ff; /* Màu sáng hơn cho đường link */
}

.stat-card {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  border: 1px solid var(--dark-border);
  transition: transform 0.3s ease;
  color: var(--dark-text); /* Thêm màu chữ sáng hơn */
}

.stat-card:hover {
  transform: translateY(-3px);
  border-color: var(--primary-color);
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(123, 63, 228, 0.1);
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.benefit-card {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  border: 1px solid var(--dark-border);
  height: 100%;
  transition: transform 0.3s ease;
  color: var(--dark-text); /* Thêm màu chữ sáng hơn */
}

.benefit-card p {
  color: #d0d0f0; /* Màu sáng hơn cho văn bản trong benefit card */
}

/* Tạo class rõ ràng hơn cho text-muted trong theme tối */
.text-muted {
  color: #9999cc !important; /* Màu muted sáng hơn cho chế độ tối */
}

/* Tăng độ sáng cho heading trong các card */
.dark-card h3, .dark-card h5, .dark-card h6 {
  color: #ffffff;
}

/* Màu rõ ràng hơn cho các số liệu thống kê */
.stat-card h3 {
  color: #ffffff;
  font-weight: 600;
}

/* Làm nổi bật phần hướng dẫn 'How It Works' */
.referral-benefits h6 {
  color: #e0e0ff;
  font-weight: 600;
}
</style>