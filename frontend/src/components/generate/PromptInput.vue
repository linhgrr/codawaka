<template>
  <div class="mb-4">
    <label for="prompt" class="form-label fw-bold">Describe requirement</label>
    <textarea
      id="prompt"
      class="form-control custom-textarea"
      :value="promptValue"
      rows="8"
      placeholder="Enter problem description..."
      required
      @input="$emit('update:promptValue', $event.target.value)"
    ></textarea>
  </div>
</template>

<script>
export default {
  name: 'PromptInput',
  props: {
    promptValue: {
      type: String,
      required: true
    }
  },
  emits: ['update:promptValue']
}
</script>

<style scoped>
.custom-textarea {
  border: 1px solid var(--dark-border);
  border-radius: 8px;
  padding: 12px;
  transition: all 0.3s ease;
  background-color: rgba(0, 0, 0, 0.2);
  color: var(--dark-text);
  resize: vertical;
  min-height: 200px;
  font-family: 'Consolas', 'Monaco', monospace;
}

.custom-textarea:focus {
  border-color: #0070f3;
  box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.2);
}

.form-label {
  color: var(--dark-text-secondary);
  font-weight: 500;
}
</style>