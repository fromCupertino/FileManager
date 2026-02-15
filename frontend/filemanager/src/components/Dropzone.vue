<template>
  <div
    class="dropzone"
    :class="{ 'dropzone--active': isDragging }"
    @dragover.prevent="isDragging = true"
    @dragleave="isDragging = false"
    @drop.prevent="handleDrop"
  >
    <p class="dropzone__text">Drag & Drop file here or click to select</p>
    <input
      ref="inputRef"
      type="file"
      class="dropzone__input"
      aria-label="Choose file"
      @change="handleSelect"
    />
    <button type="button" class="dropzone__button" @click="openPicker">
      Choose File
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['select'])

const inputRef = ref(null)
const isDragging = ref(false)

function openPicker() {
  inputRef.value?.click()
}

function handleSelect(e) {
  const file = e.target.files?.[0]
  if (file) emit('select', file)
  e.target.value = ''
}

function handleDrop(e) {
  isDragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) emit('select', file)
}
</script>
