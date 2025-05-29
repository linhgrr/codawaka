<template>
  <div class="buy-credits container">
    <h1 class="mt-4 mb-3">Buy Credits</h1>
    
    <div class="row">
      <div class="col-md-8 mx-auto">
        <div class="card bg-dark text-light">
          <div class="card-body">
            <h5 class="card-title">Purchase Information</h5>
            <p class="card-text">Price: 1,000 VND / credit</p>
            <p class="card-text">Minimum purchase: 10 credits</p>
            
            <div class="form-group mb-3">
              <label for="creditAmount">Credits to purchase:</label>
              <input
                type="number"
                id="creditAmount"
                v-model="creditAmount"
                class="form-control bg-dark text-light"
                min="10"
                :class="{ 'is-invalid': validationError }"
              />
              <div class="invalid-feedback" v-if="validationError">
                {{ validationError }}
              </div>
              <small class="form-text text-muted">Total amount: {{ formatCurrency(creditAmount * 1000) }} VND</small>
            </div>
            
            <button
              class="btn btn-primary mt-3"
              @click="buyCredits"
              :disabled="isLoading || creditAmount < 10"
            >
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
              Process Payment
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Payment History -->
    <div class="row mt-4" v-if="paymentHistory && paymentHistory.length > 0">
      <div class="col-12">
        <h3>Payment History</h3>
        <div class="table-responsive">
          <table class="table table-dark table-striped">
            <thead>
              <tr>
                <th>Date</th>
                <th>Credits</th>
                <th>Amount</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="transaction in paymentHistory" :key="transaction.id">
                <td>{{ formatDate(transaction.created_at) }}</td>
                <td>{{ transaction.credits }}</td>
                <td>{{ formatCurrency(transaction.amount) }} VND</td>
                <td>
                  <span :class="getStatusClass(transaction.status)">
                    {{ getStatusText(transaction.status) }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'BuyCreditsView',
  data() {
    return {
      creditAmount: 10,
      validationError: '',
      isLoading: false,
      paymentHistory: []
    };
  },
  mounted() {
    this.loadPaymentHistory();
  },
  methods: {
    ...mapActions(['createPayment', 'fetchPaymentHistory', 'fetchCredits']),
    
    buyCredits() {
      // Validate input
      if (this.creditAmount < 10) {
        this.validationError = 'Minimum purchase is 10 credits';
        return;
      }
      
      this.validationError = '';
      this.isLoading = true;
      
      this.createPayment({ credits: this.creditAmount })
        .then(response => {
          // Redirect directly to the payment URL instead of showing QR code
          window.location.href = response.checkout_url;
          
          // Still update payment history in the background
          this.loadPaymentHistory();
        })
        .catch(error => {
          console.error('Payment error:', error);
          let errorMessage = 'An error occurred while creating payment';
          
          if (error.response && error.response.data && error.response.data.detail) {
            errorMessage = error.response.data.detail;
          }
          
          this.$toast.error(errorMessage);
          this.isLoading = false;
        });
    },
    
    loadPaymentHistory() {
      this.fetchPaymentHistory()
        .then(history => {
          this.paymentHistory = history;
        })
        .catch(error => {
          console.error('Error loading payment history:', error);
        });
    },
    
    formatCurrency(value) {
      return new Intl.NumberFormat('en-US').format(value);
    },
    
    formatDate(isoString) {
      try {
        const date = new Date(isoString);
        return date.toLocaleString('en-US', { 
          year: 'numeric', 
          month: 'short', 
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      } catch (error) {
        return isoString;
      }
    },
    
    getStatusClass(status) {
      switch (status) {
        case 'completed':
          return 'badge bg-success';
        case 'pending':
          return 'badge bg-warning text-dark';
        case 'failed':
          return 'badge bg-danger';
        default:
          return 'badge bg-secondary';
      }
    },
    
    getStatusText(status) {
      switch (status) {
        case 'completed':
          return 'Completed';
        case 'pending':
          return 'Pending';
        case 'failed':
          return 'Failed';
        default:
          return status;
      }
    }
  }
}
</script>

<style scoped>
.buy-credits {
  color: #f8f9fa;
}

.card {
  border-color: #343a40;
}

.form-control {
  border-color: #495057;
}

.form-control:focus {
  background-color: #2b3035;
  color: #f8f9fa;
  border-color: #0d6efd;
}

.table {
  color: #f8f9fa;
}
</style>