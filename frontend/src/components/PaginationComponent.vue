<template>
  <nav aria-label="Pagination" v-if="totalPages > 1">
    <ul class="pagination justify-content-center">
      <!-- Nút Previous -->
      <li class="page-item" :class="{ disabled: currentPage === 1 }">
        <a class="page-link" href="#" @click.prevent="onPageChange(currentPage - 1)" aria-label="Previous">
          <span aria-hidden="true">&laquo;</span>
        </a>
      </li>
      
      <!-- Trang đầu tiên -->
      <li class="page-item" :class="{ active: currentPage === 1 }">
        <a class="page-link" href="#" @click.prevent="onPageChange(1)">1</a>
      </li>
      
      <!-- Dấu ... trước -->
      <li v-if="showLeftEllipsis" class="page-item disabled">
        <span class="page-link">...</span>
      </li>
      
      <!-- Các trang ở giữa -->
      <li 
        v-for="page in middlePages" 
        :key="page" 
        class="page-item"
        :class="{ active: currentPage === page }"
      >
        <a class="page-link" href="#" @click.prevent="onPageChange(page)">{{ page }}</a>
      </li>
      
      <!-- Dấu ... sau -->
      <li v-if="showRightEllipsis" class="page-item disabled">
        <span class="page-link">...</span>
      </li>
      
      <!-- Trang cuối cùng -->
      <li v-if="totalPages > 1" class="page-item" :class="{ active: currentPage === totalPages }">
        <a class="page-link" href="#" @click.prevent="onPageChange(totalPages)">{{ totalPages }}</a>
      </li>
      
      <!-- Nút Next -->
      <li class="page-item" :class="{ disabled: currentPage === totalPages }">
        <a class="page-link" href="#" @click.prevent="onPageChange(currentPage + 1)" aria-label="Next">
          <span aria-hidden="true">&raquo;</span>
        </a>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'PaginationComponent',
  props: {
    currentPage: {
      type: Number,
      required: true
    },
    totalPages: {
      type: Number,
      required: true
    }
  },
  computed: {
    // Xác định xem có hiển thị dấu ... bên trái không
    showLeftEllipsis() {
      return this.currentPage > 3;
    },
    
    // Xác định xem có hiển thị dấu ... bên phải không
    showRightEllipsis() {
      return this.currentPage < this.totalPages - 2;
    },
    
    // Các trang ở giữa để hiển thị
    middlePages() {
      const pages = [];
      let start, end;
      
      if (this.totalPages <= 7) {
        // Nếu có ít hơn 7 trang, hiển thị tất cả
        start = 2;
        end = this.totalPages - 1;
      } else {
        // Nếu có nhiều hơn 7 trang, hiển thị trang hiện tại và 1-2 trang xung quanh
        if (this.currentPage < 5) {
          start = 2;
          end = 5;
        } else if (this.currentPage > this.totalPages - 4) {
          start = this.totalPages - 4;
          end = this.totalPages - 1;
        } else {
          start = this.currentPage - 1;
          end = this.currentPage + 1;
        }
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      
      return pages;
    }
  },
  methods: {
    onPageChange(page) {
      if (page < 1 || page > this.totalPages || page === this.currentPage) {
        return;
      }
      this.$emit('page-changed', page);
    }
  }
}
</script>

<style scoped>
.pagination {
  margin-top: 2rem;
  margin-bottom: 1rem;
}

.page-link {
  background-color: var(--dark-card-bg);
  color: var(--dark-text);
  border-color: var(--dark-border);
  padding: 0.5rem 0.75rem;
  margin: 0 2px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.page-link:hover {
  background-color: var(--dark-card-secondary);
  color: var(--primary-color);
  border-color: var(--primary-color);
}

.page-item.active .page-link {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  color: white;
}

.page-item.disabled .page-link {
  background-color: var(--dark-card-bg);
  border-color: var(--dark-border);
  color: var(--dark-text-secondary);
}
</style>