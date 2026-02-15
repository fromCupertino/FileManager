<template>
  <div class="page">
    <div class="wrapper">
      <header>
        <h1>📁 File Manager</h1>
        <input
          v-model="search"
          placeholder="Search files..."
          class="search"
        />
      </header>

      <div
        class="dropzone"
        :class="{ active: isDragging }"
        @dragover.prevent="isDragging = true"
        @dragleave="isDragging = false"
        @drop.prevent="handleDrop"
      >
        <p>Drag & Drop file here or click to select</p>
        <input type="file" @change="handleFileSelect" hidden ref="fileInput" />
        <button @click="openFilePicker">Choose File</button>
      </div>

      <div v-if="uploadProgress > 0" class="progress-wrapper">
        <div class="progress-bar" :style="{ width: uploadProgress + '%' }"></div>
      </div>

      <div class="controls">
        <label>Sort by:</label>
        <select v-model="sortBy">
          <option value="name">Name</option>
          <option value="size">Size</option>
          <option value="modified">Date</option>
        </select>

        <button @click="toggleOrder">
          {{ sortOrder === 'asc' ? '↑ Asc' : '↓ Desc' }}
        </button>
      </div>

      <transition-group name="fade" tag="div" class="grid">
        <div
          class="card"
          v-for="file in filteredFiles"
          :key="file.name"
        >
          <div class="icon">{{ getIcon(file.name) }}</div>

          <div class="info">
            <h3>{{ file.name }}</h3>
            <p>{{ formatSize(file.size) }}</p>
            <p>{{ formatDate(file.modified) }}</p>
          </div>

          <button class="download" @click="downloadFile(file.name)">
            Download
          </button>
        </div>
      </transition-group>

      <div v-if="!filteredFiles.length" class="empty">
        No matching files
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE ?? 'http://localhost:8000'

const files = ref([])
const search = ref('')
const sortBy = ref('name')
const sortOrder = ref('asc')
const selectedFile = ref(null)
const uploadProgress = ref(0)
const isDragging = ref(false)
const fileInput = ref(null)

const fetchFiles = async () => {
  const response = await axios.get(`${API_BASE}/files`)
  files.value = response.data
}

const openFilePicker = () => fileInput.value.click()
const handleFileSelect = (e) => { selectedFile.value = e.target.files[0]; uploadFile() }
const handleDrop = (e) => { isDragging.value = false; selectedFile.value = e.dataTransfer.files[0]; uploadFile() }

const uploadFile = async () => {
  if (!selectedFile.value) return
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  try {
    await axios.post(`${API_BASE}/upload`, formData, {
      onUploadProgress: (e) => uploadProgress.value = Math.round((e.loaded*100)/e.total)
    })
    uploadProgress.value = 0
    selectedFile.value = null
    await fetchFiles()
  } catch (err) {
    uploadProgress.value = 0
    alert(err.response?.status===409?'File already exists':'Upload failed')
  }
}

const downloadFile = (filename) => window.open(`${API_BASE}/download/${filename}`, '_blank')

const formatSize = (bytes) => bytes<1024?`${bytes} B`:bytes<1024*1024?`${(bytes/1024).toFixed(1)} KB`:`${(bytes/(1024*1024)).toFixed(2)} MB`
const formatDate = (iso) => new Date(iso).toLocaleString()
const getIcon = (name) => { const ext=name.split('.').pop().toLowerCase(); const map={pdf:'📕',xlsx:'📊',json:'🧾',jpg:'🖼️',jpeg:'🖼️',png:'🖼️',txt:'📄'}; return map[ext]||'📁' }
const toggleOrder = () => sortOrder.value = sortOrder.value==='asc'?'desc':'asc'
const filteredFiles = computed(()=>{
  let result=files.value.filter(f=>f.name.toLowerCase().includes(search.value.toLowerCase()))
  result.sort((a,b)=>{
    if(sortBy.value==='name') return sortOrder.value==='asc'?a.name.localeCompare(b.name):b.name.localeCompare(a.name)
    return sortOrder.value==='asc'?a[sortBy.value]-b[sortBy.value]:b[sortBy.value]-a[sortBy.value]
  })
  return result
})
onMounted(fetchFiles)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

.page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 20px;
  font-family: 'Inter', sans-serif;
  background: linear-gradient(270deg, #993300, #cc5500, #ff6600, #993300);
  background-size: 800% 800%;
  animation: gradientBG 20s ease infinite;
  color: #fff;
}

@keyframes gradientBG {
  0% { background-position:0% 50%; }
  50% { background-position:100% 50%; }
  100% { background-position:0% 50%; }
}

.wrapper {
  width: 100%;
  max-width: 1100px;
  padding: 30px;
  border-radius: 20px;
  background: rgba(0,0,0,0.35);
  backdrop-filter: blur(12px);
  box-shadow: 0 15px 40px rgba(0,0,0,0.4);
  transition: background 0.3s, color 0.3s;
}

header { display:flex; justify-content:space-between; align-items:center; margin-bottom:20px; }
header h1 { font-family:'Inter',sans-serif; }

.search {
  padding:8px 12px;
  border-radius:12px;
  border:1px solid #cc5500;
  background: rgba(255,255,255,0.1);
  color: #fff;
  outline:none;
  transition:0.3s;
  font-family:'Inter',sans-serif;
}
.search::placeholder { color:#ffb87c; }
.search:focus { border-color:#ff6600; box-shadow:0 0 8px rgba(255,102,0,0.5); }

.dropzone {
  border:2px dashed #ff6600;
  padding:40px;
  text-align:center;
  margin:20px 0;
  border-radius:20px;
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(12px);
  transition:0.3s;
  font-family:'Inter',sans-serif;
}
.dropzone.active { background: rgba(255,102,0,0.1); }

.progress-wrapper { height:8px; background:rgba(255,102,0,0.2); border-radius:10px; margin-bottom:20px; overflow:hidden; }
.progress-bar { height:100%; background:linear-gradient(90deg,#ff6600,#993300); transition:width 0.3s ease; }

.controls { display:flex; gap:10px; margin-bottom:20px; align-items:center; }
button, .download { cursor:pointer; border:none; border-radius:12px; padding:8px 12px; background:linear-gradient(135deg,#cc5500,#ff6600); color:#fff; font-weight:500; transition:0.3s; font-family:'Inter',sans-serif; }
button:hover, .download:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(204,85,0,0.5); }

.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:20px; }

.card {
  background: rgba(0,0,0,0.3);
  backdrop-filter: blur(12px);
  border-radius:20px;
  padding:20px;
  display:flex;
  flex-direction:column;
  justify-content:space-between;
  transition: transform 0.3s, box-shadow 0.3s;
  font-family:'Inter',sans-serif;
}
.card:hover { transform:translateY(-5px); box-shadow:0 15px 40px rgba(204,85,0,0.3); }

.icon { font-size:32px; margin-bottom:10px; }
.info h3 { font-size:16px; word-break:break-all; margin-bottom:5px; }
.info p { font-size:12px; margin:2px 0; }
.empty { text-align:center; margin-top:40px; font-weight:500; color:#ff6600; }

.fade-enter-active,.fade-leave-active { transition:0.3s; }
.fade-enter-from,.fade-leave-to { opacity:0; transform:translateY(10px); }
</style>
