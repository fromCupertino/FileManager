import { ref, computed } from 'vue'

/**
 * @param {import('vue').Ref<import('@/api/files.js').FileItem[]>} files
 */
export function useFileSort(files) {
  const search = ref('')
  const sortBy = ref('name')
  const sortOrder = ref('asc')

  const filteredFiles = computed(() => {
    const query = search.value.toLowerCase()
    let result = files.value.filter((f) =>
      f.name.toLowerCase().includes(query)
    )
    const order = sortOrder.value === 'asc' ? 1 : -1
    result.sort((a, b) => {
      if (sortBy.value === 'name') {
        return order * a.name.localeCompare(b.name)
      }
      if (sortBy.value === 'modified') {
        return order * (new Date(a.modified) - new Date(b.modified))
      }
      return order * (a[sortBy.value] - b[sortBy.value])
    })
    return result
  })

  function toggleOrder() {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  }

  return { search, sortBy, sortOrder, filteredFiles, toggleOrder }
}
