<template>
  <div class="admin-page">
    <div class="blockchain-grid"></div>
    <div class="container py-4">
      <h2 class="page-title mb-4">Admin Dashboard</h2>
      
      <ul class="nav nav-tabs mb-4 custom-tabs">
        <li class="nav-item">
          <a class="nav-link" :class="{ active: currentTab === 'users' }" @click.prevent="currentTab = 'users'" href="#">Users</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: currentTab === 'models' }" @click.prevent="currentTab = 'models'" href="#">Models</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: currentTab === 'history' }" @click.prevent="currentTab = 'history'" href="#">All History</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" :class="{ active: currentTab === 'payments' }" @click.prevent="currentTab = 'payments'" href="#">Payments</a>
        </li>
      </ul>
      
      <!-- Users Tab -->
      <div v-if="currentTab === 'users'">
        <user-management
          @show-add-credits="showAddCredits"
        />
        
        <!-- Add Credits Modal -->
        <div class="modal fade" id="addCreditsModal" tabindex="-1" aria-hidden="true" ref="addCreditsModal">
          <div class="modal-dialog">
            <div class="modal-content dark-modal">
              <div class="modal-header">
                <h5 class="modal-title">Add Credits</h5>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <form @submit.prevent="addCredits">
                  <div class="mb-3">
                    <label for="addAmount" class="form-label">Amount to Add</label>
                    <input type="number" class="form-control custom-input" id="addAmount" v-model="addCreditsAmount" step="0.1" min="0.1" required>
                  </div>
                  <button type="submit" class="btn btn-success">Add Credits</button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Models Tab -->
      <div v-if="currentTab === 'models'">
        <model-management />
      </div>
      
      <!-- All History Tab -->
      <div v-if="currentTab === 'history'">
        <history-management />
      </div>
      
      <!-- Payments Tab -->
      <div v-if="currentTab === 'payments'">
        <payment-management />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { showSuccess, showError } from '@/utils/toast';
import apiConfig from '@/utils/apiConfig';
import UserManagement from '@/components/admin/UserManagement.vue';
import ModelManagement from '@/components/admin/ModelManagement.vue';
import HistoryManagement from '@/components/admin/HistoryManagement.vue';
import PaymentManagement from '@/components/admin/PaymentManagement.vue';

// Bootstrap for modals
import * as bootstrap from 'bootstrap';

// API base URL
const API_URL = apiConfig.baseURL;

export default {
  name: 'AdminView',
  components: {
    UserManagement,
    ModelManagement,
    HistoryManagement,
    PaymentManagement
  },
  data() {
    return {
      currentTab: 'users',
      selectedUserId: null,
      addCreditsAmount: 10,
      addCreditsModal: null
    }
  },
  methods: {
    showAddCredits(user) {
      this.selectedUserId = user.id;
      this.addCreditsAmount = 10;
      
      if (!this.addCreditsModal && this.$refs.addCreditsModal) {
        this.addCreditsModal = new bootstrap.Modal(this.$refs.addCreditsModal);
      }
      
      if (this.addCreditsModal) {
        this.addCreditsModal.show();
      }
    },
    addCredits() {
      axios.post(`${API_URL}/admin/users/${this.selectedUserId}/add-credits?amount=${this.addCreditsAmount}`, {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
        .then(() => {
          showSuccess(`Added ${this.addCreditsAmount} credits successfully!`);
          this.$refs.userManagement?.fetchUsers();
          this.addCreditsModal.hide();
        })
        .catch(error => {
          console.error('Error adding credits:', error);
          showError('Failed to add credits. Please try again.');
        });
    }
  },
  mounted() {
    // Khởi tạo modal
    this.$nextTick(() => {
      if (this.$refs.addCreditsModal) {
        this.addCreditsModal = new bootstrap.Modal(this.$refs.addCreditsModal);
      }
    });
  }
}
</script>

<style scoped>
.admin-page {
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

.custom-tabs .nav-link {
  color: var(--dark-text-secondary);
  border: none;
  padding: 10px 20px;
  border-radius: 0;
  position: relative;
  transition: all 0.3s ease;
}

.custom-tabs .nav-link:hover {
  color: var(--dark-text);
}

.custom-tabs .nav-link.active {
  color: var(--primary-color);
  background-color: transparent;
  border-bottom: 3px solid var(--primary-color);
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

.custom-input, .custom-textarea {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid var(--dark-border);
  color: var(--dark-text);
  border-radius: 8px;
}

.custom-input:focus, .custom-textarea:focus {
  background-color: rgba(0, 0, 0, 0.3);
  border-color: var(--primary-color);
  color: var(--dark-text);
  box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.2);
}
</style>