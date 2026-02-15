<template>
  <div class="file-card">
    <div class="file-card__icon">{{ icon }}</div>
    <div class="file-card__info">
      <h3 class="file-card__name">{{ file.name }}</h3>
      <p class="file-card__meta">{{ formatSize(file.size) }}</p>
      <p class="file-card__meta">{{ formatDate(file.modified) }}</p>
    </div>
    <button
      type="button"
      class="file-card__download"
      @click="$emit('download', file.name)"
    >
      Download
    </button>
  </div>
</template>

<script setup>
import { formatSize, formatDate, getFileIcon } from '@/utils/formatters.js'
import { computed } from 'vue'

const props = defineProps({
  /** @type {import('vue').PropType<import('@/api/files.js').FileItem>} */
  file: { type: Object, required: true },
})

defineEmits(['download'])

const icon = computed(() => getFileIcon(props.file.name))
</script>
