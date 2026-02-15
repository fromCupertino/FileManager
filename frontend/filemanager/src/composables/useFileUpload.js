import { ref } from 'vue'
import { uploadFile as apiUploadFile } from '@/api/files.js'

/**
 * @param {() => Promise<void>} [onSuccess] — например refetch списка файлов
 */
export function useFileUpload(onSuccess) {
  const uploadProgress = ref(0)
  const uploadError = ref(/** @type {string | null} */ (null))

  async function upload(file) {
    if (!file) return
    uploadProgress.value = 0
    uploadError.value = null
    try {
      await apiUploadFile(file, (percent) => {
        uploadProgress.value = percent
      })
      uploadProgress.value = 0
      await onSuccess?.()
    } catch (err) {
      uploadProgress.value = 0
      const status = err.response?.status
      uploadError.value = status === 409 ? 'File already exists' : 'Upload failed'
    }
  }

  function clearError() {
    uploadError.value = null
  }

  return { uploadProgress, uploadError, upload, clearError }
}
