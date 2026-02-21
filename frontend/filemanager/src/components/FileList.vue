<template>
  <div class="file-list">
    <template v-if="files.length">
      <transition name="page" mode="out-in">
        <div :key="`page-${currentPage}`" class="file-list__page">
          <transition-group name="fade" tag="div" class="file-list__grid">
            <FileCard
              v-for="file in paginatedFiles"
              :key="file.name"
              :file="file"
              :get-file-url="getFileUrl"
              @download="$emit('download', $event)"
              @preview="$emit('preview', $event)"
            />
          </transition-group>
        </div>
      </transition>

      <div class="file-list__pagination">
        <button
          class="file-list__page-btn"
          type="button"
          :disabled="isFirstPage"
          @click="goToPage(currentPage - 1)"
        >
          Prev
        </button>

        <div class="file-list__page-numbers" role="navigation" aria-label="File list pagination">
          <button
            v-for="page in totalPages"
            :key="page"
            class="file-list__page-number"
            :class="{ 'is-active': page === currentPage }"
            type="button"
            @click="goToPage(page)"
          >
            {{ page }}
          </button>
        </div>

        <button
          class="file-list__page-btn"
          type="button"
          :disabled="isLastPage"
          @click="goToPage(currentPage + 1)"
        >
          Next
        </button>
      </div>
    </template>
    <p v-else class="file-list__empty">No matching files</p>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import FileCard from './FileCard.vue'

const PAGE_SIZE = 9

const props = defineProps({
  /** @type {import('vue').PropType<import('@/api/files.js').FileItem[]>} */
  files: { type: Array, default: () => [] },
  /** (name: string) => string — прямая ссылка на файл */
  getFileUrl: { type: Function, required: true },
})

defineEmits(['download', 'preview'])

const currentPage = ref(1)

const totalPages = computed(() => Math.max(1, Math.ceil(props.files.length / PAGE_SIZE)))

const paginatedFiles = computed(() => {
  const start = (currentPage.value - 1) * PAGE_SIZE
  return props.files.slice(start, start + PAGE_SIZE)
})

const isFirstPage = computed(() => currentPage.value === 1)
const isLastPage = computed(() => currentPage.value === totalPages.value)

function goToPage(page) {
  const clamped = Math.min(Math.max(page, 1), totalPages.value)
  currentPage.value = clamped
}

watch(
  () => props.files.length,
  () => {
    if (currentPage.value > totalPages.value) {
      currentPage.value = totalPages.value
    }
  },
)
</script>
