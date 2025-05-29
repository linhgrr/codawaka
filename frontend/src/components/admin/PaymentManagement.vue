<!-- PaymentManagement.vue -->
<template>
  <div>
    <h3 class="section-title">Quản lý giao dịch thanh toán</h3>
    
    <!-- Thống kê giao dịch -->
    <div class="row mb-4">
      <div class="col-md-12">
        <div class="card dark-card mb-4">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Thống kê giao dịch</h5>
          </div>
          <div class="card-body">
            <div v-if="loadingStats" class="text-center">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else class="row">
              <div class="col-md-4 mb-3">
                <div class="stat-card bg-success text-white p-3 rounded">
                  <h3 class="mb-2">{{ formatCurrency(stats.total_amount) }}</h3>
                  <p class="mb-0">Tổng doanh thu</p>
                </div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="stat-card bg-info text-white p-3 rounded">
                  <h3 class="mb-2">{{ stats.total_credits || 0 }}</h3>
                  <p class="mb-0">Tổng credits đã bán</p>
                </div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="stat-card bg-warning text-white p-3 rounded">
                  <h3 class="mb-2">{{ stats.total_transactions || 0 }}</h3>
                  <p class="mb-0">Tổng số giao dịch</p>
                </div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="stat-card bg-success text-white p-3 rounded">
                  <h3 class="mb-2">{{ stats.completed_transactions || 0 }}</h3>
                  <p class="mb-0">Giao dịch thành công</p>
                </div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="stat-card bg-secondary text-white p-3 rounded">
                  <h3 class="mb-2">{{ stats.pending_transactions || 0 }}</h3>
                  <p class="mb-0">Giao dịch đang xử lý</p>
                </div>
              </div>
              <div class="col-md-4 mb-3">
                <div class="stat-card bg-danger text-white p-3 rounded">
                  <h3 class="mb-2">{{ stats.failed_transactions || 0 }}</h3>
                  <p class="mb-0">Giao dịch thất bại</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Danh sách giao dịch -->
    <h4 class="section-title">Lịch sử giao dịch</h4>
    
    <div v-if="loadingTransactions" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="transactions.length === 0" class="alert alert-info dark-alert">
      Chưa có giao dịch nào trong hệ thống.
    </div>
    
    <div v-else>
      <div class="mb-3">
        <input type="text" class="form-control custom-input" placeholder="Tìm kiếm theo ID người dùng..." v-model="transactionSearch">
      </div>
      
      <div class="table-responsive">
        <table class="table table-dark table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>User ID</th>
              <th>Số tiền (VND)</th>
              <th>Credits</th>
              <th>Transaction ID</th>
              <th>Trạng thái</th>
              <th>Ngày tạo</th>
              <th>Ngày hoàn thành</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="transaction in filteredTransactions" :key="transaction.id" :class="getTransactionStatusClass(transaction.status)">
              <td>{{ transaction.id }}</td>
              <td>
                <span class="user-link" @click="viewUserTransactions(transaction.user_id)">
                  {{ transaction.user_id }}
                </span>
              </td>
              <td>{{ formatCurrency(transaction.amount) }}</td>
              <td>{{ transaction.credits }}</td>
              <td class="transaction-id">{{ transaction.transaction_id }}</td>
              <td>
                <span class="badge" :class="getStatusBadgeClass(transaction.status)">
                  {{ getStatusText(transaction.status) }}
                </span>
              </td>
              <td>{{ formatDate(transaction.created_at) }}</td>
              <td>{{ transaction.completed_at ? formatDate(transaction.completed_at) : 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Phân trang -->
      <pagination-component 
        :current-page="pagination.currentPage" 
        :total-pages="pagination.totalPages" 
        @page-changed="handlePageChange"
      />
    </div>
    
    <!-- User Transactions Modal -->
    <div class="modal fade" id="userTransactionsModal" tabindex="-1" aria-hidden="true" ref="userTransactionsModal">
      <div class="modal-dialog modal-lg">
        <div class="modal-content dark-modal">
          <div class="modal-header">
            <h5 class="modal-title">Giao dịch của người dùng #{{ selectedUserId }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div v-if="loadingUserTransactions" class="text-center">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>
            <div v-else-if="userTransactions.length === 0" class="alert alert-info dark-alert">
              Người dùng này chưa có giao dịch nào.
            </div>
            <div v-else>
              <div class="table-responsive">
                <table class="table table-dark table-hover">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Số tiền (VND)</th>
                      <th>Credits</th>
                      <th>Transaction ID</th>
                      <th>Trạng thái</th>
                      <th>Ngày tạo</th>
                      <th>Ngày hoàn thành</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="transaction in userTransactions" :key="transaction.id" :class="getTransactionStatusClass(transaction.status)">
                      <td>{{ transaction.id }}</td>
                      <td>{{ formatCurrency(transaction.amount) }}</td>
                      <td>{{ transaction.credits }}</td>
                      <td>{{ transaction.transaction_id }}</td>
                      <td>
                        <span class="badge" :class="getStatusBadgeClass(transaction.status)">
                          {{ getStatusText(transaction.status) }}
                        </span>
                      </td>
                      <td>{{ formatDate(transaction.created_at) }}</td>
                      <td>{{ transaction.completed_at ? formatDate(transaction.completed_at) : 'N/A' }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { showError } from '@/utils/toast';
import apiConfig from '@/utils/apiConfig';
import PaginationComponent from '@/components/PaginationComponent.vue';
import * as bootstrap from 'bootstrap';

const API_URL = apiConfig.baseURL;

export default {
  name: 'PaymentManagement',
  components: {
    PaginationComponent
  },
  data() {
    return {
      stats: {
        total_amount: 0,
        total_credits: 0,
        total_transactions: 0,
        completed_transactions: 0,
        pending_transactions: 0,
        failed_transactions: 0
      },
      transactions: [],
      userTransactions: [],
      loadingStats: false,
      loadingTransactions: false,
      loadingUserTransactions: false,
      selectedUserId: null,
      transactionSearch: '',
      userTransactionsModal: null,
      pagination: {
        currentPage: 1,
        totalPages: 1,
        totalItems: 0,
        itemsPerPage: 10
      }
    }
  },
  computed: {
    filteredTransactions() {
      return this.transactions.filter(transaction => {
        return transaction.user_id.toString().includes(this.transactionSearch);
      });
    }
  },
  methods: {
    fetchPaymentStats() {
      this.loadingStats = true;
      axios.get(`${API_URL}/admin/payment-statistics`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
        .then(response => {
          this.stats = response.data;
        })
        .catch(error => {
          console.error('Error fetching payment stats:', error);
          showError('Failed to fetch payment stats. Please try again.');
        })
        .finally(() => {
          this.loadingStats = false;
        });
    },
    fetchTransactions() {
      this.loadingTransactions = true;
      
      // Lấy tổng số giao dịch
      axios.get(`${API_URL}/admin/payment-transactions/count`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
        .then(countResponse => {
          this.pagination.totalItems = countResponse.data.count;
          this.pagination.totalPages = Math.ceil(this.pagination.totalItems / this.pagination.itemsPerPage);
          
          // Lấy dữ liệu giao dịch cho trang hiện tại
          const skip = (this.pagination.currentPage - 1) * this.pagination.itemsPerPage;
          const limit = this.pagination.itemsPerPage;
          
          return axios.get(`${API_URL}/admin/payment-transactions?skip=${skip}&limit=${limit}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
        })
        .then(response => {
          this.transactions = response.data;
        })
        .catch(error => {
          console.error('Error fetching transactions:', error);
          showError('Failed to fetch transactions. Please try again.');
        })
        .finally(() => {
          this.loadingTransactions = false;
        });
    },
    viewUserTransactions(userId) {
      this.selectedUserId = userId;
      this.loadingUserTransactions = true;
      
      axios.get(`${API_URL}/admin/users/${userId}/transactions`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
        .then(response => {
          this.userTransactions = response.data;
          this.showUserTransactionsModal();
        })
        .catch(error => {
          console.error('Error fetching user transactions:', error);
          showError('Failed to fetch user transactions. Please try again.');
        })
        .finally(() => {
          this.loadingUserTransactions = false;
        });
    },
    showUserTransactionsModal() {
      if (!this.userTransactionsModal && this.$refs.userTransactionsModal) {
        this.userTransactionsModal = new bootstrap.Modal(this.$refs.userTransactionsModal);
      }
      
      if (this.userTransactionsModal) {
        this.userTransactionsModal.show();
      }
    },
    handlePageChange(page) {
      this.pagination.currentPage = page;
      this.fetchTransactions();
      // Cuộn trang lên đầu
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    },
    formatDate(dateString) {
      try {
        const date = new Date(dateString);
        return date.toLocaleString();
      } catch (e) {
        return dateString;
      }
    },
    formatCurrency(amount) {
      return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
    },
    getTransactionStatusClass(status) {
      return {
        'table-success': status === 'completed',
        'table-warning': status === 'pending',
        'table-danger': status === 'failed'
      }
    },
    getStatusBadgeClass(status) {
      return {
        'bg-success': status === 'completed',
        'bg-warning': status === 'pending',
        'bg-danger': status === 'failed'
      }
    },
    getStatusText(status) {
      switch (status) {
        case 'completed':
          return 'Thành công';
        case 'pending':
          return 'Đang xử lý';
        case 'failed':
          return 'Thất bại';
        default:
          return 'N/A';
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      if (this.$refs.userTransactionsModal) {
        this.userTransactionsModal = new bootstrap.Modal(this.$refs.userTransactionsModal);
      }
    });
  },
  created() {
    this.fetchPaymentStats();
    this.fetchTransactions();
  }
}
</script>

<style scoped>
.section-title {
  color: var(--dark-text);
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.dark-card {
  background-color: var(--dark-card-bg);
  color: var(--dark-text);
  border-color: var(--dark-border);
}

.table-dark {
  background-color: var(--dark-card-bg);
  color: var(--dark-text);
  border-color: var(--dark-border);
}

.table-dark th {
  background-color: var(--dark-card-secondary);
  border-color: var(--dark-border);
  color: var(--dark-text);
}

.table-dark td {
  border-color: var(--dark-border);
}

.dark-modal {
  background-color: var(--dark-card-bg);
  color: var(--dark-text);
}

.dark-modal .modal-header {
  border-bottom: 1px solid var(--dark-border);
  background-color: var(--dark-card-secondary);
}

.dark-modal .modal-title {
  color: var(--dark-text);
}

.custom-input {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--dark-border);
  color: var(--dark-text);
  border-radius: 8px;
}

.custom-input:focus {
  background-color: rgba(0, 0, 0, 0.3);
  border-color: var(--primary-color);
  color: var(--dark-text);
  box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.2);
}

.dark-alert {
  background-color: rgba(13, 202, 240, 0.15);
  color: #5dceef;
  border-color: rgba(13, 202, 240, 0.3);
}

.user-link {
  color: var(--primary-color);
  cursor: pointer;
  text-decoration: underline;
}

.user-link:hover {
  color: var(--primary-color-hover);
}

.transaction-id {
  font-family: monospace;
  font-size: 0.85rem;
}
</style>