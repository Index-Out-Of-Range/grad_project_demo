<template>
  <div>
    <el-row
      type="flex"
      justify="space-between"
      style="padding:1% 15%; background-color: #212523; color:#999;"
    >
      <div style="display:flex; align-items:center;">
        {{ $t('message.home.version') }}:&nbsp;&nbsp; <a href="#">1.0</a>
      </div>
      <el-row type="flex" style="width: 20%;" justify="space-between">
        <div>
          {{ $t('message.home.login') }} | {{ $t('message.home.register') }}
        </div>
        <el-dropdown style="margin-left: 5%; font-size: 16px;  color:#999;">
          <div>
            {{ $t('message.language')
            }}<i class="el-icon-arrow-down el-icon--right"></i>
          </div>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item>{{ $t('message.zh') }}</el-dropdown-item>
            <el-dropdown-item>{{ $t('message.en') }}</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-row>
    </el-row>
    <el-row
      type="flex"
      align="middle"
      justify="space-between"
      style="padding:0 15%; font-size:1.5em; background-color:white"
    >
      <div style="display:flex; align-items:center; font-weight:bold;">
        <img
          src="../../assets/img/icon/Home.png"
          style="height:10%;width:10%;margin:0 2%;"
        />
        <p>{{ $t('message.system_name') }}</p>
      </div>
      <el-menu
        :default-active="path"
        router
        mode="horizontal"
        text-color="black"
        active-text-color="#3CB371"
      >
        <el-menu-item v-for="(item, i) in navList" :key="i" :index="item.name">
          {{ item.navItem }}
        </el-menu-item>
      </el-menu>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'NavMenu',
  data() {
    return {
      navList: [
        // {name: '/index', navItem: '首页'},
        {
          name: '/single_gene_search',
          navItem: this.$t('message.home.menu.menu1')
        },
        { name: '/library', navItem: this.$t('message.home.menu.menu2') },
        { name: '/download', navItem: this.$t('message.home.menu.menu3') },
        { name: '/help', navItem: this.$t('message.home.menu.menu4') },
        { name: '/login', navItem: this.$t('message.home.menu.menu5') }
      ],
      path: ''
    }
  },
  methods: {},
  mounted: function() {
    // 获得第一级路由，以设置导航栏高亮
    var x = this.$route.path.indexOf('/', 1)
    if (x !== -1) {
      this.path = this.$route.path.substring(0, x)
    } else {
      this.path = this.$route.path
    }
  },
  computed: {
    hoverBackground() {
      return '#ffd04b'
    }
  }
}
</script>

<style scoped>
  a{
    text-decoration: none;
  }

  span {
    pointer-events: none;
  }

</style>
