<template>
  <div class="empty-history">
    <div class="empty-icon">
      <i class="fas fa-history"></i>
    </div>
    <h3>No code generation history</h3>
    <p>You haven't made any code generation requests yet. Try generating new code!</p>
    <router-link to="/generate" class="btn btn-primary mt-3">
      <i class="fas fa-code me-2"></i> Generate code now
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'EmptyHistoryState'
}
</script>

<style scoped>
.empty-history {
  background: var(--dark-card-bg);
  border-radius: 15px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.empty-icon {
  font-size: 4rem;
  color: #4b5563;
  margin-bottom: 1rem;
}

.empty-history h3 {
  color: var(--dark-text);
  margin-bottom: 0.5rem;
}

.empty-history p {
  color: var(--dark-text-secondary);
  max-width: 400px;
  margin: 0 auto;
}
</style>