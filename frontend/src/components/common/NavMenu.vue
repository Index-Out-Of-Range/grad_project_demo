<template>
  <div>
    <el-row type="flex" justify="space-between" style="padding:1% 15%; background-color: #212523; color:#999;">
      <div style="display:flex; align-items:center;">
        {{ $t('message.home.version') }}:&nbsp;&nbsp; <a href="#">1.0</a>
      </div>
      <div style="width: 30%; display:flex; justify-content:space-between;">
        <div>
          {{ $t('message.home.login') }} | {{ $t('message.home.register') }}
        </div>
        <el-dropdown style="margin-left: 5%; font-size: 16px;  color:#999;" @command="handleLanguage">
          <div>
            {{ $t('message.language')}}
            <i class="el-icon-arrow-down el-icon--right"></i>
          </div>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="zh-CN">{{ $t('message.zh') }}</el-dropdown-item>
            <el-dropdown-item command="en-US">{{ $t('message.en') }}</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
    </el-row>
    <el-row type="flex" align="middle" justify="space-between" style="padding:0 15%; font-size:1.5em; background-color:white">
      <div style="display:flex; align-items:center; font-weight:bold; cursor: pointer;" @click="goToIndex">
        <img src="../../assets/img/icon/Home.png" style="height:10%;width:10%;margin:0 2%;" />
        <p>{{ $t('message.system_name') }}</p>
      </div>
      <el-menu :default-active="path" router mode="horizontal" text-color="black" active-text-color="#3CB371">
        <!-- <el-menu-item v-for="(item, i) in navList" :key="i" :index="item.name">
          {{ item.navItem }}
        </el-menu-item> -->
        <el-menu-item index="/single_gene_search">
          <span>{{ $t('message.home.menu.menu1') }}</span>
        </el-menu-item>
        <el-menu-item index="/library">
          <span>{{ $t('message.home.menu.menu2') }}</span>
        </el-menu-item>
        <el-menu-item index="/download">
          <span>{{ $t('message.home.menu.menu3') }}</span>
        </el-menu-item>
        <el-menu-item index="/help">
          <span>{{ $t('message.home.menu.menu4') }}</span>
        </el-menu-item>
        <el-menu-item index="/login">
          <span>{{ $t('message.home.menu.menu5') }}</span>
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
      // navList: [
      //   // {name: '/index', navItem: '首页'},
      //   { name: '/single_gene_search', navItem: this.$t('message.home.menu.menu1') },
      //   { name: '/library', navItem: this.$t('message.home.menu.menu2') },
      //   { name: '/download', navItem: this.$t('message.home.menu.menu3') },
      //   { name: '/help', navItem: this.$t('message.home.menu.menu4') },
      //   { name: '/login', navItem: this.$t('message.home.menu.menu5') }
      // ],
      path: ''
    }
  },
  methods: {
    handleLanguage(command) {
      if (command === 'zh-CN' && this.$i18n.locale === 'en-US') {
        this.$i18n.locale = 'zh-CN'
        window.sessionStorage.setItem('lang', 'zh-CN')
      } else if (command === 'en-US' && this.$i18n.locale === 'zh-CN') {
        this.$i18n.locale = 'en-US'
        window.sessionStorage.setItem('lang', 'en-US')
      }
    },
    goToIndex() {
      this.$router.push({
        name: 'Default'
      })
      this.path = this.$route.path
    }
  },
  mounted: function () {
    // 获得第一级路由，以设置导航栏高亮
    let x = this.$route.path.indexOf('/', 1)
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
  },
  watch: {
    // $route(to, from) {
    //   let x = to.path.indexOf('/', 1)
    //   if (x !== -1) {
    //     this.path = this.$route.path.substring(0, x)
    //   } else {
    //     this.path = this.$route.path
    //   }
    // }
  }
}
</script>

<style scoped>
a {
  text-decoration: none;
}

span {
  pointer-events: none;
}
</style>
