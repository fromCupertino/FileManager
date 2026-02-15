<template>
  <div class="file-card">
    <div class="file-card__icon">{{ icon }}</div>
    <div class="file-card__info">
      <button
        v-if="isPreviewable"
        type="button"
        class="file-card__name file-card__name--clickable"
        @click="$emit('preview', file)"
      >
        {{ file.name }}
      </button>
      <h3 v-else class="file-card__name">{{ file.name }}</h3>
      <p class="file-card__meta">{{ formatSize(file.size) }}</p>
      <p class="file-card__meta">{{ formatDate(file.modified) }}</p>
    </div>
    <div class="file-card__actions">
      <button
        type="button"
        class="file-card__copy-link"
        title="Copy direct link"
        @click="copyLink"
      >
        {{ copied ? '✓' : 'Copy link' }}
      </button>
      <button
        type="button"
        class="file-card__download"
        @click="$emit('download', file.name)"
      >
        Download
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { formatSize, formatDate, getFileIcon } from '@/utils/formatters.js'
import { isPreviewable as checkPreviewable } from '@/utils/preview.js'

const props = defineProps({
  /** @type {import('vue').PropType<import('@/api/files.js').FileItem>} */
  file: { type: Object, required: true },
  /** Прямая ссылка на файл на сервере. (name: string) => string */
  getFileUrl: { type: Function, required: true },
})

defineEmits(['download', 'preview'])

const isPreviewable = computed(() => checkPreviewable(props.file.name))
const icon = computed(() => getFileIcon(props.file.name))

const copied = ref(false)
let copyResetTimer = null

async function copyLink() {
  const url = props.getFileUrl(props.file.name)
  try {
    await navigator.clipboard.writeText(url)
    copied.value = true
    if (copyResetTimer) clearTimeout(copyResetTimer)
    copyResetTimer = setTimeout(() => { copied.value = false }, 2000)
  } catch {
    copied.value = false
  }
}
</script>
