<template>
  <el-container class="p-4 space-y-6">
    <!-- 上传视频 -->
    <el-upload
      class="upload-demo"
      drag
      action="http://localhost:5000/upload"
      :on-success="handleUploadSuccess"
      :file-list="fileList"
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">
        拖拽视频或 <em>点击上传</em>
      </div>
    </el-upload>

    <!-- 播放器和切片 -->
    <el-card v-if="m3u8Url" class="w-fit">
      <video id="video-player" class="video-js vjs-default-skin" controls preload="auto" width="640" height="360">
        <source :src="m3u8Url" type="application/x-mpegURL" />
      </video>
    </el-card>

    <!-- 目标检测结果 -->
    <el-card v-if="detectionResult.length">
      <template #header>YOLO 检测结果</template>
      <el-row :gutter="20">
        <el-col v-for="(frame, index) in detectionResult" :key="index" :span="8">
          <el-image :src="getFramePath(frame.frame)" fit="contain" class="w-full border mb-2" />
          <el-tag v-for="(obj, i) in frame.objects" :key="i" class="mr-1 mb-1">
            {{ obj.label }} - {{ obj.confidence }}
          </el-tag>
        </el-col>
      </el-row>
    </el-card>

    <!-- 字幕识别结果 -->
    <el-card v-if="subtitle.length">
      <template #header>AI 字幕识别</template>
      <el-scrollbar height="200px">
        <el-timeline>
          <el-timeline-item v-for="(line, i) in subtitle" :key="i">
            {{ line }}
          </el-timeline-item>
        </el-timeline>
      </el-scrollbar>
    </el-card>
  </el-container>
</template>

<script>
export default {
  data() {
    return {
      fileList: [],
      filename: '',
      m3u8Url: '',
      detectionResult: [],
      subtitle: []
    };
  },
  methods: {
    handleUploadSuccess(response) {
      this.filename = response.data.filename;
      this.convertToHLS();
      this.fetchSubtitles();
      this.runYOLODetection();
    },
    convertToHLS() {
      fetch('http://localhost:5000/video/hls', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename: this.filename })
      })
        .then(res => res.json())
        .then(res => {
          this.m3u8Url = `http://localhost:5000/${res.data.m3u8_url}`;
        });
    },
    fetchSubtitles() {
      fetch('http://localhost:5000/video/subtitle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename: this.filename })
      })
        .then(res => res.json())
        .then(res => {
          this.subtitle = res.data.subtitles;
        });
    },
    runYOLODetection() {
      fetch('http://localhost:5000/video/yolo-detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filename: this.filename, fps: 1 })
      })
        .then(res => res.json())
        .then(res => {
          this.detectionResult = res.data;
        });
    },
    getFramePath(path) {
      return `http://localhost:5000/${path}`;
    }
  }
};
</script>

<style>
@import 'https://vjs.zencdn.net/8.5.1/video-js.css';
</style>
