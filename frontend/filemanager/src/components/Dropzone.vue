<template>
  <div
    class="dropzone"
    :class="{ 'dropzone--active': isDragging }"
    @dragover.prevent="isDragging = true"
    @dragleave="isDragging = false"
    @drop.prevent="handleDrop"
  >
    <p class="dropzone__text">Drag & Drop files here or click to select</p>
    <input
      ref="inputRef"
      type="file"
      class="dropzone__input"
      multiple
      aria-label="Choose files"
      @change="handleSelect"
    />
    <button type="button" class="dropzone__button" @click="openPicker">
      Choose Files
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
  const fileList = e.target.files
  if (fileList?.length) emit('select', Array.from(fileList))
  e.target.value = ''
}

function handleDrop(e) {
  isDragging.value = false
  const fileList = e.dataTransfer?.files
  if (fileList?.length) emit('select', Array.from(fileList))
}
</script>
