<!-- ModelManagement.vue -->
<template>
  <div>
    <h3 class="section-title">Manage Models</h3>
    
    <div class="mb-4">
      <button class="btn btn-primary" @click="showAddModel">Add New Model</button>
    </div>
    
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
              <th>Model Name</th>
              <th>Credit Cost</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="model in models" :key="model.id">
              <td>{{ model.id }}</td>
              <td>{{ model.model_name }}</td>
              <td>{{ model.credit_cost_per_request }}</td>
              <td>{{ model.description || 'No description' }}</td>
              <td>
                <div class="btn-group btn-group-sm">
                  <button class="btn btn-outline-primary" @click="editModel(model)">Edit</button>
                  <button class="btn btn-outline-danger" @click="deleteModel(model.id)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <!-- Add/Edit Model Modal -->
    <div class="modal fade" id="modelModal" tabindex="-1" aria-hidden="true" ref="modelModal">
      <div class="modal-dialog">
        <div class="modal-content dark-modal">
          <div class="modal-header">
            <h5 class="modal-title">{{ modelForm.id ? 'Edit Model' : 'Add New Model' }}</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveModel">
              <div class="mb-3">
                <label for="modelName" class="form-label">Model Name</label>
                <input type="text" class="form-control custom-input" id="modelName" v-model="modelForm.model_name" required :disabled="!!modelForm.id">
              </div>
              <div class="mb-3">
                <label for="modelCost" class="form-label">Credit Cost Per Request</label>
                <input type="number" class="form-control custom-input" id="modelCost" v-model="modelForm.credit_cost_per_request" step="0.1" min="0.1" required>
              </div>
              <div class="mb-3">
                <label for="modelDescription" class="form-label">Description</label>
                <textarea class="form-control custom-textarea" id="modelDescription" v-model="modelForm.description" rows="3"></textarea>
              </div>
              <button type="submit" class="btn btn-primary">{{ modelForm.id ? 'Update' : 'Add' }} Model</button>
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
import * as bootstrap from 'bootstrap';

const API_URL = apiConfig.baseURL;

export default {
  name: 'ModelManagement',
  data() {
    return {
      models: [],
      loading: false,
      modelForm: {
        id: null,
        model_name: '',
        credit_cost_per_request: 1,
        description: ''
      },
      modelModal: null
    }
  },
  methods: {
    fetchModels() {
      this.loading = true;
      axios.get(`${API_URL}/models`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
        .then(response => {
          this.models = response.data;
        })
        .catch(error => {
          console.error('Error fetching models:', error);
          showError('Failed to fetch models. Please try again.');
        })
        .finally(() => {
          this.loading = false;
        });
    },
    showAddModel() {
      this.modelForm = {
        id: null,
        model_name: '',
        credit_cost_per_request: 1,
        description: ''
      };
      
      if (!this.modelModal && this.$refs.modelModal) {
        this.modelModal = new bootstrap.Modal(this.$refs.modelModal);
      }
      
      if (this.modelModal) {
        this.modelModal.show();
      }
    },
    editModel(model) {
      this.modelForm = {
        id: model.id,
        model_name: model.model_name,
        credit_cost_per_request: model.credit_cost_per_request,
        description: model.description || ''
      };
      
      if (!this.modelModal && this.$refs.modelModal) {
        this.modelModal = new bootstrap.Modal(this.$refs.modelModal);
      }
      
      if (this.modelModal) {
        this.modelModal.show();
      }
    },
    saveModel() {
      if (this.modelForm.id) {
        // Update existing model
        axios.put(`${API_URL}/admin/models/${this.modelForm.id}`, {
          credit_cost_per_request: this.modelForm.credit_cost_per_request,
          description: this.modelForm.description
        }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
          .then(() => {
            showSuccess('Model updated successfully!');
            this.fetchModels();
            this.modelModal.hide();
          })
          .catch(error => {
            console.error('Error updating model:', error);
            showError('Failed to update model. Please try again.');
          });
      } else {
        // Create new model
        axios.post(`${API_URL}/admin/models`, this.modelForm, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
          .then(() => {
            showSuccess('Model added successfully!');
            this.fetchModels();
            this.modelModal.hide();
          })
          .catch(error => {
            console.error('Error adding model:', error);
            showError('Failed to add model. Please try again.');
          });
      }
    },
    deleteModel(modelId) {
      if (confirm('Are you sure you want to delete this model? This action cannot be undone.')) {
        axios.delete(`${API_URL}/admin/models/${modelId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        })
          .then(() => {
            showSuccess('Model deleted successfully!');
            this.fetchModels();
          })
          .catch(error => {
            console.error('Error deleting model:', error);
            showError('Failed to delete model. Please try again.');
          });
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      if (this.$refs.modelModal) {
        this.modelModal = new bootstrap.Modal(this.$refs.modelModal);
      }
    });
  },
  created() {
    this.fetchModels();
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