<template>
  <div class="file-list">
    <transition-group name="fade" tag="div" class="file-list__grid">
      <FileCard
        v-for="file in files"
        :key="file.name"
        :file="file"
        :get-file-url="getFileUrl"
        @download="$emit('download', $event)"
        @preview="$emit('preview', $event)"
      />
    </transition-group>
    <p v-if="!files.length" class="file-list__empty">No matching files</p>
  </div>
</template>

<script setup>
import FileCard from './FileCard.vue'

defineProps({
  /** @type {import('vue').PropType<import('@/api/files.js').FileItem[]>} */
  files: { type: Array, default: () => [] },
  /** (name: string) => string — прямая ссылка на файл */
  getFileUrl: { type: Function, required: true },
})

defineEmits(['download', 'preview'])
</script>
