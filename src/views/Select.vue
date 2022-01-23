<template>
  <div id="select">
    <Menu />
    <div id="steps">
      <el-steps
        :active="active"
        finish-status="success"
        simple
        style="margin-top: 20px"
      >
        <el-step title="选择待处理文件"></el-step>
        <el-step title="选择网络"></el-step>
        <el-step title="处理结果"></el-step>
      </el-steps>
    </div>

    <!-- 页面一：上传 -->
    <div id="upload" v-show="set_show(0)">
      <el-upload
        class="upload-demo"
        drag
        accept=".tif"
        action="http://localhost:5001/img"
        multiple
        name="tif_file"
        :on-success="upload_success"
        :on-error="upload_failed"
      >
        <el-icon class="el-icon--upload"></el-icon>
        <div class="el-upload__text">
          将文件拖到此处或 <em>点击选择文件上传</em> 对文件进行切割
        </div>
        <template #tip>
          <div class="el-upload__tip">请上传TIF格式文件</div>
        </template>
      </el-upload>
    </div>
    <div id="choose" v-show="set_show(1)">
      <el-radio-group v-model="net_choose" size="large">
        <el-radio-button label="Unet"></el-radio-button>
        <el-radio-button label="DeeplabV3++"></el-radio-button>
      </el-radio-group>
    </div>
    <div id="process" v-show="set_show(2)">
      <el-progress type="dashboard" :percentage="0">
        <template #default="{ percentage }">
          <span class="percentage-value">{{ percentage }}%</span>
          <span class="percentage-label">Progressing</span>
        </template>
      </el-progress>
    </div>
    <div id="result" v-show="set_show(3)">结果</div>
  </div>
  <el-button style="margin-top: 12px" @click="prev" v-show="set_show(5)"
    >回到上一步</el-button
  >
  <el-button
    style="margin-top: 12px"
    type="success"
    @click="next"
    v-show="set_show(4)"
    >下一步</el-button
  >
</template>
<script>
import Menu from '@/components/Menu.vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';

export default {
  data() {
    return {
      hasUpload: true,
      active: 0,
      show: '100000', // 选择待处理文件、选择网络、处理中、处理结果、下一步、上一步
      net_choose: 'Unet',
    };
  },
  components: {
    Menu,
  },
  watch: {
    active() {
      switch (this.active) {
        case 0:
          this.show = '100000';
          break;
        case 1:
          this.show = '010011';
          break;
        case 2:
          this.show = '001000';
          let porc = setInterval(() => {
            axios.get('http://localhost:5001/seg_process').then((response) => {
              console.log(response);
              let total_count = response.data.data.total_count;
              let change_count = response.data.data.change_count;
              if (total_count == change_count) {
                clearInterval(porc);
              }
            });
          }, 1000);
          break;
        case 3:
          this.show = '000101';
          break;
      }
    },
  },
  methods: {
    set_show(num) {
      return this.show[num] == 0 ? false : true;
    },
    upload_success(response, file, fileList) {
      ElMessage({
        message: '选择文件成功',
        type: 'success',
      });
      this.hasUpload = true;
      this.active++;
    },
    upload_failed() {
      ElMessage.error('出现错误!');
      this.hasUpload = true;
    },
    set_net() {
      let net = this.net_choose == 'Unet' ? 0 : 1;
      axios.get('http://localhost:5001/set_net?net=' + net).then(() => {
        ElMessage({
          message: '已将网络设置为' + this.net_choose,
          type: 'success',
        });
        this.active++;
      });
    },
    next() {
      switch (this.active) {
        case 1:
          this.set_net();
          break;
        default:
          this.active++;
      }
    },
    prev() {
      switch (this.active) {
        case 1:
          this.active = 0;
          break;
        case 3:
          this.active = 1;
          break;
        default:
          this.active--;
      }
    },
  },
};
</script>
<style lang="stylus">
#choose, #process {
  margin: 10% auto;
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
</style>