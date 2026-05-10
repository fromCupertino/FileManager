<template>
  <aside
    class="preview-sidebar"
    :class="{
      'preview-sidebar--open': isOpen,
      'preview-sidebar--resizing': isResizing,
    }"
    :style="{ width: `${sidebarWidth}px` }"
    aria-label="Preview"
  >
    <div
      class="preview-sidebar__resize-handle"
      role="separator"
      tabindex="0"
      aria-orientation="vertical"
      aria-label="Resize preview"
      title="Drag to resize preview"
      :aria-valuemin="MIN_WIDTH"
      :aria-valuemax="maxWidth"
      :aria-valuenow="sidebarWidth"
      @pointerdown="startResize"
      @mousedown="startMouseResize"
      @keydown="resizeWithKeyboard"
    />
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
        <img :src="previewUrl" :alt="file.name" class="preview-sidebar__img" loading="lazy" />
      </template>
      <template v-else-if="previewType === 'pdf'">
        <iframe :src="previewUrl" :title="file.name" class="preview-sidebar__iframe" />
      </template>
      <template v-else>
        <p class="preview-sidebar__empty">Preview not available for this file type</p>
      </template>
    </div>
  </aside>
</template>

<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { getPreviewType } from '@/utils/preview.js'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  /** @type {import('vue').PropType<import('@/api/files.js').FileItem | null>} */
  file: { type: Object, default: null },
  /** URL для превью (inline). (name: string) => string */
  getPreviewUrl: { type: Function, required: true },
})

defineEmits(['close'])

const MIN_WIDTH = 260
const DEFAULT_WIDTH = 420
const MAX_WIDTH = 920

const sidebarWidth = ref(DEFAULT_WIDTH)
const isResizing = ref(false)
const maxWidth = ref(MAX_WIDTH)
const activePointerId = ref(null)

const previewType = computed(() => (props.file ? getPreviewType(props.file.name) : null))

const previewUrl = computed(() => (props.file ? props.getPreviewUrl(props.file.name) : ''))

function getMaxWidth() {
  return Math.min(MAX_WIDTH, Math.max(getMinWidth(), window.innerWidth - 24))
}

function getMinWidth() {
  return Math.min(MIN_WIDTH, window.innerWidth)
}

function clampWidth(width) {
  maxWidth.value = getMaxWidth()
  return Math.min(maxWidth.value, Math.max(getMinWidth(), width))
}

function updateWidth(clientX) {
  sidebarWidth.value = clampWidth(window.innerWidth - clientX)
}

function beginResize() {
  if (!props.isOpen) return

  isResizing.value = true
  document.body.classList.add('preview-sidebar-resize-active')
}

function startResize(event) {
  event.preventDefault()
  beginResize()
  if (!isResizing.value) return

  activePointerId.value = event.pointerId
  event.currentTarget.setPointerCapture?.(event.pointerId)
  updateWidth(event.clientX)
  document.addEventListener('pointermove', handlePointerMove)
  document.addEventListener('pointerup', stopResize)
  document.addEventListener('pointercancel', stopResize)
}

function startMouseResize(event) {
  if (event.button !== 0) return

  event.preventDefault()
  beginResize()
  if (!isResizing.value) return

  updateWidth(event.clientX)
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', stopResize)
}

function handlePointerMove(event) {
  if (!isResizing.value) return
  if (activePointerId.value !== null && event.pointerId !== activePointerId.value) return
  updateWidth(event.clientX)
}

function handleMouseMove(event) {
  if (!isResizing.value) return
  updateWidth(event.clientX)
}

function stopResize() {
  isResizing.value = false
  activePointerId.value = null
  document.body.classList.remove('preview-sidebar-resize-active')
  document.removeEventListener('pointermove', handlePointerMove)
  document.removeEventListener('pointerup', stopResize)
  document.removeEventListener('pointercancel', stopResize)
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', stopResize)
}

function resizeWithKeyboard(event) {
  const step = event.shiftKey ? 64 : 24

  if (event.key === 'ArrowLeft') {
    event.preventDefault()
    sidebarWidth.value = clampWidth(sidebarWidth.value + step)
  } else if (event.key === 'ArrowRight') {
    event.preventDefault()
    sidebarWidth.value = clampWidth(sidebarWidth.value - step)
  } else if (event.key === 'Home') {
    event.preventDefault()
    sidebarWidth.value = getMinWidth()
  } else if (event.key === 'End') {
    event.preventDefault()
    sidebarWidth.value = getMaxWidth()
  }
}

onBeforeUnmount(stopResize)
</script>
