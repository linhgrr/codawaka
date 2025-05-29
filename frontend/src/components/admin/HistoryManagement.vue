<!-- HistoryManagement.vue -->
<template>
  <div>
    <h3 class="section-title">All Code Generation History</h3>
    
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="history.length === 0" class="alert alert-info dark-alert">
      No code generation history found in the system.
    </div>
    
    <div v-else class="row">
      <div class="col-md-12" v-for="(item, index) in history" :key="index">
        <div class="card mb-4 history-card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <div>
              <h5 class="mb-0">{{ item.model_name }}</h5>
              <small class="text-muted">User ID: {{ item.user_id }}</small>
            </div>
            <span class="badge bg-info">Credits used: {{ item.credits_used }}</span>
          </div>
          <div class="card-body">
            <h6 class="section-title">Prompt:</h6>
            <div class="mb-3 p-3 prompt-content rounded">{{ item.prompt }}</div>
            
            <h6 class="section-title">Generated Code:</h6>
            <pre class="code-block"><code>{{ item.generated_code }}</code></pre>
            
            <small class="text-muted">Generated on: {{ formatDate(item.timestamp) }}</small>
          </div>
        </div>
      </div>
      
      <!-- Phân trang -->
      <pagination-component 
        :current-page="pagination.currentPage" 
        :total-pages="pagination.totalPages" 
        @page-changed="handlePageChange"
      />
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { showError } from '@/utils/toast';
import apiConfig from '@/utils/apiConfig';
import PaginationComponent from '@/components/PaginationComponent.vue';

const API_URL = apiConfig.baseURL;

export default {
  name: 'HistoryManagement',
  components: {
    PaginationComponent
  },
  data() {
    return {
      history: [],
      loading: false,
      pagination: {
        currentPage: 1,
        totalPages: 1,
        totalItems: 0,
        itemsPerPage: 5
      }
    }
  },
  methods: {
    fetchHistory() {
      this.loading = true;
      
      // Lấy tổng số lịch sử sinh mã
      axios.get(`${API_URL}/admin/code-history/count`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
        .then(countResponse => {
          this.pagination.totalItems = countResponse.data.count;
          this.pagination.totalPages = Math.ceil(this.pagination.totalItems / this.pagination.itemsPerPage);
          
          // Lấy dữ liệu lịch sử sinh mã cho trang hiện tại
          const skip = (this.pagination.currentPage - 1) * this.pagination.itemsPerPage;
          const limit = this.pagination.itemsPerPage;
          
          return axios.get(`${API_URL}/admin/code-history?skip=${skip}&limit=${limit}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
        })
        .then(response => {
          this.history = response.data;
        })
        .catch(error => {
          console.error('Error fetching history:', error);
          showError('Failed to fetch history. Please try again.');
        })
        .finally(() => {
          this.loading = false;
        });
    },
    handlePageChange(page) {
      this.pagination.currentPage = page;
      this.fetchHistory();
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
    }
  },
  created() {
    this.fetchHistory();
  }
}
</script>

<style scoped>
.section-title {
  color: var(--dark-text);
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.history-card {
  background-color: var(--dark-card-bg);
  border: 1px solid var(--dark-border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
  margin-bottom: 20px;
}

.history-card .card-header {
  background-color: var(--dark-card-secondary);
  border-bottom: 1px solid var(--dark-border);
  color: var(--dark-text);
}

.history-card .card-body {
  padding: 20px;
}

.prompt-content {
  background-color: var(--dark-card-secondary);
  color: var(--dark-text-secondary);
}

.code-block {
  background: #1e1e2e;
  color: #f8f8f2;
  border-radius: 8px;
  padding: 20px;
  margin: 0;
  overflow-x: auto;
  font-family: 'Consolas', 'Monaco', monospace;
  line-height: 1.5;
}

.dark-alert {
  background-color: rgba(13, 202, 240, 0.15);
  color: #5dceef;
  border-color: rgba(13, 202, 240, 0.3);
}

.text-muted {
  color: var(--dark-text-secondary) !important;
}
</style>