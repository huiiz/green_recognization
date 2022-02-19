<template>
  <div id="select">
    <Menu />
    <div id="steps">
      <el-steps
        :active="active"
        finish-status="success"
        simple
        style="margin-top: 10px"
      >
        <el-step title="选择文件夹"></el-step>
        <el-step title="选择网络"></el-step>
        <el-step title="处理结果"></el-step>
      </el-steps>
    </div>

    <!-- 页面一：上传 -->
    <div id="upload" v-if="set_show(0)">
      <!-- <el-form ref="form" :model="form" label-width="120px" style="width: 50%">
        <el-form-item label="保存至文件夹">
          <input
            type="file"
            id="file"
            hidden
            @change="fileChange"
            webkitdirectory
          />
          <el-input
            placeholder="请输入内容"
            v-model="imgSavePath"
            class="input-with-select"
          >
          </el-input>
          <el-button type="success" @click="btnChange"><el-icon><folder-add /></el-icon></el-button>
        </el-form-item>
      </el-form> -->

      <div class="el-upload-dragger folder-choice" @click="btnChange">
        <input
          type="file"
          id="file"
          hidden
          @change="fileChange"
          webkitdirectory
        />
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          <!-- 将文件拖到此处或 <em>点击选择文件上传</em> 对文件进行切割 -->
          <em>请选择图片文件夹</em>
        </div>
      </div>
    </div>
    <!-- 页面二：选择网络 -->
    <div id="choose" v-if="set_show(1)">
      <el-radio-group v-model="net_choose" size="large">
        <el-radio-button label="Unet"></el-radio-button>
        <el-radio-button label="DeeplabV3++"></el-radio-button>
      </el-radio-group>
    </div>
    <!-- 页面三：处理中 -->
    <div id="process" v-if="set_show(2)">
      <loading
        :perc="perc"
        :process_status="process_status"
        :process_step="process_step"
      />
    </div>
    <div v-if="set_show(7)">
      <loading-2 />
    </div>
    <!-- 页面四：结果 -->
    <div id="result" v-if="set_show(3)">
      <div class="pics" v-if="from != 2">
        <div class="block" v-if="pre_count > 0">
          <el-carousel
            trigger="click"
            :interval="1000"
            type="card"
            :height="getImgHeight()"
          >
            <el-carousel-item v-for="item in img_ls" :key="item">
              <el-image :src="img_url(item)"></el-image>
              <!-- <h4>面积为: {{ area_ls[item] }} km²</h4> -->
            </el-carousel-item>
          </el-carousel>
        </div>
        <h4>已完成预测{{ (pre_count / total) * 100 }}%</h4>
      </div>
      <div class="gif" v-else>
        <el-image :src="gif_url()" :fit="fit"></el-image>
      </div>
    </div>

    <el-button style="margin-top: 12px" @click="prev" v-if="set_show(5)">
      回到上一步
    </el-button>
    <el-button
      style="margin-top: 12px"
      type="success"
      @click="next"
      v-if="set_show(4)"
      >下一步</el-button
    >
    <el-button
      style="margin-top: 12px"
      type="primary"
      @click="next"
      :disabled="result_btn_disable"
      v-if="set_show(6)"
      >查看结果</el-button
    >
  </div>

  <!-- <input v-model="active1" />
  <el-button style="margin-top: 12px" type="success" @click="go">去</el-button> -->
</template>

<script>
import Menu from './Menu.vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import Loading from './Loading.vue';
import Loading2 from './Loading2.vue';
import { UploadFilled } from '@element-plus/icons-vue';

