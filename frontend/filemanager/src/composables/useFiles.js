import { ref, onMounted } from 'vue'
import { getFiles } from '@/api/files.js'

/**
 * @typedef {import('@/api/files.js').FileItem} FileItem
 */

export function useFiles() {
  const files = ref(/** @type {FileItem[]} */ ([]))
  const loading = ref(false)
  const error = ref(/** @type {string | null} */ (null))

  async function fetchFiles() {
    loading.value = true
    error.value = null
    try {
      files.value = await getFiles()
    } catch (e) {
      error.value = e.message ?? 'Failed to load files'
      files.value = []
    } finally {
      loading.value = false
    }
  }

  onMounted(fetchFiles)

  return { files, loading, error, fetchFiles }
}
