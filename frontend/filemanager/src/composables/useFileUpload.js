import { ref } from 'vue'
import { uploadFiles as apiUploadFiles } from '@/api/files.js'

/**
 * @param {() => Promise<void>} [onSuccess] — например refetch списка файлов
 */
export function useFileUpload(onSuccess) {
  const uploadProgress = ref(0)
  const uploadError = ref(/** @type {string | null} */ (null))

  /**
   * @param {File | File[]} fileOrFiles
   */
  async function upload(fileOrFiles) {
    const files = Array.isArray(fileOrFiles) ? fileOrFiles : [fileOrFiles]
    if (!files.length) return
    uploadProgress.value = 0
    uploadError.value = null
    try {
      const result = await apiUploadFiles(files, (percent) => {
        uploadProgress.value = percent
      })
      uploadProgress.value = 0
      if (result.errors?.length) {
        const first = result.errors[0]
        uploadError.value = first.detail === 'File already exists' ? 'Some files already exist' : first.detail
      }
      if (result.uploaded?.length) await onSuccess?.()
    } catch (err) {
      uploadProgress.value = 0
      uploadError.value = err.response?.status === 409 ? 'File already exists' : 'Upload failed'
    }
  }

  function clearError() {
    uploadError.value = null
  }

  return { uploadProgress, uploadError, upload, clearError }
}
