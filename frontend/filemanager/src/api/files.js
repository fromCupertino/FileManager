import { api } from './client.js'

/**
 * @typedef {Object} FileItem
 * @property {string} name
 * @property {number} size
 * @property {string} modified
 */

/**
 * @param {{ limit?: number }} [params]
 * @returns {Promise<FileItem[]>}
 */
export async function getFiles(params = {}) {
  const { data } = await api.get('/files', { params })
  return data
}

/**
 * @param {File | File[]} fileOrFiles
 * @param {(progress: number) => void} [onProgress]
 * @returns {Promise<{ uploaded: Array<{ filename: string, saved_to: string }>, errors: Array<{ filename: string, detail: string }> }>}
 */
export async function uploadFiles(fileOrFiles, onProgress) {
  const files = Array.isArray(fileOrFiles) ? fileOrFiles : [fileOrFiles]
  const formData = new FormData()
  for (const file of files) {
    formData.append('files', file)
  }
  const { data } = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: onProgress
      ? (e) => onProgress(e.total ? Math.round((e.loaded * 100) / e.total) : 0)
      : undefined,
  })
  return data
}

/**
 * @param {string} filename
 * @returns {string} URL для скачивания
 */
export function getDownloadUrl(filename) {
  const baseURL = api.defaults.baseURL ?? ''
  const base = baseURL.replace(/\/$/, '')
  return `${base}/download/${encodeURIComponent(filename)}`
}

/**
 * URL для отображения в превью (iframe/img) — без триггера скачивания
 * @param {string} filename
 * @returns {string}
 */
export function getPreviewUrl(filename) {
  return getDownloadUrl(filename) + '?preview=1'
}
