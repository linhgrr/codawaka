<!-- UserManagement.vue -->
<template>
  <div>
    <h3 class="section-title">Manage Users</h3>
    
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else>
      <div class="table-responsive">
        <table class="table table-dark table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Credits</th>
              <th>Status</th>
              <th>Admin</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.credits }}</td>
              <td>
                <span class="badge" :class="user.is_active ? 'bg-success' : 'bg-danger'">
                  {{ user.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>
                <span class="badge" :class="user.is_admin ? 'bg-primary' : 'bg-secondary'">
                  {{ user.is_admin ? 'Admin' : 'User' }}
                </span>
              </td>
              <td>
                <div class="btn-group btn-group-sm">
                  <button class="btn btn-outline-primary" @click="editUser(user)">Edit</button>
                  <button class="btn btn-outline-success" @click="$emit('show-add-credits', user)">Add Credits</button>
                  <button class="btn btn-outline-danger" @click="deleteUser(user.id)">Delete</button>
                </div>
              </td>
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
    
    <!-- Edit User Modal -->
    <div class="modal fade" id="editUserModal" tabindex="-1" aria-hidden="true" ref="editUserModal">
      <div class="modal-dialog">
        <div class="modal-content dark-modal">
          <div class="modal-header">
            <h5 class="modal-title">Edit User</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="updateUser">
              <div class="mb-3">
                <label for="editEmail" class="form-label">Email</label>
                <input type="email" class="form-control custom-input" id="editEmail" v-model="editUserForm.email">
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="editActive" v-model="editUserForm.is_active">
                <label class="form-check-label" for="editActive">Active</label>
              </div>
              <div class="mb-3 form-check">
                <input type="checkbox" class="form-check-input" id="editAdmin" v-model="editUserForm.is_admin">
                <label class="form-check-label" for="editAdmin">Admin</label>
              </div>
              <div class="mb-3">
                <label for="editCredits" class="form-label">Credits</label>
                <input type="number" class="form-control custom-input" id="editCredits" v-model="editUserForm.credits" step="0.1" min="0">
              </div>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { showSuccess, showError } from '@/utils/toast';
import apiConfig from '@/utils/apiConfig';
import PaginationComponent from '@/components/PaginationComponent.vue';
import * as bootstrap from 'bootstrap';

const API_URL = apiConfig.baseURL;

export default {
  name: 'UserManagement',
  components: {
    PaginationComponent
  },
  data() {
    return {
      users: [],
      loading: false,
      pagination: {
        currentPage: 1,
        totalPages: 1,
        totalItems: 0,
        itemsPerPage: 10
      },
      editUserForm: {
        id: null,
        email: '',
        is_active: true,
        is_admin: false,
        credits: 0
      },
      editUserModal: null
    }
  },
  methods: {
    fetchUsers() {
      this.loading = true;
      
      // Lấy tổng số người dùng
      axios.get(`${API_URL}/admin/users/count`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
        .then(countResponse => {
          this.pagination.totalItems = countResponse.data.count;
          this.pagination.totalPages = Math.ceil(this.pagination.totalItems / this.pagination.itemsPerPage);
          
          // Lấy dữ liệu người dùng cho trang hiện tại
          const skip = (this.pagination.currentPage - 1) * this.pagination.itemsPerPage;
          const limit = this.pagination.itemsPerPage;
          
          return axios.get(`${API_URL}/admin/users?skip=${skip}&limit=${limit}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
        })
        .then(response => {
          this.users = response.data;
        })
        .catch(error => {
          console.error('Error fetching users:', error);
          showError('Failed to fetch users. Please try again.');
        })
        .finally(() => {
          this.loading = false;
        });
    },
    handlePageChange(page) {
      this.pagination.currentPage = page;
      this.fetchUsers();
      // Cuộn trang lên đầu
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    },
    editUser(user) {
      this.editUserForm = {
        id: user.id,
        email: user.email,
        is_active: user.is_active,
        is_admin: user.is_admin,
        credits: user.credits
      };
      
      if (!this.editUserModal && this.$refs.editUserModal) {
        this.editUserModal = new bootstrap.Modal(this.$refs.editUserModal);
      }
      
      if (this.editUserModal) {
        this.editUserModal.show();
      }
    },
    updateUser() {
      axios.put(`${API_URL}/admin/users/${this.editUserForm.id}`, this.editUserForm, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
        .then(() => {
          showSuccess('User updated successfully!');
          this.fetchUsers();
          this.editUserModal.hide();
        })
        .catch(error => {
          console.error('Error updating user:', error);
          showError('Failed to update user. Please try again.');
        });
    },
    deleteUser(userId) {
      if (confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
        axios.delete(`${API_URL}/admin/users/${userId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
          .then(() => {
            showSuccess('User deleted successfully!');
            this.fetchUsers();
          })
          .catch(error => {
            console.error('Error deleting user:', error);
            showError('Failed to delete user. Please try again.');
          });
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      if (this.$refs.editUserModal) {
        this.editUserModal = new bootstrap.Modal(this.$refs.editUserModal);
      }
    });
  },
  created() {
    this.fetchUsers();
  }
}
</script>

<style scoped>
.section-title {
  color: var(--dark-text);
  font-weight: 600;
  margin-bottom: 1.5rem;
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