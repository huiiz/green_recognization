<template>
  <div class="common-layout" id="menu">
    <el-container>
      <el-header>
          <el-button type="success" plain @click="jumpTo('/select')">绿化提取</el-button><a class="space"></a>
          <el-button type="info" plain @click="jumpTo('/predict')">动态预测</el-button><a class="space"></a>
          <el-button type="warning" plain>功能3</el-button>
      </el-header>
    </el-container>
  </div>
</template>
<style lang="stylus">
.space {
  margin-left: 30px;
}
</style>

<script>
export default {
  name: 'Menu',
  methods: {
    jumpTo(path) {
      this.$router.push(path)
    }
  }

};
</script>
