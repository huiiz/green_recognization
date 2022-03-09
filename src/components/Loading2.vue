<template>
  <div class="spinner">
    <div class="dot1"></div>
    <div class="dot2"></div>
  </div>
  <h1>
    {{content}}
    <div class="dots">{{ dots }}</div>
  </h1>
</template>
<script>
export default {
  name: 'Loading2',
  props: ['content'],
  data() {
    return {
      dots: '',
      timer: '',
      count: 0,
    };
  },
  methods: {
    change_count() {
      this.count = this.count == 3 ? 0 : this.count + 1;
      var dots = '';
      for (var i = 0; i < this.count; i++) {
        dots += '.';
      }
      this.dots = dots;
    },
  },
  mounted() {
    this.timer = setInterval(this.change_count, 500);
  },
  beforeUnmount() {
    clearInterval(this.timer);
  },
};
</script>
<style lang="stylus">
.spinner {
  margin: 100px auto;
  width: 120px;
  height: 120px;
  position: relative;
  text-align: center;
  -webkit-animation: rotate 2s infinite linear;
  animation: rotate 2s infinite linear;
}

.dot1, .dot2 {
  width: 60%;
  height: 60%;
  display: inline-block;
  position: absolute;
  top: 0;
  background-color: #409EFF;
  border-radius: 100%;
  -webkit-animation: bounce 2s infinite ease-in-out;
  animation: bounce 2s infinite ease-in-out;
}

.dot2 {
  top: auto;
  bottom: 0px;
  -webkit-animation-delay: -1s;
  animation-delay: -1s;
}


.dots {
  display: inline-block;
}

</style>