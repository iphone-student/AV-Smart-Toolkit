<template>
  <div class="detection-container">
    <div class="controls">
      <h2>多目标检测</h2>
      <div class="algorithm-selector">
        <label>选择算法:</label>
        <select v-model="selectedAlgorithm">
          <option value="algorithm1">基础目标检测</option>
          <option value="algorithm2">高级特征识别</option>
          <option value="algorithm3">实时动作分析</option>
        </select>
      </div>
      <div class="file-upload">
  <el-button @click="openImage" type="primary">打开图片</el-button>
  <input type="file" id="image-upload" accept="image/*" @change="handleImageUpload" hidden>
  <el-button @click="openVideo" type="primary">打开视频</el-button>
  <input type="file" id="video-upload" accept="video/*" @change="handleVideoUpload" hidden>
  <el-button @click="detectImage" type="success" :disabled="!currentMedia || currentMedia !== 'image'">检测图片识别</el-button>
</div>
    </div>
    <div class="display-area">
      <div v-if="currentMedia === 'image'" class="image-display">
        <img :src="mediaSource" alt="检测结果">
      </div>
      <div v-else-if="currentMedia === 'video'" class="video-display">
        <video :src="mediaSource" controls @play="startVideoDetection"></video>
        <canvas ref="detectionCanvas"></canvas>
      </div>
      <div v-else class="placeholder">
        <p>请上传图片或视频进行检测</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

const selectedAlgorithm = ref('algorithm1');
const currentMedia = ref(null);
const mediaSource = ref('');
const detectionCanvas = ref(null);
const selectedFile = ref(null);
const detectionResults = ref(null);
let videoElement = null;
let detectionInterval = null;

onMounted(() => {
  videoElement = document.querySelector('video');
});

const openImage = () => {
  document.getElementById('image-upload').click();
};

const openVideo = () => {
  document.getElementById('video-upload').click();
};

const handleImageUpload = (e) => {
  const file = e.target.files[0];
  if (file) {
    selectedFile.value = file;
    currentMedia.value = 'image';
    mediaSource.value = URL.createObjectURL(file);
    // 模拟图片检测
    setTimeout(() => performDetection(), 500);
  }
};

const handleVideoUpload = (e) => {
  const file = e.target.files[0];
  if (file) {
    currentMedia.value = 'video';
    mediaSource.value = URL.createObjectURL(file);
  }
};

const startVideoDetection = () => {
  if (detectionInterval) clearInterval(detectionInterval);
  detectionInterval = setInterval(() => performDetection(), 100);
};

const detectImage = () => {
  if (currentMedia.value === 'image') {
    performDetection();
    // 调用后端API
    const formData = new FormData();
    formData.append('image', selectedFile.value);
    axios.post('/api/detect-image', formData)
      .then(response => {
        console.log('Detection results:', response.data);
        detectionResults.value = response.data;
      })
      .catch(error => {
        console.error('Error during detection:', error);
        ElMessage.error('检测失败，请重试');
      });
  }
};


const performDetection = () => {
  // 这里实现算法检测逻辑
  console.log(`使用${selectedAlgorithm.value}进行检测`);
  if (currentMedia.value === 'video' && detectionCanvas.value && videoElement) {
    const canvas = detectionCanvas.value;
    const ctx = canvas.getContext('2d');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    // 绘制检测框示例
    ctx.strokeStyle = 'red'; 
    ctx.lineWidth = 2;
    ctx.strokeRect(100, 100, 200, 150);
  }
};
</script>

<style scoped>
.detection-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  height: 80vh;
  box-sizing: border-box;
}

.controls {
  line-height: 2;
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: center;
  padding: 15px 20px;
  background-color: rgba(255,255,255,0.05);
  border-radius: 8px;
}

.display-area {
    height: 40px;
  flex: 1;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  min-height: 0;
  background-color: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: auto;

}

.image-display img {
  max-width: 100%;
  max-height: 80%;
  object-fit: contain;
}

.video-display {
  position: relative;
  max-width: 100%;
  max-height: 80%;
}

.video-display video {
  max-width: 100%;
  max-height: 80%;
  object-fit: contain;
}

.video-display canvas {
  position: absolute;
  top: 0;
  left: 0;
}

.placeholder {
  width: 100%;
  height: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #aaa;
  font-size: 14px;
  flex-direction: column;
  gap: 10px;
}


.algorithm-selector {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  background-color: rgba(255,255,255,0.05);
  border-radius: 6px;
}

.algorithm-selector label {
  color: #00e5ff;
  font-weight: 500;
}

.algorithm-selector select {
  padding: 6px 10px;
  border-radius: 4px;
  border: 1px solid rgba(255,255,255,0.1);
  background-color: rgba(0,0,0,0.3);
  color: #fff;
}

.file-upload {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.file-upload .el-button {
  padding: 8px 16px;
}
</style>