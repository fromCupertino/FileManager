<template>
  <div class="page">
    <div class="wrapper">
      <AppHeader v-model="search" />

      <Dropzone @select="handleFileSelect" />

      <UploadProgress :progress="uploadProgress" />
      <p v-if="uploadError" class="error-message">{{ uploadError }}</p>

      <SortControls
        :sort-by="sortBy"
        :sort-order="sortOrder"
        @update:sort-by="updateSortBy"
        @toggle-order="toggleOrder"
      />

      <FileList
        :files="filteredFiles"
        :get-file-url="getPreviewUrl"
        @download="openDownload"
        @preview="openPreview"
      />
    </div>

    <PreviewSidebar
      :is-open="!!previewFile"
      :file="previewFile"
      :get-preview-url="getPreviewUrl"
      @close="previewFile = null"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
import Dropzone from '@/components/Dropzone.vue'
import UploadProgress from '@/components/UploadProgress.vue'
import SortControls from '@/components/SortControls.vue'
import FileList from '@/components/FileList.vue'
import PreviewSidebar from '@/components/PreviewSidebar.vue'
import { useFiles } from '@/composables/useFiles.js'
import { useFileUpload } from '@/composables/useFileUpload.js'
import { useFileSort } from '@/composables/useFileSort.js'
import { getDownloadUrl, getPreviewUrl } from '@/api/files.js'

const { files, fetchFiles } = useFiles()
const { search, sortBy, sortOrder, filteredFiles, toggleOrder } = useFileSort(files)
const { uploadProgress, uploadError, upload, clearError } = useFileUpload(fetchFiles)

const previewFile = ref(null)

function updateSortBy(v) {
  sortBy.value = v
}

function handleFileSelect(file) {
  clearError()
  upload(file)
}

function openDownload(filename) {
  window.open(getDownloadUrl(filename), '_blank')
}

function openPreview(file) {
  previewFile.value = file
}

watch(uploadError, (err) => {
  if (err) setTimeout(clearError, 4000)
})
</script>
