<template>
  <el-progress type="dashboard" :percentage="perc">
    <template #default="{ percentage }">
      <span class="percentage-value">{{ percentage }}%</span>
      <span class="percentage-label">{{ process_status }}</span>
    </template>
  </el-progress>
  <h2>{{ process_step }}</h2>
</template>

<script>
export default {
  name: 'Loading',
  props: {
    perc: Number,
    process_status: String,
    process_step: String,
  },
};
</script>
<style lang="stylus">
@keyframes rotate {
  100% {
    -webkit-transform: rotate(360deg);
  }
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
    -webkit-transform: rotate(360deg);
  }
}

@keyframes bounce {
  0%, 100% {
    -webkit-transform: scale(0);
  }

  50% {
    -webkit-transform: scale(1);
  }
}

@keyframes bounce {
  0%, 100% {
    transform: scale(0);
    -webkit-transform: scale(0);
  }

  50% {
    transform: scale(1);
    -webkit-transform: scale(1);
  }
}

.percentage-value {
  display: block;
  margin-top: 10px;
  font-size: 28px;
}

.percentage-label {
  display: block;
  margin-top: 10px;
  font-size: 12px;
}

.demo-progress .el-progress--line {
  margin-bottom: 15px;
  width: 350px;
}

.demo-progress .el-progress--circle {
  margin-right: 15px;
}
</style>