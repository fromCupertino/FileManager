const SIZE_KB = 1024
const SIZE_MB = SIZE_KB * 1024

const EXT_ICONS = {
  pdf: '📕',
  xlsx: '📊',
  json: '🧾',
  jpg: '🖼️',
  jpeg: '🖼️',
  png: '🖼️',
  txt: '📄',
}

/**
 * @param {number} bytes
 * @returns {string}
 */
export function formatSize(bytes) {
  if (bytes < SIZE_KB) return `${bytes} B`
  if (bytes < SIZE_MB) return `${(bytes / SIZE_KB).toFixed(1)} KB`
  return `${(bytes / SIZE_MB).toFixed(2)} MB`
}

/**
 * @param {string} isoDate
 * @returns {string}
 */
export function formatDate(isoDate) {
  return new Date(isoDate).toLocaleString()
}

/**
 * @param {string} filename
 * @returns {string} emoji-иконка по расширению
 */
export function getFileIcon(filename) {
  const ext = filename.split('.').pop()?.toLowerCase() ?? ''
  return EXT_ICONS[ext] ?? '📁'
}
