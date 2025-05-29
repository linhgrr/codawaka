<template>
  <div class="payment-result container mt-5">
    <div class="card bg-dark text-light mx-auto" style="max-width: 600px;">
      <div class="card-body text-center">
        <div v-if="isLoading">
          <div class="spinner-border text-primary mb-3" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <h2>Verifying payment status...</h2>
          <p>Please wait a moment</p>
        </div>
        
        <div v-else-if="isSuccess">
          <div class="text-success mb-3">
            <i class="bi bi-check-circle-fill" style="font-size: 4rem;"></i>
          </div>
          <h2>Payment Successful!</h2>
          <p>Thank you, credits have been added to your account.</p>
          <p class="mb-4">Current balance: <strong>{{ userCredits }} credits</strong></p>
          <div class="d-flex justify-content-center gap-3">
            <router-link to="/buy-credits" class="btn btn-outline-primary">Buy More Credits</router-link>
            <router-link to="/generate" class="btn btn-success">Start Generating Code</router-link>
          </div>
        </div>
        
        <div v-else>
          <div class="text-danger mb-3">
            <i class="bi bi-x-circle-fill" style="font-size: 4rem;"></i>
          </div>
          <h2>Payment Failed</h2>
          <p>{{ errorMessage || 'An error occurred during the payment process.' }}</p>
          <div class="d-flex justify-content-center gap-3 mt-4">
            <router-link to="/buy-credits" class="btn btn-primary">Try Again</router-link>
            <router-link to="/" class="btn btn-outline-secondary">Back to Home</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import axios from 'axios';

export default {
  name: 'PaymentResultView',
  data() {
    return {
      isLoading: true,
      isSuccess: false,
      errorMessage: '',
      transactionId: ''
    };
  },
  computed: {
    ...mapGetters(['credits', 'isLoggedIn', 'paymentTransactions']),
    
    userCredits() {
      return this.credits;
    }
  },
  beforeCreate() {
    // Restore session from localStorage
    const token = localStorage.getItem('token');
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
  },
  created() {
    // Ensure token is set for axios
    this.restoreSession();
  },
  mounted() {
    // Get status from query params and process
    this.handleReturnFromPayment();
  },
  methods: {
    ...mapActions(['login', 'verifyPayment', 'verifyLatestPayment', 'fetchCredits', 'fetchPaymentHistory', 'restoreSession']),
    
    restoreUserSession() {
      // Restore session from localStorage if needed
      const token = localStorage.getItem('token');
      const user = JSON.parse(localStorage.getItem('user'));
      
      if (token && user && !this.isLoggedIn) {
        // Set token for axios again
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        // Log in to store without calling API
        this.$store.commit('AUTH_SUCCESS', { token, user });
        
        // Get credits info
        this.fetchCredits().catch(err => {
          console.error('Error fetching credits:', err);
          if (err.response && err.response.status === 401) {
            // If still getting 401 error, redirect to login
            this.handleSessionExpired();
          }
        });
      } else if (!this.isLoggedIn) {
        // If no login info, redirect to login
        this.handleSessionExpired();
        return;
      }
    },
    
    handleSessionExpired() {
      this.isLoading = false;
      this.isSuccess = false;
      this.errorMessage = 'Your session has expired, please log in again';
      
      // Save current URL to redirect back after login
      localStorage.setItem('redirectAfterLogin', this.$route.fullPath);
      
      // Redirect to login after 2 seconds
      setTimeout(() => {
        this.$router.push('/login');
      }, 2000);
    },
    
    handleReturnFromPayment() {
      // Get parameters from URL query parameters
      const status = this.$route.query.status;
      const code = this.$route.query.code;
      const transactionId = this.$route.query.id; // PayOS returns in 'id' parameter
      const cancel = this.$route.query.cancel;
      
      console.log('URL params:', { status, code, transactionId, cancel });
      
      // If user canceled payment
      if (cancel === 'true' || status === 'cancel') {
        this.isLoading = false;
        this.isSuccess = false;
        this.errorMessage = 'Payment was canceled';
        return;
      }
      
      // Check if we have transaction ID from PayOS
      if (transactionId && code === '00' && (status === 'PAID' || status === 'success')) {
        // Verify specific transaction by ID from PayOS
        this.verifySpecificTransaction(transactionId);
      } else {
        // If insufficient info, check most recent transaction
        this.verifyPaymentStatus();
      }
    },
    
    async verifySpecificTransaction(transactionId) {
      try {
        console.log('Verifying specific transaction:', transactionId);
        // Verify specific transaction
        const success = await this.verifyPayment(transactionId);
        
        // Update UI status
        this.isSuccess = success;
        
        if (!success) {
          this.errorMessage = 'Payment has not been confirmed. Please check again later.';
        }
      } catch (error) {
        console.error('Error verifying specific transaction:', error);
        // Try fallback method if direct verification fails
        this.verifyPaymentStatus();
      } finally {
        this.isLoading = false;
      }
    },
    
    async verifyPaymentStatus() {
      try {
        // Use action to verify most recent transaction
        const success = await this.verifyLatestPayment();
        
        // Update UI status
        this.isSuccess = success;
        
        if (!success) {
          this.errorMessage = 'Payment has not been confirmed. Please check again later.';
        }
      } catch (error) {
        console.error('Error verifying payment:', error);
        this.isSuccess = false;
        
        if (error.response && error.response.status === 401) {
          this.handleSessionExpired();
        } else {
          this.errorMessage = `Unable to verify payment status: ${error.message || 'Unknown error'}`;
        }
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style scoped>
.payment-result {
  padding: 2rem 0;
  color: #f8f9fa;
}

.card {
  border-color: #343a40;
}
</style>