<template>
  <div class="mb-4">
    <label for="model" class="form-label fw-bold">Select model</label>
    <select
      id="model"
      class="form-select custom-select"
      :value="modelValue"
      required
      @change="$emit('update:modelValue', $event.target.value)"
    >
      <option value="" disabled>Choose one model</option>
      <option
        v-for="model in models"
        :key="model.id"
        :value="model.model_name"
      >
        {{ model.model_name }} - {{ model.credit_cost_per_request }} credits
        <span v-if="model.description"> - {{ model.description }}</span>
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'ModelSelector',
  props: {
    models: {
      type: Array,
      required: true
    },
    modelValue: {
      type: String,
      required: true
    }
  },
  emits: ['update:modelValue']
}
</script>

<style scoped>
.custom-select {
  border: 1px solid var(--dark-border);
  border-radius: 8px;
  padding: 12px;
  transition: all 0.3s ease;
  background-color: rgba(0, 0, 0, 0.2);
  color: var(--dark-text);
}

.custom-select:focus {
  border-color: #0070f3;
  box-shadow: 0 0 0 3px rgba(0, 112, 243, 0.2);
}

.form-label {
  color: var(--dark-text-secondary);
  font-weight: 500;
}
</style>