<template>
  <aside
    class="preview-sidebar"
    :class="{ 'preview-sidebar--open': isOpen }"
    aria-label="Preview"
  >
    <div class="preview-sidebar__header">
      <h2 class="preview-sidebar__title">{{ file?.name ?? '' }}</h2>
      <button
        type="button"
        class="preview-sidebar__close"
        aria-label="Close preview"
        @click="$emit('close')"
      >
        ×
      </button>
    </div>
    <div class="preview-sidebar__body">
      <template v-if="!file">
        <p class="preview-sidebar__empty">Select a file</p>
      </template>
      <template v-else-if="previewType === 'image'">
        <img
          :src="previewUrl"
          :alt="file.name"
          class="preview-sidebar__img"
          loading="lazy"
        />
      </template>
      <template v-else-if="previewType === 'pdf'">
        <iframe
          :src="previewUrl"
          :title="file.name"
          class="preview-sidebar__iframe"
        />
      </template>
      <template v-else>
        <p class="preview-sidebar__empty">Preview not available for this file type</p>
      </template>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { getPreviewType } from '@/utils/preview.js'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  /** @type {import('vue').PropType<import('@/api/files.js').FileItem | null>} */
  file: { type: Object, default: null },
  /** URL для превью (inline). (name: string) => string */
  getPreviewUrl: { type: Function, required: true },
})

defineEmits(['close'])

const previewType = computed(() =>
  props.file ? getPreviewType(props.file.name) : null
)

const previewUrl = computed(() =>
  props.file ? props.getPreviewUrl(props.file.name) : ''
)
</script>
