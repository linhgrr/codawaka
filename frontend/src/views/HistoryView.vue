<template>
  <div class="history-page">
    <div class="blockchain-grid"></div>
    <div class="container py-4">
      <h2 class="page-title mb-4">Code Generation History</h2>
      
      <div v-if="loading" class="text-center my-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading history...</p>
      </div>
      
      <!-- Sử dụng component EmptyHistoryState khi không có dữ liệu -->
      <empty-history-state v-else-if="codeHistory.length === 0" />
      
      <div v-else>
        <div class="mb-4">
          <div class="history-counter">
            <div class="counter-icon">
              <i class="fas fa-list"></i>
            </div>
            <div class="counter-text">
              <span class="counter-highlight">{{ totalItems }}</span> code generation requests
            </div>
          </div>
        </div>
        
        <div class="history-timeline">
          <!-- Sử dụng component HistoryItem cho mỗi mục trong lịch sử -->
          <history-item 
            v-for="(item, index) in codeHistory" 
            :key="index" 
            :item="item"
          />
        </div>
        
        <!-- Phân trang -->
        <pagination-component 
          :current-page="currentPage" 
          :total-pages="totalPages" 
          @page-changed="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import PaginationComponent from '@/components/PaginationComponent.vue';
import HistoryItem from '@/components/history/HistoryItem.vue';
import EmptyHistoryState from '@/components/history/EmptyHistoryState.vue';
import axios from 'axios';
import apiConfig from '@/utils/apiConfig';

const API_URL = apiConfig.baseURL;

export default {
  name: 'HistoryView',
  components: {
    PaginationComponent,
    HistoryItem,
    EmptyHistoryState
  },
  data() {
    return {
      loading: true,
      currentPage: 1,
      itemsPerPage: 5,
      totalItems: 0,
      totalPages: 1
    }
  },
  computed: {
    ...mapGetters(['codeHistory'])
  },
  methods: {
    ...mapActions(['fetchCodeHistory']),
    loadHistoryData() {
      this.loading = true;
      
      // Lấy tổng số items trước
      const token = localStorage.getItem('token');
      axios.get(`${API_URL}/code/history/count`, {
        headers: { Authorization: `Bearer ${token}` }
      })
        .then(response => {
          this.totalItems = response.data.count;
          this.totalPages = Math.ceil(this.totalItems / this.itemsPerPage);
          
          // Sau đó lấy dữ liệu cho trang hiện tại
          this.fetchCodeHistory({ 
            page: this.currentPage, 
            limit: this.itemsPerPage 
          })
            .finally(() => {
              this.loading = false;
            });
        })
        .catch(error => {
          console.error('Error fetching history count:', error);
          this.loading = false;
        });
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.loadHistoryData();
      
      // Cuộn trang lên đầu khi chuyển trang
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
  },
  created() {
    this.loadHistoryData();
  }
}
</script>

<style scoped>
.history-page {
  position: relative;
  min-height: calc(100vh - 56px);
  padding: 20px 0;
  background-color: var(--dark-bg);
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

.history-counter {
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  border-radius: 12px;
  padding: 15px 20px;
  color: white;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.counter-icon {
  font-size: 1.5rem;
  margin-right: 15px;
  color: #64ffda;
}

.counter-text {
  font-size: 1.1rem;
}

.counter-highlight {
  font-weight: 700;
  color: #64ffda;
  margin: 0 3px;
}

.history-timeline {
  position: relative;
  margin-top: 30px;
}
</style>