export default {
  name: 'ToPredict',
  props: ['from'],
  data() {
    return {
      active: 0,
      // active1: 0,
      show: '10000000', // 选择待处理文件、选择网络、处理中、处理结果、下一步、上一步、查看结果、gif生成中
      net_choose: 'Unet',
      process_status: '处理中',
      process_step: '提取绿化中',
      perc: 0,
      // x: 0,
      // y: 0,
      total: 0,
      pre_count: 0,
      result_btn_disable: true,
      img_ls: [],
      // area_ls: {},
      pre_porc: null,
      imgSavePath: '',
      imgMaxHeight: 0,
    };
  },
  components: {
    Menu,
    Loading,
    Loading2,
    UploadFilled,
  },
  watch: {
    active() {
      console.log(this.active);
      switch (this.active) {
        case 0:
          this.show = '10000000';
          break;
        case 1:
          this.show = '01001100';
          break;
        case 2:
          this.show = this.from != 2 ? '00100010' : '00100000';
          this.to_predict();
          break;
        case 3:
          this.show = '00010100';
          break;
      }
    },
    // img_ls() {
    //   for (let i in this.img_ls) {
    //     let img_name = this.img_ls[i];
    //     if (!this.area_ls.hasOwnProperty(img_name)) {
    //       axios
    //         .get('http://localhost:5001/get_area?img_name=' + img_name)
    //         .then((response) => {
    //           this.area_ls[img_name] = response.data.data.area;
    //         });
    //       // this.getMaxHeight(this.img_url(img_name));
    //     }
    //   }
    // },
  },

  methods: {
    go() {
      this.active = parseInt(this.active1);
    },
    img_url(img_name) {
      // axios.get('http://localhost:5001/get_area?img_name=' + img_name)
      //     .then((response) => {
      //       this.area_ls[img_name] = response.data.data.area;
      //     });
      return 'http://localhost:5001/get_img?img_name=' + img_name;
    },
    gif_url() {
      return 'http://localhost:5001/get_gif';
    },
    set_show(num) {
      return this.show[num] == 0 ? false : true;
    },
    // upload_success(response, file, fileList) {
    //   ElMessage({
    //     message: '选择文件成功',
    //     type: 'success',
    //   });
    //   this.active++;
    // },
    // upload_failed() {
    //   ElMessage.error('出现错误!');
    // },
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
    // get_total() {
    //   axios.get('http://localhost:5001/get_total').then((response) => {
    //     console.log(response);
    //     // this.x = response.data.data.x_count;
    //     // this.y = response.data.data.y_count;
    //     this.total = response.data.data.total_count;
    //   });
    // },
    // seg_process() {
    //   this.perc = 0;
    //   let sub_porc = setInterval(() => {
    //     axios.get('http://localhost:5001/seg_process').then((response) => {
    //       console.log(response);
    //       let seg_count = response.data.data.seg_count;
    //       let change_count = response.data.data.change_count;
    //       if (this.total) {
    //         this.perc = (
    //           (10 * seg_count) / this.total +
    //           (90 * change_count) / this.total
    //         ).toFixed(2);
    //         if (this.total == change_count && this.total == seg_count) {
    //           this.process_status = '已完成';
    //           this.to_predict();
    //           clearInterval(sub_porc);
    //         }
    //       }
    //     });
    //   }, 1000);
    // },
    getImgHeight() {
      return window.screen.height * 0.7 + 'px';
    },
    // getMaxHeight(img_url) {
    //   // 创建对象
    //   var img = new Image();

    //   // 改变图片的src
    //   img.src = img_url;

    //   // 判断是否有缓存
    //   if (img.complete) {
    //     console.log(1);
    //     console.log(img.height);
    //       this.imgMaxHeight = Math.max(this.imgMaxHeight, img.height);

    //   } else {
    //     // 加载完成执行
    //     img.onload = function () {
    //       console.log(2);
    //       console.log(img.height);
    //       this.imgMaxHeight = Math.max(this.imgMaxHeight, img.height);
    //     };
    //   }
    // },
    fileChange(e) {
      try {
        const fu = document.getElementById('file');
        console.log(fu.files);
        if (fu.files.length > 0) {
          let ls = fu.files[0].path.split('\\');
          ls.pop();
          this.imgSavePath = ls.join('\\');
          console.log(this.imgSavePath);
          axios
            .get(
              'http://localhost:5001/set_img_path?img_path=' + this.imgSavePath
            )
            .then((response) => {
              console.log(response);
            });
          this.active++;
          ElMessage({
            message: '选择文件夹成功！',
            type: 'success',
          });
        } else {
          this.imgSavePath = '';
          console.log('empty');
          ElMessage({
            message: '你选择的是空文件夹！',
            type: 'warning',
          });
          // 进行提示不能选择空文件夹
        }
      } catch (error) {
        console.debug('choice file err:', error);
      }
    },
    btnChange() {
      var file = document.getElementById('file');
      file.click();
    },
    to_predict() {
      let num = this.from == '1' ? '3' : '1';
      axios.get('http://localhost:5001/predict?num=' + num).then((response) => {
        this.perc = 0;
        this.process_status = '处理中';
        // this.process_step = '提取绿化中';
        // this.get_total();
        this.pre_process();
      });
      ElMessage({
        message: '选择模型成功！',
        type: 'success',
      });
    },
    pre_process() {
      this.pre_porc = setInterval(() => {
        axios.get('http://localhost:5001/pre_process').then((response) => {
          console.log(response);
          this.total = response.data.data.total_count;
          this.pre_count = response.data.data.pre_count;
          this.img_ls = response.data.data.predict_ls;
          if (this.total) {
            this.perc = ((100 * this.pre_count) / this.total).toFixed(2);
            this.result_btn_disable = this.pre_count > 0 ? false : true;
            if (this.total == this.pre_count) {
              this.process_status = '已完成';
              if (this.active == 2) {
                if (this.from == 2) {
                  this.show = '00000001';
                  ElMessage({
                    message: '生成动态图片中',
                    type: 'success',
                  });
                  axios
                    .get('http://localhost:5001/create_gif')
                    .then((response) => {
                      this.active++;
                    });
                } else {
                  this.active++;
                }
              }
              clearInterval(this.pre_porc);
            }
          }
        });
      }, 5000);
    },
    // get_img_list() {
    //   let n = 0;
    //   let img_ls = [];
    //   for (let i = 0; i < this.x; i++) {
    //     for (let j = 0; j <script this.y; j++) {
    //       img_ls.push(i + '_' + j + '.png');
    //       n++;
    //       if (n >= this.pre_count) break;
    //     }
    //     if (n >= this.pre_count) break;
    //   }
    //   return img_ls;
    // },
    // async get_area(img_name) {
    //   if (!this.area_ls.hasOwnProperty(img_name)) {
    //     await axios
    //       .get('http://localhost:5001/get_area?img_name=' + img_name)
    //       .then((response) => {
    //         this.area_ls[img_name] = response.data.data.area;
    //       });
    //   }
    //   return this.area_ls[img_name];
    // },
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
          this.stop();
          break;
        default:
          this.active--;
      }
    },
    stop() {
      if (this.pre_porc) {
        clearInterval(this.pre_porc);
        this.img_ls = [];
        // this.area_ls = {};
        axios.get('http://localhost:5001/stop_predict').then(() => {});
      }
    },
  },
  unmounted() {
    this.stop();
  },
};
</script>
<style lang="stylus">
#choose, #process {
  margin: 10% auto;
}

.el-carousel__container {
  display: flex;
  /* 实现垂直居中 */
  align-items: center;
  /* 实现水平居中 */
  justify-content: center;
}

.el-image__inner {
  vertical-align: middle;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}

.folder-choice {
  margin: 7% auto;
}
</style>