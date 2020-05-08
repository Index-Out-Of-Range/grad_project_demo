<template>
  <div>
    <el-row>
      <el-menu :default-active="side_bar_index" router>
        <el-menu-item index="/single_gene_search">
          <i class="el-icon-search"></i>
          <span slot="title">{{ $t('message.search.menu.menu1') }}</span>
        </el-menu-item>
        <el-divider></el-divider>
        <el-menu-item index="/single_phenotype_search">
          <i class="el-icon-search"></i>
          <span slot="title">{{ $t('message.search.menu.menu2') }}</span>
        </el-menu-item>
        <el-divider></el-divider>
        <el-menu-item index="/multi_gene_search">
          <i class="el-icon-menu"></i>
          <span slot="title">{{ $t('message.search.menu.menu3') }}</span>
        </el-menu-item>
        <el-divider></el-divider>
        <el-menu-item index="/multi_phenotype_search">
          <i class="el-icon-menu"></i>
          <span slot="title">{{ $t('message.search.menu.menu4') }}</span>
        </el-menu-item>
        <el-divider></el-divider>
        <el-menu-item index="/gp_upload_file">
          <i class="el-icon-document"></i>
          <span slot="title">{{ $t('message.search.menu.menu5') }}</span>
        </el-menu-item>
      </el-menu>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'SideBar',
  data() {
    return {
      path: ''
    }
  },
  methods: {},
  props: ['side_bar_index'],
  mounted: function() {
    // 获得第一级路由，以设置导航栏高亮
    var x = this.$route.path.indexOf('/', 1)
    if (x !== -1) {
      this.path = this.$route.path.substring(0, x)
    } else {
      this.path = this.$route.path
    }
  }
}
</script>

<style scoped>
.el-menu-item.is-active {
  color: #3CB371 !important;
}

.el-divider--horizontal{
  margin:1px 0;
} 
</style>
