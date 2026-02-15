<template>
  <div v-if="progress > 0" class="upload-progress">
    <div class="upload-progress__bar" :style="{ width: progress + '%' }" />
  </div>
</template>

<script setup>
defineProps({
  progress: { type: Number, default: 0 },
})
</script>
