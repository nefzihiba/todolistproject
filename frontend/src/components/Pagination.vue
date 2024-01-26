<template>
    <div class="pagination">
      <button :disabled="currentPage === 1" @click="prevPage" class="prev-btn">Previous</button>
      <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button :disabled="currentPage === totalPages" @click="nextPage" class="next-btn">Next</button>
    </div>
  </template>
  <script setup>
const props = defineProps({
  totalPages: {
    type: Number,
    required: true,
  },
  currentPage: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(['page-changed']);

const prevPage = () => {
  if (props.currentPage > 1) {
    emit('page-changed', props.currentPage - 1);
  }
};

const nextPage = () => {
  if (props.currentPage < props.totalPages) {
    emit('page-changed', props.currentPage + 1);
  }
};
</script>