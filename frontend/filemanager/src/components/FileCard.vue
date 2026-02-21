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
    <div v-if="showManualCopyHint" class="file-card__copy-hint" role="status">
      <p class="file-card__copy-warning">
        Автоматическое копирование недоступно при HTTP-соединении. Скопируйте ссылку вручную:
      </p>
      <p class="file-card__copy-url">{{ manualCopyUrl }}</p>
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
const showManualCopyHint = ref(false)
const manualCopyUrl = ref('')
let copyResetTimer = null

async function copyLink() {
  const url = props.getFileUrl(props.file.name)
  const isHttpConnection = window.location.protocol === 'http:'

  if (isHttpConnection) {
    copied.value = false
    showManualCopyHint.value = true
    manualCopyUrl.value = url
    return
  }

  try {
    await navigator.clipboard.writeText(url)
    copied.value = true
    showManualCopyHint.value = false
    manualCopyUrl.value = ''
    if (copyResetTimer) clearTimeout(copyResetTimer)
    copyResetTimer = setTimeout(() => { copied.value = false }, 2000)
  } catch {
    copied.value = false
  }
}
</script>
