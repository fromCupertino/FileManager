const IMAGE_EXT = new Set(['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp'])
const PDF_EXT = 'pdf'

/**
 * @param {string} filename
 * @returns {'image' | 'pdf' | null}
 */
export function getPreviewType(filename) {
  const ext = filename.split('.').pop()?.toLowerCase() ?? ''
  if (IMAGE_EXT.has(ext)) return 'image'
  if (ext === PDF_EXT) return 'pdf'
  return null
}

/**
 * @param {string} filename
 * @returns {boolean}
 */
export function isPreviewable(filename) {
  return getPreviewType(filename) !== null
}
