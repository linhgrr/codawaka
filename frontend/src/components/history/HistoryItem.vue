<template>
  <div class="history-item">
    <div class="history-card">
      <div class="history-header">
        <div class="d-flex justify-content-between align-items-center">
          <div class="model-name">
            <i class="fas fa-robot me-2"></i>
            {{ item.model_name }}
          </div>
          <div class="credits-badge">
            <i class="fas fa-coins me-1"></i>
            {{ item.credits_used }} credits
          </div>
        </div>
        <div class="timestamp">
          <i class="far fa-clock me-1"></i>
          {{ formattedDate }}
        </div>
      </div>
      
      <div class="history-body">
        <div class="prompt-section">
          <h6 class="section-title">Request:</h6>
          <div class="prompt-content">{{ item.prompt }}</div>
        </div>
        
        <div class="code-section">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <h6 class="section-title mb-0">Generated Code:</h6>
            <button class="btn btn-sm btn-outline-primary" @click="copyToClipboard">
              <i class="fas fa-copy me-1"></i> Copy
            </button>
          </div>
          <pre class="code-block"><code>{{ item.generated_code }}</code></pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { showSuccess, showError } from '@/utils/toast';

export default {
  name: 'HistoryItem',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  computed: {
    formattedDate() {
      try {
        const date = new Date(this.item.timestamp);
        return date.toLocaleString('en-US', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit', 
          minute: '2-digit'
        });
      } catch (e) {
        return this.item.timestamp;
      }
    }
  },
  methods: {
    copyToClipboard() {
      navigator.clipboard.writeText(this.item.generated_code)
        .then(() => {
          showSuccess('Code copied to clipboard!');
        })
        .catch(err => {
          console.error('Failed to copy: ', err);
          showError('Could not copy the code. Please try again.');
        });
    }
  }
}
</script>

<style scoped>
.history-item {
  margin-bottom: 30px;
}

.history-card {
  background: var(--dark-card-bg);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.history-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.history-header {
  background: var(--dark-card-secondary);
  padding: 15px 20px;
  border-bottom: 1px solid var(--dark-border);
}

.model-name {
  font-weight: 600;
  color: var(--dark-text);
}

.credits-badge {
  display: inline-block;
  background: rgba(0, 112, 243, 0.2);
  color: #0070f3;
  font-size: 0.85rem;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 20px;
}

.timestamp {
  font-size: 0.85rem;
  color: var(--dark-text-secondary);
  margin-top: 5px;
}

.history-body {
  padding: 20px;
}

.section-title {
  color: var(--dark-text);
  font-weight: 600;
  margin-bottom: 10px;
}

.prompt-content {
  background: var(--dark-card-secondary);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 25px;
  color: var(--dark-text-secondary);
  white-space: pre-line;
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
</style>