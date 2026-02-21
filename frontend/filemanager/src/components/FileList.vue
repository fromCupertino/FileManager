<template>
  <div class="file-list">
    <template v-if="files.length">
      <div class="file-list__toolbar">
        <span class="file-list__view-label">View:</span>
        <div class="file-list__view-switch" role="tablist" aria-label="File view mode">
          <button
            type="button"
            class="file-list__view-btn"
            :class="{ 'is-active': viewMode === 'grid' }"
            role="tab"
            :aria-selected="viewMode === 'grid'"
            @click="viewMode = 'grid'"
          >
            Grid
          </button>
          <button
            type="button"
            class="file-list__view-btn"
            :class="{ 'is-active': viewMode === 'list' }"
            role="tab"
            :aria-selected="viewMode === 'list'"
            @click="viewMode = 'list'"
          >
            List
          </button>
        </div>
      </div>

      <transition name="page" mode="out-in">
        <div :key="`page-${currentPage}-${viewMode}`" class="file-list__page">
          <transition-group
            name="fade"
            tag="div"
            class="file-list__grid"
            :class="{ 'file-list__grid--list': viewMode === 'list' }"
          >
            <FileCard
              v-for="file in paginatedFiles"
              :key="file.name"
              :file="file"
              :get-file-url="getFileUrl"
              :compact="viewMode === 'list'"
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

const PAGE_SIZE_GRID = 9
const PAGE_SIZE_LIST = 14

const props = defineProps({
  /** @type {import('vue').PropType<import('@/api/files.js').FileItem[]>} */
  files: { type: Array, default: () => [] },
  /** (name: string) => string — прямая ссылка на файл */
  getFileUrl: { type: Function, required: true },
})

defineEmits(['download', 'preview'])

const currentPage = ref(1)
const viewMode = ref('grid')
const pageSize = computed(() => (viewMode.value === 'list' ? PAGE_SIZE_LIST : PAGE_SIZE_GRID))

const totalPages = computed(() => Math.max(1, Math.ceil(props.files.length / pageSize.value)))

const paginatedFiles = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return props.files.slice(start, start + pageSize.value)
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

watch(viewMode, () => {
  currentPage.value = 1
})
</script>
