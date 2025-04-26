<template>
  <div class="card result-card">
    <div class="card-header d-flex justify-content-between align-items-center">
      <h4 class="m-0">C++ Tool (sử dụng trong lúc thi, run trực tiếp để chạy, xem vid hướng dẫn)</h4>
      <button class="btn btn-sm btn-outline-primary" @click="copyTemplate">
        <i class="fas fa-copy me-1"></i> Copy
      </button>
    </div>
    <div class="card-body">
      <pre class="code-block"><code>{{ cppTemplate }}</code></pre>
    </div>
  </div>
</template>

<script>
import { showSuccess, showError } from '@/utils/toast';

export default {
  name: 'CppTemplate',
  props: {
    cppTemplate: {
      type: String,
      required: true
    },
    username: {
      type: String,
      default: 'Anonymous'
    },
    modelName: {
      type: String,
      required: true
    }
  },
  methods: {
    copyTemplate() {
      if (!this.cppTemplate) return;
      
      navigator.clipboard.writeText(this.cppTemplate)
        .then(() => {
          showSuccess('C++ template copied to clipboard!');
        })
        .catch(err => {
          console.error('Failed to copy: ', err);
          showError('Could not copy C++ template. Please try again.');
        });
    }
  }
}
</script>

<style scoped>
.result-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  background-color: var(--dark-card-bg);
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
  position: relative;
}

.result-card .card-header {
  background-color: var(--dark-card-secondary);
  border-bottom: 1px solid var(--dark-border);
  padding: 15px 20px;
  color: var(--dark-text);
}
</style>