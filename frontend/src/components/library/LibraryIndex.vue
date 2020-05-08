<template>
  <el-container>
    <el-aside style="width: 200px;margin-top: 20px">
      <switch></switch>
      <SideMenu @indexSelect="listByCategory" ref="sideMenu"></SideMenu>
    </el-aside>
    <el-main>
      <books class="drugs-area" ref="drugsArea"></books>
    </el-main>
  </el-container>
</template>

<script>
  import SideMenu from './SideMenu'
  import Drugs from './Drugs'

  export default {
    name: 'AppLibrary',
    components: {Drugs, SideMenu},
    methods: {
      listByCategory () {
        var _this = this
        var cid = this.$refs.sideMenu.cid
        var url = 'categories/' + cid + '/books'
        this.$axios.get(url).then(resp => {
          if (resp && resp.data.code === 200) {
            _this.$refs.drugsArea.drugs = resp.data.result
          }
        })
      }
    }
  }
</script>

<style scoped>
  .books-area {
    width: 990px;
    margin-left: auto;
    margin-right: auto;
  }
</style>
