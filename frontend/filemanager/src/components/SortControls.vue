<template>
  <div class="sort-controls">
    <label for="sort-by" class="sort-controls__label">Sort by:</label>
    <select
      id="sort-by"
      v-model="sortByModel"
      class="sort-controls__select"
      aria-label="Sort by"
    >
      <option value="name">Name</option>
      <option value="size">Size</option>
      <option value="modified">Date</option>
    </select>
    <button
      type="button"
      class="sort-controls__toggle"
      @click="$emit('toggle-order')"
    >
      {{ sortOrder === 'asc' ? '↑ Asc' : '↓ Desc' }}
    </button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  sortBy: { type: String, required: true },
  sortOrder: { type: String, required: true },
})

const emit = defineEmits(['update:sortBy', 'toggle-order'])

const sortByModel = computed({
  get: () => props.sortBy,
  set: (v) => emit('update:sortBy', v),
})
</script>
