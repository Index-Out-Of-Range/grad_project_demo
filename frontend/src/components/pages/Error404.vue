<template>
  <div>
    <div style="margin: 10%; font-weight: bold; font-size: 30px;">
      404 Page Not Found
    </div>
    <el-button type="primary" @click="goToIndex"> 返回首页 </el-button>
  </div>
</template>

<script>
export default {
  name: 'Error404',
  methods: {
    goToIndex() {
      this.$router.push({
        name: 'Default'
      })
    }
  }
}
</script>

<style scoped>
.el-button--primary {
  color: #fff;
  background-color: #3cb371;
  border-color: #3cb371;
}
</style>
