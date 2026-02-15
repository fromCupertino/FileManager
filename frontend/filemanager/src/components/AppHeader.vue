<template>
  <header class="app-header">
    <h1 class="app-header__title">📁 File Manager</h1>
    <input
      v-model="searchQuery"
      type="search"
      placeholder="Search files..."
      class="app-header__search"
      aria-label="Search files"
    />
  </header>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
})

const emit = defineEmits(['update:modelValue'])

const searchQuery = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})
</script>
